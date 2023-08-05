from Bubot.Core.Obj import Obj


class OcfResource(Obj):
    # name = 'OcfDevice'
    table = 'OcfDevice'

    @property
    def db(self):
        return 'Bubot'

    async def query(self, **kwargs):
        pipeline = [{'$unwind': {'path': '$res'}}]
        projection = {
            '_id': {'$concat': ['ocf://', '$_id', '$res.href']},
            'title': '$res.n',
            'subtitle': '$n',
            'info': {'$concat': ['di:', '$_id', {
                '$reduce': {
                    'input': '$res.rt',
                    'initialValue': ', rt: ',
                    'in': {
                        '$concat': [
                            '$$value',
                            {
                                '$cond': {
                                    'if': {'$eq': ["$$value", ", rt: "]},
                                    'then': "",
                                    'else': ", "
                                }
                            }, '$$this']
                    }
                }
            }]},
            'n': '$n',
            'di': '$_id',
            'href': '$res.href',
            'rt': '$res.rt',
            'ep': 1
        }
        result = await self.storage.pipeline(self.db, self.table, pipeline, projection=projection, **kwargs)
        return result
