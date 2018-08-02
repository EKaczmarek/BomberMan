import base64
import distutils
import distutils.util
import hashlib
import os

import cherrypy
import pymongo

from Classes.Management_server import email_sender

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def _generate_activation_key():
    return base64.urlsafe_b64encode(os.urandom(256)).decode()

@cherrypy.expose
class UsersService:
    @cherrypy.tools.json_out()
    def GET(self, nickname=None):
        with pymongo.MongoClient() as db:
            if nickname:
                players = db.bomberman.players.find({'nickname': nickname})
            else:
                players = db.bomberman.players.find({})
            if not players.count():
                raise cherrypy.HTTPError(status=404)
            keys = ['activated']
            return {p['nickname']: {k: p[k] for k in keys} for p in players}

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        with pymongo.MongoClient() as db:
            players = {p['nickname'] for p in db.bomberman.players.find({})}
            if not players.intersection({d['nickname'] for d in data}):
                new_players = [{'nickname': d['nickname'],
                                'email': d['email'],
                                'password': _hash_password(d['password']),
                                'activation_key': _generate_activation_key(),
                                'activated': False,
                                'statistics_per_game': []} for d in data]
                if new_players:
                    db.bomberman.players.insert(new_players)
                for player in new_players:
                    email_sender.send_account_activation_mail(player)
                cherrypy.response.status = 201
            else:
                raise cherrypy.HTTPError(409)

    def PATCH(self, nickname, activation_key):
        with pymongo.MongoClient() as db:
            if db.bomberman.players.find({'nickname': nickname, 'activation_key': activation_key}).count() == 1:
                db.bomberman.players.update({'nickname': nickname}, {'$set': {'activated': True}}, upsert=False)
            else:
                raise cherrypy.HTTPError(404)

def _has_required_statistics(statistics):
    required_statistics = {'players_count', 'place'}
    return {k for k in statistics.keys()}.issuperset(required_statistics)

def _calculate_single_game_score(statistics):
    return int(statistics['players_count'] ** 2 / statistics['place'])

def _calculate_all_games_score(statistics):
    return sum([_calculate_single_game_score(s) for s in statistics])

@cherrypy.expose
class RankingService:
    @cherrypy.tools.json_out()
    def GET(self, nickname=None, scores='false'):
        with pymongo.MongoClient() as db:
            if nickname:
                players = db.bomberman.players.find({'nickname': nickname})
            else:
                players = db.bomberman.players.find({})
            if not players.count():
                raise cherrypy.HTTPError(status=404)
            ranking = {p['nickname']: p['statistics_per_game'] for p in players}
            try:
                if distutils.util.strtobool(scores):
                    ranking = {k: _calculate_all_games_score(v) for k, v in ranking.items()}
            except ValueError:
                raise cherrypy.HTTPError(status=400)
            return ranking

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        with pymongo.MongoClient() as db:
            players = {p['nickname'] for p in db.bomberman.players.find({})}
            if not {k for k in data.keys()}.difference(players):
                for k, v in data.items():
                    if isinstance(v, dict) and _has_required_statistics(v):
                        db.bomberman.players.update({'nickname': k}, {'$push': {'statistics_per_game': v}}, upsert=False)
                    else:
                        raise cherrypy.HTTPError(400)
                cherrypy.response.status = 201
            else:
                raise cherrypy.HTTPError(404)

def main():
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
    cherrypy.tree.mount(RankingService(), '/api/ranking/', conf)
    cherrypy.quickstart(UsersService(), '/api/users/', conf)

if __name__ == '__main__':
    main()