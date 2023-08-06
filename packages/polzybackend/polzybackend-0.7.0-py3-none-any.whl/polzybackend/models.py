from polzybackend import db, auth
from polzybackend.utils import generate_id, date_format
from polzybackend.utils.auth_utils import generate_token, get_expired, is_supervisor, load_attributes
from datetime import datetime, date
from sqlalchemy import and_, or_
from functools import reduce
from uuid import UUID
import json
import os


# authentication
@auth.verify_token
def verify_token(token):
    user = User.query.filter_by(access_key=token).first()
    if user and user.key_expired > datetime.utcnow():
        return user


#
# Authentication Models
#

#
# Association Models
#

# association table for user-role relation
user_company_roles = db.Table(
    'user_company_roles',
    db.Column('user_id', db.String(56), db.ForeignKey('users.id'), primary_key=True),
    db.Column('company_id', db.String(56), db.ForeignKey('companies.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)


class CompanyToCompany(db.Model):
    #
    # association object between companies
    #
    __tablename__ = 'company_company'
    parent_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    child_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    parent = db.relationship('Company', backref='child_companies', foreign_keys=[parent_id])
    child = db.relationship('Company', backref='parent_companies', foreign_keys=[child_id])


class UserToCompany(db.Model):
    #
    # association object between user and company
    #
    __tablename__ = 'user_company'
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), primary_key=True)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    user = db.relationship(
        'User',
        lazy='subquery',
        backref='companies',
        foreign_keys=[user_id],
    )
    company = db.relationship(
        'Company',
        lazy='subquery',
        backref='users',
        foreign_keys=[company_id],
    )
    roles = db.relationship(
        'Role',
        lazy='subquery',
        secondary=user_company_roles,
        primaryjoin=and_(user_id == user_company_roles.c.user_id, company_id == user_company_roles.c.company_id),
        backref=db.backref('user_to_companies'),
    )
    #badges = db.relationship(
    #    'GamificationBadge',
    #    lazy='subquery',
    #    primaryjoin="and_(UserToCompany.user_id==GamificationBadge.user_id, "
    #                     "UserToCompany.company_id==GamificationBadge.company_id)"
    #)


    def to_json(self):
        return {
            'id': self.company.id,
            'name': self.company.name,
            'displayedName': str(self.company),
            'attributes': load_attributes(self.company.attributes),
        }

    def to_admin_json(self):
        child_companies = CompanyToCompany.query.filter_by(parent_id=self.company_id).all()
        return {
            'id': self.company.id,
            'name': self.company.name,
            'displayedName': str(self.company),
            'childCompanies': [{
                'id': ch.child_id,
                'name': ch.child.name,
                'attributes': ch.attributes,
            } for ch in child_companies],
            'users': [{
                'id': u.user.id,
                'email': u.user.email,
                'roles': [r.name for r in u.roles],
                'attributes': u.attributes if u.attributes else '',
            } for u in self.company.users],
        }


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    is_supervisor = db.Column(db.Boolean, nullable=False, default=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    email = db.Column(db.String(64), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    displayed_name = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    # oauth_provider_id = db.Column(db.Integer, db.ForeignKey('oauth_providers.id'), nullable=False)
    # oauth_user_id = db.Column(db.String(128), nullable=False)
    # oauth_token = db.Column(db.String(128), nullable=False)
    access_key = db.Column(db.String(128), nullable=False, default=generate_token)
    key_expired = db.Column(db.DateTime, nullable=False, default=get_expired)
    # current session attributes
    stage = db.Column(db.String(8), nullable=True)
    language = db.Column(db.String(8), nullable=True)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=True)

    # relationships
    # oauth_provider = db.relationship(
    #    'OAuthProvider',
    #    foreign_keys=[oauth_provider_id],
    # )
    company = db.relationship(
        'UserToCompany',
        primaryjoin=and_(
            id == UserToCompany.user_id,
            company_id == UserToCompany.company_id,
        ),
        uselist=False,
        lazy='subquery',
    )
    badges = db.relationship(
        'GamificationBadge',
        primaryjoin="and_(User.id==GamificationBadge.user_id, "
                         "User.company_id==GamificationBadge.company_id)"
    )

    def __str__(self):
        return self.displayed_name or self.first_name or self.last_name or self.email.split('@')[0]

    def set_stage(self, stage):
        self.stage = stage
        db.session.commit()

    def set_language(self, language):
        self.language = language
        db.session.commit()

    def set_company(self, company_id=None, company=None):
        # check if company data is provided
        if company_id is None and company is None:
            raise Exception('Neither Company ID nor Company provided')

        # check if company should be fetched
        if company is None:
            company = Company.query.get(company_id)
        
        # check if company exists
        if company is None:
            raise Exception('Company not found')

        # get UserToCompany instance
        user_company = UserToCompany.query.filter(and_(
            UserToCompany.user_id == self.id,
            UserToCompany.company_id == company.id,
        )).first()

        # check if association exists
        if user_company is None:
            raise Exception(f'User is not assigned to company ID {company_id}')

        # set company
        self.company_id = company.id
        db.session.commit()

        # return company json
        return user_company.to_json()

    def is_supervisor(self):
        return reduce(lambda result, company: result or is_supervisor(company), self.companies, False)

    def get_permissions(self):
        if self.company:
            user_roles = [r.name.lower() for r in self.company.roles]

            return {
                'policy': any(role in ['admin', 'clerk'] for role in user_roles),
                'antrag': any(role in ['admin', 'agent'] for role in user_roles),
            }

        return {
            'policy': False,
            'antrag': False,
        }

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': str(self),
            'isSupervisor': self.is_supervisor(),
            'stage': self.stage,
            'accessToken': self.access_key,
            'companies': [company.to_json() for company in self.companies],
        }

    def get_admin_json(self):
        return {
            'possibleRoles': [r.name for r in Role.query.all()],
            'companies': [company.to_admin_json() for company in filter(
                lambda company: is_supervisor(company),
                self.companies
            )],
        }


'''
class OAuthProvider(db.Model):
    __tablename__ = 'oauth_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    client_id = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return self.name
'''


#
# Company Model
#
class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128), unique=True, nullable=False)
    displayed_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(16), nullable=True)
    country = db.Column(db.String(32), nullable=True)
    post_code = db.Column(db.String(8), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    attributes = db.Column(db.String(1024), nullable=True)

    def __str__(self):
        return self.displayed_name or self.name


#
# Activity Models
#
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    creator_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    policy_number = db.Column(db.String(64), nullable=False)
    effective_date = db.Column(db.Date, nullable=False, default=date.today)
    type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(64), nullable=True)
    finished = db.Column(db.DateTime, nullable=True)
    attributes = db.Column(db.String, nullable=True)
    
    # relationships
    creator = db.relationship(
        'User',
        backref=db.backref('created_activities', order_by='desc(Activity.created)'),
        foreign_keys=[creator_id],
    )

    def __str__(self):
        return self.id

    @classmethod
    def new(cls, data, policy, current_user):
        # 
        # create instance using data
        #

        instance = cls(
            policy_number=policy.number,
            effective_date=datetime.strptime(policy.effective_date, date_format).date(),
            type=data['activity'].get('name'),
            creator_id=current_user.id,
            attributes=json.dumps(data['activity'].get('fields'))
        )
        
        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    @classmethod
    def read_policy(cls, policy_number, effective_date, current_user):
        #
        # create instance of reading a policy
        #

        instance = cls(
            policy_number=policy_number,
            effective_date=datetime.strptime(effective_date, date_format).date(),
            type='Read Policy',
            creator=current_user,
            finished=datetime.utcnow(),
            status='OK',
        )

        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    def finish(self, status):
        #
        # sets is_finished to True 
        #
        self.status = status
        self.finished = datetime.utcnow()
        db.session.commit()


