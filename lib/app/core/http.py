"""Enhanced Web Request Handler
. supports Jinja2
. supports PyJade
. supports JSON response

"""

__author__ = 'me@michaelgillette.net (Michael Gillette)'

import os
import time
from webapp2 import RequestHandler
from webapp2 import get_app, cached_property
from webapp2_extras import jinja2
from google.appengine.api import modules


class Request(RequestHandler):
    """Web Request Handler
    All the spice of life
    """

    @cached_property
    def current_module_name(self):
        return modules.get_current_module_name()

    @cached_property
    def app_modules(self):
        module_list = modules.get_modules()
        config_module_keys = map('{}_host'.format, module_list)
        config_module_urls = map(modules.get_hostname, module_list)
        return dict(
            zip(config_module_keys, config_module_urls)
        )

    @cached_property
    def jinja2(self):
        jinja2.default_config.update({
            'environment_args': {
                'extensions': [
                    'jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'pyjade.ext.jinja.PyJadeExtension'
                ]
            }
        })
        return jinja2.get_jinja2(app=self.app)

    def to_html(self, template_path, **view_data):
        view_data.update(self.app_modules)
        view_data.update({
            'NOCACHE': time.time(),
            'VERSION': os.environ['CURRENT_VERSION_ID'],
            'REQUEST': self.request
        })
        html = self.jinja2.render_template(template_path, **view_data)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)

