#!/usr/bin/env python3

import argparse
import calendar as cal
import csv
import datetime
import os
import re
import time


def check(inp):
    """Checking if user input is clean"""
    while True:
        if re.sub(r'[0-9.]+', '', inp):
            inp = input('Incorrect input! > ')
        else:
            return float(inp)


def init_vars(args):
    """Initializing vars saved during previous sessions"""
    # read snapshot file
    try:
        with open(args.snapshot, 'r') as f:
            csvfile = csv.reader(f, delimiter=',')
            lastrow = [row for row in csvfile if row][-1]
            last_diff = float(lastrow[-2])
            last_cost = float(lastrow[-1])
    except Exception as ex:
        print('"snapshot.csv" not found! creating...')
        with open(args.snapshot, 'w') as f:
            csvfile = csv.writer(f, delimiter=',')
            income = check(input('Your current income?> '))
            gain = check(input('Amount to gain?> '))
            last_cost = check(input("Today's costs?> "))
            last_diff = income - gain
            csvfile.writerow([time.ctime(), last_diff, last_cost])

    # get current time object
    today = datetime.datetime.now()
    # get number of days left in this month
    days_left = int(cal.month(today.year, today.month).split()[-1]) - today.day
    return days_left, last_cost, last_diff


def add_costs(costs, args):
    """Adding the amount of money spent today"""
    days_left, last_cost, last_diff = init_vars(args)
    with open(args.snapshot, 'a') as f:
        csvfile = csv.writer(f, delimiter=',')
        goal = round((last_diff / days_left), 2)
        last_diff = last_diff + (goal - (last_cost * 2))
        csvfile.writerow([time.ctime(), last_diff, costs])
        last_cost = costs
    print('snapshot.csv updated.')
    return days_left, last_cost, last_diff


def clean(args):
    """Erasing history"""
    if re.match(r'[yY].*', input('Erase history? (y/n)> ')):
        open(args.snapshot, 'w').close()
        print('{0} successfully erased.'.format(args.snapshot))


def balance(args):
    if args.clean:
        clean(args)
    if args.add:
        days_left, last_cost, last_diff = add_costs(check(args.add), args)
    else:
        days_left, last_cost, last_diff = init_vars(args)

    # set goal
    goal = round((last_diff / days_left), 2)
    # calculating new goal based on the days and money left
    new_goal = round(((last_diff + (goal - (last_cost * 2))) / days_left), 2)
    print('Maximum', new_goal, 'per day.')


if __name__ == '__main__':
    prs = argparse.ArgumentParser(description="""
    This is a small util that helps you to control your daily consts.
    Just answer two questions:
        What is your monthly income?
        How much do you want to save?
    And this util will calculate the max amount of money you can spend per day
    in order to reach your saving goal.
    """)
    prs.add_argument('-a', '--add',
                     help='Add a daily cost (amount of money spent today).',
                     required=False)
    prs.add_argument('-i', '--income',
                     help='Modify income constant.',
                     required=False)
    prs.add_argument('-g', '--gain',
                     help='Modify gain constant.',
                     required=False)
    prs.add_argument('-s', '--snapshot', default="snapshot.csv",
                     help='Specify separate snapshot.csv file.',
                     required=False)
    prs.add_argument('-clean', '--clean', action='store_true',
                     help='Erases snapshot.csv history.',
                     required=False)
    arguments = prs.parse_args()
    balance(arguments)

