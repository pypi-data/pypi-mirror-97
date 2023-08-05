#!/usr/bin/env python
"""Ingest Generic Database tables using multi-value insert statements and multiprocessing.

Usage:
  %s <configFile> <inputFile>... [--fileoffiles] [--table=<table>] [--tableDelimiter=<tableDelimiter>] [--bundlesize=<bundlesize>] [--nprocesses=<nprocesses>] [--nfileprocesses=<nfileprocesses>] [--loglocationInsert=<loglocationInsert>] [--logprefixInsert=<logprefixInsert>] [--loglocationIngest=<loglocationIngest>] [--logprefixIngest=<logprefixIngest>] [--types=<types>] [--skiphtm] [--nullValue=<nullValue>] [--fktable=<fktable>] [--fktablecols=<fktablecols>] [--fktablecoltypes=<fktablecoltypes>] [--fkfield=<fkfield>] [--fkfrominputdata=<fkfrominputdata>] [--racol=<racol>] [--deccol=<deccol>]
  %s (-h | --help)
  %s --version

Options:
  -h --help                                Show this screen.
  --version                                Show version.
  --fileoffiles                            Read the CONTENTS of the inputFiles to get the filenames. Allows many thousands of files to be read, avoiding command line constraints.
  --table=<table>                          Target table name.
  --tableDelimiter=<tableDelimiter>        Table delimiter (e.g. \\t \\s ,) where \\t = tab and \\s = space. Space delimited assumes one or more spaces between fields [default: \\s]
  --bundlesize=<bundlesize>                Group inserts into bundles of specified size [default: 1]
  --nprocesses=<nprocesses>                Number of processes to use per ingest file. Warning: nprocesses x nfileprocesses should not exceed nCPU. [default: 1]
  --nfileprocesses=<nfileprocesses>        Number of processes over which to split the files. Warning: nprocesses x nfileprocesses should not exceed nCPU. [default: 1]
  --loglocationInsert=<loglocationInsert>  Log file location [default: /tmp/]
  --logprefixInsert=<logprefixInsert>      Log prefix [default: inserter]
  --loglocationIngest=<loglocationIngest>  Log file location [default: /tmp/]
  --logprefixIngest=<logprefixIngest>      Log prefix [default: ingester]
  --types=<types>                          Python column types in the same order as the column headers.
  --skiphtm                                Don't bother calculating HTMs. They're either already done or we don't need them.
  --nullValue=<nullValue>                  Value of NULL definition (e.g. NaN, NULL, \\N, None) [default: \\N]
  --fktable=<fktable>                      Cassandra has a flat schema, so join to another table file via a foreign key (e.g. exposures).
  --fktablecols=<fktablecols>              The valid columns in the foreign key table we want to use - comma separated, no spaces (e.g. expname,object,mjd,filter,mag5sig,zp_mag,fwhm_px,exptime,detem).
  --fktablecoltypes=<fktablecoltypes>      The valid (python) column types in the foreign key table we want to use - comma separated, no spaces (e.g. str,str,float,str,float,float,float,float,float).
  --fkfield=<fkfield>                      Foreign key field [default: expname]
  --fkfrominputdata=<fkfrominputdata>      Foreign key from input data. If set to filename it will use the datafile filename as the key [default: filename]
  --racol=<racol>                          Column that represents the RA [default: ra]
  --deccol=<deccol>                        Column that represents the Declination [default: dec]

Example:
   %s config_cassandra.yaml 01a58464o0535o.dph --fktable=/Users/kws/atlas/dophot/all_co_exposures.tst --fkfield=expname --fktablecols=mjd,expname,exptime,filter,mag5sig --types=float,float,float,int,int,float,float,float,float,float,float,float,float,float,float,float,float,float --fktablecoltypes=float,str,float,str,float --table=atlasdophot --racol=RA --deccol=Dec

"""
import sys
__doc__ = __doc__ % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
from docopt import docopt
import os, shutil, re
from gkutils.commonutils import Struct, cleanOptions, readGenericDataFile, dbConnect, which, splitList, parallelProcess
from datetime import datetime
from datetime import timedelta
import subprocess
#import MySQLdb
from cassandra.cluster import Cluster
import gzip
from collections import OrderedDict

# 2021-02-11 KWS Import the new htmNameBulk function! No need anymore to rely on an external binary!
#                No need to write temporary files anymore.
from gkhtm._gkhtm import htmNameBulk


def nullValue(value, nullValue = '\\N'):
   returnValue = nullValue

   if value and value.strip():
      returnValue = value.strip()

   return returnValue

