import queue
import json

class Messenger:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

    def announce_badge(self, badge, text=None, anchors=None, duration=None):
        # set toast props
        msg_data = {
            'uri': f'/{badge.type.name.lower()}/{badge.level.name.lower()}',
            'text': text or f'{badge.level.name} Badge {badge.type.title} Achieved',
            'anchorOrigin': anchors or {
                'vertical': 'top',
                'horizontal': 'left',
            },
            'autoHideDuration': duration,
        }

        # get the message
        message = self.format_dict(
            event='newbadge',
            data=msg_data,
        )
        
        self.announce(message)

    @classmethod
    def format_sse(cls, data: str, event=None) -> str:
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg

    @classmethod
    def format_dict(cls, data: dict, event=None) -> str:
        msg = f'data: {json.dumps(data)}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg
