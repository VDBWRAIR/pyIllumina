from .. import syncdata
from nose.tools import eq_, raises

import tempfile
from os.path import join, dirname, basename, normpath
import os
import shutil
from contextlib import contextmanager

class TestSyncData(object):
    def mktempfile( self, path ):
        print path
        open( path, 'w' ).close()
        return path

    @contextmanager
    def mktempdir( self, dir=None ):
        path = tempfile.mkdtemp( prefix='miseqtmp', dir=dir )
        try:
            yield path
        finally:
            import shutil
            shutil.rmtree( path )

    def setUp( self ):
        self.tempdir = tempfile.mkdtemp( prefix='miseqtmp' )
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

    def make_rsynctests( self, dir ):
        dirs = [str(i) for i in range( 1,3 )]
        files = ['file'+str(i) for i in range( 1,3 )]
        fastqs = [str(i)+'.fastq' for i in range(1,3)]

        for f in files:
            self.mktempfile( join(dir,f) )
        for d in dirs:
            os.mkdir( join(dir,d) )
            for f in files:
                self.mktempfile( join(dir, d, d+f) )
        os.mkdir(join(dir,'basecalls'))
        for fq in fastqs:
            self.mktempfile( join(dir,'basecalls',fq) )

    def get_structure( self, path ):
        structure = {}
        for root, dirs, files in os.walk( path ):
            rootbn = basename(root)
            structure[rootbn] = files
        return structure

    def test_syncrundir( self ):
        with self.mktempdir( self.tempdir ) as dstdir:
            with self.mktempdir( self.tempdir ) as srcdir:
                self.make_rsynctests( srcdir )
                src_struc = self.get_structure( srcdir )
                syncdata.rsync( srcdir, dstdir )
                dst_struc = self.get_structure( dstdir )
                del dst_struc[basename(dstdir)]
                eq_( src_struc, dst_struc )

    def tst_syncfastq( self, bcdir ):
        with self.mktempdir( self.tempdir ) as dstdir:
            with self.mktempdir( self.tempdir ) as srcdir:
                self.make_rsynctests( srcdir )
                src_struc = self.get_structure( srcdir )
                syncdata.sync_fastq( srcdir, dstdir,  bcdir )
                dst_struc = self.get_structure( dstdir )
                del dst_struc[basename(dstdir)]
                eq_( src_struc[normpath(bcdir)], dst_struc[normpath(bcdir)] )
                for dir, files in dst_struc.items():
                    if dir != 'basecalls':
                        eq_( files, [] )

    def test_syncfastqnoslash( self ):
        self.tst_syncfastq( 'basecalls' )

    def test_syncfastqslash( self ):
        self.tst_syncfastq( 'basecalls/' )
