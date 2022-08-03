import logging
import re
import collections
import struct
from io import StringIO
import codecs
import binascii
import math
import sys

def string_searcher(data, search_long=False):
  strings=[]
    
  last_string_pos=0

  if search_long:
    pattern = '[\x00-\xff][\x01-\xff]\x00\x00'
  else:
    pattern = '[\x02-\xff]\x00\x00\x00'
  
  for i in re.finditer(pattern, data):
    m = i.group(0)[0:4]

    string_length = struct.unpack('L', m)[0]

    start = i.start()

    if start+string_length+3 >= len(data):
      continue

    if data[start+string_length+3] != '\x00':
      continue

    if re.search('[\x00-\x1f\x80-\xff]', data[start+4:start+string_length+3]):
      continue

    strings.append((i.start(), string_length, data[start+4:start+4+string_length-1]))
  
  return strings

unprint = [' \\0',' \\1',' \\2',' \\3',' \\4',' \\5',' \\6',
           ' \\a',' \\b',' \\t',' \\n',' \\v',' \\f',' \\r']
def hprint(data, n=4, s=6):
  address_width = int(math.log(len(data))/math.log(10))+1

  for x in range(0, len(data), n*s):
    dline = data[x:x+n*s]
    
    hline = binascii.b2a_hex(dline)
    hline=[hline[h:h+2] for h in range(0, len(hline), 2)]
    
    dline=[dline[h:h+n] for h in range(0, len(dline), n)]

    print( '{0:<{width}}:'.format(x, width=address_width), \
          '   '.join([' '.join(hline[h:h+n]) for h in range(0, len(hline), n)]))
    print (' '*(address_width+1),)
    for g in dline:
      for x in g:
        if ord(x) <= 13:
          sys.stdout.write(unprint[ord(x)])
        elif ord(x) < 32:
          sys.stdout.write('\\'+str(ord(x)))
        elif ord(x) >= 127:
          sys.stdout.write(str(ord(x)))
        else:
          print (x+' ',)
      print (' ',)
    print('\n')

def sdiff(*a):
  for i,d in enumerate(zip(*a)):
    print ('{}:'+'\t{}'*len(a)).format(i,*(ord(x) if isinstance(x, str) else x for x in d))
def db_float_encode(f):
  return struct.unpack('L', struct.pack('f', f))[0]+32623*2**32
def db_float_decode(s):
  return struct.unpack('f', struct.pack('L', s%2**32))[0]
def uint32_encode(*i):
  return struct.pack('L'*len(i), *i)
def uint32_decode(s):
  return struct.unpack('L'*(len(s)/4), s)
def uint64_encode(*i):
  return struct.pack('Q'*len(i), *i)
def uint64_decode(s):
  return struct.unpack('Q'*(len(s)/8), s)

def read_string(data):
  string_length = struct.unpack('L', data[0:4])[0]

  if string_length:
    string = data[4:4+string_length]
    assert string[-1] == '\x00'
    return string[:-1]
  return None


class NonePropertyException(Exception):
  ''' Exception when when None name is encountered. Usually means array end'''
  pass

class Uasset(object):
  def __init__(self, filename=None):
    ''' Create a Uasset parser.
    
        filename - Name of uasset file. None to skip loading '''

    self.logger = logging.getLogger()
    
    self.handles={}
    self.array_handles={}

    # If filename specified
    if filename:
      # Load it
      self.load(filename)

  def read(self, *args, **kwargs):
    ''' Read from the data buffer '''
    return self.data.read(*args, **kwargs)

  def read_uint16(self):
    ''' Read a uint16 from the data buffer '''
    return struct.unpack('H', self.data.read(2))[0]
  def read_int16(self):
    ''' Read a int16 from the data buffer '''
    return struct.unpack('h', self.data.read(2))[0]
  def read_uint32(self):
    ''' Read a uint32 from the data buffer '''
    return struct.unpack('L', self.data.read(4))[0]
  def read_int32(self):
    ''' Read a int32 from the data buffer '''
    return struct.unpack('l', self.data.read(4))[0]
  def read_uint64(self):
    ''' Read a uint64 from the data buffer '''
    return struct.unpack('Q', self.data.read(8))[0]
  def read_int64(self):
    ''' Read a int64 from the data buffer '''
    return struct.unpack('q', self.data.read(8))[0]
  def read_float(self):
    ''' Read a single float from the data buffer '''
    return struct.unpack('f', self.data.read(4))

  def read_uint16s(self, n=1):
    ''' Read multiple uint16s from the data buffer '''
    return struct.unpack('H'*n, self.data.read(2*n))
  def read_int16s(self, n=1):
    ''' Read multiple int16s from the data buffer '''
    return struct.unpack('h'*n, self.data.read(2*n))
  def read_uint32s(self, n=1):
    ''' Read multiple uint32s from the data buffer '''
    return struct.unpack('L'*n, self.data.read(4*n))
  def read_int32s(self, n=1):
    ''' Read multiple int32s from the data buffer '''
    return struct.unpack('l'*n, self.data.read(4*n))
  def read_uint64s(self, n=1):
    ''' Read multiple uint64s from the data buffer '''
    return struct.unpack('Q'*n, self.data.read(8*n))
  def read_int64s(self, n=1):
    ''' Read multiple int64s from the data buffer '''
    return struct.unpack('q'*n, self.data.read(8*n))
  def read_floats(self, n=1):
    ''' Read multiple single floats from the data buffer '''
    return struct.unpack('f'*n, self.data.read(4*n))

  def read_string(self):
    ''' Read a string from the data buffer, including null terminator '''
    string_length = self.read_int32()
    if string_length > 0:
      string = self.data.read(string_length)
    elif string_length < 0:
      string = self.data.read(string_length*-2).decode('utf-16')
    else:
      return None

    assert string[-1] == '\x00'
    return string[:-1]

  def peek(self, peek_size):
    ''' Peek at the data buffer '''
    return self.data.buf[self.data.pos:self.data.pos+peek_size]
  
  def read_header(self):
    pass # Haven't cared enough to parse anything but DataTables

  def load(self, filename):
    ''' Load the uasset file '''
    
    # Buffer the whole file
    with open(filename, 'rb') as fid:
      self.data = StringIO(fid.read())
    
    # Load header
    self.read_header()

    self.logger.debug('head: {} @ {}'.format(self.count, self.data.pos))

    # Start reading all the items
    self.items=collections.OrderedDict()
    for x in range(self.count):
      self.read_item()

    # I suspect this is a checksum
    self.footer = self.read()
    assert len(self.footer) == 4

