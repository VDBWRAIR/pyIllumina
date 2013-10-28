import re
import csv
import collections

class SampleSheet(object):
    def __init__( self, path ):
        self.path = path
        self._sections = collections.OrderedDict()

    @property
    def sections( self ):
        self._parse()
        return self._sections.keys()

    def __getitem__( self, val ):
        self._parse()

        if val not in self._sections:
            raise IndexError( "No section named {}".format(val) )
        return self._sections[val]

    def _parse( self ):
        if self._sections:
            return
        current_section = ''
        current_data = []
        with open(self.path, 'Ub') as fh:
            for line in fh:
                if line.startswith('['):
                    if current_data:
                        self._sections[current_section].parse( current_data )
                        current_data = []
                    current_section = line.strip().replace(']','').replace('[','')
                    self._sections[current_section] = Section(current_section)
                else:
                    current_data.append( line )
            self._sections[current_section].parse( current_data )

    def __str__( self ):
        rStr = ''
        for s in self.sections:
            rStr += str(self[s]) + '\n\n'
        return rStr[:-2]

class Section(object):
    def __init__( self, section_name ):
        '''
            @param section_name - Name of the section between the [ and ]
        '''
        self.name = section_name

    def parse_keyval( self, data ):
        '''
            Parses a data list of keyval entries

            @param data - List of key,val strings
        '''
        setattr( self, self.name, collections.OrderedDict() )
        for line in data:
            line = line.rstrip()
            if line:
                name, val = line.split(',')
                getattr( self, self.name )[name] = val

    def parse_valonly( self, data ):
        setattr( self, self.name, [] )
        for line in data:
            line = line.rstrip()
            if line:
                getattr( self, self.name ).append( line )

    def parse_csv( self, data ):
        self.headers = data[0].rstrip().split(',')
        setattr( self, self.name, [] )
        for line in csv.DictReader( data[1:], fieldnames=self.headers ):
            getattr( self, self.name ).append(line)

    def peek( self, data ):
        numcommas = data[0].count( ',' )
        if numcommas == 1:
            return 'keyval'
        elif numcommas == 0:
            return 'valonly'
        else:
            return 'csv'

    def parse( self, data ):
        '''
            Parses the data portion of a section

            @param data - List of lines between two sections ommitting the empty lines
        '''
        type = self.peek( data )
        self.type = type
        
        if type == 'keyval':
            self.parse_keyval( data )
        elif type == 'valonly':
            self.parse_valonly( data )
        elif type == 'csv':
            self.parse_csv( data )
        else:
            raise ValueError( "{} is not any of required types {}".format(type,validtypes) )

    def __str__( self ):
        rStr = '[{}]\n'.format(self.name)
        vals = getattr( self, self.name )
        if self.type == 'keyval':
            rStr += "\n".join( ['{},{}'.format(k,v) for k,v in vals.items()] )
        elif self.type == 'valonly':
            rStr += "\n".join( vals )
        elif self.type == 'csv':
            rStr += ",".join( self.headers ) + '\n'
            for d in vals:
                for h in self.headers:
                    rStr += d[h] + ','
                rStr = rStr[:-1] + '\n'
            rStr = rStr[:-1]
        return rStr
