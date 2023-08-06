import functools
from django.utils.module_loading import import_string as django_import_string
from bluedot_rest_framework.settings import api_settings


def get_dict_value(_dict, keys, default=None):
    # default=None，在key值不存在的情况下，返回None
    keys_list = keys.split('.')
    # 以“.”为间隔，将字符串分裂为多个字符串，其实字符串为字典的键，保存在列表keys_list里
    if isinstance(_dict, dict):
        # 如果传入的数据为字典
        dictionary = dict(_dict)
        # 初始化字典
        for i in keys_list:
            # 按照keys_list顺序循环键值
            try:
                if dictionary.get(i) != None:
                    dict_values = dictionary.get(i)
                # 如果键对应的值不为空，返回对应的值
                elif dictionary.get(i) == None:
                    dict_values = dictionary.get(int(i))
                # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
            except:
                return default
                # 如果字符串型的键转换整数型错误，返回None
            dictionary = dict_values
        return dictionary
    else:
        # 如果传入的数据为非字典
        try:
            dictionary = dict(eval(_dict))
            # 如果传入的字符串数据格式为字典格式，转字典类型，不然返回None
            if isinstance(dictionary, dict):
                for i in keys_list:
                    # 按照keys_list顺序循环键值
                    try:
                        if dictionary.get(i) != None:
                            dict_values = dictionary.get(i)
                        # 如果键对应的值不为空，返回对应的值
                        elif dictionary.get(i) == None:
                            dict_values = dictionary.get(int(i))
                        # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                    except:
                        return default
                        # 如果字符串型的键转换整数型错误，返回None
                    dictionary = dict_values
                return dictionary
        except:
            return default


def import_string(dotted_path):
    keys = dotted_path.split('.')
    settings = getattr(api_settings, keys.pop(0))
    import_str = get_dict_value(settings, '.'.join(keys))
    return django_import_string(import_str)