class DataTable(Uasset):
  def read_header(self):
    ''' Read the header, including the lut. '''

    self.header1 = self.read(28) # I dunno
    self.header2 = self.read_string() # It's a string! Usually says "None"
    self.header3 = self.read(4) # I dunno
    self.lut_entries = self.read_uint32() # Number of entries
    self.header4 = self.read(68) # More stuff I don't know
    self.lut_entries2 = self.read_uint32() # Number of entries... AGAIN?
    self.header5 =self.read(68) # Even more stuff I don't know
    
    # Double checking. It's always been true *Shrugs*
    assert self.lut_entries==self.lut_entries2
    
    # load the LUT. Kind of like columns, the first column values, and
    # datatypes all mixed together
    self.read_lut()
    self.logger.debug('l {}'.format(self.data.pos))

    # Sub-headers, I hate sub-headers!
    self.mid1=[]

    mid = self.read_int32()
    while mid >= 0:
      self.mid1.append((mid,)+self.read_int32s(6))
      mid = self.read_int32()
    self.mid2 = (mid,)+self.read_int32s(18)
    self.mid3 = self.read_int32s(self.mid2[-1])
    self.mid4 = self.read_int32s(7)
    self.mid5 = self.read(1)
    self.mid6 = self.read_int32s(4)

    # Read the number of items (think of it as rows in a spreadsheet)
    self.count=self.read_uint32()
    
  def read_lut(self):
    ''' Read the lut from the header '''

    self.lut=collections.OrderedDict()
    for x in range(self.lut_entries):
      name = self.read_string()
      self.lut[name] = self.read(4) # Don't know what's in these 4 bytes. UID?
    
  def decode_word(self):
    ''' Decode the index using a LUT '''
    return self.lut.keys()[self.read_uint64()]

  def read_property(self):
    ''' Read a value. Like an element from a spreadsheet '''
    
    # Name comes first
    property_name = self.decode_word()

    # If it's None, raise Exception
    if property_name == 'None':
      raise NonePropertyException()

    # Type is second
    property_type = self.decode_word()

    self.logger.info('{} [{}]'.format(property_name, property_type))
   
    # Read in the value, using the appropriate handler
    return property_name, self.handles[property_type]()

  def read_properties(self):
    ''' General read properties routine
    
        Reads properties until None is encountered. This works for both reading
        items and reading a struct'''
    properties={}
    try:
      while True:
        key, value = self.read_property()
        properties[key] = value
    except NonePropertyException as e:
      pass
    return properties

  def read_item(self):
    ''' Read an item (row) and all the properties (columns) to go with it '''
    #item_key = self.decode_word()
    item_key = self.lut.keys()[self.read_uint32()]
    x = self.read_uint32()
    self.logger.warning('Item {} {}'.format(item_key, self.data.pos))
    self.items[item_key] = self.read_properties()
    if x != 0:
      self.items[item_key+'_n'] = x

