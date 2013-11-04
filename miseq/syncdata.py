#!/usr/bin/env python

from os.path import dirname, basename, join, normpath
import sys
import argparse
import subprocess
import shlex
import os

import util
import rundir

# Defaults
DEFAULT_DEST = "/home/EIDRUdata/NGSData/RawData/MiSeq"
DEFAULT_SRC = "/MiSeq/Illumina/MiSeqOutput"

def main():
    args = parse_args()
    src = args.src
    dst = args.dest
    try:
        sync_run( src, dst )
    except ValueError:
        sync_latest( src, dst )

def sync_latest( src, dst ):
    rd = rundir.IlluminaOutputDir( src )
    try:
        sync_run( rd.get_latest_run().abspath, dst )
    except AttributeError:
        print "There are no valid Illumina Runs in {}".format(src)

def sync_run( src, dst ):
    rund = rundir.IlluminaRunDir( src )

    sync_fastq( rund.abspath, dst, rund.BASECALLERDIR )
    sync_rundir( rund.abspath, dst )

def sync_rundir( src, dst ):
    '''
        Syncs the basename of src into dst
        aka rsync -av --progress src dst/
        that is, ensure src does not have trailing /
        so that it is synced into dst
    '''
    print "Syncing everything else"
    # Ensure path does not have trailing /
    src = normpath( src )
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

    return dst

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
        help='Path to illumina run to sync into dest or '\
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
