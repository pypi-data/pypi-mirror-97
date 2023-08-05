# fastutils

Collection of simple utils.

## Install

```shell
pip install fastutils
```

## Installed Utils

- aesutils # use cipherutils instead
- cacheutils
   - get_cached_value
- cipherutils
   - DecryptFailed
   - ResultEncoderBase     # result encoder base
   - RawDataEncoder        # result encoder, default result encoder to most ciphers
   - HexlifyEncoder        # result encoder
   - Base64Encoder         # result encoder
   - SafeBase64Encoder     # result encoder
   - Utf8Encoder           # result encoder
   - MappingCipherBase     # self-designed cipher base, by mapping every byte from 0-255 to random-seeds.
   - AesCipher    # standard cipher, default to aes-128-ecb with sha1prng_key. Can NOT sorting, Can NOT searching partly.
   - MysqlAesCipher # It's a subclass of AesCipher with key=mysql_aes_key.
   - S1Cipher     # self-designed, based on MappingCipherBase. `Not suggest to use. Can NOT sorting, CAN searching partly in binary mode, CAN NOT searching partly in hexlify mode`.
   - S2Cipher     # self-designed, based on MappingCipherBase. `Not suggest to use. Can NOT sorting, Can NOT searching partly`.
   - S12Cipher    # self-designed, turn 1 byte data to 2 byte data with random gap. `Not suggest to use. Can sorting, Can NOT searching partly`.
   - IvCipher     # self-designed, trun integer number increase randomly. `Can sorting, Can NOT seaching partly, Number stored in number`.
   - IvfCipher    # self-designed, based on IvCihper, for float number encrypt and decrypt. `Can sorting, Can NOT seaching partly. Number stored in string`.
- dictutils
   - _NULL
   - Object
   - deep_merge
   - select
   - attrgetorset
   - attrset
   - update
   - ignore_none_item   # None, [], {} will be ignored. 0, False, "" and other empty element will keep.
   - to_object
   - fix_object
   - change
   - changes
   - prefix_key
- fsutils
   - mkdir
   - rm
   - filecopy
   - treecopy
   - copy
   - readfile
   - write
   - pathjoin
   - get_temp_workspace
   - rename
   - move
   - file_content_replace
   - touch
   - expand
   - expands
   - first_exists_file
   - get_application_config_filepath
   - load_application_config
   - info # get file info
   - get_size_deviation
   - get_unit_size
   - get_size_display
   - TemporaryFile
- funcutils
   - get_inject_params
   - call_with_inject
   - classproperty
   - get_default_values
   - BunchCallable
- hashutils
   - get_file_md5
   - get_file_sha
   - get_file_sha1
   - get_file_sha224
   - get_file_sha256
   - get_file_sha384
   - get_file_sha512
   - get_md5
   - get_sha
   - get_sha1
   - get_sha224
   - get_sha256
   - get_sha384
   - get_sha512
   - get_md5_base64
   - get_sha_base64
   - get_sha1_base64
   - get_sha224_base64
   - get_sha256_base64
   - get_sha384_base64
   - get_sha512_base64
   - get_pbkdf2_hmac
   - get_pbkdf2_md5
   - get_pbkdf2_sha
   - get_pbkdf2_sha1
   - get_pbkdf2_sha224
   - get_pbkdf2_sha256
   - get_pbkdf2_sha384
   - get_pbkdf2_sha512
   - validate_pbkdf2_hmac
   - validate_pbkdf2_md5
   - validate_pbkdf2_sha
   - validate_pbkdf2_sha1
   - validate_pbkdf2_sha224
   - validate_pbkdf2_sha256
   - validate_pbkdf2_sha384
   - validate_pbkdf2_sha512
- imageutils
   - get_image_bytes
   - get_base64image
   - parse_base64image
   - resize
- jsonutils
   - SimpleJsonEncoder
   - simple_json_dumps
   - register_global_encoder
