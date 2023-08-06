from flask import current_app
from importlib import import_module
from polzybackend.mediators import Policy, Antrag
#from polzybackend.models import Activity


def import_class(name):
    #
    # imports class from string 'name' 
    #

    components = name.split('.')
    module_name = '.'.join(components[:-1])
    mod = import_module(module_name)
    cls = getattr(mod, components[-1])
    return cls


'''
def activity_class(activity_type_class):
    #
    # returns activity class
    #

    if current_app.config.get(activity_type_class):
        return import_class(current_app.config.get(activity_type_class))

    return Activity
'''

def all_stages():
    #
    # returns list of all stages
    #

    if current_app.config.get('CLASSNAME_STAGES'):
        lClass = import_class(current_app.config.get('CLASSNAME_STAGES'))()
        return lClass.getAllStages

    raise Exception('Method to Get Stages NOT defined')


def record_login(user):
    if current_app.config.get('LOGIN_RECORDER'):
        import_class(current_app.config.get('LOGIN_RECORDER'))(user).record_login_activity()


def permissions(user):
    #
    # returns user's permissions
    #
    record_login(user)
    if current_app.config.get('METHOD_GET_PERMISSIONS'):
        permissions_method = import_class(current_app.config['METHOD_GET_PERMISSIONS'])
        return permissions_method(user)

    # default method
    return user.get_permissions()


def policy_class():
    #
    # returns policy class of the current implementation
    #

    if current_app.config.get('CLASSNAME_POLICY'):
        return import_class(current_app.config.get('CLASSNAME_POLICY'))

    return Policy


def antrag_class():
    #
    # returns antrag class of the current implementation
    #

    if current_app.config.get('CLASSNAME_ANTRAG'):
        return import_class(current_app.config['CLASSNAME_ANTRAG'])

    return Antrag

def antrag_products():
    #
    # returns list of avalaibale products
    #

    if current_app.config.get('CLASSNAME_PRODUCTS'):
        return import_class(current_app.config['CLASSNAME_PRODUCTS'])

    raise Exception('Class NOT difined to derive products')

def gamification_ranking(user):
    #
    # returns user's gamification ranking
    #

    if current_app.config.get('CLASSNAME_GAMIFICATION_HITLIST'):
        lClass = import_class(current_app.config.get('CLASSNAME_GAMIFICATION_HITLIST'))()
        return lClass.deriveUserRanking(user)

    raise Exception("Class NOT difined to derive user's ranking")
