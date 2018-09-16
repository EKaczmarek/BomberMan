import signal
import sys
from Classes.Screen_codes.Application_server import Application_server
import requests
from Classes.CONFIG.config_services import services_config
import random
import logging
from PyQt5.QtCore import QTimer

global URL
global AUTH
global SERVER_CONFIG
global SERVICES_URL

SERVICES_URL = 'http://' + str(services_config['IP'] + ':' + str(services_config['port']))
URL = str(SERVICES_URL) + '/api/privileged/game_servers/'
AUTH = requests.auth.HTTPBasicAuth('game_server', 'game_server123')
SERVER_CONFIG = {
    "name": "foo123",
    "ip": "192.168.1.1",
    "port": random.randint(8888, 9999),
    "max_players_count": 20
}

class Terminated(BaseException):
    pass

def clean():
    requests.delete(URL, auth=AUTH, timeout=1, params={'name': SERVER_CONFIG['name']})
    print('Server deleted: {}'.format(SERVER_CONFIG['name']))

def sigint_handler(*args):
    clean()
    raise KeyboardInterrupt

def sigterm_handler(*args):
    clean()
    raise Terminated

if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
    application = Application_server(sys.argv)
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)
    print("Uruchomiono server")
    application.setup()

    new_server = SERVER_CONFIG
    # json file to run main_server.py
    try:
        response = requests.post(URL, auth=AUTH, json=[new_server], timeout=1 )
        if response.ok:
            print("Server created: {}".format(new_server['name']))
            print()
        else:
            print("Server not created")

    except requests.exceptions.RequestException:
        text = "Can't connect to management server"
        #self.error_connection_server_logging.emit(True, text)
        print(text)

    application.server.set_bomb.connect(application.set_bomb_response)
    application.server.game_state.game_over.connect(application.game_over_response)

    print("jifsdfdsf")
    sys.exit(application.exec_())