- listutils
   - int_list_to_bytes # deprecated, see strutils.ints2bytes
   - pad
   - chunk
   - clean_none
   - ignore_none_element # alias of clean_none
   - unique
   - replace
   - append_new
   - group
   - compare
   - first
   - CyclicDependencyError
   - topological_sort
   - topological_test
- logutils
   - setup
- nameutils
   - get_random_name
   - get_last_names
   - get_suggest_first_names
   - last_names_choices # global variable
   - first_names_choices # global variable
- numericutils
   - binary_decompose
   - decimal_change_base
   - get_float_part
   - float_split
- pinyinutils
   - to_pinyin
- randomutils
   - Random
      - random
      - randint
      - get_bytes
      - choice
      - choices
      - shuffle
   - UuidGenerator
      - next
   - uuidgen
   - uuid1
   - uuid3
   - uuid4
   - uuid5
- rsautils
   - newkeys
   - load_private_key
   - load_public_key
   - load_public_key_from_private_key
   - encrypt
   - decrypt
   - export_key
- strutils
   - random_string
   - char_force_to_int
   - force_bytes
   - force_text
   - force_int
   - force_float
   - force_numeric
   - wholestrip
   - split
   - str_composed_by
   - is_str_composed_by_the_choices (alias of str_composed_by)
   - is_hex_digits
   - join_lines
   - is_urlsafeb64_decodable
   - is_base64_decodable
   - is_unhexlifiable
   - text_display_length
   - text_display_shorten
   - smart_get_binary_data
   - is_chinese_character
   - binarify
   - unbinarify
   - ints2bytes
   - int2bytes
   - substrings
   - combinations
   - clean
   - camel
   - format_with_mapping
      - no_mapping
      - none_to_empty_string
   - unquote
   - is_uuid
   - stringlist_append
   - html_element_css_append
   - remove_prefix
   - remove_suffix
   - encodable
   - decodable
- sysutils
   - get_worker_id
   - get_daemon_application_pid
   - get_random_script_name
   - execute_script
- threadutils
   - ServiceBase
   - Service
   - SimpleProducerConsumerServerBase
   - SimpleProducerConsumerServer
- timeutils
   - TimeService
- treeutils
   - build_tree
   - walk_tree
   - print_tree
- typingutils
   - register_global_caster
   - smart_cast
   - cast_uuid
   - cast_numeric
   - cast_dict
   - cast_str
   - cast_bytes
   - cast_list
   - cast_bool
   - cast_float
   - cast_int

## Help

### logutils.setup default logging format

```
logging_config = {
   "version": 1,
   "disable_existing_loggers": False,
   "formatters": {
      "default": {
            "format": "{asctime} {levelname} {pathname} {lineno} {module} {funcName} {process} {thread} {message}",
            "style": "{"
      },
      "message_only": {
            "format": "{message}",
            "style": "{",
      },
      "json": {
            "class": "jsonformatter.JsonFormatter",
            "format": {
               "asctime": "asctime",
               "levelname": "levelname",
               "pathname": "pathname",
               "lineno": "lineno",
               "module": "module",
               "funcName": "funcName",
               "process": "process",
               "thread": "thread",
               "message": "message",
            },
      },
   },
   "handlers": {
      "default_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
      },
      "default_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": logfile,
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "formatter": "default",
      },
      "json_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
      },
      "json_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": logfile,
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "formatter": "json",
      },
   },
   "loggers": {
   },
   "root": {
      "handlers": ["default_file", "default_console"],
      "level": loglevel,
      "propagate": True,
   }
}
```


### Mostly get help by help( ... ) in ipython

*Example*

```
In [9]: from fastutils import strutils

In [10]: help(strutils.random_string)
Help on function random_string in module fastutils.strutils:

random_string(length, choices='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

```

### Some function using *args, **kwargs paramters, see help below.

### cipherutils.IvCipher

*Instance Init Parameters*

- password: required.

