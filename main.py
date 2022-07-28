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

        # data = polar.get_userinfo()
        # print('type: '+str(type(data)))
        # print('content: '+str(data))

        ### test notifications ### 

        # data = polar.get_notifications()
        # print('type: '+str(type(data)))
        # print('content: '+str(data))

        ### test activities ###

        # activity_transaction = polar.get_activities()
        # print('type: '+str(type(activity_transaction)))
        # print('content: '+str(activity_transaction))
        
        # if 'activity-log' in activity_transaction:
        #     activity_data = polar.get_activity_summary(activity_transaction['activity-log'])
        #     print('type: '+str(type(activity_data)))
        #     print('content: '+str(activity_data))

        #     activity_data = polar.get_step_samples(activity_transaction['activity-log'])
        #     print('type: '+str(type(activity_data)))
        #     print('content: '+str(activity_data))

        #     activity_data = polar.get_zone_samples(activity_transaction['activity-log'])
        #     print('type: '+str(type(activity_data)))
        #     print('content: '+str(activity_data))
        # else:
        #     print('no activity-transactions-available.')

        ### test training ###

        # exercise_transaction = polar.get_training_transaction()
        # print('type: '+str(type(exercise_transaction)))
        # print('content: '+str(exercise_transaction))

        # if 'exercises' in exercise_transaction:
        #     training_data = polar.get_training_summary(exercise_transaction['exercises'])
        #     print('type: '+str(type(training_data)))
        #     print('content: '+str(training_data))

        #     training_data = polar.get_training_heartratezones(exercise_transaction['exercises'])
        #     print('type: '+str(type(training_data)))
        #     print('content: '+str(training_data))

        #     training_data = polar.get_training_as_FIT(exercise_transaction['exercises'])
        #     print('type: '+str(type(training_data)))
        #     print('content: '+str(training_data))

        #     training_data = polar.get_training_as_gpx(exercise_transaction['exercises'])
        #     print('type: '+str(type(training_data)))
        #     print('content: '+str(training_data))

        #     training_data = polar.get_training_as_tcx(exercise_transaction['exercises'])
        #     print('type: '+str(type(training_data)))
        #     print('content: '+str(training_data))
        # else:
        #     print('no training transactions available.')

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

        # ## test physical ####
        # phy_transaction = polar.get_physical_transaction()
        # print('type: '+str(type(phy_transaction)))
        # print('content: '+str(phy_transaction))
        # write_json2file(phy_transaction, 'phy_transaction.json')


        # if 'physical-informations' in phy_transaction:
        #     physical_data = polar.get_physical_infos(phy_transaction['physical-informations'])
        #     print('type: '+str(type(physical_data)))
        #     print('content: '+str(physical_data))
        #     write_json2file(physical_data, 'physical_data.json')

        # else:
        #     print('no physical-info-transactions available.')


        print('test finished')
    else:
        print('Authentication failed. Check your client_id and client_secret in credentials.yml')
