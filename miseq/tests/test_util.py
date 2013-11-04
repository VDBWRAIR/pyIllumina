from .. import util
from nose.tools import eq_, raises

import util as testutil

import tempfile
import shutil
import os
from os.path import join, dirname, basename
import gzip

class TestUtil( testutil.BaseClass ):
    def test_ungzip( self ):
        contents = '123457abcdefg'*1000
        fn = 'test'
        with gzip.open(fn+'.gz','wb') as gz:
            gz.write(contents)

        util.ungzip( fn+'.gz', fn )

        eq_( contents, open(fn).read() )
