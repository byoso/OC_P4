#! /usr/bin/env python3
# coding: utf-8


"""Module regroupant les models utilisés par le programme """

import uuid


class Tournament:
    """Classe définissant les tournois"""
    def __init__(
        self, name, location, date, description, timer=None,
        players_number=8, rounds_number=4, id=None, matches_trace=None
    ):
        self.name = name
        self.location = location
        self.date = date
        self.description = description
        self.players_number = players_number
        self.rounds_number = rounds_number
        self.players_ids = []
        self.rounds_ids = []
        self.players = []
        self.rounds = []
        if matches_trace:
            self.matches_trace = matches_trace
        else:
            self.matches_trace = []
        self.timer = timer
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        return f"<{self.name}-{self.id}>"

    def serialize(self):
        """Serialize a tournament object"""
        rounds_ids = []
        for round in self.rounds:
            rounds_ids.append(round.id)
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "description": self.description,
            "timer": self.timer,
            "players_number": self.players_number,
            "rounds_number": self.rounds_number,
            "players_ids": self.players_ids,
            "rounds_ids": rounds_ids,
            "matches_trace": self.matches_trace,
        }

    @property
    def status(self):
        """Indique si le tournoi est 'à venir', 'en cours', ou 'terminé'
        """
        if len(self.rounds_ids) == 0:
            status = "à venir"
        elif len(self.rounds_ids) < int(self.rounds_number):
            status = "en cours"
        else:
            status = "terminé"
            for round in self.rounds:
                for match in round.matches:
                    if not match.played:
                        status = "en cours"
                        break
                if status != "terminé":
                    break
        return status


class Player:
    """Classe définissant les joueurs"""
    def __init__(
            self, first_name, last_name, ranking,
            birth_date=None, gender=None, score=0, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.ranking = ranking
        self.score = score
        self.birth_date = birth_date
        self.gender = gender  # M, F, None
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        return f"\n<Player :\
                \nfirst_name: {self.first_name}\
                \nlast_name: {self.last_name}\
                \nranking: {self.ranking}\
                \nscore: {self.score}\
                \nid: {self.id}>"

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        """Serialize a player object"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "ranking": self.ranking,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "score": self.score
        }


class Match:
    """Classe définissant les matches"""
    def __init__(self, player1, player2, played=False, id=None, winner=None):
        self.player1 = player1
        self.player2 = player2
        self.played = played
        self.winner = winner
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        return str(
            f"<match: {self.player1.last_name}"
            f" -VS- {self.player2.last_name}"
            f" - {self.id}>"
        )

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        """Serialize a Match object"""
        return {
            "id": self.id,
            "player1": self.player1.id,
            "player2": self.player2.id,
            "played": self.played,
            "winner": self.winner,
        }


class Round:
    """Classe définissant les rounds"""
    def __init__(self, name="", matches=None, id=None, played=False):
        self.name = name
        self.played = played
        if matches is None:
            self.matches = []
        else:
            self.matches = matches
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        return f"<{self.name} - matches: {len(self.matches)}>"

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        """Serialize a Round object"""
        matches_ids = []
        for match in self.matches:
            matches_ids.append(match.id)
        return {
            "name": self.name,
            "id": self.id,
            "matches_ids": matches_ids,
            "played": self.played,
        }


if __name__ == '__main__':
    print("Veuillez ne pas executer ce module directement")
