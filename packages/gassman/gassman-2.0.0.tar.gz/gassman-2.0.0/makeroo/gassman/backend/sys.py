from .web import JsonBaseHandler

from ...pkgutils import package_version


class SysVersionHandler (JsonBaseHandler):
    def post(self):
        data = [package_version('gassman')]

        self.write_response(data)
