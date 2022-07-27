from argparse import ArgumentParser
from config import REDIRECT_URL
from polar import PolarAccessLink


if __name__ == '__main__':
    polar = PolarAccessLink()
    if polar.authorize() == 200:
        count = polar.get_activities()
        print(count)

