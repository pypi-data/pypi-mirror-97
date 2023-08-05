from Bubot.Core.Obj import Obj
from Bubot.Core.Ocf import find_drivers
from BubotObj.OcfDevice.subtype.Device.Device import Device


class OcfDriver(Obj):
    name = 'OcfDriver'

    async def query(self, **kwargs):
        drivers = find_drivers()
        result = []
        filter = kwargs.get('filter', {})
        for name in drivers:
            try:
                search = filter.get('searchString')
                if search and name.upper().find(search.upper()) < 0:
                    continue
                # if self.drivers[name].get('data') is None:
                driver = Device.init_from_config(class_name=name)
                # self.drivers[name]['handler'] = _device
                driver.set_device_id('')
                result.append(dict(
                    _id=name,
                    name=driver.get_device_name(),
                    links=driver.get_discover_res(),
                    _actions=driver.get_install_actions()
                ))
            except Exception as e:
                pass
        result.sort(key=lambda x: x.get('name'))
        return result

    async def find_by_id(self, _id, **kwargs):
        driver = Device.init_from_config(class_name=_id)
        return {
            "id": _id,
            "links": driver.data,
            "_actions": driver.get_install_actions()
        }