### cipherutils.IvfCipher

*Instance Init Parameters*

- password: required.
- result_encoder: default to cipherutils.RawDataEncoder(), choices are: cipherutils.HexlifyEncoder(), cipherutils.Base64Encoder(), cipherutils.SafeBase64Encoder().
- kwargs: dict type.
   - int_digits: default to 12
   - float_digits: default to 4

*Note*

- When float_digits=0, the plain number is treat as integer value.

### cipherutils.AesCipher

*Instance Init Parameters*

- password: required.
- result_encoder: default to cipherutils.RawDataEncoder(), choices are: cipherutils.HexlifyEncoder(), cipherutils.Base64Encoder(), cipherutils.SafeBase64Encoder(), cipherutils.Utf8Encoder(),
- kwargs: dict type.
   - padding: default to cipherutils.aes_padding_pkcs5.
   - key: default to cipherutils.sha1prng_key.
   - mode: default to AES.MODE_ECB (from Crypto.Cipher import AES).

*Example*

```shell
In [1]: from fastutils import cipherutils

In [2]: cipher = cipherutils.AesCipher(password="testpwd", result_encoder=cipherutils.HexlifyEncoder(), kwargs={"key": cipherutils.mysql_aes_key}, force_text=True)
   ...:

In [3]: text1 = "test content"

In [4]: text2 = cipher.encrypt(text1)

In [5]: print(text2)
299aa4e15a40d69e56674a94d9b66cc3

In [6]: text3 = cipher.decrypt(text2)

In [7]: print(text3)
test content

In [8]: text1 == text3
Out[8]: True

In [9]:

```

## Releases

### v0.39.7 2021/03/03

- Fix strutils.force_byte, strutils.force_text.

### v0.39.6 2021/02/25

- Fix encode_datetime problem.

### v0.39.5 2021/02/24

- Add field name while failed to do typing cast.

### v0.39.4 2021/02/24

- Add more default jsonutils encoders.

### v0.39.1 2021/02/21

- Fix logutils.setup default config for windows.

### v0.39.0 2021/02/19

- Change logutils.setup parameter name.
- Fix bizerror.BizError encoding problem in jsonutils.

### v0.38.2 2021/02/10

- Add timeutils.TimeService.

### v0.37.11 2021/01/29

- Fix fsutils.write.

### v0.37.10 2021/01/29

- fsutils.readfile add default params. The default value will be returned if the target file is not exists.
- Add dictutils.diff function.
- Force folder create in fsutils.write.
- Make sure log folder exists in logutils.setup.
- Add sysutils.execute_script.

### v0.37.3 2020/12/28

- Add PyYAML deps in requirements.txt.

### v0.37.2 2020/12/28

- SimpleProducerConsumerServerBase.on_consume_error function add new parameter: task.
- Fix threadutils problems. Many changes are made.

### v0.37.0 2020/11/22

- Add fsutils.load_application_config.

### v0.36.2 2020/11/17

- Add fsutils.TemporaryFile
- Add threadutils.SimpleProducerConsumerServer and fix problems in ServiceCore.

### v0.35.0 2020/11/14

- strutils.is_uuid add allow_bad_characters parameter, default to False. For some old bad application using '815f5ecb-eg07-43af-8de2-87d3898093b5' as UUID.
- Add nameutils.guess_surname.
- Add fsutils.get_size_deviation, fsutils.get_unit_size and fsutils.get_size_display.

### v0.34.0 2020/11/09

- Add sysutils.get_daemon_application_pid.
- Add httputils.

### v0.33.0 2020/11/03

- Add fsutils.info
- Add strutils.encodable and strutils.decodable

### v0.32.0 2020/10/30

- Add funcutils.try_again_on_error.

### v0.31.0 2020/10/30

- Add fsutils.expands.
- Add fsutils.get_application_config_filepath.

### v0.30.1 2020/09/26

- Add cipherutils result_encoders' typing tips.

