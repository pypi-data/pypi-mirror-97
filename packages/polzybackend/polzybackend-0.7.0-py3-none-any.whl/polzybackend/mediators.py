from polzybackend.utils import generate_id
import uuid
from copy import deepcopy


class Policy:
    #
    # Policy details, activities, attributes 
    #

    def __init__(self, number, date):
        #
        # initialization
        #

        self.id = generate_id()
        self.number = number
        self.effective_date = date
        self.data = None
        self.user = None

    def set_user(self, user):
        self.user = deepcopy(user)

    def setStage(self, stage):
        self.stage = stage

    def setLanguage(self, language):
        self.language = language

    def fetch(self):
        #
        # IMPORTANT: this method should be define within custon implementation
        #
        # fetches policy details from Policy Management System
        #

        raise Exception('Method "fetch" is not defined in Policy class')

    def getValueList(self, valueListName):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # returns list of values of the given name 
        #

        raise Exception('Method "getValueList" is not defined in Policy class')

    def executeActivity(self, data):
        #
        # IMPORTANT: this method should be define within custon implementation
        #
        # executes policy activity defined in data
        #

        raise Exception('Method "executeActivity" is not defined in Policy class')

    def get(self):
        #
        # returns Policy data
        #

        result = {'id': self.id}
        if self.data:
            result.update(self.data)

        return result


class Antrag:
    #
    # PoLZy interface instance for antrag
    #

    def __init__(self, product_name, user):
        self.id = generate_id()
        self.product_name = product_name
        self.user = deepcopy(user)
        self.instance = None


    def clone(self):
        antrag_copy = deepcopy(self)
        antrag_copy.id = generate_id()

        return antrag_copy


    def initialize(self):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # initializes antrag instance within Policy Management System 
        #

        raise Exception('Initialize method is not defined in Antrag class')


    def get(self):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # returns antrag instance as json object to front-end 
        #

        raise Exception('Method "get" is not defined in Antrag class')


    def getValueList(self, valueListName):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # returns list of values of the given name 
        #

        raise Exception('Method "getValueList" is not defined in Antrag class')
 

    def updateFields(self, data):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # updates antrag fields based on data
        #

        raise Exception('Method "updateFields" is not defined in Antrag class')


    def executeActivity(self, data):
        #
        # IMPORTANT: this method should be define within custom implementation
        #
        # executes antrag activity defined in data
        #

        raise Exception('Method "executeActivity" is not defined in Antrag class')

