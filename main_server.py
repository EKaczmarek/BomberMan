import sys
from Classes.Screen_codes.Application_server import Application_server
import requests
from Classes.CONFIG.config_services import services_config
import random
import logging

if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    application = Application_server(sys.argv)
    print("Uruchomiono server")
    application.setup()

    services_URL = 'http://' + str(services_config['IP'] + ':' + str(services_config['port']))

    new_server = {
        "name": "foo123",
        "ip": "192.168.43.75",
        "port": random.randint(8888, 9999),
        "max_players_count": 20
    }
    # json file to run main_server.py
    try:
        URL = str(services_URL) + '/api/privileged/game_servers/'
        AUTH = requests.auth.HTTPBasicAuth('game_server', 'game_server123')
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


