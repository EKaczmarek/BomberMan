import json

import cherrypy
import requests

class UserActivation:
    @cherrypy.expose
    def activate(self, nickname, activation_key):
        url = 'http://localhost:8080/api/users/'
        response = requests.get(url, params={'nickname': nickname})
        if response.ok:
            found_user = json.loads(response.content.decode())
            if found_user[nickname]['activated']:
                return 'Your account has already been activated'
            response = requests.patch(url, data={'nickname': nickname, 'activation_key': activation_key})
            if response.ok:
                return 'Your account has been activated'
        return '{} {}'.format(response.status_code, response.reason)

def main():
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.quickstart(UserActivation(), '/')

if __name__ == '__main__':
    main()