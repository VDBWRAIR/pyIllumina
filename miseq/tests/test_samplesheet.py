import tempfile
import os

from nose.tools import eq_, raises

from .. import SampleSheet
import fixtures


class TestSampleSheet(object):
    SAMPLESHEETS = fixtures.sample_sheet_fixtures()
    SAMPLESHEET = '''[KeyVal]
Key1,Val1
Key2,Val2

[ValOnly]
Val1
Val2

[Data]
h1,Sample_Name,h2,h3,h4
1,S1,2,3,4
5,S2,6,7,8
9,S3,10,11,12'''

    @classmethod
    def setUpClass( self ):
        fd, self.samplesheet = tempfile.mkstemp()
        with open(self.samplesheet,'w') as fh:
            fh.write(self.SAMPLESHEET)
        return self.samplesheet

    @classmethod
    def tearDownClass( self ):
        os.unlink( self.samplesheet )

    def test_iter( self ):
        ss = SampleSheet.SampleSheet( self.samplesheet )
        eq_( ['S1','S2','S3'], sorted([sn for sn in ss]) )

    def test_getitem( self ):
        ss = SampleSheet.SampleSheet( self.samplesheet )
        assert isinstance( ss['KeyVal'], SampleSheet.Section )
        assert isinstance( ss['ValOnly'], SampleSheet.Section )
        assert isinstance( ss['Data'], SampleSheet.Section )

    def test_tostr( self ):
        ss = SampleSheet.SampleSheet( self.samplesheet )
        eq_( self.SAMPLESHEET, str(ss) )

class TestSection( object ):
    def setUp( self ):
        self.inst = SampleSheet.Section( 'Test' )
        self.kvdata = [
            'Attribute1,Value1',
            'Attribute2,Value2'
        ]
        self.valueonlydata = [
            '151',
            '151'
        ]
        self.csvdata = [
            'h1,h2,h3,h4',
            '1,2,3,4',
            '5,6,7,8',
            '9,10,11,12'
        ]

    def test_parsekeyval( self ):
        self.inst.parse( self.kvdata )
        for d in self.kvdata:
            name, val = d.split(',')
            eq_( self.inst.Test.get( name ), val )

    def test_parsevalonly( self ):
        self.inst.parse( self.valueonlydata )
        eq_( self.inst.Test, self.valueonlydata )

    def test_parsecsv( self ):
        hdr = self.csvdata[0].split(',')
        self.inst.parse( self.csvdata )
        for de,dr in zip(self.csvdata[1:],self.inst.Test):
            di = dict( zip(hdr,de.split(',')) )
            eq_( di, dr )

    def test_peek( self ):
        expectedtypes = [
            (['value'],'valonly'),
            (['value,value'],'keyval'),
            (['value,value,value'],'csv')
        ]
        for v,t in expectedtypes:
            print v
            eq_( t, self.inst.peek( v ) )

    def test_tostr( self ):
        tests = [
            (self.kvdata, "\n".join( self.kvdata )),
            (self.valueonlydata, "\n".join( self.valueonlydata )),
            (self.csvdata, "\n".join( self.csvdata ))
        ]

        for data, dstr in tests:
            inst = SampleSheet.Section('Test')
            inst.parse( data )
            print inst.Test
            dstr = '[Test]\n' + dstr
            eq_( dstr, str(inst) )

class TestDataSection(object):
    data = '''[Data]
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Sample_Project,Description,GenomeFolder
Sample1,SampleName1,,,,,C:\Illumina\MiSeq Reporter\Genomes\PhiX\Illumina\RTA\Sequence\Chromosomes'''

    def test_parse( self ):
        ss = SampleSheet.DataSection('Data')
        ss.parse( self.data.splitlines()[1:] )
        assert isinstance( ss.samples['SampleName1'], dict )
