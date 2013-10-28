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
    rp = 'runParameters.xml'
    cji = 'CompletedJobInfo.xml'

    def setUp( self ):
        self.tempdir = tempfile.mkdtemp()
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

    def test_isrundir( self ):
        create( self.rp )
        assert util.isRunDir( self.tempdir )
        remove( self.rp )
        create( self.cji )
        assert not util.isRunDir( self.tempdir )
        remove( self.cji )

    def test_iscompleted( self ):
        create( self.rp )
        assert not util.isCompleted( self.tempdir )
        create( self.cji )
        assert util.isCompleted( self.tempdir )
        remove( self.rp )
        assert not util.isCompleted( self.tempdir )
        remove( self.cji )

    def test_getlatestrun( self ):
        os.mkdir( 'one' )
        create( join('one',self.rp) )
        create( join('one',self.cji) )
        os.mkdir( 'two' )
        create( join('two',self.rp) )
        os.mkdir( 'three' )
        os.mkdir( 'four' )
        create( join('four',self.rp) )
        create( join('four',self.cji) )

        eq_( 'four', util.getLatestRun( self.tempdir ) )