### v0.30.0 2020/09/23

- Add strutils.stringlist_append.
- Add strutils.html_element_css_append.
- Add strutils.split2.
- Add strutils.remove_prefix.
- Add strutils.remove_suffix.
- Change strutils.split("", [","]) returns [] instead of [""].
- Add cipherutils.MysqlAesCipher.
- Add listutils.topological_sort.
- Add nameutils.

### v0.29.0 2020/09/15

- Use pypinyin module instead of dragonmapper.
   - Replace the result lve to lue.

### v0.28.2 2020/09/04

- Fix dictutils.update, so that it can works on anything.

### v0.28.1 2020/09/02

- Add default parameter to fsutils.first_exists_file.

### v0.28.0 2020/09/02

- Add fsutils.first_exists_file.
- Add fsutils.expand.
- Add listutils.first.

### v0.27.0 2020/08/31

- Add lower_first parameter for strutils.camel.
- Add dictutils.prefix_key.
- Add sysutils.get_worker_id.

### v0.26.0 2020/08/26

- Add treeutils.build_tree from list.
- Add treeutils.walk_tree.
- Add treeutils.print_tree.
- Add fsutils.touch.

### v0.25.0 2020/08/25

- Add strutils.is_uuid.
- Add typingutils.cast_uuid.

### v0.24.2 2020/08/17

- fsutils.file_content_replace add ignore_errors parameter.

### v0.24.1 2020/08/14

- typingutils.cast_xxx treat empty string as None.
- randomutils.UuidGenerator.next add parameter n, so that it can generate n uuids. If n==1, returns a UUID instance, and if n>1, returns a list of UUIDs.

### v0.24.0 2020/08/13

- Add strutils.unquote.

### v0.23.0 2020/08/13

- Add funcutils.get_default_values.
- Add funcutils.chain.

### v0.22.0 2020/08/12

- Add none-dict support in dictutils.change and dictutils.changes.
- Add strutils.format_with_mapping.

### v0.21.0 2020/08/07

- Add listutils.compare(old_set, new_set).
- Add dictutils.change(object_instance, data_dict, object_key, dict_key=None) -> bool.
- Add dictutils.changes(object_instance, data_dict, keys) -> bool:
- Change listutils.replace, turn the default value of parameter inplace from True to False.
- Fix Object instance problems.

### v0.20.0 2020/08/05

- Add strutils.clean and change strutils.camel.
- Add dictutils.to_object.
- Add pinyinutils.


### v0.19.0 2020/07/31

- Add fsutils.filecopy and fsutils.treecopy. Tips: fsutils.copy combines the function of filecopy and treecopy, if the src is a file then use filecopy, and if the src is a folder then use treecopy.
- Fix problem in fsutils.copy.

### v0.18.0 2020/07/31

- Add strutils.camel.

### v0.17.0 2020/07/31

- Add fsutils.file_content_replace.
- Add fsutils.move.
- Change fsutils.rename's behavior.
- Change fsutils.copy's behavior.

### v0.16.0 2020/07/31

- Add fsutils.

### v0.15.2 2020-07-25

- Add hostname, seed1, seed4 in domain_template of randomutils.UuidGenerator.

### v0.15.1 2020-07-24

- Add incr-lock for counter incr in randomutils.UuidGenerator.

### v0.15.0 2020-07-24

- Add randomutils.UuidGenerator.

### v0.14.0 2020-07-16

- Add strutils.substrings.
- Add strutils.combinations.
- Add cipherutils.Utf8Encoder.
- Add cipherutils.S1Cipher.
- Add cipherutils.S2Cipher.
- Add funcutils.classproperty
- WARN: Change a cipherutils.CipherBase's parameter name from encoder to result_encoder.

### v0.13.4 2020-07-11

- Use new algorithm to improve randomutils.shuffle's performance.

### v0.13.3 2020-07-11

