from gkutils.commonutils import readGenericDataFile

filename = '/Users/kws/Documents/code/gitdev/gkdbutils/gkdbutils/ingesters/cassandra/01a58464o0535o.dph'
data = readGenericDataFile(filename, delimiter = ' ', useOrderedDict = False)
for row in data:
    print(row['RA'], row['Dec'], row['m'], row['dminst'])
