"""
    Download all the data from a chart and print it
    The data is JSON formatted
    date: 01/10/2020
    author: Maurin
"""

import argparse
from datetime import date, timedelta

from loreiosdk.spyglass_script import Spyglass

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_id')
parser.add_argument('--chart_id')
parser.add_argument('--url', default='wss://ui.getlore.io/storyteller')
parser.add_argument('--usr')
parser.add_argument('--pwd')
parser.add_argument('--start_date')
parser.add_argument('--end_date')

args = parser.parse_args()

if args.end_date is None and args.start_date is None:
    today = date.today()
    args.start_date = str(today - timedelta(days=1))
    args.end_date = str(today)

if not args.url or not args.usr or not args.pwd\
        or not args.dataset_id or not args.chart_id:
    raise Exception("Missing some information")

# initialize spyglass
spyglass = Spyglass(args.url, args.usr, args.pwd, args.dataset_id)

# tigger the command and get the data
for data in spyglass.streaming_cmd('chart',
                                   args.chart_id,
                                   stream=None,
                                   unlimited=None,
                                   json=None,
                                   start_date=None,
                                   end_date=args.end_date):
    print(data)
