"""
    Download all the data from a script and
    date: 01/10/2020
    author: Maurin
"""

import argparse
import os
import getpass
from datetime import date, timedelta

import boto3
from loreiosdk.spyglass_script import Spyglass

parser = argparse.ArgumentParser()
parser.add_argument('--s3_bucket', type=unicode)
parser.add_argument('--s3_path', type=unicode)
parser.add_argument('--s3_access_key_id', type=unicode)
parser.add_argument('--s3_secret_access_key', type=unicode)
parser.add_argument('--filename', default='tmp.txt', type=unicode)
parser.add_argument('--format', default='json', type=unicode)
parser.add_argument('--project_id', type=unicode)
parser.add_argument('--chart_id', type=unicode)
parser.add_argument('--url', default='wss://ui.getlore.io/storyteller',
                    type=unicode)
parser.add_argument('--usr', type=unicode)
parser.add_argument('--pwd', type=unicode)
parser.add_argument('--fltr', default='{}', type=unicode)
parser.add_argument('--local', dest='local', action='store_true')
parser.add_argument('--start_date', type=unicode)
parser.add_argument('--end_date', type=unicode)

args = parser.parse_args()

if args.end_date is None and args.start_date is None:
    today = date.today()
    args.start_date = str(today - timedelta(days=1))
    args.end_date = str(today)
assert args.end_date is not None and args.start_date is not None, "start_date and end_date need to be either both specified or both not specified"
print "\n  Using start_date = {}, end_date = {}".format(args.start_date,
                                                        args.end_date)

assert args.project_id is not None, "project_id must be specified"

if args.usr is None:
    args.usr = raw_input("Username : ")
if args.pwd is None:
    args.pwd = getpass.getpass()

s3_bucket = args.s3_bucket
s3_path = args.s3_path
s3_access_key_id = args.s3_access_key_id
s3_secret_access_key = args.s3_secret_access_key
filename = args.filename

# initialize spyglass
spyglass = Spyglass(args.url, args.usr, args.pwd)

if not args.local:
    assert s3_bucket, "S3 info ( s3_bucket ) required OR use --local"
    assert s3_path, "S3 info ( s3_path ) required OR use --local"
    assert s3_access_key_id, "S3 info ( s3_access_key_id ) required OR use --local"
    assert s3_secret_access_key, "S3 info ( s3_secret_access_key ) required OR use --local"
    # initialize s3
    s3 = boto3.client(
        's3',
        aws_access_key_id=s3_access_key_id,
        aws_secret_access_key=s3_secret_access_key
    )

(status, seqno, _) = spyglass.cmd('session', args.project_id)

# open a /tmp file
file = open(filename, "w")

# Example --fltr input on command line:
#       --fltr '{"op" : ">","left" : "5d5e2432cb856d4ccb1e64c2","right_type" : "constant","right" : 3}'

# get stream 
if args.format.lower() == 'json':
    chart_args = [args.chart_id, '--json']
elif args.format.lower() == 'csv':
    chart_args = [args.chart_id]
else:
    raise ValueError("--format should be one of ['csv','json']")

for data in spyglass.streaming_cmd('chart',
                                   *chart_args,
                                   stream=None,
                                   event_filter="'" + args.fltr + "'",
                                   start_date=args.start_date,
                                   end_date=args.end_date):
    # write to local tmp file
    file.write(data['message'])
file.close()

if not args.local:
    s3.upload_file(filename, s3_bucket, s3_path + '/' + filename)
    os.remove(filename)
