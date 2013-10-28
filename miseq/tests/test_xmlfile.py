from nose.tools import eq_, raises

import fixtures
from .. import XMLFile

class TestXMLFile( object ):
    xmlfiles = fixtures.xml_fixtures()

    def test_property( self ):
        cji = self.xmlfiles['CompletedJobInfo.xml']
        xml = XMLFile.XMLFile( cji )
        eq_( xml.Instrument, 'M02261' )

        rp = self.xmlfiles['runParameters.xml']
        xml = XMLFile.XMLFile( rp )
        eq_( xml.Username, 'sbsuser' )
