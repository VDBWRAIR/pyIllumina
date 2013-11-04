from .. import rundir

from nose.tools import eq_, raises

import tempfile
import shutil
import os
from glob import glob
from os.path import join, dirname, basename, abspath
import datetime

def create( filepath ):
    open(filepath,'w').close()

def remove( filepath ):
    os.unlink( filepath )

def create_mockrundir( mockdirpath, completed=True ):
    '''
        Create a directory with a runParameters.xml and CompletedJobInfo.xml
          in it unless completed is False then only runParameters.xml will be
          created
    '''
    import util
    util.make_mockrundir( mockdirpath, completed )

class BaseClass( object ):
    def setUp( self ):
        self.tempdir = tempfile.mkdtemp()
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

class TestIlluminaOutputDir( BaseClass ):
    def test_rundirsrelpath( self ):
        testdirs = ['1','2','3']
        for d in testdirs:
            create_mockrundir( d )
        os.mkdir( '4' )
        os.chdir( '/' )
        dirs = rundir.IlluminaOutputDir( self.tempdir ).run_dirs
        eq_( testdirs, sorted([ird.basename for ird in dirs]) )

    def test_rundirs( self ):
        testdirs = ['1','2','3']
        for d in testdirs:
            create_mockrundir( d )
        os.mkdir( '4' )
        dirs = rundir.IlluminaOutputDir( self.tempdir ).run_dirs
        eq_( testdirs, sorted([ird.basename for ird in dirs]) )

    def test_getlatestrunnocompleted( self ):
        create_mockrundir( 'one', False )
        outdir = rundir.IlluminaOutputDir( self.tempdir )
        eq_( None, outdir.get_latest_run( ) )
        
    def test_getlatestrun( self ):
        create_mockrundir( 'one' )
        create_mockrundir( 'two', False )
        os.mkdir( 'three' )
        create_mockrundir( 'four' )

        outdir = rundir.IlluminaOutputDir( self.tempdir )
        eq_( 'four', outdir.get_latest_run( ).basename )

    def test_createdate( self ):
        create_mockrundir( 'testdir' )
        now = datetime.datetime.now()
        cdate = rundir.IlluminaRunDir( 'testdir' ).createdate 
        tdiff = (now - cdate).seconds 
        print now
        print cdate
        assert tdiff <= 1

    def test_startdate( self ):
        create_mockrundir( 'testdir' )
        now = datetime.datetime.now()
        sdate = rundir.IlluminaRunDir( 'testdir' ).startdate 
        tdiff = (now - sdate).seconds 
        print now
        print sdate
        assert tdiff <= 1

    @raises(OSError)
    def test_missingcompleted( self ):
        create_mockrundir( 'testdir', False )
        rundir.IlluminaRunDir( 'testdir' ).completeddate
    
    def test_completeddate( self ):
        create_mockrundir( 'testdir' )
        now = datetime.datetime.now()
        cdate = rundir.IlluminaRunDir( 'testdir' ).completeddate 
        tdiff = (now - cdate).seconds
        print now
        print cdate
        assert tdiff <= 1
    
class TestIlluminaRunDir( BaseClass ):
    rp = rundir.IlluminaRunDir.RUNPARAMSFILE
    cji = rundir.IlluminaRunDir.COMPLETEDFILE

    def test_isrundir( self ):
        create( self.rp )
        assert rundir.IlluminaRunDir.is_rundir( self.tempdir )
        remove( self.rp )
        create( self.cji )
        assert not rundir.IlluminaRunDir.is_rundir( self.tempdir )
        remove( self.cji )

    def test_iscompleted( self ):
        create( self.rp )
        rdir = rundir.IlluminaRunDir( self.tempdir )
        assert not rdir.completed()
        create( self.cji )
        assert rdir.completed()
        remove( self.rp )
        assert not rdir.completed()
        remove( self.cji )

    def test_bcdir( self ):
        create_mockrundir( 'testy' )
        ird = rundir.IlluminaRunDir( 'testy' )
        abpath = join(abspath( 'testy' ), ird.BASECALLERDIR)
        eq_( abpath, ird.bcdir )

    def test_getreads( self ):
        create_mockrundir( 'testdir' )
        ird = rundir.IlluminaRunDir('testdir')
        mockreads = glob(join(ird.bcdir,'*.fastq.gz'))
        create(join(ird.bcdir,'notaread'))

        eq_( mockreads, ird.get_reads() )
