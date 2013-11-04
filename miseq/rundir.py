from os.path import join, basename, dirname, exists, splitext
import os.path
import os
import datetime
from glob import glob

import util

class IlluminaOutputDir( object ):
    def __init__( self, path ):
        self.path = path
        self._run_dirs = []

    @property
    def run_dirs( self ):
        '''
            Property to return list of All Output directories in
            the current OutputDirectory
            
            @returns list of IlluminaRunDir
        '''
        for d in glob(join(self.path,'*')):
            try:
                self._run_dirs.append( IlluminaRunDir(d) )
            except ValueError:
                continue

        return self._run_dirs

    def get_latest_run( self ):
        '''
            Return the latest MiSeq Run directory in dirpath
        '''
        try:
            return max( [d for d in self.run_dirs if d.completed()], key=lambda rundir: rundir.completeddate )
        except ValueError:
            return None

class IlluminaRunDir( object ):
    COMPLETEDFILE = 'CompletedJobInfo.xml'
    RUNPARAMSFILE = 'runParameters.xml'
    BASECALLERDIR = 'Data/Intensities/BaseCalls/'

    def __init__( self, path ):
        if not IlluminaRunDir.is_rundir( path ):
            raise ValueError( "{} is not a valid Run Directory".format(path) )

        self.path = path
        self.abspath = os.path.abspath( path )
        self.basename = basename( path )

    @staticmethod
    def is_rundir( path ):
        '''
            Returns True if dirpath is a MiSeq Run directory
        '''
        return exists( join(path,'runParameters.xml') )

    @property
    def bcdir( self ):
        ''' return abspath to BASECALLERDIR '''
        return join( self.abspath, self.BASECALLERDIR )

    @property
    def createdate( self ):
        ''' Datetime of when the RunDir was created '''
        # Lets use the mtime of the runParameters.xml file
        mtime = os.path.getmtime( join(self.path,self.RUNPARAMSFILE) )
        return datetime.datetime.fromtimestamp( mtime )

    @property
    def startdate( self ):
        ''' When the project started '''
        return self.createdate

    @property
    def completeddate( self ):
        ''' When the RunDir was finished running '''
        mtime = os.path.getmtime( join(self.abspath,self.COMPLETEDFILE) )
        return datetime.datetime.fromtimestamp( mtime )

    def completed( self ):
        '''
            Only returns True if the directory contains a CompletedJobInfo.xml file 
            which signifies that the directory is ready to be synced
        '''
        return exists( join(self.abspath,self.COMPLETEDFILE) ) and IlluminaRunDir.is_rundir(self.abspath)

    def get_reads( self ):
        '''
            Returns all the fastq.gz files for the run

            @returns list of abs paths to each fastq
        '''
        return glob( join(self.bcdir,'*.fastq.gz') )

    def extract_reads( self, dstdir ):
        '''
            Extracts all of the read files into dstdir
             essentially doubling+uncompressed space the amount of storage

            @returns a list of abspaths to the extracted reads
        '''
        extracted_reads = []
        for readgz in self.get_reads():
            bn,ext = splitext( basename(readgz) )
            read = join(dstdir,bn)
            util.ungzip( readgz, read )
            extracted_reads.append( read )
        return extracted_reads

class MiSeqRunDir( IlluminaRunDir ):
    pass
