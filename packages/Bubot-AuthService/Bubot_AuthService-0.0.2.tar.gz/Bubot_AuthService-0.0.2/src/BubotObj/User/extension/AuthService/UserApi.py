from aiohttp import web
from bson.json_util import dumps
from Bubot.Helpers.ExtException import ExtException, KeyNotFound, Unauthorized
from Bubot.Helpers.Action import async_action
from base64 import b64encode, b64decode
import os
import hashlib
from BubotObj.User.extension.AuthService.User import User
from BubotObj.User.UserApi import UserApi as BaseUserApi
from BubotObj.Session.Session import Session


class UserApi(BaseUserApi):
    name = "User"
    handler = User
    file = __file__
    extension = True

    @async_action
    async def api_sign_in_by_password(self, view, **kwargs):
        action = kwargs['_action']
        try:
            login = view.data['login']
            password = view.data['password']
        except KeyError as err:
            raise KeyNotFound(detail=err)
        user = User(view.storage, lang=view.lang, form='CurrentUser')
        _auth = action.add_stat(await user.find_user_by_auth('password', login))
        bad_password = Unauthorized()

        _password = b64decode(_auth['password'])
        salt = _password[:32]
        if _auth['id'] != login or _password != self._generate_password_hash(salt, password):
            raise bad_password
        # _session = kwargs['session']
        session = action.add_stat(await Session.create_from_request(user, view))
        action.set_end(self.response.json_response({
            'session': str(session.obj_id),
            'user': user.data
        }))
        return action

    @async_action
    async def api_sign_up_by_password(self, view, **kwargs):
        action = kwargs['_action']
        try:
            login = view.data['login']
            password = view.data['password']
        except KeyError as err:
            raise KeyNotFound(detail=err)

        salt = os.urandom(32)
        password = b64encode(self._generate_password_hash(salt, password)).decode()

        user = User(view.storage, lang=view.lang, form='CurrentUser')
        res = action.add_stat(await user.add_auth({
            'type': 'password',
            'id': login,
            'password': password
        }, **kwargs))
        # if res:
        # if str(b64encode(password)) == res.get('password'):
        session = action.add_stat(await Session.create_from_request(user, view))
        return self.response.json_response({'session': str(session.obj_id)})

    @staticmethod
    def _generate_password_hash(salt, password):
        return salt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    @async_action
    async def api_read_session_info(self, view, **kwargs):
        action = kwargs['_action']
        try:
            user_link = view.session.get('user')
            if not user_link:
                return web.json_response({"session": view.session.identity})
            # user = action.add_stat(self.handler.init_by_ref(user_link, lang=view.lang, form='CurrentUser'))
            user = User(view.storage, lang=view.lang, form='CurrentUser')
            action.add_stat(await user.find_by_link(user_link))
            result = {
                "session": view.session.identity,
                "user": view.session.get('user'),
                "account": view.session.get('account'),
                "accounts": user.data.get('account', [])
            }
            return action.set_end(self.response.json_response(result, dumps=dumps))
            # login = view.data['login']
            # password = view.data['password']
        except KeyError as err:
            raise KeyNotFound(detail=err)

    @async_action
    async def api_sign_out(self, view, **kwargs):
        action = kwargs['_action']
        try:
            session = action.add_stat(await Session.init_from_request(view))
            await session.close()
            view.session.invalidate()
        except KeyError:  # нет сессии
            pass
        # session = await new_session(view.request)
        # session['last_visit'] = time.time()
        return action.set_end(self.response.json_response({}))

    # def _get_session_response(self, session, user):
