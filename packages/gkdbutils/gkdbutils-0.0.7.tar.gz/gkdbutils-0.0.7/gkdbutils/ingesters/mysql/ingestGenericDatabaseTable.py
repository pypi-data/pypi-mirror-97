#!/usr/bin/env python
"""Ingest Generic Database tables using multi-value insert statements and multiprocessing.

Usage:
  %s <configFile> <inputFile>... [--table=<table>] [--bundlesize=<bundlesize>] [--nprocesses=<nprocesses>] [--loglocationInsert=<loglocationInsert>] [--logprefixInsert=<logprefixInsert>] [--loglocationIngest=<loglocationIngest>] [--logprefixIngest=<logprefixIngest>]
  %s (-h | --help)
  %s --version

Options:
  -h --help                                Show this screen.
  --version                                Show version.
  --table=<table>                          Target table name.
  --bundlesize=<bundlesize>                Group inserts into bundles of specified size [default: 100]
  --nprocesses=<nprocesses>                Number of processes to use - warning - beware of opening too many processes [default: 8]
  --loglocationInsert=<loglocationInsert>  Log file location [default: /tmp/]
  --logprefixInsert=<logprefixInsert>      Log prefix [default: inserter]
  --loglocationIngest=<loglocationIngest>  Log file location [default: /tmp/]
  --logprefixIngest=<logprefixIngest>      Log prefix [default: ingester]

Example:
   %s /tmp/bile.csv.gz

"""
import sys
__doc__ = __doc__ % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
from docopt import docopt
import os, shutil, re
from gkutils.commonutils import Struct, cleanOptions, readGenericDataFile, dbConnect, which, splitList, parallelProcess
from datetime import datetime
from datetime import timedelta
import subprocess
import MySQLdb
import gzip


def nullValue(value):
   returnValue = '\\N'

   if value and value.strip():
      returnValue = value.strip()

   return returnValue

def nullValueNULL(value):
   returnValue = None

   if value and value.strip():
      returnValue = value.strip()

   return returnValue

def boolToInteger(value):
    returnValue = value
    if value == 'true':
        returnValue = '1'
    if value == 'false':
        returnValue = '0'
    return returnValue

