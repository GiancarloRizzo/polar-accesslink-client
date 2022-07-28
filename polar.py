#!/usr/bin/env python

from __future__ import print_function

from utils import load_config, save_config
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
    

### user-data ###############################################################################################################################################################################################################################################

    def get_userinfo(self):
        """
        Returns basic user-data.
        """
        r = requests.post('https://www.polaraccesslink.com/v3/users', params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        else:
            self.config['user_id'] = r['member-id']
            save_config(self.config, CONFIG_FILENAME)
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}'.format(self.user_id), params={}, headers = self.headers)
        return json.loads(r.text)

    def delete_user(self, user_id):
        """
        Deletes user by user-id.
        """
        r = requests.delete('https://www.polaraccesslink.com/v3/users/{}'.user_id, params={}, headers = self.headers)
        return

### notifications ###########################################################################################################################################################################################################################################

    def get_notifications(self):
        r = requests.get('https://www.polaraccesslink.com/v3/notifications', params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        else:        
            return json.loads(r.text)

### activity ################################################################################################################################################################################################################################################

    def get_activity_transaction(self):
        """
        Returns transaction with list of available activities.
        """
        activities = []

        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/'.format(self.config['user_id']), params={}, headers = self.headers)

        if r.status_code  != 201:
            return []

        self.transaction = json.loads(r.text)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        activities = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        return activities

    def get_activity_summary(self, activities):
        """
        Returns activity-summaries for given list of activies.
        """
        summaries = {}
        
        for activity in activities:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}'.format(self.config['user_id'],self.transaction['transaction_id'],activity), params={}, headers = self.headers)
            if r.status_code != 200:
                return {}
            
            summaries[activity] = json.loads(r.text)
        return summaries

        
    def get_step_samples(self, activity):
        """
        Returns step-samples for given list of activies.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/step-samples'.format(self.config['user_id'],self.transaction['transaction_id'],activity), params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        
        stepsamples = json.loads(r.text)
        return stepsamples

    def get_zone_samples(self, activity):
        """
        Returns zone-samples for given list of activies.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}/activities/{}/zone-samples'.format(self.config['user_id'],self.transaction['transaction_id'],activity), params={}, headers = self.headers)
        if r.status_code != 200:
            return None
        
        zonesamples = json.loads(r.text)
        return zonesamples



### training data ######################################################################################################################################################################################################################################

    def get_training_transaction(self):
        """
        Returns transaction with list of available exercises.
        """
        exercises = []
        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions'.format(self.config['user_id']), params={}, headers = self.headers)
        if r.status_code != 201: #201==created
            return exercises
        
        self.transaction_training = json.loads(r.text)

        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'],self.transaction_training,exercises), params={}, headers = self.headers)
        exercises =  json.loads(r.text)


        requests.put('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'], self.transaction_training), params={}, headers = self.headers)
        return exercises


    def get_training_summary(self, trainings):
        """
        Returns training-summaries for given list of exercises.
        """
        summaries = {}
        
        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}'.format(self.config['user_id'],self.transaction['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return summaries
            
            summaries[training] = json.loads(r.text)
        return summaries

    def get_training_as_FIT(self, trainings):
        """
        Returns training-data in .FIT-fomat for given list of exercises.
        """
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/fit'.format(self.config['user_id'],self.transaction['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets


    def get_training_as_gpx(self, trainings):
        """
        Returns training-data in .GPX-fomat for given list of exercises.
        """
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/gpx'.format(self.config['user_id'],self.transaction['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

    
    def get_training_heartratezones(self, trainings):
        """
        Returns heartrate-rones for given list of exercises.
        """
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/heart-rate-zones'.format(self.config['user_id'],self.transaction['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

    # def get_available_samples():

    # def get_sample_data():

    def get_training_as_tcx(self, trainings):
        """
        Returns training-data in .TCX-fomat for given list of exercises.
        """
        exercise_datasets= {}

        for training in trainings:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}/exercises/{}/tcx'.format(self.config['user_id'],self.transaction['transaction_id'],training), params={}, headers = self.headers)
            if r.status_code != 200:
                return exercise_datasets
            
            exercise_datasets[training] = r.text
        return exercise_datasets

### sleep data ######################################################################################################################################################################################################################################

    def get_sleep(self):
        """
        Returns sleep-data for last 28 days.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/sleep', params={}, headers = self.headers)
        if r.status_code != 200:
            return ''
        else: 
            return json.loads(r.text)
    
    def get_sleep_by_date(self, date):
        """
        Returns sleep-data for given date in ISO-8601.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/sleep/{}'.format(date), params={}, headers = self.headers)
        if r.status_code != 200:
            return ''
        else: 
            return json.loads(r.text)
    
    def get_available_sleeps(self):
        """
        Returns all available sleeps within last 28 days.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/sleep/available', params={}, headers = self.headers)
        if r.status_code != 200:
            return []
        else: 
            return json.loads(r.text)

### recharges ########################################################################################################################################################################################################################################

    def get_recharges(self):
        """
        Returns recharge-data for last 28 days.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/nightly-recharge', params={}, headers = self.headers)
        if r.status_code != 200:
            return []
        else: 
            return json.loads(r.text)
    
    def get_recharge_by_date(self, date):
        """
        Returns recharge-data for given date in ISO-8601.
        """
        r = requests.get(f'https://www.polaraccesslink.com/v3/users/nightly-recharge/{date}', params={}, headers = self.headers)
        if r.status_code != 200:
            return {}
        else: 
            return json.loads(r.text)
    
### physical #########################################################################################################################################################################################################################################

    def get_physical_transaction(self):
        """
        Returns transaction with list of available physical-infos.
        """
        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/'.format(self.config['user_id']), params={}, headers = self.headers)

        if r.status_code  != 201:
            return None

        self.transaction_phy = json.loads(r.text)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/{}'.format(self.config['user_id'], self.transaction_phy['transaction-id']), params={}, headers = self.headers)
        physical_infos = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/{}'.format(self.config['user_id'], self.transaction_phy['transaction-id']), params={}, headers = self.headers)
        return physical_infos

    def get_physical_infos(self, transactions):
        """
        Returns available physical-infos for given list of physical-transactions
        """
        physical_infos = {}
        
        for transaction in transactions:
            r = requests.get('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/{}/physical-informations/{}'.format(self.config['user_id'],self.transaction_phy['transaction_id'],transaction), params={}, headers = self.headers)
            if r.status_code != 200:
                return physical_infos
            
            physical_infos[transaction] = json.loads(r.text)
        return physical_infos
