from BubotObj.OcfDriver.OcfDriver import OcfDriver
from Bubot.Core.CatalogObjApi import CatalogObjApi
from Bubot.Core.DeviceLink import DeviceLink
from BubotObj.OcfDevice.subtype.Device.Device import Device
from Bubot.Helpers.Action import async_action
from BubotObj.OcfDevice.OcfDevice import OcfDevice
from datetime import datetime
import asyncio


class OcfDriverApi(CatalogObjApi):
    handler = OcfDriver

    @async_action
    async def api_find_devices(self, view, **kwargs):
        async def notify(_data):
            await asyncio.sleep(0.2)
            current = datetime.now()
            if (current - status['time_last_notify']).total_seconds() > 0.5:
                if progress:
                    _data = {
                        'progress': progress + _data.get('progress', 1),
                        'message': f'found {found + _data.get("found", 0)} {_data.get("message", "")}'
                    }
                else:
                    _data = {
                        'progress': _data.get('progress', 1),
                        'message': f'found {_data.get("found", 0)} {_data.get("message", "")}'
                    }

                await view.notify(_data)
                status['time_last_notify'] = current

        action = kwargs['_action']
        handler, data = await self.prepare_json_request(view)
        items = data['items']
        if items is None:  # ищем все устройства
            items = await handler.query(data['filter'])
        count = len(items)
        devices = []
        found = 0
        status = {
            'time_last_notify': datetime.now()
        }
        progress = None
        await view.notify({'message': f'Ищем...'})
        for i, item in enumerate(items):
            if count > 2:
                progress = (i + 1) * 100 * 100 / (count * 100)
            device = Device.init_from_config(item['links'])
            device.coap = view.device.coap
            devices += action.add_stat(await device.find_devices(notify=notify))
            found += len(devices)
        await view.notify({'message': f'Founded {found}'})
        return self.response.json_response(devices)

    @async_action
    async def api_add_devices(self, view, **kwargs):
        handler, data = await self.prepare_json_request(view)
        items = data['items']
        if items is None:  # ищем все устройства
            items = await handler.query(data['filter'])
        for i, item in enumerate(items):
            device = Device.init_from_config(item['links'])
            device.save_config()
            di = device.get_device_id()
            await view.device.action_add_device({
                'di': di,
                'n': device.get_device_name(),
                'dmno': device.__class__.__name__}
            )

            # add device ti db
            device_data = DeviceLink.init_from_device(device).to_object_data()
            ocf_device = OcfDevice(view.storage, account_id=view.session.get('account'))
            await ocf_device.update(device_data)
        return self.response.json_response(data['items'])
