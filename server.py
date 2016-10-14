# -*- coding: utf-8 -*-
import os
import sys
import tornado.ioloop
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def render(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.set_header('Cache-Control', 'must-revalidate; max-age=0')
        self.set_header('Access-Control-Allow-Origin', '*')
        super(BaseHandler, self).render(*args, **kwargs)

class MapHandler(BaseHandler):
    def get(self, page="map.html"):
        self.render(page)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", MapHandler),
                (r"/map.html", MapHandler),
            ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__)),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            )
        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    application = Application()
    application.listen(8888)
    print "started server on http://localhost:8888"
    tornado.ioloop.IOLoop.instance().start()
