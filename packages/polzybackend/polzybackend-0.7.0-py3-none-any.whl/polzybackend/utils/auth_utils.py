from random import choice
from datetime import datetime, timedelta
from functools import reduce
import uuid
import string
import json


ACCESS_KEY_LENGTH = 64
EXPIRED_HOURS = 24


def generate_token(length=ACCESS_KEY_LENGTH):
    simbols = string.ascii_letters + string.digits + '!#$%&*+-<=>?@'
    return ''.join(choice(simbols) for i in range(length))


def get_expired(hours=EXPIRED_HOURS, days=0):
    return datetime.utcnow() + timedelta(hours=hours, days=days)


def is_supervisor(company):
	return reduce(lambda result, role: result or role.is_supervisor, company.roles, False)

def load_attributes(attributes):
	try:
		return json.loads(attributes)
	except Exception:
		return None
