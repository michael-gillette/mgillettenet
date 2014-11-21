#!/usr/bin/env python
#
# Copyright 2014 michaelgillette.net
#

"""Personal Website

My chunk of real estate on the internets.

"""

__author__ = 'me@michaelgillette.net (Michael Gillette)'


from webapp2 import WSGIApplication
from core.base import net
from core import config



class Index(net.HttpRequest):
    """Serves a list of 
    """
    def get(self):
        self.render_html('index.tmpl')

wsgi = WSGIApplication([
    ('/', Index)
], debug=config.development)
