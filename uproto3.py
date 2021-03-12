try: import ustruct as struct
except ImportError: import struct


class UnknownTypeException(Exception): pass
class ValueNotSetException(Exception): pass


def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)
    return _partial


def UEnum(*sequential, **named):
    '''
    Generates a dynamic type with named numeric members.
    '''

    def is_valid(cls, value):
        return value in cls.reverse_mapping

    enums = dict(((x, i) for i, x in enumerate(sequential)), **named)
    enums['reverse_mapping'] = dict((value, key) for key, value in enums.items())
    enums['is_valid'] = classmethod(is_valid)
    return type('Enum', (object,), enums)


_MessageRegistry = {}

def register_message(name):
    '''
    Global registry of message types by name
    to instantiate classes from message field subtype
    '''
    def _register_message(cls):
        global _MessageRegistry
        _MessageRegistry[name] = cls
        return cls
    return _register_message

def get_message_type(name):
    global _MessageRegistry
    return _MessageRegistry[name]


def get_header_for_tag(_tag, _type):
    '''
    Constructs protobuf header bytes
    '''
    if _tag < 0xF:
        return bytes([(_tag << 3) | _type])
    else:
        data = []
        value = (_tag << 3) | _type
        while value >= 0x7f:
            data.append((value & 0x7F) | 0x80)
            value = value >> 7
            data.append(value & 0x7F)
        return bytes(data)

def encode_varint(value):
    '''
    Varint packed number encoding
    '''
    data = []
    while True:
        towrite = value & 0x7f
        value >>= 7
        if value:
            data.append(towrite | 0x80)
        else:
            data.append(towrite)
            break
    return bytes(data)

def encode_fixed(n, fmt='<f'):
    return struct.pack(fmt, n)

def decode_fixed(n, fmt='<f'):
    return struct.unpack(fmt, n)[0]

def encode_zig_zag(n, bits=32):
    return (n << 1) ^ (n >> (bits - 1))

def decode_zig_zag(n):
    return (n >> 1) ^ -(n & 1)


WireType = UEnum(Invalid=-1, Varint=0, Bit64=1, Length=2, Bit32=5)
FieldType = UEnum(Invalid=-1, Optional=1, Required=2, Repeated=3)


class VarType(object):

    def __init__(self, tag=None, data=None, sub_type=-1, field_type=-1, **kwargs):
        self._tag = tag
        self._data = data
        self._sub_type = sub_type
        self._field_type = field_type
        self._submessage_type = kwargs.get('submessage_type', '')
        self._oneof = kwargs.get('oneof', '')
        self._value = [] if field_type == FieldType.Repeated else None

    def reset(self):
        self._data = None
        self._value = [] if self._field_type == FieldType.Repeated else None

    def is_valid(self):
        return True

    @property
    def tag(self):
        return self._tag

    @staticmethod
    def get_type():
        return WireType.Invalid

    def data(self):
        return self._data

    def parse_data(self, data):
        self._data = data

    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __repr__(self):
        return '{}({}: {})'.format(self.__class__.__name__, self._tag, self._value)


VarintSubType = UEnum(
    Int32=1,
    Int64=2,
    UInt32=3,
    UInt64=4,
    SInt32=5,
    SInt64=6,
    Bool=7,
    Enum=8,
)

