#!/usr/bin/env python3
#coding:utf-8

import os
import pyodbc
from json import dumps
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.options
import tornado.web
from datetime import datetime
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
        print(2)
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
            "id": -1,
        }
        if not user_name or not password:
            self.write(dumps(rst))
            return
        self.application.cursor.execute("SELECT User_Id FROM dbo.UserInfo WHERE  User_Name=? AND User_Pwd=?", user_name, password)
        user_info = self.application.cursor.fetchone()
        if not user_info:
            self.write(dumps(rst))
            return
        rst["code"] = 1
        rst["id"] = user_info.User_Id
        self.write(dumps(rst))

class RegisterHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        self.write(dumps({"code": 0}))

class GetCarsInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        rst = {
            "code": 0,
            "data": []
        }
        self.application.cursor.execute("SELECT CI_ID, CI_SN, CI_SelfN FROM dbo.CarList1")
        while 1:
            row = cursor.fetchone()
            if not row:
                break
            rst["data"].append({"id": row.CI_user_id, "SN": row.CI_SN, "SelfN": row.SelfN})
        if len(rst["data"]):
            rst["code"] = 1
        self.write(dumps(rst))

class GetGPSInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        data = json_decode(self.request.body)
        begin_time = data["begin_time"]
        end_time = data["end_time"]
        rst = {
            "code": 0,
            "data": []
        }
        '''
        if not begin_time or not end_time:
            self.write(dumps(rst))
            return
        '''
        day=begin_time[0:10].replace("-", "")
        if (rst["code"] == 0 and day == "20170220"):
            rst["code"] = 1
            with open('gpsline.txt', 'r') as f:
                while 1:
                    row = f.readline()
                    print(row)
                    if not row:
                        break
                    row = row.split()
                    rst["data"].append({"lng": row[0], "lat": row[1], "id": row[2], "time": row[3] + ' ' + row[4]})
        else:
            self.application.cursor.execute("SELECT MobileID, RecvTime, Longitude, Latitude FROM dbo.GpsLog%s WHERE RecvTime BETWEEN ? AND ?" % (day), begin_time, end_time)
            while 1:
                row = self.application.cursor.fetchone()
                if not row:
                    break
                rst["data"].append({"lng": row.Longitude, "lat": row.Latitude, "id": row.MobileID, "time": row.RecvTime.strftime('%Y-%m-%d %H:%M:%S')})
        if len(rst["data"]):
            rst["code"] = 1
        print(rst["data"])
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
            login_url='/login',
            debug = True
        )
        self.cnxn = pyodbc.connect(r'Driver={SQL Server};Server=PROVERBS-PC\SQLEXPRESS;Database=gps;Trusted_Connection=yes;')
        self.cursor = self.cnxn.cursor()
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()