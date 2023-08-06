# Extended command line client for pystache

```
usage: pystache-cli [-h] [--loglevel {debug,info,warning,error}]
                    [--partial_paths [PARTIAL_PATHS [PARTIAL_PATHS ...]]]
                    [--partial_file_extension PARTIAL_FILE_EXTENSION]
                    [--file_encoding FILE_ENCODING] [--strict]
                    [--separators SEPARATORS SEPARATORS]
                    output_file template_file [context_file]

positional arguments:
  output_file           filepath to save output
  template_file         filepath to input template
  context_file          optional filepath to context json

optional arguments:
  -h, --help            show this help message and exit
  --loglevel {debug,info,warning,error}, -l {debug,info,warning,error}
  --partial_paths [PARTIAL_PATHS [PARTIAL_PATHS ...]], -p [PARTIAL_PATHS [PARTIAL_PATHS ...]]
  --partial_file_extension PARTIAL_FILE_EXTENSION, -x PARTIAL_FILE_EXTENSION
  --file_encoding FILE_ENCODING, -e FILE_ENCODING
  --strict, -s          if set: raise exception on missing keys
  --separators SEPARATORS SEPARATORS
                        left and right separator (default is '{{' '}}')
```