from BubotObj.OcfResource.OcfResource import OcfResource
from Bubot.Core.DeviceLink import ResourceLink
from Bubot.Core.CatalogObjApi import CatalogObjApi
from BubotObj.OcfDevice.subtype.Device.Device import Device
from Bubot.Helpers.Action import async_action


class OcfResourceApi(CatalogObjApi):
    handler = OcfResource

    def __init__(self, response, **kwargs):
        super().__init__(response, **kwargs)
        self.filter_fields['rt'] = self.filter_rt

    @async_action
    async def api_find_devices(self, view, **kwargs):
        async def notify(message):
            message['percent'] = percent
            await view.notify(message)

        handler, data = await self.prepare_json_request(view)
        items = data['items']
        if items is None:  # ищем все устройства
            items = await handler.query(data['filter'])
        count = len(items)
        devices = []
        for i, item in enumerate(items):
            if count > 2:
                percent = (i + 1) * 100 / count
            else:
                percent = None
            device = Device.init_from_config(class_name=item['id'])
            devices += await device.find_devices(notify=notify)
        # for elem in devices:
        #     new_device = Device.init_from_config(elem)
        #     new_device.save_config()
        #     di = new_device.get_device_id()
        # await view.device.action_add_device({'di': di, 'dmno': device.__class__.__name__})
        # raise Exception('bbbad')
        return self.response.json_response(devices)

    @async_action
    async def api_read(self, view, **kwargs):
        handler, data = await self.prepare_json_request(view)
        res_link = ResourceLink.init_from_link(data)
        result = await res_link.retrieve(view.device)
        return self.response.json_response(result)

    @async_action
    async def api_update(self, view, **kwargs):
        handler, data = await self.prepare_json_request(view)
        res_link = ResourceLink.init_from_link(data)
        result = await view.device.request('update', res_link, data['res'])
        if result.operation == 'changed':
            return self.response.json_response(result.cn)
        else:
            return self.response.json_response(result.cn, status=501)  # todo сделать контроль исключений при случае

    @staticmethod
    def filter_rt(filter, key, filter_value):
        filter['res.rt'] = {'$elemMatch': {'$eq': filter_value}}
