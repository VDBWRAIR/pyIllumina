from .. import files

from nose.tools import eq_, raises

import tempfile

class TestIlluminaFormattedFile( object ):
    def test_init( self ):
        fd, tfile = tempfile.mkstemp()
        files.IlluminaFormattedFile( tfile )
