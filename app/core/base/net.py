#!/usr/bin/env python
#
# Copyright 2014 michaelgillette.net
#

"""Base Request Handler

Overrides webapp2s default handler for Module Intelligent handling

"""

__author__ = 'me@michaelgillette.net (Michael Gillette)'

import os
from webapp2 import RequestHandler
from webapp2 import cached_property
from webapp2_extras import jinja2, json
from google.appengine.api import app_identity
from google.appengine.api import modules
from core import config

if config.development:
    module_get_host = modules.get_hostname
else:
    module_get_host = ('{}.%s.appspot.com' % app_identity.get_application_id()).format

class HttpRequest(RequestHandler):
    """Renders a Jinja2 Template to the Response Stream

        Attached to this class is a Jinja2 Environment instance
        cached in the AE App Registry for quick lookups.
    """
    @cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        jinja2.default_config['template_path'] = 'views'
        return jinja2.get_jinja2(app=self.app)
    @cached_property
    def modules(self):
        # Returns a dictionary of Module URLs
        apps = modules.get_modules()
        app_keys = map('{}_host'.format, apps)
        app_urls = map(module_get_host, apps)
        return dict(zip(app_keys, app_urls))
    @cached_property
    def SYSTEM(self):
        return dict(
            VERSION = os.environ['CURRENT_VERSION_ID'],
            DEVSERVER = config.development,
            PRODUCTION = not config.development,
        **self.modules)
    def render_html(self, template, module=None, **kwds):
        # renders a jinja2 template with the provided kwd dict
        # assign a specific module or the current running module
        tmpl = '%s/%s' % (
            module or modules.get_current_module_name(), template
        )
        kwds.update(self.SYSTEM)
        kwds.update({
            'REQUEST': self.request
        })
        html = self.jinja2.render_template(tmpl, **kwds)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)
