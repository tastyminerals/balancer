#!/usr/bin/env python3

import argparse
import calendar
import csv
import datetime
import re
import time


def init_vars(args):
    # read rc file if exists
    try:
        with open(args.config_file, 'r') as f:
            config = f.read()
        income = float(re.findall(r'income\W+([0-9]+)', config)[0])
        gain = float(re.findall(r'gain\W+([0-9]+)', config)[0])
    except OSError:
        print('".balancerc" not found!')
        config = []
        config.append(' '.join(['income:', input('Your current income? > ')]))
        config.append(' '.join(['gain:', input('Amount to gain? > ')]))
        with open('.balancerc', 'w') as f:
            f.write('\n'.join(config))
        income, gain = config
    # read costs.csv file
    try:
        with open(args.costs, 'r') as f:
            costs = csv.reader(f, delimiter=',')
            last_cost = float([row for row in costs][-1][-1])
    except OSError:
        print('"costs.csv" not found!')
        last_cost = float(input('Expenses? > '))
        costs = [time.ctime(), last_cost]
        with open('costs.csv', 'a') as f:
            csvfile = csv.writer(f, delimiter=',')
            csvfile.writerow(costs)

    # get current time object
    today = datetime.datetime.now()
    # get number of days in this month
    days = int(calendar.month(today.year, today.month).split()[-1])
    return income, gain, days, last_cost


def save_snapshot():
    pass

def balance(args):
    income, gain, days, last_cost = init_vars(args)
    # set goal
    diff = (income - gain)
    goal = round((diff / days), 2)
    new_goal = round(((diff + (goal - last_cost)) / days), 2)
    print(last_cost)
    print(goal)
    print(new_goal)

if __name__ == '__main__':
    prs = argparse.ArgumentParser(description="""
    Shows how much you can spend tomorrow based on the amount of money
    spent on previous days.""")
    prs.add_argument('-f', '--config_file', default=".balancerc",
                     help='Specify separate config file.',
                     required=False)
    prs.add_argument('-c', '--costs', default="costs.csv",
                     help='Specify separate consts.csv file.',
                     required=False)
    arguments = prs.parse_args()
    balance(arguments)
