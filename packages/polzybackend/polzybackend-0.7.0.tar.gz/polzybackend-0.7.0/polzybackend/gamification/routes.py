from flask import jsonify, request, current_app
from polzybackend.gamification import bp
from polzybackend.models import GamificationBadge, GamificationBadgeType
from polzybackend import auth
from polzybackend.utils.import_utils import gamification_ranking


@bp.route('/badges')
@auth.login_required
def badges():
    #
    # returns list of all user badges
    #

    try:
        badges = [badge.to_json() for badge in auth.current_user().badges]
        return jsonify(badges), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get Gamification Badges: {e}')
        return jsonify({'error': 'Bad Request'}), 400


def filter_badge(x, badge):
    if x.type.name == badge.get('type') and x.level.name == badge.get('level'):
        return x


@bp.route('/badges/seen', methods=['POST'])
@auth.login_required
def make_badge_seen():
    #
    # makes the bage as seen
    #

    try:

        # get request data and badge
        data = request.get_json()
        badge = data.get('badge')
        if badge is None:
            raise Exception('Badge data not found in request')

        ###### DEUG OUTPUT
        print("\n**** Badge Seen:")
        import json
        print(json.dumps(data, indent=2))

        # find badge in user badges
        userBadge = list(filter(lambda x: filter_badge(x, badge), auth.current_user().badges))
        if len(userBadge) == 0:
            raise Exception(f"Badge Type {badge.get('type')} not found in user's badges")

        # update badge instance
        userBadge[0].set_seen()

        # return updated lit of badges
        return jsonify([badge.to_json() for badge in auth.current_user().badges]), 200

    except Exception as e:
        current_app.logger.exception(f'Making Gamification Badge seen fails: Badge={badge}\n{e}')
        return jsonify({'error': 'Bad Request'}), 400


@bp.route('/badges/types')
@auth.login_required
def badge_types():
    #
    # returns list of available types of badges
    #

    try:
        badge_types = GamificationBadgeType.query.order_by('id').all()
        return jsonify([badge.to_json() for badge in badge_types]), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get Gamification Badge Types: {e}')
    
    return jsonify({'error': 'Bad Request'}), 400


@bp.route('/rankings')
@auth.login_required
def rankings():
    #
    # returns user's rankings
    #

    try:
        return jsonify(gamification_ranking(auth.current_user())), 200
    except Exception as e:
        current_app.logger.exception(f"Faild to get user's gamification rankings: {e}")
    
    return jsonify({'error': 'Bad Request'}), 400


