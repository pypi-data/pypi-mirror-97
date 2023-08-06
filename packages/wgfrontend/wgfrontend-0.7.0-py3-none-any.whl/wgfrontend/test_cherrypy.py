#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cherrypy
import datetime
import os, os.path
import random
import string


filename_sslcert = '/etc/wgfrontend/server.pem'
filename_sslkey = '/etc/wgfrontend/key.pem'
USERS = {'test': 'test'}

def validate_password(realm, username, password):
    if username in USERS and USERS[username] == password:
       return True
    return False

def check_username_and_password(username, password):
    if username in USERS and USERS[username] == password:
       return
    return 'invalid username/password'
    
def login_screen(from_page='..', username='', error_msg='', **kwargs):
    """Based on https://docs.cherrypy.org/en/latest/_modules/cherrypy/lib/cptools.html"""
    content="""
    <form method="post" action="do_login">
      <div align=center>
        <span class=errormsg>%s</span>
        <table>
          <tr>
            <td>
              Login:
            </td>
            <td>
              <input type="text" name="username" value="%s" size="40" />
            </td>
          <tr>
            <td>
              Password:
            </td>
            <td>
              <input type="password" name="password" size="40" />
              <input type="hidden" name="from_page" value="%s" />
            </td>
          </tr>
          <tr>
            <td colspan=2 align=right>
              <input type="submit" value="Login" />
            </td>
          </tr>
        </table>
      </div>
    </form>
    """ % (error_msg, username, from_page)
    title='Login'
    return ('<html><body>' + content + '</body></html>').encode('utf-8')
    return cherrypy.tools.encode('<html><body>' + content + '</body></html>')

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
                    <head>
                      <link href="/static/css/style.css" rel="stylesheet">
                    </head>
                    <body>
                      <form method="get" action="generate">
                        <input type="text" value="8" name="length" />
                        <button type="submit">Give it now!</button>
                      </form>
                    </body>
                  </html>"""

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def logout(self):
          username = cherrypy.session['username']
          cherrypy.session.clear()
          return '''%s you have been logged out of the system at datetime %s''' % (username, datetime.datetime.now())


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.join(os.path.abspath(os.getcwd()), 'webroot'),
            'tools.session_auth.on': True,
            #'tools.session_auth.on_login': on_login,
            'tools.session_auth.login_screen': login_screen,
            'tools.session_auth.check_username_and_password': check_username_and_password,
#            'tools.encode.on': True,
#            'tools.encode.encoding': 'utf-8',
#            'tools.auth_basic.on': True,
#            'tools.auth_basic.realm': 'Towalink WireGuard User Interface',
#            'tools.auth_basic.checkpassword': validate_password,
#            'tools.auth_basic.accept_charset': 'UTF-8',
            },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        },
        '/favicon.ico':
        {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(os.path.abspath(os.getcwd()), 'webroot', 'static', 'favicon.ico')
        }
    }
    if os.path.exists(filename_sslcert) and os.path.exists(filename_sslkey):
        cherrypy.server.ssl_module = 'builtin'
        cherrypy.server.ssl_certificate = filename_sslcert
        cherrypy.server.ssl_private_key = filename_sslkey
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                           })
    cherrypy.quickstart(StringGenerator(), '/', conf)
