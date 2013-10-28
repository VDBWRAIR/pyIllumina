from os.path import join, basename, dirname
import os

def isRunDir( dirpath ):
    '''
        Returns True if dirpath is a MiSeq Run directory
    '''
    return os.path.exists( join(dirpath,'runParameters.xml') )

def isCompleted( dirpath ):
    '''
        Only returns if the directory contains a CompletedJobInfo.xml file 
        which signifies that the directory is ready to be synced
    '''
    return os.path.exists( join(dirpath,'CompletedJobInfo.xml') ) and isRunDir(dirpath)

def getLatestRun( dirpath ):
    '''
        Return the latest MiSeq Run directory in dirpath
    '''
    completed_runs = [cr for cr in os.listdir( dirpath ) if isCompleted(join(dirpath,cr))]
    return max( completed_runs, key=lambda x: os.stat(join(dirpath,x)).st_ctime )
