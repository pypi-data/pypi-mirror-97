from time import time
import json
from .ExtException import ExtException, CancelOperation
import asyncio


class Action:
    def __init__(self, name=None, begin=True):
        self.name = name
        self.param = {}
        # self.error = None
        self.result = None
        self.begin = None
        self.end = None
        self.time = 0
        self.total_time = 0
        self.stat = {}
        if begin:
            self.set_begin()

    def set_begin(self):
        self.begin = time()

    def set_end(self, result=None):
        if self.end:
            return self
        self.end = time()
        if not self.begin:
            self.begin = self.end
        self.total_time = round(self.end - self.begin, 3)
        if result is not None:
            self.result = result
        if self.name:
            self.update_stat(self.name, [self.total_time - self.time, 1])
        return self

    def add_stat(self, action):
        if not isinstance(action, Action):
            return action
        for elem in action.stat:
            self.update_stat(elem, action.stat[elem])
        return action.result

    def update_stat(self, name, stat):
        self.time += stat[0]
        if name not in self.stat:
            self.stat[name] = stat
        else:
            self.stat[name][1] += stat[1]
            self.stat[name][0] += stat[0]
        pass

    # def __bool__(self):
    #     return False if self.error else True

    # def __str__(self):
    #     pass

    def to_dict(self):
        return {
            'result': self.result,
            'stat': {
                'action': self.name,
                'time': self.total_time,
                'detail': self.stat
            }
        }

    def dump(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
        pass

    def load(self, json_string):
        _tmp = json.loads(json_string)
        self.name = _tmp.get('name')
        # self.error = _tmp.get('error', None)
        self.result = _tmp.get('result', None)
        self.begin = _tmp.get('begin', None)
        self.end = _tmp.get('end', None)
        self.time = _tmp.get('time', 0)
        self.stat = _tmp.get('stat', {})
        return self

    def ext_exception(self, error, **kwargs):
        kwargs['action'] = kwargs.get('action', self.name)
        kwargs['parent'] = error
        kwargs['skip_traceback'] = 1
        _class = kwargs.get('exception_class', ExtException)
        return _class(**kwargs)


def async_action(f):
    async def wrapper(*args, **kwargs):
        try:
            name = f'{args[0].__name__}.{f.__name__}'
        except Exception:
            try:
                name = f'{args[0].__class__.__name__}.{f.__name__}'
            except Exception:
                name = f.__name__
        action = Action(name)
        try:
            kwargs['_action'] = action
            result = await f(*args, **kwargs)
            result = action.add_stat(result)
            if not isinstance(result, Action):
                return result
            return action.set_end(result)
        except asyncio.CancelledError as err:
            raise action.ext_exception(err, action=name, exception_class=CancelOperation)
        except ExtException as err:
            err = action.ext_exception(err, action=name)
            raise err
        except Exception as err:
            raise action.ext_exception(err, action=name)

    return wrapper


def action(f):
    def wrapper(*args, **kwargs):
        try:
            name = f'{args[0].__name__}.{f.__name__}'
        except Exception:
            try:
                name = f'{args[0].__class__.__name__}.{f.__name__}'
            except Exception:
                name = f.__name__
        action = Action(name)
        try:
            kwargs['_action'] = action
            result = f(*args, **kwargs)
            result = action.add_stat(result)
            if not isinstance(result, Action):
                return result
            return action.set_end(result)
        except ExtException as err:
            raise action.ext_exception(err, action=name)
        except Exception as err:
            raise action.ext_exception(err, action=name)

    return wrapper
