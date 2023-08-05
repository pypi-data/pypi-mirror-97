from BubotObj.User.User import User as BaseUser
from Bubot.Helpers.Action import async_action
from Bubot.Helpers.ExtException import ExtException, Unauthorized
from Bubot.Helpers.Helper import ArrayHelper


class User(BaseUser):
    # name = 'User'
    extension = True
    file = __file__

    @classmethod
    async def find_by_cert(cls, storage, cert, create=False):
        data = cert.get_user_data_from_cert()
        self = cls(storage)
        try:
            data = await self.find_by_keys(data['keys'])
            self.init_by_data(data)
        except KeyError:
            if create:
                self.init_by_data(data)
                await self.update()
            else:
                raise KeyError
        return self

    @property
    def db(self):
        return 'AuthService'

    @async_action
    async def add_auth(self, data, **kwargs):
        action = kwargs['_action']
        session = kwargs.get('session', {})
        user_id = session.get('user')
        res = action.add_stat(await self.query(
            filter={'auth.type': data['type'], 'auth.id': data['id']},
            projection={'_id': 1, 'auth': 1},
            limit=1
        ))
        if res:
            raise ExtException('Такой пользователь уже зарегистрирован')
        if user_id:
            try:
                action.add_stat(await self.find_by_id(user_id, projection={'_id': 1, 'auth': 1}))
                action.add_stat(await self.push('auth', data))
            except KeyError:
                session['user'] = None
        else:
            self.data = {
                'title': data['id'],
                'auth': [data]
            }
            res = action.add_stat(await self.update())

    @async_action
    async def find_user_by_auth(self, _type, _id, **kwargs):
        action = kwargs["_action"]
        self.add_projection(kwargs)
        kwargs['projection']['auth'] = True
        res = action.add_stat(await self.query(
            filter={
                'auth.type': _type,
                'auth.id': _id,
            },
            limit=1
        ))
        bad_password = Unauthorized()
        if not res:
            raise bad_password
        i = ArrayHelper.find(res[0]['auth'], _type, 'type')
        if i < 0:
            raise bad_password
        user_data = res[0]
        auth = user_data.pop('auth')
        self.init_by_data(user_data)
        return auth[i]
