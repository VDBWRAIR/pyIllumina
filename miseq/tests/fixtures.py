from os.path import join, basename, dirname
from glob import glob

THIS_DIR = join( dirname( __file__ ), 'fixtures' )

def sample_sheet_fixtures( ):
    return glob( join( THIS_DIR, 'SampleSheet*.csv' ) )

def xml_fixtures( ):
    return {basename(p):p for p in glob( join( THIS_DIR, 'xmlfiles', '*' ) )}
