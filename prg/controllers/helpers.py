#! /usr/bin/env python3
# coding: utf-8


"""Module regroupant les helpers utilisés pour aléger la facade"""


from prg.controllers.menus import Menu
from ..models.models import Tournament, Match
from ..views.views import (
    Message, ViewPlayer, ViewTournament, ViewRound, ViewMatch)
from . import settings


class TournamentHelper:
    """Collection de handlers appelés par la facade pour tout ce qui
    concerne les tournois. Sert à aléger la façade"""
    @staticmethod
    def tournament_create():
        """Crée un tournoi dans la base de donnée
        à partir d'un formulaire"""
        name, location, date, description, timer = \
            ViewTournament.tournament_create()
        tournament = Tournament(
            name,
            location,
            date,
            description,
            timer,
            settings.DEFAULT_PLAYERS_NUMBER,
            settings.DEFAULT_ROUNDS_NUMBER
            )
        return tournament

    @staticmethod
    def tournament_select(tournaments):
        """Renvoie l'index du tournoi selectionné dans la liste affichée"""
        try:
            index = int(ViewTournament.tournament_select())
            tournaments[index]
        except (IndexError, ValueError):
            Message.input_error()
            return None
        return index

    @staticmethod
    def tournament_update(tournament):
        """Renvoie un tournoi modifié si ses champs sont valides"""
        response = ViewTournament.tournament_update()
        try:
            number = int(response['players_number'])
            if number % 2 != 0:
                response['players_number'] = ""
                Message.max_players()
        except ValueError:
            Message.max_players()
            response['players_number'] = ""
        if response["name"] != "":
            tournament.name = response['name'].strip()
        if response['location'] != "":
            tournament.location = response['location'].strip()
        if response['date'] != "":
            tournament.date = response['date'].strip()
        if response["description"] != "":
            tournament.description =\
                response['description'].strip()
        if response['timer'] != "":
            tournament.timer = response['timer'].strip()
        if response["players_number"] != "" and tournament.status == "à venir":
            tournament\
                .players_number = response['players_number']
        if response["rounds_number"] != "":
            tournament.rounds_number = response['rounds_number']
        return tournament


class PlayerHelper:
    @staticmethod
    def player_select(players):
        """Renvoie l'index du joueur selectionné dans la liste affichée"""
        try:
            index = int(ViewPlayer.player_select())
            players[index]
        except (IndexError, ValueError):
            Message.input_error()
            return None
        return index

    @staticmethod
    def player_update(player):
        """Gère le formulaire de modification d'un joueur,
        renvoie le joueur modifié"""
        response = ViewPlayer.player_create()
        try:
            response["ranking"] = int(response["ranking"])
        except ValueError:
            Message.input_error()
        response["gender"] = response["gender"].upper()
        if response["gender"] not in "MF ":
            response["gender"] = ""
        if response["first_name"] != "":
            player.first_name = response["first_name"]
        if response["last_name"] != "":
            player.last_name = response["last_name"]
        if response["ranking"] != "":
            player.ranking = response["ranking"]
        if response["birth_date"] != "":
            player.birth_date = response["birth_date"]
        if response["gender"] != "":
            player.gender = response["gender"]
        return player


class RoundHelper:
    @staticmethod
    def set_round_one(players):
        """Renvoie la liste de matches pour le premier round"""
        players = sorted(players, key=lambda player: int(player.ranking))

        index_descendant = len(players)-1
        index_montant = 0
        liste1 = []
        liste2 = []
        while index_montant < index_descendant:
            liste1.append(players[index_montant])
            liste2.append(players[index_descendant])
            index_montant += 1
            index_descendant -= 1
        liste2.reverse()

        matches_list = []
        for joueur in liste1:
            index = liste1.index(joueur)
            match = Match(joueur, liste2[index])
            matches_list.append(match)

        return matches_list

    @staticmethod
    def round_select(rounds):
        """Renvoie l'index du round selectionné par l'utilisateur dans
        la liste affichée"""
        try:
            index = int(ViewRound.round_select(rounds))
            rounds[index]
        except (IndexError, ValueError):
            Message.input_error()
            return None
        return index


class MatchHelper:
    @staticmethod
    def match_select(matches):
        """Renvoie l'index du match selectionné par l'utilisateur dans
        la liste affichée"""
        try:
            index = int(ViewMatch.match_select())
            matches[index]
        except (IndexError, ValueError):
            Message.input_error()
            return None
        return index

    @staticmethod
    def record_match_result(match, round):
        """Enregistre le resultat du match"""
        def check_round_played(round):
            """Si tous les matches sont played, alors
            le round est played aussi."""
            not_played = list(filter(
                lambda x: not x.played, round.matches))
            if len(not_played) == 0:
                round.played = True
        response = Menu.record_match_result(match)
        if match.played:
            Message.match_already_played()
            check_round_played(round)
            return "match_selected"
        if response == "match_selected":
            check_round_played(round)
            return "match_selected"
        if response == "player1":
            match.player1.score += 1
            match.winner = "1"
            match.played = True
            check_round_played(round)
            return "match_selected"
        if response == "player2":
            match.player2.score += 1
            match.winner = "2"
            match.played = True
            check_round_played(round)
            return "match_selected"
        if response == "nul":
            match.player1.score += 0.5
            match.player2.score += 0.5
            match.winner = "nul"
            match.played = True
            check_round_played(round)
            return "match_selected"


def trace(match):
    """renvoie la trace d'un match sous forme de string"""
    str_trace = match.player1.id+" VS "+match.player2.id
    return str_trace


def sort_round1(liste):
    """tri la liste de joueurs pour le round 1"""
    liste = sorted(liste, key=lambda player: int(player.ranking))
    return liste


def sort_round2(liste):
    """tri la liste pour les rounds 2 et +
    tri par score, si score égal, tri par classement"""
    liste = sorted(liste, key=lambda player: player.score)
    scores_values = []
    for player in liste:
        if player.score not in scores_values:
            scores_values.append(player.score)
    under_lists = []
    for value in scores_values:
        under_lists.append(
            list(filter(lambda player: player.score == value, liste))
        )
    new_list = []
    for under_list in under_lists:
        under_list = sort_round1(under_list)
        new_list.extend(under_list)

    return new_list
