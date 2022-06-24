import base64
from urllib import response
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
import requests as requestx
import requests
import json


from werkzeug import Response
from session import SessionProvider

import io
from PIL import Image


class Gateway:
    name='gateway'
    database = RpcProxy('user_service')
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
        self.session_provider.delete_session(cookie['SESS'])
        response.delete_cookie('SESS')
        return response

    @http('POST', '/upload_files')
    def upload_files(self, request):
        cookie = request.cookies
        if cookie:
            # data = format(request.get_data(as_text=False))
            # tmp = requestx.utils.unquote(data)
            # el = tmp.split('=')
            # tmpname = el[2]
            # elname = tmpname.split('Content-Type: ')
            # filename = elname[0]
            # eltype = elname[1].split('\n')
            # contenttype = eltype[0]
            # #binary = eltype[1].split('\r\n\r\n\x89PNG\r\n\x1a\n')
            # yy = "XXX = " + str(eltype)
            # return yy

            # files = {'file': open('Capture.png','rb')}
            # values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
            # r = requests.post('localhost:8000/upload_files', files=files, data=values)
            # return r

            url = 'localhost:8000/upload_files'
            files = {'file': open('gateway.py', 'rb')}

            r = requests.post(url, files=files)
            return str(r)
        else:
            return "Please login"
