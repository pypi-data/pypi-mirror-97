import requests
import json
try:
    from polzybackend import messenger
    noFlaskMode = False
except ImportError:
    # We're not in Flask
    noFlaskMode = True

base_url = "http://0.0.0.0:9000/"
token = None
header = None


def get_token():
    # fixme: This is the old gamification implementation, which should be completely removed
    return None

    global token, header
    res = requests.post(base_url + "auth/login", json={"email": "admin@fasifu.com", "password": "admin@fasifu"})
    token = json.loads(res.content).get("token")
    header = {'X-Auth-Token': token}
    if not token:
        print("Can't get AuthUser token!!")


def update_achievement(variable="policy_inquiry", user_id="1"):
    # fixme: This is the old gamification implementation, which should be completely removed
    return None

    if not token:
        try:
            get_token()
        except Exception as e:
            print("can't get user token. in GamificationHandler.py")

    if token:
        try:
            res = requests.post(base_url + f"increase_value/{variable}/{str(user_id)}", headers=header,
                                data={"value": "1"})
            json_response = json.loads(res.content)
            if json_response["achievements"]:
                announceMessage(
                    f"Congratulations! you have achieved {json_response['achievements'][0]['internal_name']}",
                    duration=5000
                )
        except Exception as ex:
            print(ex)


def announceMessage(message, duration=3000, level='default', horizontal='left', vertical='bottom'):
    if noFlaskMode:
        return
    msg = json.dumps({
        'text': message,
        'autoHideDuration': duration,
        'variant': level,
        'anchorOrigin': {
            'horizontal': horizontal,
            'vertical': vertical,
        }
    })
    messenger.announce(f"data: {msg}\n\n")

