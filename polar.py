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

    def register_user(self):
        """
        Register user based on oauth2-authentication-credentials. No return-value.
        """
        r = requests.post('https://www.polaraccesslink.com/v3/users', params={}, headers = self.headers)
        self.config['user_id'] = r['member-id']
        save_config(self.config, CONFIG_FILENAME)
        return 

    def delete_user(self, user_id):
        """
        Deletes user by user-id. No return-value.
        """
        r = requests.delete('https://www.polaraccesslink.com/v3/users/{}'.format(user_id), params={}, headers = self.headers)
        return

    def get_userinfo(self):
        """
        Returns basic user-data.
        """
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}'.format(self.config['user_id']), params={}, headers = self.headers)
        return json.loads(r.text)

### notifications ###########################################################################################################################################################################################################################################
    # cant fetch any notifications via api-call...
    # def get_notifications(self):
    #     r = requests.get('https://www.polaraccesslink.com/v3/notifications', params={}, headers=self.headers)
    #     if r.status_code != 200:
    #         print('statuscode for notifications: '+str(r.status_code))
    #         return None
    #     else:        
    #         return json.loads(r.text)

### activity ################################################################################################################################################################################################################################################

    def get_activity_transaction(self):
        """
        Returns transaction with list of available activities. 
        
        Once a transaction is done, the same transaction-data is not available by an additional request anymore.
        
        Only data that has been uploaded to Flow after the user has been registered to your client will be available. 
        Only data that has been uploaded in the last 30 days will be available.
        """
        activities = []

        r = requests.post('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/'.format(self.config['user_id']), params={}, headers = self.headers)

        if r.status_code  != 201:
            return []

        self.transaction = json.loads(r.text)
        print(self.transaction)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        activities = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/activity-transactions/{}'.format(self.config['user_id'], self.transaction['transaction-id']), params={}, headers = self.headers)
        return activities

    def get_activity_summary(self, activities):
        """
        Returns list of activity-summaries for given list of activities.
        """
        summaries = []
        
        for activity in activities:
            r = requests.get('{}'.format(activity), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            summaries.append(json.loads(r.text))
        return summaries

        
    def get_step_samples(self, activities):
        """
        Returns list of step-samples for given list of activities.
        """
        stepsamples = []

        for activity in activities:
            r = requests.get('{}'.format(activity), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            stepsamples.append(json.loads(r.text))
        return stepsamples

    def get_zone_samples(self, activities):
        """
        Returns list of zone-samples for given list of activies.
        """
        zonesamples = []

        for activity in activities:
            r = requests.get('{}'.format(activity), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            zonesamples.append(json.loads(r.text))
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
        print(self.transaction_training)
        
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'],self.transaction_training['transaction-id']), params={}, headers = self.headers)
        print(r.status_code)
        exercises = json.loads(r.text)


        requests.put('https://www.polaraccesslink.com/v3/users/{}/exercise-transactions/{}'.format(self.config['user_id'], self.transaction_training['transaction-id']), params={}, headers = self.headers)
        print(r.status_code)
        return exercises


    def get_training_summary(self, trainings):
        """
        Returns list of training-summaries for given list of exercises.
        """
        summaries = []
        
        for training in trainings:
            r = requests.get('{}'.format(training), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            summaries.append(json.loads(r.text))
        return summaries

    def get_training_as_FIT(self, trainings):
        """
        Returns list of training-data in .FIT-fomat for given list of exercises.
        """
        exercise_datasets= []

        for training in trainings:
            r = requests.get('{}'.format(training), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            exercise_datasets.append(json.loads(r.text))
        return exercise_datasets


    def get_training_as_gpx(self, trainings):
        """
        Returns list of training-data in .GPX-fomat for given list of exercises.
        """
        exercise_datasets= []

        for training in trainings:
            r = requests.get('{}'.format(training), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            exercise_datasets.append(json.loads(r.text))
        return exercise_datasets

    
    def get_training_heartratezones(self, trainings):
        """
        Returns heartrate-rones for given list of exercises.
        """
        exercise_datasets= []

        for training in trainings:
            r = requests.get('{}'.format(training), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            exercise_datasets.append(json.loads(r.text))
        return exercise_datasets

    def get_training_as_tcx(self, trainings):
        """
        Returns list of training-data in .TCX-fomat for given list of exercises.
        """
        exercise_datasets= []

        for training in trainings:
            r = requests.get('{}'.format(training), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            exercise_datasets.append(json.loads(r.text))
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
        Returns list of all available sleeps within last 28 days.
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
            return {}

        self.transaction_phy = json.loads(r.text)
        r = requests.get('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/{}'.format(self.config['user_id'], self.transaction_phy['transaction-id']), params={}, headers = self.headers)
        physical_infos = json.loads(r.text)

        requests.put('https://www.polaraccesslink.com/v3/users/{}/physical-information-transactions/{}'.format(self.config['user_id'], self.transaction_phy['transaction-id']), params={}, headers = self.headers)
        return physical_infos

    def get_physical_infos(self, transactions):
        """
        Returns list of all available physical-infos for given list of physical-transactions
        """
        physical_infos = []
        
        for transaction in transactions:
            r = requests.get('{}'.format(transaction), params={}, headers = self.headers)
            print(r.status_code)
            if r.status_code != 200:
                print('continued')
                continue
            
            physical_infos.append(json.loads(r.text))
        return physical_infos