#
# File Model
#
class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    filename = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=False)
    processed = db.Column(db.Boolean, nullable=True, default=False)
    status_ok = db.Column(db.Boolean, nullable=True, default=False)
    details = db.Column(db.String(256), nullable=True, default="{}")
    parent_id = db.Column(db.String(56), nullable=True)

    # relationships
    user = db.relationship('User', backref='files', foreign_keys=[user_id])
    company = db.relationship('Company', backref='files', foreign_keys=[company_id])

    @classmethod
    def new(cls, user, filename, id, parent_id=None):
        # 
        # create new instance of File
        #

        instance = cls(
            id=id,
            filename=filename,
            user_id=user.id,
            company_id=user.company_id,
            parent_id=parent_id,
        )

        db.session.add(instance)
        db.session.commit()
        
        return instance

    def set_processed(self, details={}):
        self.processed = True
        self.status_ok = details.get("status_ok", True)
        if isinstance(details, dict):
            details = json.dumps(details)
        self.details = details
        db.session.commit()

    def get_current_filename(self):
        original_filename, extension = os.path.splitext(self.filename)
        return self.id + extension


#
# Antrag Model
#
class AntragActivityRecords(db.Model):
    __tablename__ = "antrag_activity_records"
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    antrag_id = db.Column(db.String(56), primary_key=True)
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=False)
    antragsnummer = db.Column(db.String(56), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(16), nullable=False)
    searchString = db.Column(db.String, nullable=False)
    json_data = db.Column(db.String, nullable=False)
    json_data_activities = db.Column(db.String, default="{}")
    class_name = db.Column(db.String, nullable=False)
    sapClient = db.Column(db.String(16), nullable=False)
    tag = db.Column(db.String, default=None)

    # relationships
    user = db.relationship('User', foreign_keys=[user_id])
    company = db.relationship('Company', foreign_keys=[company_id])

    @classmethod
    def new(cls, antrag):
        json_data = {}
        for activities in antrag.Aktivitaeten:
            json_data[activities.__class__.__name__] = activities.toJson()

        instance = cls(
            antrag_id=str(antrag.id),
            user_id=str(antrag.user.id),
            company_id=str(antrag.user.company_id),
            antragsnummer=antrag.antragsnummer,
            status=antrag.status,
            searchString=antrag.searchstring,
            json_data=json.dumps(antrag.Felder.toJSON()),
            json_data_activities=json.dumps(json_data),
            class_name=antrag.__class__.__name__,
            sapClient=antrag.sapClient,
            tag=antrag.tag,
        )
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def getSearchString(cls, user: User, searchString):
        if searchString is None:
            return
        strings = searchString.split()
        instances = {}

        # looping through all records for current user & company
        for obj in cls.query.filter_by(user_id=user.id, company_id=user.company_id).all():
            print('\n*** Found Antrags:')
            print(obj)
            values = [value.lower() for value in obj.searchString.split()]
            values.append(str(obj.antragsnummer))
            flag = True
            for string in strings:
                if not string.lower().strip() in values:  # matching split & lowered value for flexiblity
                    flag = False
                    break
            if flag:
                if not obj.antrag_id in instances:
                    instances[obj.antrag_id] = obj
                else:
                    if instances[obj.antrag_id].timestamp < obj.timestamp:  # if current object is latest than previously
                        instances[obj.antrag_id] = obj                      # stored then replace it with current object
        return list(instances.values())

    @classmethod
    def getLatest(cls, antrag_id):
        instance = cls.query.filter_by(antrag_id=antrag_id).order_by(cls.timestamp.desc()).first()
        if not instance:  # if no result from antrag_id then it might be record id. This is only for flexibility
            instance = cls.query.filter_by(id=antrag_id).order_by(cls.timestamp.desc()).first()
        return instance

    def get_label(self):
        return ' '.join((
            self.searchString,
            self.antragsnummer,
            self.timestamp.strftime("%d.%m.%Y, %H:%M:%S"),
        ))

    def to_dict(self):
        dic = {
            "id": self.id,
            "user_id": self.user_id,
            "company_id": self.company_id,
            "antragsnummer": self.antragsnummer,
            "status": self.status,
            "timestamp": self.timestamp.strftime("%d.%m.%Y, %H:%M:%S"),
            "searchString": self.searchString,
            "json_data": json.loads(self.json_data)
        }
        return dic

    def to_json(self):
        return json.dumps(self.to_dict())