def nullValueNULL(value):
   returnValue = None

   if value and not isinstance(value, int) and value.strip() and value != 'NULL':
      returnValue = value.strip()

   return returnValue

def boolToInteger(value):
    returnValue = value
    if value == 'true':
        returnValue = 1
    if value == 'false':
        returnValue = 0
    return returnValue

def calculate_htm_name_bulk(generateHtmNameBulk, htmLevel, tempRaDecFile):
    # Call the C++ HTM ID calculator
    htmIDs = []

    p = subprocess.Popen([generateHtmNameBulk, str(htmLevel), tempRaDecFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()

    if output.strip():
        htmIDs = output.strip().split('\n')

    return htmIDs


# Use INSERT statements so we can use multiprocessing
def executeLoad(session, table, data, bundlesize = 100, types = None):

    rowsUpdated = 0

    if len(data) == 0:
        return rowsUpdated

    if types is None:
        return rowsUpdated

    keys = list(data[0].keys())


    if len(keys) != len(types):
        print("Keys & Types mismatch")
        return rowsUpdated

    typesDict = OrderedDict()

    i = 0
    for k in keys:
        typesDict[k] = types[i]
        i += 1

    #print(keys)
    #print(types)

    formatSpecifier = ','.join(['%s' for i in keys])

    chunks = int(1.0 * len(data) / bundlesize + 0.5)
    if chunks == 0:
        subList = [data]
    else:
        bins, subList = splitList(data, bins = chunks, preserveOrder = True)


    for dataChunk in subList:
        try:
            sql = "insert into %s " % table
            # Force all keys to be lowercase and devoid of hyphens
            sql += "(%s)" % ','.join(['%s' % k.lower().replace('-','') for k in keys])

            sql += " values "
            sql += ',\n'.join(['('+formatSpecifier+')' for x in range(len(dataChunk))])
            sql += ';'

            values = []
            for row in dataChunk:
                for key in keys:
                    value = nullValueNULL(boolToInteger(row[key]))
                    if value is not None:
                        value = eval(typesDict[key])(value)
                    values.append(value)

            #print(sql)
            session.execute(sql, tuple(values))


        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)
            #print "Error %d: %s" % (e.args[0], e.args[1])

    return


def workerInsert(num, db, objectListFragment, dateAndTime, firstPass, miscParameters):
    """thread worker function"""
    # Redefine the output to be a log file.
    options = miscParameters[0]

    pid = os.getpid()
    sys.stdout = open('%s%s_%s_%d_%d.log' % (options.loglocationInsert, options.logprefixInsert, dateAndTime, pid, num), "w")
    cluster = Cluster(db['hostname'])
    session = cluster.connect()
    session.set_keyspace(db['keyspace']) 

    combinedTypes = options.types
    if options.fktablecoltypes is not None and options.types is not None:
        combinedTypes = options.types + ',' + options.fktablecoltypes

    # Add 3 string columns if the HTMs are being requested. You will not be able to insert into a table
    # if its htm name components are not specified.
    if not options.skiphtm:
        combinedTypes = combinedTypes + ",str,str,str"

    types = combinedTypes.split(',')
    #print (types)

    # This is in the worker function
    objectsForUpdate = executeLoad(session, options.table, objectListFragment, int(options.bundlesize), types=types)

    print("Process complete.")
    cluster.shutdown()
    print("Connection Closed - exiting")

    return 0

def ingestData(options, inputFiles, fkDict = None):

    #if not options.skiphtm:
    #    generateHtmNameBulk = which('generate_htmname_bulk')
    #    if generateHtmNameBulk is None:
    #        sys.stderr.write("Can't find the generate_htmname_bulk executable, so cannot continue.\n")
    #        exit(1)

    import yaml
    with open(options.configFile) as yaml_file:
        config = yaml.safe_load(yaml_file)

    username = config['cassandra']['local']['username']
    password = config['cassandra']['local']['password']
    keyspace = config['cassandra']['local']['keyspace']
    hostname = config['cassandra']['local']['hostname']

    db = {'username': username,
          'password': password,
          'keyspace': keyspace,
          'hostname': hostname}

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    delimiter=options.tableDelimiter
    if delimiter == '\\s':
        delimiter = ' '
    if delimiter == '\\t':
        delimiter = '\t'

    for inputFile in inputFiles:
        print("Ingesting %s" % inputFile)
        if 'gz' in inputFile:
            # It's probably gzipped
            f = gzip.open(inputFile, 'rb')
            print(type(f).__name__)
        else:
            f = inputFile
    
        data = readGenericDataFile(f, delimiter=delimiter, useOrderedDict=True)

        foreignKey = options.fkfrominputdata
        if foreignKey == 'filename':
            foreignKey = os.path.basename(inputFile).split('.')[0]


        if fkDict:
            for i in range(len(data)):
                try:
                    if options.fktablecols:
                        # just pick out the specified keys
                        keys = options.fktablecols.split(',')
                        for k in keys:
                            data[i][k] = fkDict[foreignKey][k]
                    else:
                        # Use all the keys by default
                        for k,v in fkDict[foreignKey].items():
                            data[i][k] = v
                except KeyError as e:
                    pass

        print(data[0])
        pid = os.getpid()
    
        if not options.skiphtm:
            #tempRADecFile = '/tmp/' + os.path.basename(inputFile) + 'radec_' + str(pid)
            #tempLoadFile = '/tmp/' + os.path.basename(inputFile) + '_' + str(pid) + '.csv'
    
            coords = []
            #with open(tempRADecFile, 'wb') as f:
            #    for row in data:
            #        f.write('%s %s\n' % (row['ra'], row['dec']))
            for row in data:
                coords.append([float(row[options.racol]), float(row[options.deccol])])
    
            #htm16Names = calculate_htm_name_bulk(generateHtmNameBulk, 16, tempRADecFile)
            htm16Names = htmNameBulk(16, coords)
    
            #os.remove(tempRADecFile)

            # For Cassandra, we're going to split the HTM Name across several columns.
            # Furthermore, we only need to do this once for the deepest HTM level, because
            # This is always a subset of the higher levels.  Hence we only need to store
            # the tail end of the HTM name in the actual HTM 16 column.  So...  we store
            # the full HTM10 name as the first 12 characters of the HTM 16 one, then the
            # next 3 characters into the HTM 13 column, then the next 3 characters (i.e.
            # the last few characters) the HTM 16 column
            # e.g.:
            # ra, dec =      288.70392, 9.99498
            # HTM 10  = N02323033011
            # HTM 13  = N02323033011 211
            # HTM 16  = N02323033011 211 311

            # Incidentally, this hierarchy also works in binary and we should seriously
            # reconsider how we are currently using HTMs.

            # HTM10 ID =    13349829 = 11 00 10 11 10 11 00 11 11 00 01 01
            # HTM13 ID =   854389093 = 11 00 10 11 10 11 00 11 11 00 01 01  10 01 01
            # HTM16 ID = 54680902005 = 11 00 10 11 10 11 00 11 11 00 01 01  10 01 01  11 01 01


            for i in range(len(data)):
                # Add the HTM IDs to the data
                data[i]['htm10'] = htm16Names[i][0:12]
                data[i]['htm13'] = htm16Names[i][12:15]
                data[i]['htm16'] = htm16Names[i][15:18]
    
    
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
    fkDict = miscParameters[1]
    pid = os.getpid()
    sys.stdout = open('%s%s_%s_%d_%d.log' % (options.loglocationIngest, options.logprefixIngest, dateAndTime, pid, num), "w")

    # This is in the worker function
    objectsForUpdate = ingestData(options, objectListFragment, fkDict = fkDict)

    print("Process complete.")

    return 0

def ingestDataMultiprocess(options, fkDict = None):

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    # Read the contents of the input file(s) to get the filenames to process.
    files = options.inputFile

    if options.fileoffiles:
        files = []
        for f in options.inputFile:
            with open(f) as fp:
                content = fp.readlines()
                content = [filename.strip() for filename in content]
            files += content

    print(files)
    nProcessors, fileSublist = splitList(files, bins = int(options.nfileprocesses), preserveOrder=True)
    
    print("%s Parallel Processing..." % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))
    parallelProcess([], dateAndTime, nProcessors, fileSublist, workerIngest, miscParameters = [options, fkDict], drainQueues = False)
    print("%s Done Parallel Processing" % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


def main(argv = None):
    opts = docopt(__doc__, version='0.1')
    opts = cleanOptions(opts)

    # Use utils.Struct to convert the dict into an object for compatibility with old optparse code.
    options = Struct(**opts)

    fkDict = {}
    # If we have a foreign key table, read the data once only.  Pass this to the subprocesses.
    if options.fktable:
        fkeys = readGenericDataFile(options.fktable, delimiter='\t')
        for row in fkeys:
            fkDict[row[options.fkfield]] = row

    ingestDataMultiprocess(options, fkDict = fkDict)

    #files = options.inputFile
    #if options.fileoffiles:
    #    files = []
    #    for f in inputFile:
    #        with open(f) as fp:
    #            content = fp.readlines()
    #        files += content
    #ingestData(options, files, fkDict = fkDict)


if __name__=='__main__':
    main()