- Add randomutils.shuffle.
- Change randomutils.randint parameters from (max, min=0) to (a, b=None).

### v0.13.2 2020-07-10

- Add listutils.group.
- Add rsautils.export_key. And rsautils use Crypto.PublicKey.RSA for the base engine.

### v0.13.1 2020-07-01

- Add strutils.force_float and strutils.force_numeric.
- Add typingutils.cast_numeric support.

### v0.13.0 2020-06-26

- IvfCihper accept integer value when float_digits=0.
- Fix IvfCihper deviation problem which is caused by wrong module used in decrypt.
- IvfCihper use new algorithm in computing module and max_value, **so that result encrypted by version v0.12.0 can not decrypted by version v0.13.0**.

### v0.12.0 2020-06-25

- Add IvfCihper for float number encrypt and decrypt. The output of IvfCipher.encrypt is string.

### v0.11.1 2020-06-23

- Use class instead of raw api for s12 and iv ciphers. It's can avoid many times in generating seeds.

### v0.11.0 2020-06-20

- Add cipherutils.
- Add strutils.binarify and strutils.unbinarify.
- Add randomutils.Random.
- Change aesutils functions' return type. Note: use cipherutils instead.

### v0.10.1 2020-05-19

- Add bizerror dependency.

### v0.10.0 2020-04-23

- Add strutils.is_chinese_character to test if the character is a chinese character.
- Add cacheutils.get_cached_value to get or set cached value.

### v0.9.0 2020-03-05

- Add listutils.append_new to append new value and only new value to the list.

### v0.8.0 2020-01-15

- Add strutils.smart_get_binary_data.
- Add rsautils.

### v0.7.0 2020-01-14

- Add hashutils.get_file_hash.
- Add extra install requires for python 2.x.
- Add imageutils.parse_base64image and imageutils.get_image_bytes.
- Fix jsonutils.make_simple_json_encoder ignore bases problem.

### v0.6.0 2020-01-07

- Add imageutils, add imageutils.get_base64image to make base64 image that can be rendered by web browser.
- Add imageutils.resize to scale image size.
- Add Image-Object-Encode support in jsonutils.
- Add threadutils, add threadutils.Service to simplify long-run-service programming.
- Raise bizerror.MissingParameter error in funcutils.get_inject_params while missing required parameter.

### v0.5.4 2019-12-10

- Fix hashutils.get_hash_hexdigest and hashutils.get_hash_base64 problem.

### v0.5.3 2019-12-08

- Using typingutils.smart_cast in funcutils.get_inject_params.

### v0.5.2 2019-12-08

- Add unit test cases for typingutils.
- Fix cast_list, do strip for every element in comma-separated-list.
- Fix base64 import missing in typingutils.

### v0.5.1 2019-12-08

- Add typingutils.cast_str.

### v0.5.0 2019-12-08

- Set library property in get_encoder in jsonutils.
- Add typingutils.

### v0.4.0 2019.12.07

- Add jsonutils, provides simple json encoder register system.

### v0.3.2 2019.10.29

- Fix problems for python 2.7.
- Fix name error of funcutils.

### v0.3.1 2019.10.28

- Fix problem casued by str.isascii() which is new from python 3.7.

### v0.3.0 2019.09.24

- Add listutils.unique to remove duplicated elements from the list.
- Add listutils.replace to replace element value in thelist with new_value in collection of map.

### v0.2.0 2019.09.10

- Add functuils.get_inject_params to smartly choose parameters from candidates by determine with the function's signature.
- Add functuils.call_with_inject to smartly call the function by smartly choose parameters.

### v0.1.1 2019.08.27

- Add strutils.wholestrip function, use to remove all white spaces in text.
- Fix strutils.is_urlsafeb64_decodable, strutils.is_base64_decodable and strutils.is_unhexlifiable functions, that have problem to test text contains whitespaces.

### v0.1.0 2019.08.23

- Add simple utils about operations of aes, dict, hash, list and str.
