# micropython-uproto3

## Project Status

Based on https://github.com/jazzycamel/micropython-uprotobuf/

This project is very much a work in progress and, as such, is incomplete. It only targets compatibility with proto3, and drops support for many proto2-specific features (optional/required, defaults).

### FIXME

* Handle assignment inside sub-messages

## Usage

It is assumed that Google Protobuf has been installed and the compiler (`protoc`) is on the `$PATH`. It is also assumed that a version of Python (preferably 3) is also available and the `protobuf` module has been installed (`pip install protobuf`).

Assuming you have a protocol specification file available (in this case called `test.proto`) containing something like the following:

```proto
syntax = "proto3";

package test;

message TestMessage {
  enum TestEnum {
    UNKNOWN=0;
    A=1;
    B=2;
    C=3;
  }
  int32 a = 1;
  string b = 2;
  int64 c = 4;
  float d = 5;
  double e = 6;
  TestEnum f = 7;
  bool g = 8;
  fixed32 h = 9;
  sint32 i = 10;
  sfixed64 j = 11;
  repeated int32 k = 12;
  oneof test_oneof {
    int32 l = 13;
    int32 m = 14;
    int32 n = 15;
  }
}
```

then a MicroPython compatible module can be created using the uproto3 plugin as follows:

```sh
$ git clone https://github.com/michael-sayapin/micropython-uproto3.git
$ cd micropython-uproto3
$ chmod +x uproto3_plugin.py
$ protoc --plugin=protoc-gen-custom=uproto3_plugin.py --custom_out=. test.proto
```

This will generate a python module named `test_upb3.py`, which can be imported and used by micropython, containing a class named `TestMessage`. This class can currently be used to parse and encode binary messages as follows:

```python
from test_upb3 import TestMessage

received_message = TestMessage()
received_message.parse("\x08\x96\x01")

if received_message.which_test_oneof() == 'n':
  # field called "n" was present in "test_oneof" group
  print(received_message.n)

message_to_send = TestMessage(
  a=1,
  b='hello',
  f=TestMessage.TestEnum.C,
  k=[1, 2],
  l=123,
)
# alas, this will not work:
# message_to_send.k.append(3)
# this will:
message_to_send.k = message_to_send.k + [3]
binary_data = message_to_send.serialize()
```