class Varint(VarType):

    def __init__(self, tag=None, data=None, sub_type=-1, field_type=-1, **kwargs):
        super().__init__(tag, data, sub_type, field_type, **kwargs)
        if sub_type == VarintSubType.Enum:
            self._enum = kwargs['enum']

    @staticmethod
    def get_type():
        return WireType.Varint

    def parse_data(self, data):
        self._data = data
        if self._field_type == FieldType.Repeated:
            while data:
                shift = 0
                value = 0
                while True:
                    d = data[0]
                    data = data[1:]
                    value |= (d & 0x7f) << shift
                    shift += 7
                    if not (d & 0x80) or not data:
                        break
                self._value.append(value)
        else:
            value = 0
            for i, d in enumerate(self._data):
                value |= (d & 0x7f) << (i * 7)
            if self._sub_type in (VarintSubType.SInt32, VarintSubType.SInt64):
                value = decode_zig_zag(value)
            elif self._sub_type == VarintSubType.Bool:
                value = bool(value)
            self._value = value

    def set_value(self, value):
        self._value = value

    def serialize(self):
        if not self._value:
            self._data = b''
            return self._data
        if self._field_type == FieldType.Repeated:
            data = get_header_for_tag(self._tag, WireType.Length)
            v = self._value
        else:
            data = get_header_for_tag(self._tag, WireType.Varint)
            v = [self._value]
        _data = b''
        for x in v:
            if not x:
                continue
            if self._sub_type in (VarintSubType.SInt32, VarintSubType.SInt64):
                x = encode_zig_zag(x, 32 if self._sub_type == VarintSubType.SInt32 else 64)
            if self._sub_type == VarintSubType.Bool:
                _data += bytes([int(x)])
            else:
                _data += encode_varint(x)
        if self._field_type == FieldType.Repeated:
            data += encode_varint(len(_data))
        data += _data
        self._data = bytes(data)
        return self._data

    def __repr__(self):
        if self._sub_type != VarintSubType.Enum:
            return super().__repr__()
        valueName = self._enum.reverse_mapping.get(self._value, None)
        return '{}({}: {})'.format(self.__class__.__name__, self._tag, valueName)


LengthSubType = UEnum(
    String=1,
    Message=2,
    Group=3,
    Bytes=4,
)

class Length(VarType):

    @staticmethod
    def get_type():
        return WireType.Length

    def parse_data(self, data):
        self._data = data
        if self._sub_type == LengthSubType.String:
            value = self._data.decode('utf8')
        elif self._sub_type == LengthSubType.Message:
            if not hasattr(self, '_submessage_type'):
                raise Exception('_submessage_type not set')
            value = get_message_type(self._submessage_type)()
            value.parse(self._data)
        else:
            value = self._data
        if self._field_type == FieldType.Repeated:
            self._value.append(value)
        else:
            self._value = value

    def set_value(self, value):
        self._value = value

    def serialize(self):
        data = b''
        if not self._value:
            self._data = bytes(data)
            return self._data
        if hasattr(self, '_submessage_type'):
            if isinstance(self._value, list) and self._field_type == FieldType.Repeated:
                for submessage in self._value:
                    data += get_header_for_tag(self._tag, WireType.Length)
                    if isinstance(submessage, str):
                        encoded_submessage = bytes(submessage, 'utf8')
                    elif isinstance(submessage, bytes):
                        encoded_submessage = submessage
                    else:
                        encoded_submessage = submessage.serialize()
                    data += encode_varint(len(encoded_submessage))
                    data += encoded_submessage
            else:
                value = self._value.serialize()
                data += get_header_for_tag(self._tag, WireType.Length)
                data += encode_varint(len(value))
                data += bytes(value)
        else:
            data += get_header_for_tag(self._tag, WireType.Length)
            if isinstance(self._value, bytes):
                data += encode_varint(len(self._value))
                data += self._value
            else:
                data += encode_varint(len(bytes(self._value, 'utf8')))
                data += bytes(self._value, 'utf8')
        self._data = bytes(data)
        return self._data


FixedSubType = UEnum(
    Fixed64=1,
    SignedFixed64=2,
    Double=3,
    Fixed32=4,
    SignedFixed32=5,
    Float=6,
)

class Fixed(VarType):

    def __init__(self, tag=None, data=None, sub_type=-1, field_type=-1, **kwargs):
        super().__init__(tag, data, sub_type, field_type, **kwargs)
        if sub_type == FixedSubType.Float:
            self._fmt = '<f'
        elif sub_type == FixedSubType.Double:
            self._fmt = '<d'
        elif sub_type in (FixedSubType.Fixed32, FixedSubType.SignedFixed32):
            self._fmt = '<i'
        elif sub_type in (FixedSubType.Fixed64, FixedSubType.SignedFixed64):
            self._fmt = '<q'

    def get_type(self):
        if self._sub_type in (FixedSubType.Fixed64, FixedSubType.SignedFixed64, FixedSubType.Double):
            return WireType.Bit64
        else:
            return WireType.Bit32

    def parse_data(self, data):
        self._data = data
        value = decode_fixed(self._data, self._fmt)
        if self._field_type == FieldType.Repeated:
            self._value.append(value)
        else:
            self._value = value

    def set_value(self, value):
        self._value = value

    def serialize(self):
        if not self._value:
            self._data = b''
            return self._data
        data = bytes(get_header_for_tag(self._tag, self.get_type()))
        self._data = data + encode_fixed(self._value, self._fmt)
        return self._data


