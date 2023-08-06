"""Query cassandra by RA and dec. The coords variable should be RA and dec, comma separated with NO SPACE. (To facilitate negative declinations.)

Usage:
  %s <coords> <radius> [--coordsfromfile]
  %s (-h | --help)
  %s --version

Options:
  -h --help                    Show this screen.
  --version                    Show version.
  --low=<n>                    Value of ndet below which we regard data as good [default: 250].
  --high=<n>                   Value of ndet above which we regard data as bad [default: 2000].
  --coordsfromfile             Treat the coordinates parameter as a file of coordinates.

"""
import sys
__doc__ = __doc__ % (sys.argv[0], sys.argv[0], sys.argv[0])
from docopt import docopt
from gkutils.commonutils import Struct, readGenericDataFile, cleanOptions

from gkutils.commonutils import coneSearchHTMCassandra
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

import csv

def main(argv = None):
    opts = docopt(__doc__, version='0.1')
    opts = cleanOptions(opts)

    # Use utils.Struct to convert the dict into an object for compatibility with old optparse code.
    options = Struct(**opts)

    keyspace = 'atlas'
    host = ['db0', 'db1', 'db2', 'db3', 'db4']
    table = 'atlas_detections'
    
    radius = 2.0
    radius = float(options.radius)
    
    # random star
    #ra = 83.20546
    #dec = -20.70055
    
    # ATLAS17nij
    #ra = 82.46704
    #dec = -19.52058
    
    # ATLAS20biio
    #ra = 83.24691
    #dec = -19.11739
    
    # ATLAS20bbio - very good!!
    #ra = 81.27903
    #dec = -21.24643
    
    # ATLAS18vre
    #ra = 84.19551
    #dec = -22.41100
    
    # ATLAS19bdbm
    #ra = 85.10436
    #dec = -18.09766
    
    # ATLAS20bbff
    #ra = 86.52075
    #dec = -23.56601
    
    # ATLAS20ymv - THIS IS the CENTRE OBJECT. We did a 10 degree sweep around this.
    #ra = 74.55677
    #dec = -20.35753
    
    # ATLAS17lvn - bright foreground star
    #ra = 68.75953
    #dec = -14.22797
    
    cluster = Cluster(host)
    session = cluster.connect()
    session.row_factory = dict_factory
    session.set_keyspace(keyspace)
    coordslist = []

    if options.coordsfromfile:
        coordslist = readGenericDataFile(options.coords, delimiter=',')
    else:
        coordslist.append({'ra': options.coords.split(',')[0], 'dec': options.coords.split(',')[1]})

    for c in coordslist:
        data = coneSearchHTMCassandra(session, c['ra'], c['dec'], radius, table, refineResults = True)
        if data:
            for row in data:
                #print (row)
                print (row['mjd'], "%.2f" % row['m'], "%.2f" % row['dminst'], row['filter'], "%.6f" % row['ra'], "%.6f" % row['dec'], row['expname'])
    
    cluster.shutdown()

if __name__ == '__main__':
    main()

