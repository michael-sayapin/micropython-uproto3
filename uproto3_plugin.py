#!/usr/bin/env python

from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor_pb2 import DescriptorProto, OneofDescriptorProto, EnumDescriptorProto, FieldDescriptorProto
from itertools import chain

from uproto3 import FieldType

import os.path
import logging

def traverse(proto_file):
    def _traverse(package, items):
        for item in items:
            yield item, package
            if isinstance(item, DescriptorProto):
                for e in item.enum_type:
                    yield e, package
                for nested in item.nested_type:
                    nested_package = package + item.name
                    for nested_item in _traverse(nested, nested_package):
                        yield nested_item, nested_package
    return chain(
        _traverse(proto_file.package, proto_file.enum_type),
        _traverse(proto_file.package, proto_file.message_type),
    )

def get_wire_type(field_type):
    return {
        FieldDescriptorProto.TYPE_BOOL:     ("WireType.Varint", "VarintSubType.Bool"),
        FieldDescriptorProto.TYPE_BYTES:    ("WireType.Length", "LengthSubType.Bytes"),
        FieldDescriptorProto.TYPE_DOUBLE:   ("WireType.Bit64",  "FixedSubType.Double"),
        FieldDescriptorProto.TYPE_ENUM:     ("WireType.Varint", "VarintSubType.Enum"),
        FieldDescriptorProto.TYPE_FIXED32:  ("WireType.Bit32",  "FixedSubType.Fixed32"),
        FieldDescriptorProto.TYPE_FIXED64:  ("WireType.Bit64",  "FixedSubType.Fixed64"),
        FieldDescriptorProto.TYPE_FLOAT:    ("WireType.Bit32",  "FixedSubType.Float"),
        # FIXME: this does not work currently
        FieldDescriptorProto.TYPE_GROUP:    ("WireType.Length", "LengthSubType.Group"),
        FieldDescriptorProto.TYPE_INT32:    ("WireType.Varint", "VarintSubType.Int32"),
        FieldDescriptorProto.TYPE_INT64:    ("WireType.Varint", "VarintSubType.Int64"),
        FieldDescriptorProto.TYPE_MESSAGE:  ("WireType.Length", "LengthSubType.Message"),
        FieldDescriptorProto.TYPE_SFIXED32: ("WireType.Bit32",  "FixedSubType.SignedFixed32"),
        FieldDescriptorProto.TYPE_SFIXED64: ("WireType.Bit64",  "FixedSubType.SignedFixed64"),
        FieldDescriptorProto.TYPE_SINT32:   ("WireType.Varint", "VarintSubType.SInt32"),
        FieldDescriptorProto.TYPE_SINT64:   ("WireType.Varint", "VarintSubType.SInt64"),
        FieldDescriptorProto.TYPE_STRING:   ("WireType.Length", "LengthSubType.String"),
        FieldDescriptorProto.TYPE_UINT32:   ("WireType.Varint", "VarintSubType.UInt32"),
        FieldDescriptorProto.TYPE_UINT64:   ("WireType.Varint", "VarintSubType.UInt64"),
    }[field_type]

def get_field_type(field_type):
    assert FieldType.is_valid(field_type)
    name = FieldType.reverse_mapping[field_type]
    return "FieldType.{}".format(name)

def generate_code(request, response):
    for proto_file in request.proto_file:
        output = "from uproto3 import UEnum, Message, LengthSubType, VarintSubType, FixedSubType, FieldType, WireType, register_message\n"

        imports = []
        enums = {}
        fields = ""

        files = list(traverse(proto_file))

        for item, package in files:
            # first, process all enums
            if isinstance(item, EnumDescriptorProto):
                enums[item.name] = ''
                enums[item.name] += "\n    {} = UEnum(\n".format(item.name)
                for value in item.value:
                    enums[item.name] += '        {}={},\n'.format(value.name, value.number)
                enums[item.name] += "    )\n"

        for item, package in files:

            # we do not need non-package protos
            if not package:
                continue

            oneofs = []
            if hasattr(item, 'oneof_decl') and item.oneof_decl:
                oneofs = item.oneof_decl

            if isinstance(item, DescriptorProto):
                fields += "\n\n@register_message('.{}.{}')\nclass {}(Message):\n".format(package, item.name, item.name)
                for field in item.field:
                    if field.type == FieldDescriptorProto.TYPE_ENUM:
                        fields += enums[field.type_name.split('.')[-1]]
                fields += "\n    _proto_fields = [\n"
                for field in item.field:
                    oneof = None
                    if hasattr(field, 'oneof_index') and field.HasField('oneof_index'):
                        oneof = oneofs[field.oneof_index].name
                    _type, subType = get_wire_type(field.type)
                    fields += "        dict(tag={}, name='{}', type={}, sub_type={}".format(
                        field.number,
                        field.name,
                        _type,
                        subType,
                    )
                    if get_field_type(field.label) != 'FieldType.Optional':
                        fields += ", field_type={}".format(get_field_type(field.label))
                    if oneof:
                        fields += ", oneof='{}'".format(oneof)
                    if field.type == FieldDescriptorProto.TYPE_ENUM:
                        enum_name = field.type_name.split('.')[-1]
                        fields += ", enum={}".format(enum_name)
                    if field.type == FieldDescriptorProto.TYPE_MESSAGE:
                        field_package, _ = field.type_name.strip('.').rsplit('.', 1)
                        if field_package and field_package != package:
                            imports.append(field_package)
                        fields += ", submessage_type='{}'".format(field.type_name)
                    fields += "),\n"
                fields += "    ]\n"

        imports = sorted(list(set(imports)))
        for package in imports:
            output += "import {}_upb3\n".format(package)

        output += fields
        f = response.file.add()
        f.name = "{}_upb3.py".format(os.path.splitext(proto_file.name)[0])
        f.content = output


if __name__ == '__main__':
    from sys import stdin, stdout

    data = stdin.buffer.read()
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)
    response = plugin.CodeGeneratorResponse()
    generate_code(request, response)
    output = response.SerializeToString()
    stdout.buffer.write(output)