#
# Gamification Models
#
class GamificationEvent(db.Model):
    __tablename__ = 'gamification_events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __str__(self):
        return self.name


class GamificationActivity(db.Model):
    __tablename__ = 'gamification_activities'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    processed = db.Column(db.DateTime, nullable=True)
    is_processed = db.Column(db.Boolean, nullable=False, default=False)
    event_details = db.Column(db.String(1024), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('gamification_events.id'), nullable=False)
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=False)

    # relationships
    event = db.relationship('GamificationEvent', foreign_keys=[event_id])
    user = db.relationship('User', backref='gamification_activities', foreign_keys=[user_id])
    company = db.relationship('Company', backref='gamification_activities', foreign_keys=[company_id])

    def __str__(self):
        msg = f'{self.user.email}: {self.event.name}'
        if self.processed:
            return f'{msg} - processed at {self.processed.strftime("%d.%m.%Y, %H:%M:%S")}'
        else:
            return f'{msg} - NOT processed'

    @classmethod
    def new(cls, user, event, event_details):
        # 
        # create instance based on the provided data
        #

        if not isinstance(event, GamificationEvent):
            if isinstance(event, int):
                event = db.session.query(GamificationEvent).filter_by(id=event).first()
            elif isinstance(event, str):
                event = db.session.query(GamificationEvent).filter_by(name=event).first()

        instance = cls(
            user_id=user.id,
            company_id=user.company.company_id,
            event=event,
            event_details=event_details,
        )

        db.session.add(instance)
        db.session.commit()
        
        return instance

    def set_processed(self, commit=True):
        #
        # set activity as processed
        #

        self.processed = datetime.utcnow()
        self.is_processed = True

        # save to db
        if commit:
            db.session.commit()


