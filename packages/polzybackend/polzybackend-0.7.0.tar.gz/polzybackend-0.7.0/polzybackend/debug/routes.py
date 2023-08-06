from . import bp
from polzybackend import messenger, db
from polzybackend.models import User, GamificationBadge, GamificationBadgeType, GamificationBadgeLevel
from flask import jsonify
import json
from random import sample, choice

# toast debugging route
@bp.route('/ping')
def ping():
    #msg = messenger.format_sse(data='ping', event='fasifu')
    data = {
        'text': 'Fasifu message!',
        #'variant': 'success',
        #'anchorOrigin': {
        #    'vertical': 'top',
        #    'horizontal': 'left',
        #},
        #'autoHideDuration': 2000,
    }
    msg = f"data: {json.dumps(data)}\n\n"
    messenger.announce(msg=msg)
    return {'success': msg}, 200


# new badge for admin in current organization
@bp.route('/newbadge')
def newbadge():

    # get user 
    user = User.query.first()
    if user is None:
        return {'error': 'There are no user in DB'}, 400

    # create random badge
    # get possible types
    badge_level = GamificationBadgeLevel.query.first()
    all_types = GamificationBadgeType.query.all()
    search_type = True
    count = 0
    while search_type:
        badge_type = choice(all_types)
        search_type = any(b.type == badge_type for b in user.badges)
        if search_type:
            current_badge = next(filter(lambda b: b.type == badge_type, user.badges))
            #search_type = any(b.type == badge_type and b.level.next_level is None for b in user.badges)
            if current_badge.level.next_level:
                badge_level = current_badge.level.next_level
                new_badge = current_badge
                new_badge.level = badge_level
                new_badge.is_seen = False
                search_type = False
        else:
            new_badge = GamificationBadge(
                user=user,
                company=user.company.company,
                type=badge_type,
                level=badge_level,
            )
            db.session.add(new_badge)

        # break if all user badges of the highest level
        if count > 100:
            raise Exception('No new badge is available:(')
    
    db.session.commit()

    messenger.announce_badge(new_badge)
    return {'success': 'OK'}, 200


# returns all available users
@bp.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.email for u in users]), 200

