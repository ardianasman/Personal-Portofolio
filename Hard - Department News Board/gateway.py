from http import cookies
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

    @http('POST', '/post_news')
    def post_news(self, request):
        cookie = request.cookies
        if cookie:
            data = format(request.get_data(as_text=True))
            tmp = requestx.utils.unquote(data)
            el = tmp.split('=')

            result = self.database.post_news(el[1])
            return result
        else:
            return "Please login"

    @http('POST', '/delete_news/<int:x>')
    def delete_news(self,request, x):
        cookie = request.cookies
        if cookie:
            result = self.database.delete_news(x)
            return result

    @http('POST', '/update_news/<int:x>')
    def update_news(self, request, x):
        cookie = request.cookies
        if cookie:
            data = format(request.get_data(as_text=True))
            tmp = requestx.utils.unquote(data)
            el = tmp.split('=')
            result = self.database.update_news(x, el[1])
            return result

    @http('GET', '/get_all_news')
    def get_all_news(self, request):
        data = self.database.get_all_news()
        return str(data)

    @http('GET', '/get_news/<int:x>')
    def get_news(self,request, x):
        data = self.database.get_news(x)
        return str(data)
