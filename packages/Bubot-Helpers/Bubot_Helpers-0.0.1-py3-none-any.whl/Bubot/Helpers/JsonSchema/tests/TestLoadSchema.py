import unittest
from Bubot.Helpers.JsonSchema.JsonSchema4 import JsonSchema4


class TestLoadSchema(unittest.TestCase):

    def test_load_schema(self):
        schema = JsonSchema4()

    def test_load_bubot_schema(self):
        dir = ['D:\\project\\bubot3\\bubot_AdminPanel\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_Core\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_Modbus\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_PidController\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_WebServer\\src\\BubotObj\\OcfSchema\\schema']
        rt = ['oic.r.openlevel']
        json_schema = JsonSchema4(dir=dir)
        # try:
        res = json_schema.load_from_rt(rt)
        # except Exception as err:
        #     a = 1
        # pass.

    def test_load_bubot_schema2(self):
        dir = ['D:\\project\\bubot3\\bubot_AdminPanel\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_Core\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_Modbus\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_PidController\\src\\BubotObj\\OcfSchema\\schema', 'D:\\project\\bubot3\\bubot_WebServer\\src\\BubotObj\\OcfSchema\\schema']
        rt = ['oic.r.switch.binary']
        rt = ['bubot.serialserver.con', 'oic.wk.con', 'bubot.con']
        json_schema = JsonSchema4(dir=dir)
        # try:
        res = json_schema.load_from_rt(rt)
        # except Exception as err:
        #     a = 1
        pass