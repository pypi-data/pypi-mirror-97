from flask import jsonify, request, current_app
from datetime import date
from polzybackend.administration import bp
from polzybackend.models import User
from polzybackend import auth, db
from polzybackend.models import User, Company, Role, UserToCompany, CompanyToCompany
#from polzybackend.utils.auth_utils import str_id_to_bytes
from sqlalchemy import and_


@bp.route('/admin')
@auth.login_required
def get_admin_data():
    # returns admin data for companies where current user is admin
    try:
        result = auth.current_user().get_admin_json()
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.warning(f'Failed to get admin data: {e}')
        return {'error': 'Failed to fetch data'}, 400


@bp.route('/admin/user-company/<string:action>', methods=['POST'])
@auth.login_required
def manage_user(action):
    #
    # manage user in company
    # <action> should be one of:
    # - add -> add user to company
    # - edit -> edit user roles in company
    # - remove -> remove user from company
    #

    try:
        # validate action
        if not action in ['add', 'edit', 'remove']:
            raise Exception(f"Action '{action}' is not supported") 
        
        # get request data
        data = request.get_json()
        
        # check for required fields in data
        if data.get('companyId') is None:
            raise Exception('Company ID is not defined in request')
        if data.get('email') is None:
            raise Exception('User e-mail is not defined in request')
        # roles are required by 'add' and 'edit' actions
        if (action in ['add', 'edit']) and (data.get('roles') is None):
            raise Exception(f'User roles are not defined in request. Required for action: {action}')

        # get company from db
        company = Company.query.get(data['companyId'])
        if company is None:
            raise Exception(f'Company with ID {data["companyId"]} not found')

        # get user from db
        user = User.query.filter_by(email=data['email']).first()
        # check if user exists
        if user is None:
            # create user for action 'add'
            if action == 'add':
                user = User(email=data['email'])
                db.session.add(user)
            # raise UserNotFound
            else:
                raise Exception(f'User {data["email"]} not found')

        # get or create user to company association
        if action in ['edit', 'remove']:
            # get
            user_to_company = UserToCompany.query.filter(and_(
                UserToCompany.company == company,
                UserToCompany.user == user,
            )).first()
            if user_to_company is None:
                raise Exception(f'User {data["email"]} not found in company {data["companyId"]}')
        else:
            # create
            user_to_company = UserToCompany(
                user=user,
                company=company,
            )
            db.session.add(user_to_company)

        # set user roles and attributes
        if action in ['add', 'edit']:
            # roles
            roles = []
            for name, value in data['roles'].items():
                if value:
                    # get role
                    role = Role.query.filter_by(name=name).first()
                    if role is None:
                        raise Exception(f"Role '{name}' not found")
                    roles.append(role)                
            # update user roles
            user_to_company.roles = roles

            # attributes
            if not data.get('attributes') is None:
                user_to_company.attributes = data['attributes']
        
        # remove user from company
        else:
            db.session.delete(user_to_company)

        # commit changes
        db.session.commit()
        
        # return updated admin data
        return jsonify(auth.current_user().get_admin_json()), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.warning(f"Failed to execute action '{action}'\nPayload: {request.get_json()}\nException: {e}")
        return {'error': str(e)}, 400


@bp.route('/admin/child-company/<string:action>', methods=['POST'])
@auth.login_required
def manage_child_company(action):
    #
    # manage child companies
    # <action> should be one of:
    # - add -> add user to company
    # - edit -> edit user roles in company
    # - remove -> remove user from company
    #

    try:
        # validate action
        if not action in ['add', 'edit', 'remove']:
            raise Exception(f"Action '{action}' is not supported") 
        
        # get request data
        data = request.get_json()
        
        # check for required fields in data
        if data.get('parentCompanyId') is None:
            raise Exception('Parent company ID is not defined in request')
        if data.get('childCompanyId') is None:
            raise Exception('Child company ID is not defined in request')
        if action == 'edit' and data.get('attributes') is None:
            raise Exception(f'Attributes are not defined in request. Required for action: {action}')

        # get companies from db
        parent_company = Company.query.get(data['parentCompanyId'])
        if parent_company is None:
            raise Exception(f'Company with ID {data["parentCompanyId"]} not found')

        child_company = Company.query.get(data['childCompanyId'])
        if child_company is None:
            raise Exception(f'Company with ID {data["childCompanyId"]} not found')

        # get company-to-company association
        company_company = CompanyToCompany.query.filter(and_(
            CompanyToCompany.parent == parent_company,
            CompanyToCompany.child == child_company,
        )).first()
        if company_company is None:
            raise Exception(f'Company ID {data["parentCompanyId"]} does not have child company ID {data["childCompanyId"]}')

        # update attributes
        if action == 'edit':
            company_company.attributes = data['attributes']

        if action == 'remove':
            db.session.delete(company_company)

        # commit changes
        db.session.commit()
        
        # return updated admin data
        return jsonify(auth.current_user().get_admin_json()), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.warning(f"Failed to execute action '{action}'\nPayload: {request.get_json()}\nException: {e}")
        return {'error': str(e)}, 400

