from uproto3 import UEnum, Message, LengthSubType, VarintSubType, FixedSubType, FieldType, WireType, register_message
import google.protobuf.DescriptorProto_upb3
import google.protobuf.EnumDescriptorProto_upb3
import google.protobuf.GeneratedCodeInfo_upb3
import google.protobuf.SourceCodeInfo_upb3
import google.protobuf.UninterpretedOption_upb3


@register_message('.google.protobuf.FileDescriptorSet')
class FileDescriptorSet(Message):

    _proto_fields = [
        dict(tag=1, name='file', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.FileDescriptorProto'),
    ]


@register_message('.google.protobuf.FileDescriptorProto')
class FileDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='package', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=3, name='dependency', type=WireType.Length, sub_type=LengthSubType.String, field_type=FieldType.Repeated),
        dict(tag=10, name='public_dependency', type=WireType.Varint, sub_type=VarintSubType.Int32, field_type=FieldType.Repeated),
        dict(tag=11, name='weak_dependency', type=WireType.Varint, sub_type=VarintSubType.Int32, field_type=FieldType.Repeated),
        dict(tag=4, name='message_type', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.DescriptorProto'),
        dict(tag=5, name='enum_type', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.EnumDescriptorProto'),
        dict(tag=6, name='service', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.ServiceDescriptorProto'),
        dict(tag=7, name='extension', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.FieldDescriptorProto'),
        dict(tag=8, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.FileOptions'),
        dict(tag=9, name='source_code_info', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.SourceCodeInfo'),
        dict(tag=12, name='syntax', type=WireType.Length, sub_type=LengthSubType.String),
    ]


@register_message('.google.protobuf.DescriptorProto')
class DescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='field', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.FieldDescriptorProto'),
        dict(tag=6, name='extension', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.FieldDescriptorProto'),
        dict(tag=3, name='nested_type', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.DescriptorProto'),
        dict(tag=4, name='enum_type', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.EnumDescriptorProto'),
        dict(tag=5, name='extension_range', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.DescriptorProto.ExtensionRange'),
        dict(tag=8, name='oneof_decl', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.OneofDescriptorProto'),
        dict(tag=7, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.MessageOptions'),
        dict(tag=9, name='reserved_range', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.DescriptorProto.ReservedRange'),
        dict(tag=10, name='reserved_name', type=WireType.Length, sub_type=LengthSubType.String, field_type=FieldType.Repeated),
    ]


@register_message('.google.protobuf.ExtensionRangeOptions')
class ExtensionRangeOptions(Message):

    _proto_fields = [
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.FieldDescriptorProto')
class FieldDescriptorProto(Message):

    Label = UEnum(
        LABEL_OPTIONAL=1,
        LABEL_REQUIRED=2,
        LABEL_REPEATED=3,
    )

    Type = UEnum(
        TYPE_DOUBLE=1,
        TYPE_FLOAT=2,
        TYPE_INT64=3,
        TYPE_UINT64=4,
        TYPE_INT32=5,
        TYPE_FIXED64=6,
        TYPE_FIXED32=7,
        TYPE_BOOL=8,
        TYPE_STRING=9,
        TYPE_GROUP=10,
        TYPE_MESSAGE=11,
        TYPE_BYTES=12,
        TYPE_UINT32=13,
        TYPE_ENUM=14,
        TYPE_SFIXED32=15,
        TYPE_SFIXED64=16,
        TYPE_SINT32=17,
        TYPE_SINT64=18,
    )

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=3, name='number', type=WireType.Varint, sub_type=VarintSubType.Int32),
        dict(tag=4, name='label', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=Label),
        dict(tag=5, name='type', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=Type),
        dict(tag=6, name='type_name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='extendee', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=7, name='default_value', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=9, name='oneof_index', type=WireType.Varint, sub_type=VarintSubType.Int32),
        dict(tag=10, name='json_name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=8, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.FieldOptions'),
        dict(tag=17, name='proto3_optional', type=WireType.Varint, sub_type=VarintSubType.Bool),
    ]


@register_message('.google.protobuf.OneofDescriptorProto')
class OneofDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.OneofOptions'),
    ]


@register_message('.google.protobuf.EnumDescriptorProto')
class EnumDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='value', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.EnumValueDescriptorProto'),
        dict(tag=3, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.EnumOptions'),
        dict(tag=4, name='reserved_range', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.EnumDescriptorProto.EnumReservedRange'),
        dict(tag=5, name='reserved_name', type=WireType.Length, sub_type=LengthSubType.String, field_type=FieldType.Repeated),
    ]


@register_message('.google.protobuf.EnumValueDescriptorProto')
class EnumValueDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='number', type=WireType.Varint, sub_type=VarintSubType.Int32),
        dict(tag=3, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.EnumValueOptions'),
    ]


@register_message('.google.protobuf.ServiceDescriptorProto')
class ServiceDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='method', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.MethodDescriptorProto'),
        dict(tag=3, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.ServiceOptions'),
    ]


@register_message('.google.protobuf.MethodDescriptorProto')
class MethodDescriptorProto(Message):

    _proto_fields = [
        dict(tag=1, name='name', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=2, name='input_type', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=3, name='output_type', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=4, name='options', type=WireType.Length, sub_type=LengthSubType.Message, submessage_type='.google.protobuf.MethodOptions'),
        dict(tag=5, name='client_streaming', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=6, name='server_streaming', type=WireType.Varint, sub_type=VarintSubType.Bool),
    ]


@register_message('.google.protobuf.FileOptions')
class FileOptions(Message):

    OptimizeMode = UEnum(
        SPEED=1,
        CODE_SIZE=2,
        LITE_RUNTIME=3,
    )

    _proto_fields = [
        dict(tag=1, name='java_package', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=8, name='java_outer_classname', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=10, name='java_multiple_files', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=20, name='java_generate_equals_and_hash', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=27, name='java_string_check_utf8', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=9, name='optimize_for', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=OptimizeMode),
        dict(tag=11, name='go_package', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=16, name='cc_generic_services', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=17, name='java_generic_services', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=18, name='py_generic_services', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=42, name='php_generic_services', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=23, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=31, name='cc_enable_arenas', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=36, name='objc_class_prefix', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=37, name='csharp_namespace', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=39, name='swift_prefix', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=40, name='php_class_prefix', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=41, name='php_namespace', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=44, name='php_metadata_namespace', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=45, name='ruby_package', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.MessageOptions')
class MessageOptions(Message):

    _proto_fields = [
        dict(tag=1, name='message_set_wire_format', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=2, name='no_standard_descriptor_accessor', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=3, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=7, name='map_entry', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.FieldOptions')
class FieldOptions(Message):

    CType = UEnum(
        STRING=0,
        CORD=1,
        STRING_PIECE=2,
    )

    JSType = UEnum(
        JS_NORMAL=0,
        JS_STRING=1,
        JS_NUMBER=2,
    )

    _proto_fields = [
        dict(tag=1, name='ctype', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=CType),
        dict(tag=2, name='packed', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=6, name='jstype', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=JSType),
        dict(tag=5, name='lazy', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=3, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=10, name='weak', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.OneofOptions')
class OneofOptions(Message):

    _proto_fields = [
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.EnumOptions')
class EnumOptions(Message):

    _proto_fields = [
        dict(tag=2, name='allow_alias', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=3, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.EnumValueOptions')
class EnumValueOptions(Message):

    _proto_fields = [
        dict(tag=1, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.ServiceOptions')
class ServiceOptions(Message):

    _proto_fields = [
        dict(tag=33, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.MethodOptions')
class MethodOptions(Message):

    IdempotencyLevel = UEnum(
        IDEMPOTENCY_UNKNOWN=0,
        NO_SIDE_EFFECTS=1,
        IDEMPOTENT=2,
    )

    _proto_fields = [
        dict(tag=33, name='deprecated', type=WireType.Varint, sub_type=VarintSubType.Bool),
        dict(tag=34, name='idempotency_level', type=WireType.Varint, sub_type=VarintSubType.Enum, enum=IdempotencyLevel),
        dict(tag=999, name='uninterpreted_option', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption'),
    ]


@register_message('.google.protobuf.UninterpretedOption')
class UninterpretedOption(Message):

    _proto_fields = [
        dict(tag=2, name='name', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.UninterpretedOption.NamePart'),
        dict(tag=3, name='identifier_value', type=WireType.Length, sub_type=LengthSubType.String),
        dict(tag=4, name='positive_int_value', type=WireType.Varint, sub_type=VarintSubType.UInt64),
        dict(tag=5, name='negative_int_value', type=WireType.Varint, sub_type=VarintSubType.Int64),
        dict(tag=6, name='double_value', type=WireType.Bit64, sub_type=FixedSubType.Double),
        dict(tag=7, name='string_value', type=WireType.Length, sub_type=LengthSubType.Bytes),
        dict(tag=8, name='aggregate_value', type=WireType.Length, sub_type=LengthSubType.String),
    ]


@register_message('.google.protobuf.SourceCodeInfo')
class SourceCodeInfo(Message):

    _proto_fields = [
        dict(tag=1, name='location', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.SourceCodeInfo.Location'),
    ]


@register_message('.google.protobuf.GeneratedCodeInfo')
class GeneratedCodeInfo(Message):

    _proto_fields = [
        dict(tag=1, name='annotation', type=WireType.Length, sub_type=LengthSubType.Message, field_type=FieldType.Repeated, submessage_type='.google.protobuf.GeneratedCodeInfo.Annotation'),
    ]
