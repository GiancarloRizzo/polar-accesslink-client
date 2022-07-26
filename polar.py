#!/usr/bin/env python

from __future__ import print_function

from utils import load_config
import requests
from accesslink import AccessLink
import json
CONFIG_FILENAME = "config.yml"


try:
    input = raw_input
except NameError:
    pass



class PolarAccessLink(object):
    """Example application for Polar Open AccessLink v3."""

    def __init__(self):
        self.config = load_config(CONFIG_FILENAME)

        if "access_token" not in self.config:
            print("Authorization is required. Run authorization.py first.")
            return

        self.accesslink = AccessLink(client_id=self.config["client_id"],
                                     client_secret=self.config["client_secret"],
                                     )


    def get_activities(self):
        activities = []
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.config['access_token'])
        }

        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/'.format(self.config['user_id']), params={}, headers = headers)

        if r.status_code  != 200:
            return activities

        self.transaction = json.loads(r.text)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = headers)
        activities = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = headers)
        return activities

    def get_activity_summary(self, activities):
        summaries = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.config['access_token'])
        }
        
        for activity in activities:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = headers)
            if r.status_code != 200:
                return summaries
            
            summaries['activity_id'] = json.loads(r.text)
        return summaries

        
    def get_step_samples(self, activity):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.config['access_token'])
        }

        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/step-samples'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = headers)
        if r.status_code != 200:
            return 'status_code: '+str(r.status_code)
        
        stepsamples = json.loads(r.text)
        return stepsamples

    def get_zone_samples(self, activity):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.config['access_token'])
        }

        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/zone-samples'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = headers)
        if r.status_code != 200:
            return 'status_code: '+str(r.status_code)
        
        zonesamples = json.loads(r.text)
        return zonesamples



### training data ######################################################################################################################################################################################################################################
    # def get_trainingdata_metrics(self):
    #     data = self.accesslink.training_data.create_transaction(self.config["user_id"], self.config["access_token"])
    #     return data

### training data ######################################################################################################################################################################################################################################
    # def get_physicalinfo_metrics(self):
    #     data = self.accesslink.physical_info.create_transaction(self.config["user_id"], self.config["access_token"])      
    #     return data

### training data ######################################################################################################################################################################################################################################
    # def get_userdata(self):
    #     data = self.accesslink.users.get_information(self.config["user_id"], self.config["access_token"])
    #     return data