#! /usr/bin/env python3
# coding: utf-8

"""Ce module regroupe les mécanismes de
 gestion des réponses faites par l'utilisateur aux divers menu"""


from ..views.views import (
    ViewPlayer, ViewTournament, ViewBase, ViewRound,
    ViewMatch, ViewReport)


class Menu:
    """Collection de handlers appelés par la facade pour générer
    les Menu"""
    @staticmethod
    def menu_base():
        """Menu racine
        renvoie une ordre à Facade.handle(ordre)"""
        checked = False
        while not checked:
            choice = ViewBase.menu_base()
            if choice == "1":
                checked = True
                return "tournaments_show"
            if choice == "2":
                checked = True
                return "reports"
            if choice == "x":
                checked = True
                return "x"
            if choice == "save":
                checked = True
                return "save", "base_menu"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_tournaments():
        """Menu de gestion des tournois
        renvoie une ordre à Facade.handle(ordre)"""
        checked = False
        while not checked:
            choice = ViewTournament.menu_tournaments()
            if choice == "1":
                checked = True
                return "tournament_create"
            if choice == "2":
                checked = True
                return "tournaments_show"
            if choice == "3":
                checked = True
                return "tournament_select"
            if choice == "0":
                checked = True
                return "base_menu"
            if choice == "save":
                checked = True
                return "save", "tournaments_show"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_tournament(tournament):
        """Menu de gestion d'un tournoi selectionné
        renvoie une ordre à Facade.handle(ordre)"""
        checked = False
        while not checked:
            choice = ViewTournament.menu_tournament(tournament)
            if choice == "0":
                checked = True
                return "tournaments_show"
            if choice == "1":
                checked = True
                return "handle_add_player"
            if choice == "2":
                checked = True
                return "handle_show_players_in_tournament"
            if choice == "3":
                checked = True
                return "tournament_course"
            if choice == "suppr":
                checked = True
                return "tournament_delete"
            if choice == "modif":
                checked = True
                return "tournament_update"
            if choice == "save":
                checked = True
                return "save", "tournament_selected"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_players_in_tournament(tournament):
        """Menu de gestion des joueurs d'un tournoi"""
        checked = False
        while not checked:
            choice = ViewPlayer.menu_players()
            if choice == "1":
                checked = True
                return "handle_add_player"
            if choice == "2":
                checked = True
                return "handle_show_players_in_tournament"
            if choice == "3":
                checked = True
                return "player_select"
            if choice == "0":
                checked = True
                return "tournament_selected"
            if choice == "save":
                checked = True
                return "save", "handle_show_players_in_tournament"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_player_selected(player):
        """Menu de gestion d'un joueur selectionné"""
        checked = False
        while not checked:
            choice = ViewPlayer.menu_player_selected(player)
            if choice == "0":
                checked = True
                return "handle_show_players_in_tournament"
            if choice == "modif":
                checked = True
                return "player_update"
            if choice == "suppr":
                checked = True
                return "player_delete"
            if choice == "save":
                checked = True
                return "save", "player_selected"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_tournament_course(tournament):
        """Menu du déroulement d'un tournoi"""
        checked = False
        while not checked:
            choice = ViewTournament.menu_tournament_course(tournament)
            if choice == "0":
                checked = True
                return "tournament_selected"
            if choice == "1":
                checked = True
                return "tournament_start"
            if choice == "3":
                checked = True
                return "round_select"
            if choice == "save":
                checked = True
                return "save", "tournament_course"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def menu_round(round):
        """Menu sous l'affichage des rounds d'un tournoi"""
        checked = False
        while not checked:
            choice = ViewRound.round_selected(round)
            if choice == "0":
                checked = True
                return "tournament_course"
            if choice == "1":
                checked = True
                return "next_round"
            if choice == "3":
                checked = True
                return "match_select"
            if choice == "save":
                checked = True
                return "save", "round_selected"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def match_selected(match):
        """Menu de gestion d'un tournoi selectionné"""
        checked = False
        while not checked:
            choice = ViewMatch.match_selected(match)
            if choice == "0":
                checked = True
                return "round_selected"
            if choice == "1":
                checked = True
                return "record_match_result"
            if choice == "save":
                checked = True
                return "save", "match_selected"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def record_match_result(match):
        """Menu d'enregistrement du resultat d'un match"""
        checked = False
        while not checked:
            choice = ViewMatch.record_match_result(match)
            if choice == "0":
                checked = True
                return "match_selected"
            if choice == "1":
                checked = True
                return "player1"
            if choice == "2":
                checked = True
                return "player2"
            if choice == "3":
                checked = True
                return "nul"
            if choice == "save":
                checked = True
                return "save", "record_match_result"
            if choice == "load":
                checked = True
                return "load", "tournaments_show"

    @staticmethod
    def reports():
        """Menu racine des rapports"""
        checked = False
        while not checked:
            choice = ViewReport.reports()
            if choice == "1":
                checked = True
                return "reports_players_by"
            if choice == "2":
                checked = True
                return "reports_tournaments"
            if choice == "0":
                checked = True
                return "base_menu"
            if choice == "save":
                checked = True
                return "save", "reports"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_players(players):
        """Menu du rapport des joueurs"""
        checked = False
        while not checked:
            choice = ViewReport.reports_players(players)
            if choice == "1":
                checked = True
                return "reports_players_by", "ranking"
            if choice == "2":
                checked = True
                return "reports_players_by", "alpha"
            if choice == "0":
                checked = True
                return "reports"
            if choice == "save":
                checked = True
                return "save", "reports_players_by"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_tournaments():
        """Menu du rapport des tournois"""
        checked = False
        while not checked:
            choice = ViewReport.reports_tournaments()
            if choice == "0":
                checked = True
                return "reports"
            if choice == "3":
                checked = True
                return "reports_tournament_select"
            if choice == "save":
                checked = True
                return "save", "reports_tournaments"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_tournament(tournament):
        """Menu du rapport d'un tournoi selectionné"""
        checked = False
        while not checked:
            choice = ViewReport.reports_tournament(tournament)
            if choice == "0":
                checked = True
                return "reports_tournaments"
            if choice == "1":
                checked = True
                return "reports_rounds"
            if choice == "2":
                checked = True
                return "reports_matches"
            if choice == "3":
                checked = True
                return "reports_tournament_players_by"
            if choice == "save":
                checked = True
                return "save", "reports_tournament_selected"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_tournament_players_by(players, tournament):
        """Menu du rapport des joueurs d'un tournoi selectionné"""
        print(f"Liste des joueurs du tournoi : {tournament.name}")
        checked = False
        while not checked:
            choice = ViewReport.reports_players(players)
            if choice == "1":
                checked = True
                return "reports_tournament_players_by", "ranking"
            if choice == "2":
                checked = True
                return "reports_tournament_players_by", "alpha"
            if choice == "0":
                checked = True
                return "reports_tournament_selected"
            if choice == "save":
                checked = True
                return "save", "reports_tournament_players_by"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_rounds(tournament):
        """Menu du rapport des rounds d'un tournoi selectionné"""
        checked = False
        while not checked:
            choice = ViewReport.reports_rounds(tournament)
            if choice == "0":
                checked = True
                return "reports_tournament_selected"
            if choice == "save":
                checked = True
                return "save", "reports_rounds"
            if choice == "load":
                checked = True
                return "load", "reports"

    def reports_matches(tournament, matches):
        """Menu du rapport des matches d'un tournoi selectionné"""
        checked = False
        while not checked:
            choice = ViewReport.reports_matches(tournament, matches)
            if choice == "0":
                checked = True
                return "reports_tournament_selected"
            if choice == "save":
                checked = True
                return "save", "reports_matches"
            if choice == "load":
                checked = True
                return "load", "reports"
