import asyncio
import inspect
from .ExtException import ExtException, HandlerNotFoundError

import copy
from collections import OrderedDict
from datetime import datetime, timedelta
import json
import os
import re


class Helper:

    @staticmethod
    def get_obj_class(path, obj_name, **kwargs):
        folder_name = f'.{obj_name}' if kwargs.get('folder') else ''
        class_name = obj_name
        suffix = kwargs.get('suffix')
        if suffix:
            class_name += suffix
        full_path = f'{path}{folder_name}.{class_name}.{class_name}'
        try:
            return Helper.get_class(full_path)
        except ExtException as err:
            raise HandlerNotFoundError(detail=f'object {obj_name}', parent=err)

    @staticmethod
    def get_class(class_full_path):
        try:
            parts = class_full_path.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
            return m
        except ImportError as err:
            # ошибки в классе  или нет файла
            raise ExtException(
                'Unable to import object',
                detail=class_full_path,
                action='Helper.get_class',
                parent=err

            )
        except AttributeError as err:
            # Нет такого класса
            # raise AttributeError('get_class({0}: {1})'.format(class_full_path, str(e)))
            raise ExtException(
                'Object not found',
                detail=class_full_path,
                action='Helper.get_class'
            )
        except Exception as err:
            raise ExtException(
                'Unable to import object',
                detail=class_full_path,
                action='Helper.get_class'
            )

    @classmethod
    def loads_exception(cls, data):
        try:
            data = json.loads(data)
            _handler = Helper.get_class(f'{data["__module__"]}.{data["__name__"]}')
            return _handler(**data)
        except ExtException as err:
            return ExtException(data, action='Helper.loads_exception', parent=err)

    @staticmethod
    def convert_ticks_to_datetime(ticks):
        return datetime(1, 1, 1) + timedelta(microseconds=ticks // 10)

    @staticmethod
    def update_dict(*args):
        size = len(args)
        if size == 1:
            return Helper._update_dict({}, args[0])
        elif size > 1:
            result = args[0]
            for i in range(size - 1):
                result = Helper._update_dict(result, args[i + 1])
            return result

    @staticmethod
    def _update_dict(base, new):
        if not new:
            return base
        for element in new:
            try:
                if element in base and base[element] is not None:
                    if isinstance(new[element], dict):
                        base[element] = Helper._update_dict(base[element], new[element])
                    elif isinstance(new[element], list):
                        base[element] = ArrayHelper.unique_extend(base[element], new[element])
                    else:
                        base[element] = new[element]
                else:
                    try:
                        base[element] = copy.deepcopy(new[element])
                    except TypeError as e:
                        if not base:
                            base = {
                                element: copy.deepcopy(new[element])
                            }
                        else:
                            raise Exception('Непредвиденная ситуация при ')
            except ExtException as e:
                try:
                    _elem = '{0}.{1}'.format(element, e.stack[len(e.stack) - 1]['dump']['element'])
                    _msg = e.stack[0]['dump']['message']
                except ExtException:
                    _msg = str(e)
                    _elem = element
                raise ExtException(
                    e,
                    action='Helper.update_dict',
                    detail='{1} - {0}'.format(_msg, _elem),
                    dump={
                        'element': _elem})
            except Exception as e:
                raise ExtException(
                    605,
                    action='Helper.update_dict',
                    detail='{0}({1})'.format(e, element),
                    dump={
                        'element': element,
                        'message': str(e)
                    })
        return base

    @classmethod
    def xml_to_json(cls, elem, array_mode):
        if not array_mode:
            d = OrderedDict()
            for key, value in elem.attrib.items():
                # d.__setitem__(d, "key", value)
                d[key] = value
            elem_text = elem.text
            if elem_text is None:
                d = elem.tag
            else:
                elem_text = elem_text.strip()
                if elem_text:
                    # d.__setitem__(d, "Значение", elem_text)
                    d["Значение"] = elem_text
        else:
            d = []
        array = OrderedDict()
        names_check = {"main": [], "sub": {}}
        for sub_elem in elem:
            this_array = True if sub_elem.find("[@Имя]") else False
            try:
                value = cls.xml_to_json(sub_elem, this_array)
            except Exception as error:
                element = sub_elem.tag + (
                    "." + sub_elem.get('Имя') if this_array else "") + "." + error.detail if hasattr(
                    error, 'detail') else ''
                raise ExtException(error, dump={'element': element})
            if this_array:
                item_name = sub_elem.get('Имя')
                if array_mode:
                    # Проверяем повторение подэлементов при наличии узла Имя, так как все одноименные узлы
                    # с таким атрибутом будут слиты в 1, а по атрибуту "Имя" добавлены как элементы.
                    # Одинаковых атрибутов "Имя" в рамках одноименных узлов быть не должно
                    sub_checked = []
                    if sub_elem.tag in names_check["sub"]:
                        sub_checked = names_check["sub"][sub_elem.tag]
                    if item_name in sub_checked:
                        raise ExtException('Дублирующиеся узлы в xml файле.', dump=sub_elem.tag + "." + item_name)
                    sub_checked.append(item_name)
                    names_check["sub"][sub_elem.tag] = sub_checked
                    if sub_elem.tag not in array:
                        if sub_elem.tag == item_name:
                            array[sub_elem.tag] = value
                        else:
                            array[sub_elem.tag] = OrderedDict()
                        d.append({"Имя": sub_elem.tag, "Значение": array[sub_elem.tag]})
                    if sub_elem.tag != item_name:
                        array[sub_elem.tag][item_name] = value
                else:
                    if sub_elem.tag not in d:
                        d[sub_elem.tag] = OrderedDict()
                    if sub_elem.tag == item_name:
                        d[sub_elem.tag] = value
                    else:
                        d[sub_elem.tag][item_name] = value
            else:
                if array_mode:
                    # Тут просто проверям наличие одноименных узлов без атрибута "Имя".
                    if sub_elem.tag in names_check["main"]:
                        raise ExtException('Дублирующиеся узлы в xml файле.', dump=sub_elem.tag + "." + item_name)
                    names_check["main"].append(sub_elem.tag)
                    if isinstance(value, str):
                        d.append(value)
                    else:
                        value_new = OrderedDict()  # Для порядка Имя-Значение в результате делаем новый результат.
                        value_new["Имя"] = sub_elem.tag
                        value_new.update(value)
                        # for value_key in value.keys():
                        #     value_new[value_key] = value[value_key]
                        d.append(value_new)
                else:
                    d[sub_elem.tag] = value
        return d

    @classmethod
    def update_element_in_dict(cls, _data, _path, _value):
        _num = re.compile('^\d+$')
        _path = _path.split('.')
        current = _data
        size = len(_path)
        for i, elem in enumerate(_path):
            if _num.match(elem):
                elem = int(elem)
            if i == size - 1:
                current[elem] = _value
            else:
                current = current[elem]

    @classmethod
    def compare(cls, base, new):
        def compare_dict(_base, _new):
            pass

        def compare_list(_base, _new):
            pass

        if isinstance(base, dict):
            difference = False
            res = {}
            for elem in new:
                try:
                    if base and elem in base:
                        if isinstance(new[elem], dict):
                            _difference, _res = cls.compare(base[elem], new[elem])
                            if _difference:
                                difference = True
                                res[elem] = copy.deepcopy(_res)
                        else:
                            if new[elem] != base[elem]:
                                difference = True
                                res[elem] = new[elem]
                    else:
                        difference = True
                        res[elem] = new[elem]
                except Exception as e:
                    raise Exception('compare: {0}'.format(str(e)), elem)
        else:
            difference = False
            res = None
            if base != new:
                difference = True
                res = new
        return difference, res

    @classmethod
    def get_default_config(cls, current_class, root_class, cache):
        _type = root_class.__name__
        try:
            return cache['{0}_{1}'.format(_type, cls.__name__)]
        except KeyError:
            pass
        schema = {}

        for elem in current_class.__bases__:
            if issubclass(elem, root_class):
                try:
                    _schema = cache['{0}_{1}'.format(_type, elem.__name__)]
                except KeyError:
                    _schema = cls.get_default_config(elem, root_class, cache)
                    cache['res' + elem.__name__] = Helper.update_dict({}, _schema)
                Helper.update_dict(schema, _schema)
        if hasattr(current_class, 'file'):
            config_path = '{0}/{1}.json'.format(os.path.dirname(current_class.file), current_class.__name__)
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    _schema = json.load(file)
                    Helper.update_dict(schema, _schema)
            except FileNotFoundError:
                return schema
            except Exception as e:
                pass
        cache['{0}_{1}'.format(_type, current_class.__name__)] = Helper.update_dict({}, schema)
        return schema


def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        # kwargs['loop'] = loop
        if inspect.iscoroutinefunction(f):
            future = f(*args, **kwargs)
        else:
            coroutine = asyncio.coroutine(f)
            future = coroutine(*args, **kwargs)
        loop.run_until_complete(future)

    return wrapper


def convert_ticks_to_datetime(ticks):
    return datetime(1, 1, 1) + timedelta(microseconds=ticks // 10)


class ArrayHelper:
    # делаем список уникальных записей, объединяемые массивы должны быть однотипными
    # списки объектов объединаются по ключевому полю которое есть в первой записи списка
    default_object_uid_props = ['_id', 'id', 'di', 'title', 'name', 'n']

    @classmethod
    def unique_extend(cls, a, b, **kwargs):
        if not len(a):
            a.extend(b)
            return a
        if not len(b):
            return a
        if isinstance(a[0], str):
            for elem in b:
                if elem not in a:
                    a.append(elem)
            return a
        if isinstance(a[0], dict):
            object_uid_prop = cls.detect_object_uid_prop(a, kwargs.get('object_uid', cls.default_object_uid_props))
            if object_uid_prop is None:
                c = copy.deepcopy(b)
                a.extend(c)
                return a
            index = cls.index_list(a, object_uid_prop)
            for elem in b:
                uid = elem.get(object_uid_prop)
                if uid not in index:
                    a.append(elem)
        return a


    @classmethod
    def detect_object_uid_prop(cls, data, object_uid_fields):
        for _key in object_uid_fields:
            if _key in data[0]:
                return _key
        return None

    @classmethod
    def update(cls, items, item, field='id'):
        for i in range(len(items)):
            if items[i][field] == item[field]:
                items[i] = item
                return
        items.append(item)

    @classmethod
    def index_list(cls, items, field='id'):
        res = {}
        for index in range(len(items)):
            try:
                res[items[index][field]] = index
            except KeyError:
                pass
        return res

    @classmethod
    def find(cls, items, value, field='id'):
        for i in range(len(items)):
            if items[i][field] == value:
                return i
        return -1
