import uuid

#
# system date format
#
date_format = "%Y-%m-%d"


#
# id generator
#
def generate_id():
    return str(uuid.uuid4())