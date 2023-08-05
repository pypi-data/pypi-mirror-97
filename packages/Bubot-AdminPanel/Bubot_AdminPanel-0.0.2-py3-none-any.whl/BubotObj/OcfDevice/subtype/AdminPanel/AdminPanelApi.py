from Bubot.Helpers.Action import async_action, Action
from BubotObj.OcfDevice.subtype.WebServer.ApiHelper import DeviceApi


class AdminPanelApi(DeviceApi):
    @async_action
    async def api_read_navigation(self, view, **kwargs):
        # await view.check_right(account="Bubot", object="OcfDevice", level=10)
        result = {
            'items': [
                {
                    'path': '/OcfDevice/List/',
                    'icon': 'mdi-radio-tower',
                    'title': 'Devices',
                    'props': ''
                },
                {
                    'path': '/OcfResource/List/',
                    'title': 'Resources',
                    'icon': 'mdi-radio-tower',
                    'props': ''
                },
                {
                    'path': '/OcfDriver/List/',
                    'title': 'Drivers',
                    'icon': 'mdi-radio-tower',
                    'props': ''
                }
            ],
            'index': {},
            'default': '/OcfDevice/List'
        }

        return self.response.json_response(result)