class GamificationUserStats(db.Model):
    __tablename__ = 'gamification_statistics'
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), primary_key=True, nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_types.id'), primary_key=True)
    daily = db.Column(db.Integer, default=0)
    weekly = db.Column(db.Integer, default=0)
    monthly = db.Column(db.Integer, default=0)
    yearly = db.Column(db.Integer, default=0)
    all_time = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', backref='gamification_statistics', foreign_keys=[user_id])
    company = db.relationship('Company', backref='gamification_statistics', foreign_keys=[company_id])
    type = db.relationship('GamificationBadgeType', backref="gamification_badge_types", foreign_keys=[type_id])

    def __str__(self):
        return self.user_id + f" - {self.type_id} -" + " -- " + str(self.get_user_statistics())

    def check_timeline(self):
        year_is_changed = self.last_updated.date().year < datetime.now().date().year
        # year_is_changed used when year changed but month or week number is same
        changes = False
        if self.last_updated.date() < datetime.now().date() or year_is_changed:
            self.daily = 0
            changes = True
        if self.last_updated.date().isocalendar()[1] < datetime.now().date().isocalendar()[1] or year_is_changed:
            self.weekly = 0
            changes = True
        if self.last_updated.date().month < datetime.now().date().month or year_is_changed:
            self.monthly = 0
            changes = True
        if year_is_changed:
            self.yearly = 0
            changes = True
        if changes:  # only update last_update time when it is needed
            self.last_updated = datetime.now()
            db.session.commit()

    def add_points(self, points=1, weight=1):
        self.check_timeline()
        weighted_point = points * weight
        self.daily += weighted_point
        self.weekly += weighted_point
        self.monthly += weighted_point
        self.yearly += weighted_point
        self.all_time += weighted_point
        self.update_badge()
        return {"all time": self.all_time}

    def get_user_statistics(self):
        self.check_timeline()
        json_data = {"daily": self.daily, "weekly": self.weekly, "monthly": self.monthly,
                     "annual": self.yearly, "all time": self.all_time}
        return json_data

    @classmethod
    def new(cls, user_id, company_id, type_id):
        instance = cls(
            user_id=user_id,
            company_id=company_id,
            type_id=type_id,
        )
        db.session.add(instance)
        db.session.commit()

        return instance

    def update_badge(self):
        level_id = self.get_level_id()
        badge = db.session.query(GamificationBadge).filter_by(user_id=self.user_id).filter_by(
            company_id=self.company_id).filter_by(type_id=self.type_id).filter_by(level_id=level_id).first()
        if not badge:
            badge = GamificationBadge(
                user_id=self.user_id, company_id=self.company_id, type_id=self.type_id, level_id=level_id)
            db.session.add(badge)
            db.session.commit()
            ToastNotifications.new(
                message=badge.id, type="badge", company_ids=self.company_id, user_ids=self.user_id
            )

    def get_level_id(self):
        level = db.session.query(GamificationBadgeLevel).filter(and_(self.all_time >= GamificationBadgeLevel.min_level,
            (or_(self.all_time <= GamificationBadgeLevel.max_level, GamificationBadgeLevel.max_level == None)))).first()
        return level.id

    @staticmethod
    def get_type_id(event: GamificationEvent, event_details):
        eventName = event.name.lower()
        event_details = json.loads(event_details)
        eventType = event_details.get("lineOfBusiness")
        if "policy" in eventName and eventType:
            return db.session.query(GamificationBadgeType).filter_by(name=f"Polizze {eventType}").first().id
        elif "antrag" in eventName and eventType:
            return db.session.query(GamificationBadgeType).filter_by(name=f"Antrag {eventType}").first().id
        elif "login" in eventName:
            return db.session.query(GamificationBadgeType).filter_by(name="Login").first().id
        elif "policy" in eventName:
            return db.session.query(GamificationBadgeType).filter_by(name=f"Policy").first().id
        elif "antrag" in eventName:
            return db.session.query(GamificationBadgeType).filter_by(name=f"Antrag").first().id
        else:
            print(f"{eventName} event is ignored.")
            return None

    @staticmethod
    def get_weight(event: GamificationEvent, event_details):
        eventName = event.name
        event_details = json.loads(event_details)
        lob = event_details.get("lineOfBusiness", "")
        activityName = event_details.get("Activity")
        if lob and activityName:
            id_ = db.session.query(GamificationActivityWeight).filter(and_(
                GamificationActivityWeight.activity_name == activityName,
                GamificationActivityWeight.line_of_business == lob)).first()
        else:
            if lob and eventName:
                id_ = db.session.query(GamificationActivityWeight).filter(and_(
                    GamificationActivityWeight.activity_name == eventName,
                    GamificationActivityWeight.line_of_business == lob)).first()
            else:
                id_ = db.session.query(GamificationActivityWeight).filter_by(activity_name=eventName).first()
        if not id_:
            print(f"Combination of activityName: {str(activityName)}, lineOfBusiness: {str(lob)} or "
                  f"event: {str(eventName)} not found in Weight table. Using default value 10.")
            id_ = db.session.query(GamificationActivityWeight).filter_by(activity_name="default").first()
            if not id_:
                print("Default weight not found in database. Returning 10")
                return 10
        return id_.points

    @classmethod
    def create_or_update_row(cls, activity: GamificationActivity, commit=True):
        type_id = cls.get_type_id(activity.event, activity.event_details)
        weightage = cls.get_weight(activity.event, activity.event_details)
        if not type_id:
            return None
        user_id = activity.user_id
        company_id = activity.company_id
        user_stats = db.session.query(GamificationUserStats).filter_by(user_id=user_id
            ).filter_by(company_id=company_id).filter_by(type_id=type_id).first()
        if user_stats:
            user_stats.add_points(weight=weightage)
        if not user_stats:
            user_stats = GamificationUserStats.new(user_id=user_id, company_id=company_id, type_id=type_id)
            user_stats.add_points(weight=weightage)
        if commit:
            db.session.commit()
        return user_id

    @staticmethod
    def commit():
        db.session.commit()

