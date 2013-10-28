#!/usr/bin/env python2

import sys
from os.path import basename, dirname, join

try:
    from miseq.runParameters import RunParameters
except ImportError:
    print "Error importing necessary modules(miseq)"
    print "Did you activate the environment first by running . bin/activate??"
    sys.exit(-1)

if len(sys.argv) != 2:
    print "You need to specify the location of the runParameters.xml file"
    sys.exit(-1)

rp = RunParameters( sys.argv[1] )
output_folder = rp.SampleSheetFolder.replace('D:','/MiSeq').replace('\\','/')
sample_sheet = rp.SampleSheetName

sample_sheet_path = join( output_folder, sample_sheet )
print sample_sheet_path
