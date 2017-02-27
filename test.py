#!/usr/bin/env python3
#coding:utf-8

import os
from json import dumps
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.options
import tornado.web
from tornado.escape import json_decode
from tornado.options import define, options

define('port', default=8000, help='run on the given port', type=int)

class WelcomeHandler(tornado.web.RequestHandler):
    def get(self):
        print(1)
        self.render(
            "login.html",
        )

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
        )

class LoginHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        data = json_decode(self.request.body)
        user_name = data['user_name']
        password = data['password']
        rst = {
            "code": 0,
        }
        if not user_name or not password:
            self.write(dumps(rst))
            return
        for user_info in self.application.user:
            if user_info['user_name'] == user_name and user_info['password'] == password:
                rst['code'] = 1
                self.write(dumps(rst))
        self.write(dumps(rst))

class RegisterHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        self.write(dumps({"code": 0}))

class GetCarsInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        rst = {
            "code": 1,
            "data": self.application.car
        }
        self.write(dumps(rst))

class GetGPSInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        data = json_decode(self.request.body)
        begin_time = data['begin_time']
        end_time = data['end_time']
        rst = {
            "code": 1,
            "data": []
        }
        print(begin_time)
        print(end_time)
        for x in self.application.gps:
            print (x['time'] + str(x['time'] >= begin_time) + str(x['time'] <= end_time))
            if x['time'] >= begin_time and x['time'] <= end_time:
                rst['data'].append(x)
        if len(rst["data"]):
            rst["code"] = 1
        day=begin_time[0:10].replace("-", "")
        print(day)
        if (len(rst['data']) == 0 and day == "20170220"):
            rst["code"] = 1
            with open('gpsline.txt', 'r') as f:
                while 1:
                    row = f.readline()
                    print(row)
                    if not row:
                        break
                    row = row.split()
                    rst["data"].append({"lng": row[0], "lat": row[1], "id": row[2], "time": row[3] + ' ' + row[4]})
        print(rst['data'])
        self.write(dumps(rst))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", WelcomeHandler),
            (r"/index", MainHandler),
            (r"/api/login", LoginHandler),
            (r"/api/register", RegisterHandler),
            (r"/api/get_cars_info", GetCarsInfoHandler),
            (r"/api/get_gps_info", GetGPSInfoHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            login_url='/login'
        )
        self.user=[]
        self.car=[]
        self.gps=[]
        with open('user.txt', 'r') as f:
            while 1:
                row = f.readline()
                if not row:
                    break
                row = row.split()
                self.user.append({'user_name': row[1], 'password': row[2]})
        with open('car.txt', 'r') as f:
            while 1:
                row = f.readline()
                if not row:
                    break
                row = row.split()
                self.car.append({'id': row[0], 'SN': row[1], 'SelfN': row[2]})
        with open('gps.txt', 'r') as f:
            while 1:
                row = f.readline()
                if not row:
                    break
                row = row.split()
                self.gps.append({'lng': float(row[3]), 'lat': float(row[4]), 'id': row[0], 'time': row[1]+' '+row[2]})
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