@register_message('uproto3.Message')
class Message:

    def __init__(self, **kwargs):
        self._fields_lut = {}
        self._fields = {}
        self._oneofs = {}
        for field in self._proto_fields:
            if field['type'] == WireType.Varint:
                klass = Varint
            elif field['type'] == WireType.Length:
                # FIXME: parse submessages as Message
                klass = Length
            elif field['type'] in (WireType.Bit32, WireType.Bit64):
                klass = Fixed
            else:
                raise UnknownTypeException
            self._fields_lut[field['tag']] = field['name']
            self._fields[field['name']] = klass(**field)
            setattr(
                self.__class__,
                field['name'],
                property(
                    partial(self.__get, field['name']),
                    partial(self.__set, field['name']),
                )
            )
            if field.get('oneof'):
                setattr(
                    self.__class__,
                    'which_' + field['oneof'],
                    partial(self.__which_oneof, field['oneof']),
                )
        self.fields = self._fields
        for k, v in kwargs.items():
            Message.__set(k, self, v)

    @staticmethod
    def __which_oneof(oneof, instance):
        return instance._oneofs.get(oneof)

    @staticmethod
    def __get(name, instance):
        return instance._fields[name]

    @staticmethod
    def __set(name, instance, value):
        if name not in instance._fields:
            return
        if instance._fields[name]._oneof:
            # reset other fields
            for k in instance._fields:
                if instance._fields[k]._oneof == instance._fields[name]._oneof:
                    instance._fields[k].reset()
            instance._oneofs[instance._fields[name]._oneof] = name
        instance._fields[name].set_value(value)

    def __iter__(self):
        return iter(self._fields.keys())

    def reset(self):
        for field in self.values():
            field.reset()

    def is_valid(self):
        for field in self.values():
            if not field.is_valid():
                # print('Field {} is not valid!'.format(field.tag))
                return False
        else:
            return True

    def keys(self):
        return self._fields.keys()

    def values(self):
        return self._fields.values()

    def items(self):
        return self._fields.items()

    def serialize(self):
        data = b''
        for i in self._fields_lut.keys():
            name = self._fields_lut[i]
            d = self._fields[name].serialize()
            if d is not None:
                data += bytes(d)
        return data

    def parse(self, msg):
        self.reset()
        i = 0
        while i < len(msg):
            byte = msg[i]
            _type = byte & 0x7
            if not WireType.is_valid(_type):
                i += 1
                continue
            if byte <= 0x7f:
                tag = byte >> 3
            else:
                # FIXME: this smells
                bitpos = 0
                result = 0
                while byte & 0x80:
                    result |= (byte & 0x7F) << bitpos
                    bitpos += 7
                    i += 1
                    byte = msg[i]
                    if bitpos > 32:
                        raise Exception('cant handle >32bit varint')
                result |= ((byte & 0x7F) << bitpos)
                _type = result & 0x7
                tag = result >> 3
            data = None
            if _type == WireType.Varint:
                data = []
                while True:
                    i += 1
                    data.append(msg[i])
                    if not msg[i] & 0x80:
                        break
                i += 1
            elif _type in (WireType.Bit32, WireType.Bit64, WireType.Length):
                if _type == WireType.Length:
                    shift = 0
                    length = 0
                    while True:
                        i += 1
                        d = int(msg[i])
                        length |= (d & 0x7f) << shift
                        shift += 7
                        if not (d & 0x80):
                            break
                else:
                    length = 4 if _type == WireType.Bit32 else 8
                i += 1
                data = msg[i:i+length]
                i += length
            else:
                raise UnknownTypeException
            if tag not in self._fields_lut:
                continue
            name = self._fields_lut[tag]
            if name not in self._fields:
                continue
            if self._fields[name]._oneof:
                # protobuf spec says to nullify all other fields in oneof group
                for k in self._fields:
                    if self._fields[k]._oneof == self._fields[name]._oneof:
                        self._fields[k].reset()
                self._oneofs[self._fields[name]._oneof] = name
            self._fields[name].parse_data(data)
        return self.is_valid()
