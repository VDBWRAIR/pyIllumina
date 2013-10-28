import re

class XMLFile(object):
    def __init__( self, path ):
        self.path = path
        self._contents = ''

    @property
    def contents( self ):
        if self._contents == '':
            with open(self.path) as fh:
                self._contents = fh.read()
        return self._contents

    def _dyn_property( self, property ):
        '''
            Fetch property value or values by name
        '''
        pat = '<{}>(.*?)</{}>'.format(property,property)
        m = re.search( pat, self.contents )
        if not m:
            raise AttributeError("{} is not a valid property of RunParameters".format(property))

        return m.group(1)

    def __getattr__( self, name ):
        return self._dyn_property( name )