## Badges

class GamificationBadgeDescription(db.Model):
    #
    # Badge earn requirements for given Type and Level
    #
    __tablename__ = 'gamification_badge_descriptions'
    type_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_types.id'), primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_levels.id'), primary_key=True)
    description = db.Column(db.String(512), nullable=False)

    # relationships
    type = db.relationship('GamificationBadgeType', foreign_keys=[type_id])
    level = db.relationship('GamificationBadgeLevel', foreign_keys=[level_id])

class GamificationBadgeLevel(db.Model):
    __tablename__ = 'gamification_badge_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    min_level = db.Column(db.Integer, unique=True, nullable=False)
    max_level = db.Column(db.Integer, unique=True, nullable=True)
    is_lowest = db.Column(db.Boolean, nullable=False, default=False,)
    next_level_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_levels.id'), nullable=True)

    #relationships
    next_level = db.relationship('GamificationBadgeLevel', remote_side=[next_level_id], uselist=False)

    def __str__(self):
        return self.name

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_level = self.get_next_level_min()

    def get_next_level_name(self):
        if self.next_level:
            return self.next_level.name

    def get_next_level_min(self):
        if self.next_level:
            return self.next_level.min_level - 1
        return None


class GamificationBadgeType(db.Model):
    __tablename__ = 'gamification_badge_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(32), nullable=False)

    # reletionaships
    descriptions = db.relationship(
        'GamificationBadgeDescription',
        primaryjoin="GamificationBadgeType.id==GamificationBadgeDescription.type_id",
    )

    def get_description(self):
        return {(d.level.name if not d.level.is_lowest else 'lowest'): d.description for d in self.descriptions}

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'title': self.title,
            'description': self.get_description(),
        }

