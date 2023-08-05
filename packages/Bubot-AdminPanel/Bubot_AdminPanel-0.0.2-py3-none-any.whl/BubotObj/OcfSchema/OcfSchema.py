from Bubot.Core.Obj import Obj
from Bubot.Helpers.JsonSchema.JsonSchema4 import JsonSchema4
from Bubot.Core.Ocf import find_schemas
from Bubot.Helpers.Action import async_action, action


class OcfSchema(Obj):
    name = 'OcfSchema'
    schemas_cache = {}
    schemas_dir = []

    async def query(self, **kwargs):
        raise NotImplemented
        # drivers, schemas = Device.find_drivers()
        # result = []
        # for name in drivers:
        #     try:
        #         # if self.drivers[name].get('data') is None:
        #         driver = Device.init_from_config(class_name=name)
        #         # self.drivers[name]['handler'] = _device
        #         result.append(dict(
        #             id=name,
        #             name=name,
        #             links=driver.data,
        #             _actions=driver.get_install_actions()
        #         ))
        #     except Exception as e:
        #         pass
        #
        # return result
        # result = {}
        # cursor = self.client[db][name].find(
        #     filter=kwargs.get('filter', None),
        #     projection=kwargs.get('projection', None),
        #     skip=kwargs.get('skip', 0),
        #     limit=kwargs.get('limit', 0)
        # )
        # sort = kwargs.get('sort')
        # if sort:
        #     cursor.sort(sort)
        # result = await cursor.to_list(length=1000)
        # await cursor.close()

    @async_action
    async def find_by_id(self, _id, **kwargs):
        if not self.schemas_dir:
            self.schemas_dir = find_schemas()
        return self.get_schema_by_rt(_id.split('+'))

    @action
    def get_schema_by_rt(self, rt, **kwargs):
        json_schema = JsonSchema4(cache=self.schemas_cache, dir=self.schemas_dir)
        return json_schema.load_from_rt(rt)
