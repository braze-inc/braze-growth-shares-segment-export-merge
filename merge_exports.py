#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import os

from datetime import datetime, timedelta
import re
import gzip
import json
import requests
import csv
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import io
from io import TextIOWrapper
from zipfile import ZipFile
import logging
import boto3
import gc

from dotenv import load_dotenv
load_dotenv()

# Method to process s3 bucket, and save to cloud storage
# All files within the data directory will be process then moved to a done folder.
def mergeExports():
    exportsdir = './' + os.environ['exportdir'].rstrip('/').lstrip('/').strip() + '/'
    brazefields = [sf.strip() for sf in os.environ['exportfields'].split(',')]

    dateprefix = datetime.utcnow().strftime('%Y-%m-%d_%H%M%S')
    fileprefix ="./"
    if ('outputpath' in os.environ) and  (os.environ['outputpath'].strip()):
        fileprefix += os.environ['outputpath'].strip().rstrip('/').lstrip('/') + '/'



    extract = True
    extension = 'csv'

    if ('extractfiles' in os.environ) and (os.environ['extractfiles'].strip().lower() in ['false', '0', 'f', 'n', 'no']):
        extract = False
    combineonly = False
    if ('combineonly' in os.environ) and (os.environ['combineonly'].strip().lower() in ['true', '1', 't', 'y', 'yes']):
        combineonly = True
    fileformat = 'comma'
    delimiter = ','
    if ('fileformat' in os.environ):
        if (os.environ['fileformat'].strip().lower() in ['tab']):
            fileformat = 'tab'
            delimiter = '\t'
        elif (os.environ['fileformat'].strip().lower() in ['json']):
            fileformat = 'json'
    outdelimiter = ','
    if ('outputdelimiter' in os.environ) and (os.environ['outputdelimiter'].strip().lower() in ['tab']):
        outdelimiter = '\t'
        extension = 'txt'

    outfile = open("{}{}_{}_results.{}".format(fileprefix,os.environ['outputname'].strip(),dateprefix,extension), "w")
    if not combineonly:
        csvwriter = csv.writer(outfile, delimiter=outdelimiter)
        outfile.write(outdelimiter.join(brazefields) + "\n")

    exportslist = os.scandir(exportsdir)
    for exportfile in exportslist:
        if (exportfile.is_file()):
            if (exportfile.name.endswith(('.zip', '.gz'))):
                with ZipFile(exportfile, 'r') as zip:
                    for csvs in zip.infolist():
                        print("Processing file {} in {}".format(csvs.filename,exportfile.name))
                        csvfile = zip.open(csvs, 'r')

                        if combineonly:
                            # for rows in csvfile:
                            # csvfile = zip.read(csvs, 'r')
                            csvdata = TextIOWrapper(csvfile, 'utf-8')
                            for rows in csvdata:
                                outfile.write(rows)
                        else:
                            if (fileformat == 'json'):
                                csvdata = TextIOWrapper(csvfile, 'utf-8')
                                for records in csvdata:
                                    record_json = json.loads(records)
                                    row = []
                                    for fields in brazefields:
                                        if fields in record_json:
                                            row.append(record_json[fields])
                                        else:
                                            if 'custom_attributes' in record_json:
                                                if fields in record_json['custom_attributes']:
                                                    row.append(record_json['custom_attributes'][sfv])
                                                else:
                                                    row.append(None)
                                            else:
                                                row.append(None)
                                    csvwriter.writerow(row)
                            else:
                                csvdata = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'), delimiter=delimiter)
                                for records in csvdata:
                                    row = []
                                    for fields in brazefields:
                                        if fields in records:
                                            row.append(records[fields])
                                        else:
                                            row.append(None)
                                            # print(records[fields], end=',')
                                    csvwriter.writerow(row)
            elif exportfile.name.endswith(('.txt','.csv','.tab')):
                print("Processing file {}".format(exportfile.name))
                csvfile = open(exportfile, 'r')

                if combineonly:
                    # csvfile = read(exportfile, 'r')
                    for rows in csvfile:
                        outfile.write(rows)
                else:
                    if fileformat == 'json':
                        for records in csvfile:
                            record_json = json.loads(records)
                            row = []
                            for fields in brazefields:
                                if fields in record_json:
                                    row.append(record_json[fields])
                                else:
                                    if 'custom_attributes' in record_json:
                                        if fields in record_json['custom_attributes']:
                                            row.append(record_json['custom_attributes'][sfv])
                                        else:
                                            row.append(None)
                                    else:
                                        row.append(None)
                            csvwriter.writerow(row)
                    else:
                        csvdata = csv.DictReader(csvfile, delimiter=delimiter)
                        for records in csvdata:
                            row = []
                            for fields in brazefields:
                                if fields in records:
                                    row.append(records[fields])
                                else:
                                    row.append(None)
                                    # print(records[fields], end=',')
                            csvwriter.writerow(row)
    print("Results saved in {}".format(outfile.name))

if __name__ == '__main__':
    mergeExports()