class GamificationBadge(db.Model):
    __tablename__ = 'gamification_badges'
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_types.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('gamification_badge_levels.id'), nullable=False)
    achieved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_seen = db.Column(db.Boolean, nullable=False, default=False)

    # relationships
    user = db.relationship('User', backref='gamification_badges', foreign_keys=[user_id])
    company = db.relationship('Company', foreign_keys=[company_id])
    type = db.relationship('GamificationBadgeType', foreign_keys=[type_id])
    level = db.relationship('GamificationBadgeLevel', foreign_keys=[level_id])

    def __str__(self):
        return f'Badge {self.level.name} {self.type.name} for {self.user.email}'

    def set_seen(self):
        self.is_seen = True
        db.session.commit()

    def to_json(self):
        return {
            'type': self.type.name,
            'level': self.level.name,
            'next_level': self.level.get_next_level_name(),
            'isSeen': self.is_seen,
        }

    @classmethod
    def get_user_stats(cls, user_id=user_id):
        user = db.session.query(cls).filter_by(user_id=user_id).all()
        json_data = [data.to_json() for data in user]
        return json_data


class GamificationActivityWeight(db.Model):
    __table_name__ = "gamification_activity_weight"
    __table_args__ = (db.UniqueConstraint('activity_name', 'line_of_business', name='unique'),)
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(32), nullable=False)
    line_of_business = db.Column(db.String(16), nullable=True)
    points = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_points(cls, id):
        if id:
            weight = cls.query.filter(cls.id == id).first()
            if weight:
                return weight.points
        print("Weightage id is either not supplied or not found in Weightage table. Returned default value of 1")
        return 1

    @classmethod
    def new(cls, activity_name, line_of_business, points=1):
        instance = cls(activity_name=activity_name, line_of_business=line_of_business, points=points)
        db.session.add(instance)
        db.session.commit()

    def to_json(self):
        js = {
            "id": self.id,
            "activity_name": self.activity_name,
            "line_of_business": self.line_of_business,
            "points": self.points
        }
        return js

    @classmethod
    def get_all_id_points(cls):
        all_rows = cls.query.all()
        all_data = {row.id: row.points for row in all_rows}
        return all_data


class ToastNotifications(db.Model):
    __tablename__ = "toast_notifications"
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(16), default="default", nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    seen_at = db.Column(db.DateTime)

    @classmethod
    def new(cls, message, type="default", company_ids=None, user_ids=None):
        companies = []
        if company_ids:
            if isinstance(company_ids, list):
                for company_id in company_ids:
                    if db.session.query(Company).filter_by(id=company_id).first():
                        companies.append(company_id)
                    else:
                        print(f"Company id {company_id} is not correct. Please recheck.")
            else:
                if db.session.query(Company).filter_by(id=company_ids).first():
                    companies.append(company_ids)
                else:
                    print(f"Company id {company_ids} is not correct. Please recheck.")
        else:
            companies = [company.id for company in db.session.query(Company).all()]
        if not companies:
            print("Supplied company ids are not valid. Hence no notification will be updated")
        for company_id in companies:
            users = []
            if not user_ids:
                users = [user.id for user in db.session.query(User).filter_by(company_id=company_id).all()]
            else:
                if isinstance(user_ids, list):
                    for user_id in user_ids:
                        if db.session.query(User).filter_by(id=user_id).first():
                            users.append(user_id)
                        else:
                            print(f"User id {user_id} is not correct. Please recheck.")
                else:
                    if db.session.query(User).filter_by(id=user_ids).first():
                        users.append(user_ids)
                    else:
                        print(f"User id {user_ids} is not correct. Please recheck.")
            for user_id in users:
                instance = cls(company_id=company_id, user_id=user_id, message=message, type=type)
                db.session.add(instance)
        db.session.commit()

    def set_seen(self):
        self.seen_at = datetime.now()
        db.session.commit()


class AntragNummer(db.Model):
    count = db.Column(db.Integer, default=10000000, primary_key=True)

    @staticmethod
    def get_count():
        count = db.session.query(AntragNummer).first().count
        AntragNummer.update_count()  # updating 100 as it calls count, because of program stops before completing 100,
        return count                 # then current base value will be resent and it will create same ids

    @staticmethod
    def update_count():
        instance = db.session.query(AntragNummer).first()
        instance.count += 100
        db.session.add(instance)
        db.session.commit()
