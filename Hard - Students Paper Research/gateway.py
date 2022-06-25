from http import cookies
import os
from pathlib import Path
from unittest import result
from urllib import response
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from redis import ResponseError
import requests as requestx

import json

from werkzeug.wrappers import Response
from session import SessionProvider

class Gateway:
    name = 'gateway'
    database = RpcProxy('service')
    session_provider = SessionProvider()

    @http('GET', '/check')
    def check(self, request):
        cookie = request.cookies
        return Response(cookie['SESS'])

    @http('POST', '/register')
    def register(self,request):
        data = request.get_data(as_text=True)
        arr= data.split('&')
        username=''
        password=''
        for i in arr:
            el = i.split('=')
            if(el[0] == 'username'):
                username=el[1]
            elif(el[0] == 'password'):
                password = el[1]
        msg = str(self.database.register(username,password))
        return Response(msg)

    @http('GET', '/login')
    def login(self,request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = '' 
        password = '' 
        for i in arr:
            el = i.split("=")
            if(el[0] == "username"):
                username = el[1]
            elif(el[0] == "password"):
                password = el[1]
            
        z = self.database.login(username,password)
            
        if(z==1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESS', session_id)
            return response
        else:
            return json.dumps("Username/pass salah")
    
    @http('POST', '/logout')
    def logout(self,request):
        cookie = request.cookies
        if cookie:
            acc = self.session_provider.delete_session(cookie['SESS'])

            if acc:
                response = Response("Logged out")
                response.delete_cookie('SESS')
            else:
                response = Response("Logout failed")
                return response
        else:
            response = Response("Please login")
            return response

    @http('POST', '/upload_files')
    def upload_files(self, request):
        cookie = request.cookies
        if cookie:
            path = Path('Files')
            if(path.exists()):
                for file in request.files.items():
                    _, files = file
                    files.save(f"{path}/{files.filename}")
                return "Success"
            else:
                os.makedirs(path)
                for file in request.files.items():
                    _, files = file
                    files.save(f"{path}/{files.filename}")
                return "Success"
            
        else:
            return "Please login"
    
    @http('GET', '/download_file/<string:x>')
    def download_file(self, request, x):
        cookie = request.cookies
        if cookie:
            path = Path('Files/'+x)
            if(path.exists()):
                if(open(f"{path}", "rb").read()):
                    return Response(open(f"{path}", "rb").read())
                else:
                    return "No file exists with that name"

                
        else:
            return "Please login"