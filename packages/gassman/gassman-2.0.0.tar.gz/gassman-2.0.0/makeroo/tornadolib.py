from typing import Optional
from os.path import join
import pkg_resources

from tornado.template import BaseLoader, Template


class PackagedTemplateLoader (BaseLoader):
    def __init__(self, basename: str, folder: str = 'tornado_templates', *args, **kwargs):
        super(PackagedTemplateLoader, self).__init__(*args, **kwargs)
        self.basename = basename
        self.folder = folder

    def resolve_path(self, name: str, parent_path: Optional[str] = None):
        p = self.folder

        if parent_path is not None:
            p = join(p, parent_path)

        return join(p, name)

    def _create_template(self, name):
        template = Template(
            pkg_resources.resource_string(self.basename, name),
            name=name,
            loader=self,
        )

        return template
