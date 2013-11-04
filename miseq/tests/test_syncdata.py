from .. import syncdata
from .. import rundir 
from nose.tools import eq_, raises

from test_rundir import create_mockrundir
import util

import tempfile
from os.path import join, dirname, basename, normpath
import os
import shutil

class TestSyncData(object):
    def setUp( self ):
        self.tempdir = tempfile.mkdtemp( prefix='miseqtmp' )
        os.chdir( self.tempdir )

    def tearDown( self ):
        os.chdir( '/' )
        shutil.rmtree( self.tempdir )

    def make_rsynctests( self, dir ):
        ''' Makes dir a mock Illumina Run directory '''
        import util
        util.make_mockrundir( dir )

    def get_structure( self, path ):
        structure = {}
        for root, dirs, files in os.walk( path ):
            rootbn = basename(root)
            structure[rootbn] = files
        return structure

    def test_syncrundir( self ):
        with util.mktempdir( self.tempdir ) as dstdir:
            with util.mktempdir( self.tempdir ) as srcdir:
                self.make_rsynctests( srcdir )
                src_struc = self.get_structure( srcdir )
                syncdata.sync_run( srcdir, dstdir )
                dst_struc = self.get_structure( dstdir )
                del dst_struc[basename(dstdir)]
                eq_( src_struc, dst_struc )

    def tst_syncfastq( self, bcdir ):
        with util.mktempdir( self.tempdir ) as dstdir:
            with util.mktempdir( self.tempdir ) as srcdir:
                self.make_rsynctests( srcdir )
                src_struc = self.get_structure( srcdir )
                syncdata.sync_fastq( srcdir, dstdir,  bcdir )
                dst_struc = self.get_structure( dstdir )
                del dst_struc[basename(dstdir)]
                eq_( src_struc[basename(normpath(bcdir))], dst_struc[basename(normpath(bcdir))] )
                for dir, files in dst_struc.items():
                    if dir != basename(normpath(bcdir)):
                        eq_( files, [] )

    def test_syncfastqnoslash( self ):
        self.tst_syncfastq( rundir.IlluminaRunDir.BASECALLERDIR[:-1] )

    def test_syncfastqslash( self ):
        self.tst_syncfastq( rundir.IlluminaRunDir.BASECALLERDIR )

    def test_synclatest( self ):
        with util.mktempdir( self.tempdir ) as dstdir:
            os.chdir( self.tempdir )
            dir1 = create_mockrundir( 'run1' )
            dir2 = create_mockrundir( 'run2' )
            syncdata.sync_latest( self.tempdir, dstdir )
            eq_( 'run2', os.listdir( dstdir )[0] )
