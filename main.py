from argparse import ArgumentParser

from matplotlib.style import available
from config import REDIRECT_URL
from polar import PolarAccessLink
import oauth
from datetime import datetime, timedelta
from utils import write_json2file

searched_day = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    polar = PolarAccessLink()

    if oauth.run() == True:
        ### test userinfo ###

        user_data = polar.get_userinfo()
        print('type: '+str(type(user_data)))
        print('content: '+str(user_data))
        write_json2file(user_data, 'user_data.json')

        ### test activities ###

        activity_transaction = polar.get_activity_transaction()
        print('type: '+str(type(activity_transaction)))
        print('content: '+str(activity_transaction))
        write_json2file(activity_transaction, 'activity_transactions.json')
        
        activity_transaction = {
            "activity-log": [
                "https://www.polaraccesslink.com/v3/users/58763163/activity-transactions/679748935/activities/1538467360",
                "https://www.polaraccesslink.com/v3/users/58763163/activity-transactions/679748935/activities/1538467384"
            ]
        }
        if 'activity-log' in activity_transaction:
            activity_data = polar.get_activity_summary(activity_transaction['activity-log'])
            print('type: '+str(type(activity_data)))
            print('content: '+str(activity_data))
            write_json2file(activity_data, 'activity_summaries.json')

            activity_stepsamples = polar.get_step_samples(activity_transaction['activity-log'])
            print('type: '+str(type(activity_data)))
            print('content: '+str(activity_data))
            write_json2file(activity_stepsamples, 'activity_stepsamples.json')

            activity_zonesamples = polar.get_zone_samples(activity_transaction['activity-log'])
            print('type: '+str(type(activity_data)))
            print('content: '+str(activity_data))
            write_json2file(activity_zonesamples, 'activity_zonesamples.json')
        else:
            print('no activity-transactions-available.')

        ### test training ###

        exercise_transaction = polar.get_training_transaction()
        print('type: '+str(type(exercise_transaction)))
        print('content: '+str(exercise_transaction))
        write_json2file(exercise_transaction, 'exercise_transactions.json')

        if 'exercises' in exercise_transaction:
            training_summaries = polar.get_training_summary(exercise_transaction['exercises'])
            print('type: '+str(type(training_summaries)))
            print('content: '+str(training_summaries))
            write_json2file(training_summaries, 'training_summaries.json')

            training_zones = polar.get_training_heartratezones(exercise_transaction['exercises'])
            print('type: '+str(type(training_zones)))
            print('content: '+str(training_zones))
            write_json2file(training_zones, 'training_zones.json')

            training_fitdata = polar.get_training_as_FIT(exercise_transaction['exercises'])
            print('type: '+str(type(training_fitdata)))
            print('content: '+str(training_fitdata))
            write_json2file(training_fitdata, 'training_fitdata.json')

            training_gpxdata = polar.get_training_as_gpx(exercise_transaction['exercises'])
            print('type: '+str(type(training_gpxdata)))
            print('content: '+str(training_gpxdata))
            write_json2file(training_gpxdata, 'training_gpxdata.json')

            training_tcxdata = polar.get_training_as_tcx(exercise_transaction['exercises'])
            print('type: '+str(type(training_tcxdata)))
            print('content: '+str(training_tcxdata))
            write_json2file(training_gpxdata, 'training_gpxdata.json')

        else:
            print('no training transactions available.')

        ### test sleep ###

        sleeps = polar.get_sleep()
        print('type: '+str(type(sleeps)))
        print('content: '+str(sleeps))
        write_json2file(sleeps, 'sleeps.json')


        sleep_data = polar.get_sleep_by_date(searched_day)
        print('type: '+str(type(sleep_data)))
        print('content: '+str(sleep_data))
        write_json2file(sleep_data, 'sleep_by_date_'+searched_day+'.json')

        available_sleeps = polar.get_available_sleeps()
        print('type: '+str(type(available_sleeps)))
        print('content: '+str(available_sleeps))
        write_json2file(available_sleeps, 'available_sleeps.json')

        ### test recharges ###

        recharges = polar.get_recharges()
        print('type: '+str(type(recharges)))
        print('content: '+str(recharges))        
        write_json2file(recharges, 'recharges.json')

        recharge = polar.get_recharge_by_date(searched_day)
        print('type: '+str(type(recharge)))
        print('content: '+str(recharge))
        write_json2file(recharge, 'recharge_by_date_'+searched_day+'.json')

        ### test physical ####
        phy_transaction = polar.get_physical_transaction()
        print('type: '+str(type(phy_transaction)))
        print('content: '+str(phy_transaction))
        write_json2file(phy_transaction, 'phy_transaction.json')


        if 'physical-informations' in phy_transaction:
            physical_data = polar.get_physical_infos(phy_transaction['physical-informations'])
            print('type: '+str(type(physical_data)))
            print('content: '+str(physical_data))
            write_json2file(physical_data, 'physical_data.json')

        else:
            print('no physical-info-transactions available.')


        print('test finished')
    else:
        print('Authentication failed. Check your client_id and client_secret in credentials.yml')
