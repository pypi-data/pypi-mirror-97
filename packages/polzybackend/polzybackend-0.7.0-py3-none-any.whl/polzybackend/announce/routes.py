from flask import Response
from polzybackend.announce import bp
from polzybackend import auth, db
from polzybackend import messenger
from polzybackend.models import ToastNotifications, GamificationBadge
import json
from logging import getLogger

logger = getLogger("PyC")

@bp.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = messenger.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(
        stream(),
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
            "X-Accel-Buffering": "no",
        },
        mimetype='text/event-stream',
    )


@bp.route("/notifications")#, methods=["POST"])
@auth.login_required
def notifications():
    user = auth.current_user()
    toast = db.session.query(ToastNotifications).filter_by(
        seen_at=None).filter_by(user_id=user.id).filter_by(company_id=user.company_id).first()
    if toast:
        if toast.type == "badge":
            badge = db.session.query(GamificationBadge).filter_by(id=toast.message).first()
            if badge:
                messenger.announce_badge(badge=badge, duration=5000)
            else:
                logger.info(f"Badge id {str(toast.message)} not found.")
        else:
            msg = json.dumps({
                'text': toast.message,
                'autoHideDuration': 3000,
                'variant': toast.type,
                'anchorOrigin': {
                    'horizontal': 'left',
                    'vertical': 'bottom',
                }
            })
            messenger.announce(f'data: {msg}\n\n')
        toast.set_seen()
        return Response(response=f"New Notifications found", status=200)
    return Response(response=f"No Notification", status=200)
