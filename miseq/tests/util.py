from contextlib import contextmanager
import tempfile
from os.path import join, dirname, basename, normpath
import os.path
import os
import shutil
import gzip

from .. import rundir

class BaseClass( object ):
    def setUp( self ):
        self.tempdir = tempfile.mkdtemp()
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

def mktempfile( path ):
    print "Created: {}".format(path)
    with gzip.open( path, 'w' ) as fh:
        fh.write( path )
    return path

def mkgztempfile( path ):
    print "Created: {}".format(path)
    with gzip.open( path, 'w' ) as fh:
        fh.write( path )
    return path

@contextmanager
def mktempdir( dir=None ):
    path = tempfile.mkdtemp( prefix='miseqtmp', dir=dir )
    try:
        yield path
    finally:
        import shutil
        shutil.rmtree( path )

def make_mockrundir( dir, completed=True ):
        dirs = [str(i) for i in range( 1,3 )]
        files = ['file'+str(i) for i in range( 1,3 )]
        fastqs = [str(i)+'.fastq.gz' for i in range(1,3)]

        if not os.path.isdir( dir ):
            os.mkdir( dir )

        rpf = join(dir,rundir.IlluminaRunDir.RUNPARAMSFILE)
        mktempfile( rpf )
        if completed:
            mktempfile( join(dir,rundir.IlluminaRunDir.COMPLETEDFILE) )

        for f in files:
            mktempfile( join(dir,f) )
        for d in dirs:
            os.mkdir( join(dir,d) )
            for f in files:
                mktempfile( join(dir, d, d+f) )

        bcdir = join(dir,rundir.IlluminaRunDir.BASECALLERDIR)
        os.makedirs( bcdir )
        for fq in fastqs:
            mkgztempfile( join(bcdir,fq) )
