
class Format( object ):
    pass

class IlluminaFormattedFile( file ):
    def __init__( self, *args, **kwargs ):
        super(IlluminaFormattedFile, self ).__init__( *args, **kwargs )

    def parse_filename( self, regex ):
        '''
            Parses the internal filename into pieces defined in the regex

            @param regex - Regular expression with named expressions

            @returns dictionary from re.match(<name>).groupdict()
        '''

class IlluminaFastqFile( IlluminaFormattedFile ):
    FORMAT = '{samplename}_{barcodesequence}_{lane}_{read}_{set}.fastq.gz'
    PARSE_RE = '(?P<samplename>\S+?)_(?P<barcodesequence>S\d+)_(?P<lane>L\d{3})_(?P<read>R[12])_(?P<set>S\d{3}).fastq.gz'

    def __init__( self, *args, **kwargs ):
        super( IlluminaFastqFile, self ).__init__( *args, **kwargs )
