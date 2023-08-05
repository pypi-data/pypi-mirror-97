import os.path
from BubotObj.OcfDevice.subtype.Device.Device import Device


class AuthService(Device):
    file = __file__
    template = False

    def add_route(self, app):
        path_device = os.path.dirname(self.file)
        # app.router.add_route('*', '/api/auth/{action}', AuthServiceApi)
        app.router.add_static(f'/ui/{self.__class__.__name__}/', f'{path_device}/static/ui')