def calculate_htm_ids_bulk(generateHtmidBulk, htmLevel, tempRaDecFile):
    # Call the C++ HTM ID calculator
    htmIDs = []

    p = subprocess.Popen([generateHtmidBulk, str(htmLevel), tempRaDecFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()

    if output.strip():
        htmIDs = output.strip().split('\n')

    return htmIDs


# Use INSERT statements so we can use multiprocessing
def executeLoad(conn, table, data, bundlesize = 100):

    rowsUpdated = 0

    if len(data) == 0:
        return rowsUpdated

    keys = list(data[0].keys())
    formatSpecifier = ','.join(['%s' for i in keys])

    chunks = int(1.0 * len(data) / bundlesize + 0.5)
    if chunks == 0:
        subList = [data]
    else:
        bins, subList = splitList(data, bins = chunks, preserveOrder = True)


    for dataChunk in subList:
        try:
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            sql = "insert ignore into %s " % table
            sql += "(%s)" % ','.join(['`%s`' % k for k in keys])
            sql += " values "
            sql += ',\n'.join(['('+formatSpecifier+')' for x in range(len(dataChunk))])
            sql += ';'

            values = []
            for row in dataChunk:
                for key in keys:
                    values.append(nullValueNULL(boolToInteger(row[key])))

            cursor.execute(sql, tuple(values))

            rowsUpdated = cursor.rowcount
            cursor.close ()

        except MySQLdb.Error as e:
            print(cursor._last_executed)
            print("Error %d: %s" % (e.args[0], e.args[1]))

        conn.commit()

    return rowsUpdated


def workerInsert(num, db, objectListFragment, dateAndTime, firstPass, miscParameters):
    """thread worker function"""
    # Redefine the output to be a log file.
    options = miscParameters[0]
    sys.stdout = open('%s%s_%s_%d.log' % (options.loglocationInsert, options.logprefixInsert, dateAndTime, num), "w")
    conn = dbConnect(db['hostname'], db['username'], db['password'], db['database'], quitOnError = True)

    # This is in the worker function
    objectsForUpdate = executeLoad(conn, options.table, objectListFragment, int(options.bundlesize))

    print("Process complete.")
    conn.close()
    print("DB Connection Closed - exiting")

    return 0

def ingestData(options, inputFiles):
    generateHtmidBulk = which('generate_htmid_bulk')
    if generateHtmidBulk is None:
        sys.stderr.write("Can't find the generate_htmid_bulk executable, so cannot continue.\n")
        exit(1)

    import yaml
    with open(options.configFile) as yaml_file:
        config = yaml.load(yaml_file)

    username = config['databases']['local']['username']
    password = config['databases']['local']['password']
    database = config['databases']['local']['database']
    hostname = config['databases']['local']['hostname']

    db = {'username': username,
          'password': password,
          'database': database,
          'hostname': hostname}

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    for inputFile in inputFiles:
        print("Ingesting %s" % inputFile)
        if 'gz' in inputFile:
            # It's probably gzipped
            f = gzip.open(inputFile, 'rb')
            print(type(f).__name__)
        else:
            f = inputFile
    
        data = readGenericDataFile(f, delimiter=',', useOrderedDict=True)
        pid = os.getpid()
    
        tempRADecFile = '/tmp/' + os.path.basename(inputFile) + 'radec_' + str(pid)
        tempLoadFile = '/tmp/' + os.path.basename(inputFile) + '_' + str(pid) + '.csv'
    
        with open(tempRADecFile, 'wb') as f:
            for row in data:
                f.write('%s %s\n' % (row['ra'], row['dec']))
    
        htm10IDs = calculate_htm_ids_bulk(generateHtmidBulk, 10, tempRADecFile)
        htm13IDs = calculate_htm_ids_bulk(generateHtmidBulk, 13, tempRADecFile)
        htm16IDs = calculate_htm_ids_bulk(generateHtmidBulk, 16, tempRADecFile)
    
        os.remove(tempRADecFile)
    
        for i in range(len(data)):
            # Add the HTM IDs to the data
            data[i]['htm10ID'] = htm10IDs[i]
            data[i]['htm13ID'] = htm13IDs[i]
            data[i]['htm16ID'] = htm16IDs[i]
    
    
    
        nprocesses = int(options.nprocesses)
    
        if len(data) > 0:
            nProcessors, listChunks = splitList(data, bins = nprocesses, preserveOrder=True)
    
            print("%s Parallel Processing..." % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))
            parallelProcess(db, dateAndTime, nProcessors, listChunks, workerInsert, miscParameters = [options], drainQueues = False)
            print("%s Done Parallel Processing" % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


    
def workerIngest(num, db, objectListFragment, dateAndTime, firstPass, miscParameters):
    """thread worker function"""
    # Redefine the output to be a log file.
    options = miscParameters[0]
    sys.stdout = open('%s%s_%s_%d.log' % (options.loglocationIngest, options.logprefixIngest, dateAndTime, num), "w")

    # This is in the worker function
    objectsForUpdate = ingestData(options, objectListFragment)

    print("Process complete.")

    return 0

def ingestDataMultiprocess(options):

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    nProcessors, fileSublist = splitList(options.inputFile, bins = int(options.nprocesses), preserveOrder=True)
    
    print("%s Parallel Processing..." % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))
    parallelProcess([], dateAndTime, nProcessors, fileSublist, workerIngest, miscParameters = [options], drainQueues = False)
    print("%s Done Parallel Processing" % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


def main(argv = None):
    opts = docopt(__doc__, version='0.1')
    opts = cleanOptions(opts)

    # Use utils.Struct to convert the dict into an object for compatibility with old optparse code.
    options = Struct(**opts)
    ingestDataMultiprocess(options)
    #ingestData(options)


if __name__=='__main__':
    main()


