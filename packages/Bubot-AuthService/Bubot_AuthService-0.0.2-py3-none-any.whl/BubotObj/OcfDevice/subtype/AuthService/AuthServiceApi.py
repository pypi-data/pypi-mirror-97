from aiohttp import web
from bson.json_util import dumps
import time
from Bubot.Helpers.ExtException import ExtException, Unauthorized
from Bubot.Helpers.Action import async_action, Action
from base64 import b64encode, b64decode
from aiohttp_session import get_session
# from bubot.Helpers.Сryptography.SignedData import SignedData
import os
import hashlib
from BubotObj.User.User import User
from BubotObj.Session.Session import Session


# from bubot.Catalog.Account.Account import Account

class AuthServiceApi(web.View):
    def __init__(self, request):
        web.View.__init__(self, request)
        self.session = None
        self.storage = request.app['storage']
        self.app = request.app

    async def get(self):
        return await self.request_handler('api_get')

    async def post(self):
        return await self.request_handler('api')

    async def request_handler(self, suffix, **kwargs):
        _action = Action(name='request_handler')
        action = self.request.match_info.get('action')
        handler = f'{suffix}_{action}'
        session = await get_session(self.request)
        session['last_visit'] = time.time()
        if not action or not hasattr(self, handler):
            return web.HTTPNotFound()
        try:
            response = _action.add_stat(await getattr(self, handler)(session=session))
            _action.set_end()
            response.headers['Stat'] = dumps(_action.stat, ensure_ascii=True)
            return response
        except ExtException as err:
            return web.json_response(err.to_dict(), status=err.get_http_code())
        except Exception as err:
            return web.HTTPInternalServerError(text=str(err))

    @async_action
    async def api_auth_by_password(self, **kwargs):
        action = kwargs['_action']
        data = await self.request.post()
        login = data.get('login')
        password = data.get('password')
        user = User(self.storage)
        _auth = action.add_stat(await user.find_user_by_auth('password', login))
        bad_password = Unauthorized()

        _password = b64decode(_auth['password'])
        salt = _password[:32]
        if _auth['id'] != login or _password != self._generate_password_hash(salt, password):
            raise bad_password
        # _session = kwargs['session']
        session = Session(self.storage)
        action.add_stat(await session.create_from_request(user, self))
        return web.json_response({'session': f'{str(user.obj_id)}:{str(session.obj_id)}'})

    @staticmethod
    def _generate_password_hash(salt, password):
        return salt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    @async_action
    async def api_add_password(self, **kwargs):
        action = kwargs['_action']
        data = await self.request.post()
        login = data.get('login')
        password = data.get('password')
        user = User(self.storage)

        salt = os.urandom(32)
        password = b64encode(self._generate_password_hash(salt, password)).decode()

        res = action.add_stat(await user.add_auth({
            'type': 'password',
            'id': login,
            'password': password
        }, **kwargs))
        if res:
            if str(b64encode(password)) == res.get('password'):
                return web.json_response({})

        raise Unauthorized()
