#!/usr/bin/env python

from os.path import dirname, basename, join
import sys
import argparse
import subprocess
import shlex
import os

from miseq import util

# Defaults
DEFAULT_DEST = "/home/EIDRUdata/NGSData/RawData/MiSeq"
DEFAULT_SRC = "/MiSeq/Illumina/MiSeqOutput"

# Common Dirs
BASECALLS_DIR = "Data/Intensities/BaseCalls/"

def main():
    args = parse_args()
    src = args.src
    dst = args.dest

    # If a non run directory was given assume that
    # the user specified the OutputDirectory and get the
    # latest run to transfer
    if not util.isRunDir( src ):
        src = join(src,util.getLatestRun( src ))
        assert src

    sync_fastq( src, dst, BASECALLS_DIR )
    sync_rundir( src, dst )

def sync_rundir( src, dst ):
    print "Syncing everything else"
    rsync( src, dst )

def sync_fastq( src, dst, path ):
    '''
        Just sync the fastqs that are under join(dst,path)
    '''
    srcbn = basename(src)
    src = join(src,path)
    dst = join(dst,srcbn,path)
    try:
        os.makedirs( dst )
    except OSError as e:
        if e.errno != 17:
            raise e

    print "Syncing Fastqs"
    rsync( src, dst, exclude=['Matrix','L001','Phasing','Alignment'] )

def rsync( src, dst, exclude=[], include=[] ):
    ''' Just call rsync with src and dst '''
    exclude = " --exclude ".join( exclude )
    if exclude: exclude = '--exclude ' + exclude
    include = " --include ".join( include )
    if include: include = '--include ' + include
    cmd = 'rsync -av --progress {}{} {} {}'.format(exclude,include,src,dst)
    print "Running {}".format(cmd)
    cmd = shlex.split( cmd )
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    
    for line in iter(p.stdout.readline,b''):
        print line.rstrip()

def parse_args():
    parser = argparse.ArgumentParser(
        description='Automatically sync data from MiSeq. Syncs the fastq files '\
            'first and then the rest for quicker access'
    )

    parser.add_argument(
        '-s',
        '--src',
        dest='src',
        default=DEFAULT_SRC,
        help='Path to run to sync into dest or '\
            'directory that contains MiSeq runs and latest will be used'\
            '[Default:{}]'.format(DEFAULT_SRC)
    )

    parser.add_argument(
        '-d',
        '--dest',
        dest='dest',
        default=DEFAULT_DEST,
        help='Base directory to copy runs into[Default:{}]'.format(DEFAULT_DEST)
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
