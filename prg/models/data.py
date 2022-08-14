#! /usr/bin/env python3
# coding: utf-8


"""Ce module contient uniquement la classe Data"""


from tinydb import TinyDB

from .models import Tournament, Player, Round, Match


class Data:
    """Cette classe gère les données de l'application, ainsi que les
    échanges (save/load) avec la base de donnée"""
    def __init__(self):
        self.db = TinyDB('db.json')
        self.players = []
        self.rounds = []
        self.tournaments = []

    def save(self):
        """Sauvegarde les valeurs de l'objet data dans la base de donées"""
        self.db.drop_table('tournaments')
        self.db.drop_table('players')
        self.db.drop_table('rounds')
        self.db.drop_table('matches')
        for tournament in self.tournaments:
            self.db.table("tournaments").insert(tournament.serialize())
            for player in tournament.players:
                self.db.table("players").insert(player.serialize())
            for round in tournament.rounds:
                self.db.table("rounds").insert(round.serialize())
                for match in round.matches:
                    self.db.table("matches").insert(match.serialize())

    def load(self):
        """Crée l'objet data à partir des données de la base de données"""
        # chargement des joueurs
        players_doc = self.db.table("players")
        players_list = []
        for player_doc in players_doc:
            player = Player(
                player_doc['first_name'],
                player_doc['last_name'],
                player_doc['ranking'],
                player_doc['birth_date'],
                player_doc['gender'],
                player_doc['score'],
                player_doc['id'],
                )
            players_list.append(player)
        self.players = players_list

        # chargement des rounds
        rounds_doc = self.db.table("rounds")
        rounds_list = []
        for round_doc in rounds_doc:
            round = Round(
                round_doc["name"],
                None,
                round_doc["id"],
            )
            round.matches_ids = round_doc["matches_ids"]
            round.played = round_doc["played"]
            round.matches = self.load_matches(round.matches_ids)
            rounds_list.append(round)
        self.rounds = rounds_list

        # chargement des tournois
        tournaments_doc = self.db.table("tournaments")
        tournaments_list = []
        for tournament_doc in tournaments_doc:
            tournament = Tournament(
                tournament_doc['name'],
                tournament_doc['location'],
                tournament_doc['date'],
                tournament_doc['description'],
                tournament_doc['timer'],
                tournament_doc['players_number'],
                tournament_doc['rounds_number'],
                tournament_doc['id'],
                tournament_doc['matches_trace'],
                )
            tournament.players_ids = tournament_doc['players_ids']
            tournament.rounds_ids = tournament_doc['rounds_ids']
            tournament.players = self.load_players(tournament.players_ids)
            tournament.rounds = self.load_rounds(tournament.rounds_ids)
            tournaments_list.append(tournament)
        self.tournaments = tournaments_list

    def load_players(self, ids_list):
        """Renvoie une liste de joueurs dont l'id est dans ids_list"""
        players_list = []
        for player in self.players:
            if str(player.id) in ids_list:
                players_list.append(player)
        return players_list

    def get_object(self, liste, id):
        """Renvoie un objet d'une liste d'objets grâce à son id"""
        filtered = list(filter(lambda x: x.id == id, liste))
        return filtered[0]

    def load_rounds(self, ids_list):
        """Construit une liste de tours à partir d'une liste d'ids"""
        rounds_list = []
        for round in self.rounds:
            if str(round.id) in ids_list:
                rounds_list.append(round)
        return rounds_list

    def load_matches(self, ids_list):
        """Renvoie une liste de matches depuis la BD si dans la liste"""
        matches_doc = self.db.table("matches")
        matches_list = []
        for match_doc in matches_doc:
            if match_doc["id"] in ids_list:
                match = Match(
                    self.get_object(self.players, match_doc["player1"]),
                    self.get_object(self.players, match_doc["player2"]),
                    match_doc["played"],
                    match_doc["id"],
                    match_doc["winner"],
                )
                matches_list.append(match)
        return matches_list

    def delete_tournament(self, tournament):
        """Efface le tournoi donné en parametre"""
        self.tournaments.remove(tournament)

    def get_all_players(self, order_by="ranking"):
        """renvoie une liste triée de tous les joueurs"""
        players = []
        for tournament in self.tournaments:
            for player in tournament.players:
                players.append(player)
        if order_by == "ranking":
            players = sorted(players, key=lambda p: p.ranking)
        if order_by == "alpha":
            players = sorted(players, key=lambda p: p.last_name)
        return players

    def get_players(self, tournament, order_by="ranking"):
        """Renvoie la liste triée des joueurs d'un tournoi"""
        players = []
        all_players = self.get_all_players()
        players = list(filter(
            lambda p: p.id in tournament.players_ids, all_players))
        if order_by == "ranking":
            players = sorted(players, key=lambda p: p.ranking)
        if order_by == "alpha":
            players = sorted(players, key=lambda p: p.last_name)
        return players