class RokhDataTable(DataTable):
  def __init__(self, filename=None):
    super(RokhDataTable, self).__init__()
    
    # List of datatype handlers. May be Rokh specific?
    self.handles.update({"ByteProperty":   self.read_byte_property,
                         "FloatProperty":  self.read_float_property,
                         "IntProperty":    self.read_int_property,
                         "ObjectProperty": self.read_object_property,
                         "TextProperty":   self.read_text_property,
                         'ArrayProperty':  self.read_array_property,
                         'StrProperty':    self.read_str_property,
                         'StructProperty': self.read_struct_property,
                         'NameProperty':   self.read_name_property,
                         'BoolProperty':   self.read_bool_property})

    if filename:
      self.load(filename)
    
  def read_byte_property(self):
    ''' Read type ByteProperty '''

    byte_size = self.read_uint64()
    # I've only seen byte_size 8
    if byte_size == 8:
      byte_type = self.decode_word()
      assert self.read(1) == '\x00'
      return (byte_type, self.decode_word())
    raise Exception('byte property')
    
  def read_float_property(self):
    ''' Read type FloatProperty '''
    
    float_size = self.read_uint64()
    # I've only seen float_size 4
    if float_size==4:
      assert self.read(1) == '\x00'
      return self.read_float()
    raise Exception('float property')

  def read_int_property(self):
    ''' Read type IntProperty '''

    int_size = self.read_uint64()
    # I've only seen int_size 4
    if int_size==4:
      assert self.read(1) == '\x00'
      return self.read_int32()
    raise Exception('int property')

  def read_object_property(self):
    ''' Never seen one of these '''

    obj_size = self.read_uint64()
    assert self.read(1) == '\x00'
    return self.read(obj_size)

  def read_text_property(self):
    ''' Read type TextProperty '''

    # This is probably the size of both strings, and the extra nulls
    size = self.read_uint64()
    self.logger.debug('tps: {} @ {}'.format(size, self.data.pos-8))

    # Not sure if 18 is the ideal cutoff here. using size above to cya and
    # try/catch on failures may be better
    if size>=18:
      assert self.read(1) == '\x00'
      x = self.read_uint64()
      assert self.read(1) == '\x00'
      string_hash = self.read_string()
      q = self.read_string()
      self.logger.debug('tpe: {}'.format(self.data.pos))
      return q
      #return self.read_string()
    
    assert self.read(size) == '\x00'*size

    # If there is no string read, there's always an ff here
    assert self.data.read(1)=='\xff'
    # Return None instead of an empty string, so you at least know something
    # was different this time.
    return None

  def read_str_property(self):
    ''' Read StrProperty '''

    size = self.read_uint64()
    assert ord(self.read(1)) == 0
    data = self.read(size)
    return read_string(data)

  def read_name_property(self):
    ''' Read NameProperty '''

    value = self.decode_word()
    assert self.read(1) == '\x00'
    return value, self.decode_word()

  def read_bool_property(self):
    ''' Read BoolProperty '''
    return self.read(10)

  def read_struct_array_header_property(self):
    ''' Read header for a struct when reading in an array
    
    Data isn't used, mostly just to clear it off the buffer. A struct is read
    mostly like a whole item. So there's no need to use this information.
    '''

    n = self.decode_word() # name  AGAIN? Or just a number
    s = self.decode_word() # structPropery AGAIN
    # Right now this is more an info thing. I'm sure I'm missing something
    x = self.read_uint64() # A number?
    y = self.read_uint64() # Struct type possibly? Don't know. Don't need it

    u = self.read_uint64()
    v = self.read_uint64()
    assert self.read(1) == '\x00'

    return x,y

  def read_struct_property(self):

    s = self.read_uint64()
    #assert s==4 # Is this the size of data below or not?
    name = self.decode_word() # Same name again?
    
    assert self.read_uint64s(2) == (0,0)
    assert self.read(1) == '\x00'

    data = self.read(s) # is this a hash like in the lut or struct data?

    return data

  def read_array_property(self):
    ''' Read ArrayProperty
     
        This is probably the most complicated of the types. An array is an
        array of other types, even possibly a Struct. But most of the array 
        property parsing is different than the non-array parsing handlers'''

    x = self.read_uint64() # Bytes size of array data?
    element_type = self.decode_word() # Get the property type
    assert self.read(1) == '\x00'
    array_elements = self.read_uint32()
    array_data=[]

    if element_type == 'StructProperty':
      struct_type = self.read_struct_array_header_property()
      reader = self.read_properties
    elif element_type == 'StrProperty':
      reader = self.read_string
    elif element_type == 'IntProperty':
      # Might need to add in logic to get the
      # (x (total size) - array_elements_size(4 bytes)) / array_elements to determine
      # the right int size. 4 works for now :)
      reader = self.read_int32
    elif element_type == 'UInt32Property':
      reader = self.read_uint32
    elif element_type == 'NameProperty':
      reader = self.read_uint64
    else:
      raise Exception('Array type '+element_type)

    for i in range(array_elements):
      array_data.append(reader())
    return array_data