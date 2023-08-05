from BubotObj.OcfDevice.OcfDevice import OcfDevice
from Bubot.Core.CatalogObjApi import CatalogObjApi
from Bubot.Helpers.Action import async_action
from Bubot.Helpers.ExtException import ExtException, KeyNotFound


class OcfDeviceApi(CatalogObjApi):
    handler = OcfDevice

    @async_action
    async def api_discover(self, view, **kwargs):
        handler, data = await self.prepare_json_request(view)
        result = []
        devices = await view.device.discovery_resource()
        await view.notify({'message': f'found {len(devices)}'})
        for _id in devices:
            di = devices[_id].di
            try:
                _device = await handler.find_by_id(di)
            except KeyNotFound:
                _device = devices[_id].to_object_data()

            result.append(_device)

        return self.response.json_response(result)

    @async_action
    async def api_mass_add(self, view, **kwargs):
        action = kwargs['_action']
        handler, data = await self.prepare_json_request(view)
        for device_data in data['items']:
            action.add_stat(await handler.update(device_data))
        return self.response.json_response({})

    @async_action
    async def api_mass_delete(self, view, **kwargs):
        action = kwargs['_action']
        handler, data = await self.prepare_json_request(view)
        for device_data in data['items']:
            action.add_stat(await handler.delete_one(device_data['_id']))
        return self.response.json_response({})
