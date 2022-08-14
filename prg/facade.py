#! /usr/bin/env python3
# coding: utf-8


"""Module central du programme"""


from prg.models.models import Match, Player, Round
from .models.data import Data
from .controllers.helpers import (
    TournamentHelper, PlayerHelper, RoundHelper, MatchHelper,
    trace, sort_round2)
from .controllers.menus import Menu
from .views.views import ViewTournament, ViewPlayer, Message


class Facade:
    """Regroupe la logique interne de l'application.
    Doit rester le plus simple possible, on externalise les traitements
    complexes dans les modules handlers et menus"""
    def __init__(self):
        self.data = Data()
        # les index definissent les objets en cours de selection
        self.index_tournament = None
        self.index_player = None
        self.index_round = None
        self.index_match = None
        self.menu_base()

    def save(self, menu):
        """Sauvegarde les données dans la base de données"""
        self.data.save()
        Message.save()
        self.handle(menu)

    def load(self, menu):
        """charge les données depuis la base de données"""
        self.data.load()
        Message.load()
        self.handle(menu)

    def handle(self, response):
        """Redirige le controlleur suivant la response reçue depuis
        un menu.
        synopsis: self.handle(controlleur())
        """
        actions = {
            "x": exit,
            "tournament_create": self.tournament_create,
            "tournaments_show": self.tournaments_show,
            "tournament_select": self.tournament_select,
            "tournament_selected": self.tournament_selected,
            "tournament_course": self.tournament_course,
            "base_menu": self.menu_base,
            "tournament_delete": self.tournament_delete,
            "tournament_update": self.tournament_update,
            "handle_add_player": self.add_player,
            "handle_show_players_in_tournament":
                self.show_players_in_tournament,
            "player_select": self.player_select,
            "player_selected": self.player_selected,
            "player_delete": self.player_delete,
            "player_update": self.player_update,
            "save": self.save,
            "load": self.load,
            "tournament_start": self.tournament_start,
            "round_select": self.round_select,
            "round_selected": self.round_selected,
            "match_select": self.match_select,
            "match_selected": self.match_selected,
            "record_match_result": self.record_match_result,
            "next_round": self.next_round,
            "reports": self.reports,
            "reports_players_by": self.reports_players_by,
            "reports_tournaments": self.reports_tournaments,
            "reports_tournament_select": self.reports_tournament_select,
            "reports_tournament_selected": self.reports_tournament_selected,
            "reports_rounds": self.reports_rounds,
            "reports_matches": self.reports_matches,
            "reports_tournament_players_by":
                self.reports_tournament_players_by,
        }
        if isinstance(response, tuple):
            actions[response[0]](response[1])
        else:
            actions[response]()

    def menu_base(self):
        """génère le menu de base"""
        self.handle(Menu.menu_base())

    def tournament_create(self):
        """crée un nouveau tournoi et renvoie au menus des tournois"""
        self.data.tournaments.append(TournamentHelper.tournament_create())
        self.tournaments_show()

    def tournaments_show(self):
        """génère l'affichage de tous les tournois"""
        ViewTournament.tournaments_show(self.data.tournaments)
        self.handle(Menu.menu_tournaments())

    def tournament_select(self):
        """systeme de séléction d'un tournoi"""
        index = TournamentHelper.tournament_select(self.data.tournaments)
        if index is not None:
            self.index_tournament = index
            self.tournament_selected()
        else:
            self.tournaments_show()

    def tournament_selected(self):
        """Génère le menu pour le tournoi selectionné"""
        self.handle(Menu.menu_tournament(
            self.data.tournaments[self.index_tournament]))

    def tournament_delete(self):
        """Supprime le tournoi selectionné"""
        self.data.delete_tournament(
            self.data.tournaments[self.index_tournament])
        self.handle("tournaments_show")

    def tournament_update(self):
        """Modifie le tournoi selectionné"""
        self.data.tournaments[self.index_tournament] = \
            TournamentHelper.tournament_update(
                self.data.tournaments[self.index_tournament])
        self.tournament_selected()

    def tournament_course(self):
        self.handle(Menu.menu_tournament_course(
            self.data.tournaments[self.index_tournament]))

    def add_player(self):
        """Ajout d'un joueur au tournoi"""
        max = self.data.tournaments[self.index_tournament].players_number
        if len(
            self.data.tournaments[self.index_tournament].players) >= \
                int(max):
            Message.max_players()
            self.show_players_in_tournament()
        else:
            response = ViewPlayer.player_create()
            try:
                response["ranking"] = int(response["ranking"])
            except ValueError:
                Message.input_error()
                self.tournament_selected()
            response["gender"] = response["gender"].upper().strip()
            if response["gender"] not in "MF ":
                response["gender"] = " "
            player = Player(
                response["first_name"].strip(),
                response["last_name"].strip(),
                response["ranking"],
                response["birth_date"].strip(),
                response["gender"].upper().strip(),
                score=0)
            # ajout de l'id du joueur dans l'objet data
            self.data.tournaments[self.index_tournament].\
                players_ids.append(player.id)
            self.data.tournaments[self.index_tournament].\
                players.append(player)
            self.data.players.append(player)
            self.show_players_in_tournament()

    def show_players_in_tournament(self):
        """Génère l'affichage de tous les joueurs du tournoi selectionné"""
        ViewPlayer.players_show(self.data.tournaments[self.index_tournament])
        self.handle(Menu.menu_players_in_tournament(
            self.data.tournaments[self.index_tournament]))

    def player_select(self):
        """Séléction d'un joueur"""
        index = PlayerHelper.player_select(
            self.data.tournaments[self.index_tournament].players)
        if index is not None:
            self.index_player = index
            self.player_selected()
        else:
            self.show_players_in_tournament()

    def player_selected(self):
        """Affichage du joueur selectionné et menu"""
        self.handle(Menu.menu_player_selected(
            self.data.tournaments[self.index_tournament].
            players[self.index_player]))

    def player_delete(self):
        """Supprime le player selectionné"""
        player = self.data.tournaments[self.index_tournament].\
            players[self.index_player]
        id = str(player.id)
        self.data.tournaments[self.index_tournament].\
            players_ids.remove(id)
        self.data.tournaments[self.index_tournament].\
            players.remove(player)
        self.show_players_in_tournament()

    def player_update(self):
        """Modifie le joueur selectionné"""
        self.data.tournaments[self.index_tournament].\
            players[self.index_player] = \
            PlayerHelper.player_update(
                self.data.tournaments[self.index_tournament].
                players[self.index_player])
        self.player_selected()

    def tournament_start(self):
        """Débute le tournoi s'il na pas encore commencé"""
        if len(self.data.tournaments[self.index_tournament].rounds) < 1:
            self.round_one()
        else:
            round = self.data.tournaments[self.index_tournament].rounds[-1]
            index = self.data.tournaments[self.index_tournament].\
                rounds.index(round)
            self.index_round = index
            self.round_selected()

    def round_one(self):
        """Génère le premier round"""
        tournament = self.data.tournaments[self.index_tournament]
        if len(tournament.players_ids) != int(tournament.players_number):
            Message.max_players()
            self.tournament_course()
        matches = RoundHelper.set_round_one(
            self.data.tournaments[self.index_tournament].players)
        round = Round("1", matches)
        self.data.tournaments[self.index_tournament].rounds.append(round)
        self.data.tournaments[self.index_tournament].\
            rounds_ids.append(round.id)
        self.tournament_course()

    def add_trace(self, match):
        """Ajoute les matches à jouer a tournament.matches_trace"""
        str_trace1 = match.player1.id+" VS "+match.player2.id
        self.data.tournaments[self.index_tournament].\
            matches_trace.append(str_trace1)
        str_trace2 = match.player2.id+" VS "+match.player1.id
        self.data.tournaments[self.index_tournament].\
            matches_trace.append(str_trace2)

    def round2plus(self):
        """Génère la liste des matches pour les rounds suivant le premier"""
        # si une paire de joueurs à déjà joué précédmeent, on essayera
        # de les faire jouer avec les joueurs suivant, mais si eux
        # aussi ont déjà joué ensemble, alors on reste sur la première paire
        index_max = len(self.data.tournaments[self.index_tournament].players)-1
        index = 0
        matches = []
        while index < index_max:
            match_temp1 = Match(
                self.data.tournaments[self.index_tournament].players[index],
                self.data.tournaments[self.index_tournament].players[index+1])
            matches_trace = self.data.tournaments[self.index_tournament].\
                matches_trace
            if trace(match_temp1) in matches_trace and index+4 <= index_max:
                match_temp2 = Match(
                    self.data.tournaments[self.index_tournament].
                    players[index],
                    self.data.tournaments[self.index_tournament].
                    players[index+2])
                if trace(match_temp2) in matches_trace:
                    matches.append(match_temp1)
                    index += 2
                else:
                    match = match_temp2
                    match2 = (
                        self.data.tournaments[self.index_tournament].
                        players[index+1],
                        self.data.tournaments[self.index_tournament].
                        players[index+3])
                    matches.append(match)
                    self.add_trace(match)
                    matches.append(match2)
                    self.add_trace(match2)
                    index += 4
            else:
                matches.append(match_temp1)
                self.add_trace(match_temp1)
                index += 2
        return matches

    def next_round(self):
        """Génère le tour pour les tours suivant le premier"""
        if not self.data.tournaments[self.index_tournament].rounds[-1].played:
            Message.unfinished_round()
            self.round_selected()
        if len(self.data.tournaments[self.index_tournament].rounds) >= \
                int(
                    self.data.tournaments[self.index_tournament].
                    rounds_number):
            Message.finished_tournament()
            self.round_selected()

        self.data.tournaments[self.index_tournament].players = sort_round2(
            self.data.tournaments[self.index_tournament].players
        )
        matches = self.round2plus()
        round_count = len(
            self.data.tournaments[self.index_tournament].rounds_ids)+1
        round = Round(str(round_count), matches)
        self.data.tournaments[self.index_tournament].rounds.append(round)
        self.data.tournaments[self.index_tournament].\
            rounds_ids.append(round.id)
        self.tournament_course()

    def round_select(self):
        """selectionner un round"""
        index = RoundHelper.round_select(
            self.data.tournaments[self.index_tournament].rounds
        )
        if index is not None:
            self.index_round = index
            self.round_selected()
        else:
            self.tournament_course()

    def round_selected(self):
        """Génère le menu pour le round selectionné"""
        self.handle(Menu.menu_round(
            self.data.tournaments[self.index_tournament].
            rounds[self.index_round]))

    def match_select(self):
        """Séléction d'un match"""
        index = MatchHelper.match_select(
            self.data.tournaments[self.index_tournament].
            rounds[self.index_round].matches
            )
        if index is not None:
            self.index_match = index
            self.match_selected()
        else:
            self.tournament_course()

    def match_selected(self):
        match = self.data.tournaments[self.index_tournament].\
            rounds[self.index_round].matches[self.index_match]
        self.handle(Menu.match_selected(match))

    def record_match_result(self):
        round = self.data.tournaments[self.index_tournament].\
            rounds[self.index_round]
        match = self.data.tournaments[self.index_tournament].\
            rounds[self.index_round].matches[self.index_match]
        self.handle(MatchHelper.record_match_result(match, round))

    def reports(self):
        """Affiche le menu racine des rapports"""
        self.handle(Menu.reports())

    def reports_players_by(self, order_by="ranking"):
        """prépare la liste des joueurs trié par ordre alphabétique"""
        players = self.data.get_all_players(order_by)
        self.handle(Menu.reports_players(players))

    def reports_tournaments(self):
        """Affiche une liste indexée de tous les tournois, propose un menu"""
        ViewTournament.tournaments_show(self.data.tournaments)
        self.handle(Menu.reports_tournaments())

    def reports_tournament_select(self):
        """selection d'un tournoi pour ses rapports"""
        index = TournamentHelper.tournament_select(self.data.tournaments)
        if index is not None:
            self.index_tournament = index
            self.reports_tournament_selected()
        else:
            self.reports_tournaments()

    def reports_tournament_selected(self):
        tournament = self.data.tournaments[self.index_tournament]
        self.handle(Menu.reports_tournament(tournament))

    def reports_tournament_players_by(self, order_by="ranking"):
        tournament = self.data.tournaments[self.index_tournament]
        players = self.data.get_players(tournament, order_by)
        self.handle(Menu.reports_tournament_players_by(players, tournament))

    def reports_rounds(self):
        tournament = self.data.tournaments[self.index_tournament]
        self.handle(Menu.reports_rounds(tournament))

    def reports_matches(self):
        tournament = self.data.tournaments[self.index_tournament]
        matches = []
        for round in tournament.rounds:
            for match in round.matches:
                matches.append(match)
        self.handle(Menu.reports_matches(tournament, matches))
