# -*- coding: utf-8 -*-
import typing

class _NULL(object):
    pass
_NULL = _NULL()


class Object(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        changed = fix_object(self)

    def __setitem__(self, key, value):
        result = super().__setitem__(key, value)
        self.__dict__[key] = value
        return result

    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, self.__class__):
            value = to_object(value)
        self[name] = value
        result = super().__setattr__(name, value)
        return result

def to_object(data: dict) -> Object:
    result = Object()
    for key, value in data.items():
        if isinstance(value, dict):
            value = to_object(value)
        result[key] = value
        setattr(result, key, value)
    return result

def fix_object(data):
    changed = False
    keys = list(data.keys())
    for key in keys:
        value = data[key]
        if isinstance(value, dict) and not isinstance(value, Object):
            data[key] = to_object(value)
            changed = True
    return changed

def deep_merge(target : dict, data : dict) -> None:
    for key2, value2 in data.items():
        value1 = target.get(key2, None)
        if isinstance(value1, dict) and isinstance(value2, dict):
            deep_merge(value1, value2)
        else:
            target[key2] = value2


def select(data : typing.Union[dict, Object, object], path : str, default_value : typing.Any = None) -> typing.Any:
    paths = path.split(".")
    for path in paths:
        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, (list, tuple)) and path.isdigit() and int(path) < len(data):
            data = data[int(path)]
        elif hasattr(data, path):
            data = getattr(data, path)
        else:
            return default_value
    return data

def touch(data : typing.Union[dict, Object, object], path : str, default_value : typing.Any) -> typing.Any:
    """Make sure data has the path.
    If data has the path, return the orignal value.
    If data NOT has the path, create a new path, and set to default_value, returns the default value.
    """
    result = select(data, path, _NULL)
    if result == _NULL:
        update(data, path, default_value)
        return default_value
    else:
        return result

def attrgetorset(data : typing.Union[dict, Object, object], key : str, default_value : typing.Any) -> typing.Any:
    """Get or set attr to data directly, and the key is a one level key.
    If data contains the key, get the original value.
    If data NOT contains the key, set the key to the default value.
    """
    if isinstance(data, dict):
        if not key in data:
            data[key] = default_value
        return data[key]
    elif isinstance(data, list):
        key = int(key)
        if key >= len(data):
            for _ in range(key + 1 - len(data)):
                data.append(None)
            data[key] = default_value
        return data[key]
    else:
        if not hasattr(data, key):
            setattr(data, key, default_value)
        return getattr(data, key)

def attrset(data : typing.Union[dict, Object, object], key : str, value : typing.Any) -> None:
    """Set attr to data directory, and the key is a one level key.
    If data contains the key, overrdie the original value with the new value.
    If data NOT contains the key, add a new key to the new value.
    """
    if isinstance(data, dict):
        data[key] = value
    elif isinstance(data, list):
        key = int(key)
        if key >= len(data):
            for _ in range(key + 1 - len(data)):
                data.append(None)
        data[key] = value
    else:
        setattr(data, key, value)

def update(data : typing.Union[dict, Object, object], path : str, value : typing.Any) -> typing.Union[dict, Object, object]:
    """Set attr to data, and the key is a dot-seperated-path.
    If data contains the key, override the original value with the new value.
    If data NOT contains the key, add a new key to the new value.
    """
    old_data = data
    is_object = isinstance(data, Object)
    paths = path.split(".")
    for index in range(0, len(paths) - 1):
        path = paths[index]
        path_next = paths[index + 1]
        if path_next.isdigit():
            next_empty_value = []
        else:
            if is_object:
                next_empty_value = Object()
            else:
                next_empty_value = {}
        data = attrgetorset(data, path, next_empty_value)
    path = paths[-1]
    attrset(data, path, value)
    return old_data

def ignore_none_item(data: dict) -> dict:
    result = {}
    for key, value in data.items():
        if value is None:
            continue
        if not value:
            if isinstance(value, (list, dict)):
                continue
        result[key] = value
    return result


def change(object_instance : typing.Union[object, dict], data_dict : typing.Union[object, dict], object_key : str, dict_key : str = None) -> bool:
    """Update property value of object_instance, using the value from data_dict. If value changed, return True. If value is equals, return False.
    """
    dict_key = dict_key or object_key
    if isinstance(object_instance, dict):
        object_value = object_instance.get(object_key, None)
    else:
        object_value = getattr(object_instance, object_key, None)
    if isinstance(data_dict, dict):
        dict_value = data_dict.get(dict_key, None)
    else:
        dict_value = getattr(data_dict, dict_key, None)
    if object_value == dict_value:
        return False
    else:
        if isinstance(object_instance, dict):
            object_instance[object_key] = dict_value
        else:
            setattr(object_instance, object_key, dict_value)
        return True

def changes(object_instance : typing.Union[object, dict], data_dict : typing.Union[object, dict], keys : typing.List[typing.Union[str, typing.Tuple[str, str]]]) -> bool:
    """Update property values of object_instance, using the value form data_dict. If any property changed, return True. If values are equal, return False. keys is a list of string or string pair.
    """
    result = False
    for key in keys:
        if isinstance(key, (tuple, set, list)) and len(key) > 1:
            object_key = key[0]
            dict_key = key[1]
        else:
            object_key = key
            dict_key = None
        changed = change(object_instance, data_dict, object_key, dict_key)
        if changed:
            result = True
    return result

def prefix_key(data, prefix):
    """e.g. {"id": 1, "name": "mktg"} -> {"departmentId": 1, "departmentName": "mktg"}
    """
    data2 = {}
    for key, value in data.items():
        key = prefix + key.capitalize()
        data2[key] = value
    return data2


def diff(object_instance1: dict, object_instance2: dict) -> typing.Tuple[list, list, list]:
    """Find keys that changed. Returns: created_keys, updated_keys, deleted_keys
    """
    deleted_keys = []
    updated_keys = []
    created_keys = []

    keys1 = set(object_instance1.keys())
    keys2 = set(object_instance2.keys())

    deleted_keys = list(keys1 - keys2)
    created_keys = list(keys2 - keys1)
    both_keys = keys1.intersection(keys2)
    for key in both_keys:
        if object_instance1[key] != object_instance2[key]:
            updated_keys.append(key)
    
    return created_keys, updated_keys, deleted_keys
