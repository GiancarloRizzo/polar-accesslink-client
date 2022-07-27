#!/usr/bin/env python

from __future__ import print_function

from utils import load_config
import requests
from accesslink import AccessLink
import json

CONFIG_FILENAME = "credentials.yml"



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
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.config['access_token'])
        }


    def get_activities(self):
        activities = []

        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/'.format(self.config['user_id']), params={}, headers = self.headers)

        if r.status_code  != 201:
            return activities

        self.transaction = json.loads(r.text)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        activities = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        return activities

    def get_activity_summary(self, activities):
        summaries = {}
        
        for activity in activities:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = self.headers)
            if r.status_code != 200:
                return summaries
            
            summaries[activity] = json.loads(r.text)
        return summaries

        
    def get_step_samples(self, activity):
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/step-samples'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        
        stepsamples = json.loads(r.text)
        return stepsamples

    def get_zone_samples(self, activity):
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/zone-samples'.format(self.config['user_id'],self.config['transaction_id'],activity), params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        
        zonesamples = json.loads(r.text)
        return zonesamples



### training data ######################################################################################################################################################################################################################################

    def get_training_transaction(self):
        exercises = []
        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions'.format(self.config['user_id']), params={}, headers = self.headers)
        if r.status_code != 201: #201==created
            return exercises
        
        self.transaction = json.loads(r.text)

        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'],self.config['transaction_id'],exercises), params={}, headers = self.headers)
        exercises =  json.loads(r.text)


        requests.put('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        return exercises


    def get_training_summary(self, trainings):
        summaries = {}
        
        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}'.format(self.config['user_id'],self.config['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return summaries
            
            summaries[training] = json.loads(r.text)
        return summaries

    def get_training_as_FIT(self, trainings):
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/fit'.format(self.config['user_id'],self.config['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets


    def get_training_as_gpx(self, trainings):
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/gpx'.format(self.config['user_id'],self.config['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

    
    def get_training_heartratezones(self, trainings):
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/heart-rate-zones'.format(self.config['user_id'],self.config['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

    # def get_available_samples():

    # def get_sample_data():

    def get_training_as_tcx(self, trainings):
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/tcx'.format(self.config['user_id'],self.config['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

### sleep data ######################################################################################################################################################################################################################################
