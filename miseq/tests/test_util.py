from .. import util
from nose.tools import eq_, raises

import tempfile
import shutil
import os
from os.path import join, dirname, basename

def create( filepath ):
    open(filepath,'w').close()

def remove( filepath ):
    os.unlink( filepath )

class TestUtil( object ):
    def setUp( self ):
        self.tempdir = tempfile.mkdtemp()
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

