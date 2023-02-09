import json

json_encoding = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
print(json_encoding)
print(type(json_encoding))

json_decoding = json.loads(json_encoding)
print(json_decoding)
print(type(json_decoding))