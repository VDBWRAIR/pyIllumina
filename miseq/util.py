from os.path import join, basename, dirname
import os
import gzip

def ungzip( src, dst ):
    '''
        Simply uncompress src file to dst file

        @param src - Source file path or obj
        @param dst - Destination file path or obj
    '''
    chunksize = 500000
    with gzip.open(src,'rb') as gz:
        with open( dst, 'wb' ) as fh:
            chunk = gz.read(chunksize)
            while chunk != '':
                fh.write(chunk)
                chunk = gz.read(chunksize)
