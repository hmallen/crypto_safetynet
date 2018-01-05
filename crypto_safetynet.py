#!./env/bin/python

import argparse
import configparser
import datetime
from decimal import *
import logging
import os
import poloniex
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

poloniex_config_path = 'config/poloniex.ini'

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#parser = argparse.ArgumentParser()
#parser.add_argument()
#parser.add_argument()
#parser.add_argument()
#args = parser.parser_args()


def get_balances():
    user_balances = polo.returnAvailableAccountBalances()['exchange']
    try:
        bal_str = Decimal(user_balances['STR'])
    except:
        bal_str = Decimal(0)
    try:
        bal_usdt = Decimal(user_balances['USDT'])
    except:
        bal_usdt = Decimal(0)
    
    bal_dict = {'str': bal_str, 'usdt': bal_usdt}

    return bal_dict


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(poloniex_config_path)
    
    api_key = config['live']['key']
    api_secret = config['live']['secret']

    polo = poloniex.Poloniex(api_key, api_secret)

    loop_time = 30

    while (True):
        try:
            account_balances = get_balances()
            try:
                balance_str = account_balances['str']
            except KeyError:
                balance_str = 0
            try:
                balance_usdt = account_balances['usdt']
            except KeyError:
                balance_usdt = 0
            
            logger.info('Balance STR:  ' + str(balance_str))
            logger.info('Balance USDT: ' + str(balance_usdt))

            time.sleep(loop_time)

        except Exception as e:
            logger.exception(e)
            sys.exit(1)

        except KeyboardInterrupt:
            logger.info('Exit signal received.')
            sys.exit()
