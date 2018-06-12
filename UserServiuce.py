import hashlib
import random
import string
import cherrypy
import pymongo


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def _generate_activation_key(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


@cherrypy.expose
class UsersService:
    @cherrypy.tools.json_out()
    # get data about activation
    def GET(self, nickname=None):
        with pymongo.MongoClient() as db:
            if nickname:
                players = db.BomberMan.Players.find({'nickname': nickname})
            else:
                players = db.BomberMan.Players.find({})
            if not players.count():
                #raise cherrypy.HTTPError(status=404)
                pass
            keys = ['activated']
            return {p['nickname']: {k: p[k] for k in keys} for p in players}

    @cherrypy.tools.json_in()
    # Replace with auth_basic using "superadmin" credentials
    # (without pushing credentials into the repository)??
    #
    @cherrypy.tools.auth_basic(on=False)
    # user register
    def POST(self):
        data = cherrypy.request.json
        with pymongo.MongoClient() as db:
            players = {p['nickname'] for p in db.BomberMan.Players.find({})}
            if not players.intersection({d['nickname'] for d in data}):
                new_players = [{'nickname': d['nickname'],
                                'email': d['email'],
                                'password': _hash_password(d['password']),
                                'activation_key': _generate_activation_key(8),
                                'activated': False,
                                'statistics_per_game': []} for d in data]
                if new_players:
                    db.BomberMan.Players.insert(new_players)
                cherrypy.response.status = 201
            else:
                raise cherrypy.HTTPError(409)

    # activation account
    def PATCH(self, nickname, activation_key):
        with pymongo.MongoClient() as db:
            if db.BomberMan.Players.find({'nickname': nickname, 'activation_key': activation_key}).count() == 1:
                db.BomberMan.Players.update({'nickname': nickname}, {'$set': {'activated': True}}, upsert=False)
            else:
                raise cherrypy.HTTPError(404)

# db.players.update({'nickname': 'Toreno96'}, {'$push': {'statistic_per_game': {'place': 12, 'bombs_set': 10, 'players_count': 20}}})
#  ranking update
@cherrypy.expose
class RankingService:
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        with pymongo.MongoClient() as db:
            players = {p['nickname'] for p in db.BomberMan.Players.find({})}
            if not {k for k in data.keys()}.difference(players):
                for k, v in data.items():
                    db.BomberMan.Players.update({'nickname': k}, {'$push': {'statistic_per_game': v}}, upsert=False)
                cherrypy.response.status = 201
            else:
                raise cherrypy.HTTPError(404)


def main():
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
    cherrypy.tree.mount(RankingService(), '/ranking/', conf)
    cherrypy.quickstart(UsersService(), '/users/', conf)

if __name__ == '__main__':
    main()
