from Bubot.Core.Obj import Obj


class OcfDevice(Obj):
    name = 'OcfDevice'

    @property
    def db(self):
        return 'Bubot'

# todo полнотекстовый поиск