#! /usr/bin/env python3
# coding: utf-8

"""Ce module views regroupe tous les affichages du programme"""

from ..controllers import settings


def print_tournament(tournament, index):
    """Formate l'affichage d'une ligne
    de tournoi"""
    players_count = (
        f" {len(tournament.players_ids)}/"
        f"{tournament.players_number}")
    print(
        f"{index:<10}"
        f"{tournament.name:<30}"
        f"{tournament.location:<25}"
        f"{tournament.date:<15}"
        f"{players_count:<10}"
        f"{tournament.status:<10}"
        )


def print_match(match, index):
    """Formate l'affichage d'une ligne
    de match"""
    joueur1 = (
        f"{match.player1.first_name} {match.player1.last_name}"
        f" (classé {match.player1.ranking})")
    joueur2 = (
        f"{match.player2.first_name} {match.player2.last_name}"
        f" (classé {match.player2.ranking})")
    played = "non joué"
    if match.played:
        played = "joué"

    print(
        f"{index:<10}"
        f"{joueur1:<40}"
        "- Vs -"
        f"{joueur2:>40}"
        f" {played:<10}"
    )


def print_player(player, index):
    """Formate l'affichage d'une ligne
    de joueur"""
    print(
        f"{index:<10}"
        f"{player.first_name:<30}"
        f"{player.last_name:<30}"
        f"{player.ranking:^11}"
        f"{player.score:^10}"
    )


class Message:
    """Collection de messages"""
    @staticmethod
    def save():
        """Message affiché après une sauvegarde"""
        print(" _"*50)
        print("\n! Données sauvegardées !")

    @staticmethod
    def load():
        """Message affiché après un chargement"""
        print(" _"*50)
        print("\n! Données chargées !")

    @staticmethod
    def input_error():
        """Message affiché après une saisie incorrecte"""
        print(" _"*50)
        print("\n! Votre saisie est incorrecte !")

    @staticmethod
    def max_players():
        """Message affiché si l'utilisateur ne respecte pas le nombre de
        joueurs déterminé pour le tournoi"""
        print(" _"*50)
        print("\n! Vérifiez le nombre de joueurs requis pour ce tournoi !")

    @staticmethod
    def match_already_played():
        """Message affiché si l'utilisateur tente de modifier un match
        qui a déjà eu lieu"""
        print(" _"*50)
        print("\nLe match à déjà été joué, il ne peut pas être modifié.")

    @staticmethod
    def unfinished_round():
        """Message affiché si l'utilisateur tente de commencer un nouveau
        tour alors qu'un tour est encore en jeu"""
        print(" _"*50)
        print(
            "\nUn tour est encore en cours de jeu, "
            "il doit être terminé pour commencer le prochain."
        )

    @staticmethod
    def finished_tournament():
        """Message affiché si l'utilisateur tente de continuer à jouer
        un tournoi terminé"""
        print(" _"*50)
        print(
            "Ce tournoi est terminé ! consultez la liste des joueurs pour "
            "connaitre les scores.")


class ViewBase:
    """Contient les vues de base de l'application"""
    @staticmethod
    def menu_base():
        """Affiche la page initiale"""
        print("\n=== Chess Tournament Manager ===")
        print(
            "1: gérer les tournois"
            " | 2: voir les rapports"
            " | x: quitter"
            "\nsave: sauvegarder"
            " | load: charger"
        )
        choice = input("?> ")
        return choice


class ViewTournament:
    """classe regroupant les vues concernant les tournois"""

    @staticmethod
    def menu_tournaments():
        """Affiche la page de gestion des tournois"""
        print("\n== Gestion des tournois ==")
        print(
            "1: créer un nouveau tournoi"
            " | 3: selectionner un tournoi"
            " | 0: retour"
            "\nsave: sauvegarder"
            " | load: charger"
        )
        choice = input("?> ")
        return choice

    @staticmethod
    def tournament_create():
        """Affiche le formulaire de création d'un tournoi"""
        name = input("nom du tournoi ?> ")
        location = input("lieu du tournoi ?> ")
        date = input("date du tournoi ?> ")
        description = input("description ?> ")
        timer = input("temps : 1:bullet | 2:blitz | 3:coup rapide ?> ")
        return name, location, date, description, timer

    @staticmethod
    def tournament_update():
        """Affiche le formulaire de modification d'un tournoi"""
        response = {}
        response["name"] = input("nom du tournoi ?> ")
        response["location"] = input("lieu du tournoi ?> ")
        response["date"] = input("date du tournoi ?> ")
        response["description"] = input("description ?> ")
        response["timer"] = input(
            "temps : 1:bullet | 2:blitz "
            "| 3:coup rapide ?> ")
        response["players_number"] = input("nombre de joueurs ?>")
        response["rounds_number"] = input("nombre de tours ?>")
        return response

    @staticmethod
    def tournaments_show(tournaments_list):
        """Affiche la page qui liste les tournoi en mode gestion"""
        print("\n=== Liste des tournois ===")
        print(
            f"{'index':<10}{'Tournois':<30}{'Lieu':<25}"
            f"{'date':15}{'joueurs':10}{'status':10}")
        print("_"*100)
        for tournament in tournaments_list:
            print_tournament(tournament, tournaments_list.index(tournament))
        print("\n")

    @staticmethod
    def tournament_select():
        """Affiche le formulaire de selection d'un tournoi"""
        print("\n=== selectionnez un tournoi avec son index :")
        tournoi_id = input("?> ")
        return tournoi_id

    @staticmethod
    def tournament_show(tournament):
        """Affiche la page de gestion d'un tournoi selectionné,
        sans le menu"""
        date = tournament.date
        location = tournament.location
        players = (
            f"{str(len(tournament.players_ids))}/"
            f"{tournament.players_number}")
        rounds = (f"{len(tournament.rounds)}/{tournament.rounds_number}")
        print(
            f"\n== Tournoi selectionné: '{tournament.name}' =="
            f"\n Description: {tournament.description}\n"
            )
        if tournament.timer == "1":
            temps = "bullet"
        elif tournament.timer == "2":
            temps = "blitz"
        elif tournament.timer == "3":
            temps = "coup rapide"
        else:
            temps = "/"
        print(
            f"{'Date':<30}{'Lieu':<30}{'Joueurs':^10}"
            f"{'Tours':^10}{'temps':^20}")
        print("_"*100)
        print(f"{date:<30}{location:<30}{players:^10}{rounds:^10}{temps:^20}")

    @staticmethod
    def menu_tournament(tournament):
        """Affiche le menu de la page de gestion d'un tournoi selectionné"""
        ViewTournament.tournament_show(tournament)
        print(
            "\n1: Ajouter un joueur"
            " | 2: voir les joueurs"
            " | 3: déroulement du tournoi"
            "\nsuppr: supprimer ce tournoi"
            " | modif: modifier ce tournoi"
            " | 0: retour"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def menu_tournament_course(tournament):
        """Affiche la page de déroulement d'un tournoi selectionné"""
        print(f"\n== déroulement du tournoi '{tournament.name}'")
        print(
            f"Tours: {len(tournament.rounds)}/"
            f"{tournament.rounds_number}"
            f" Joueurs: {len(tournament.players_ids)}/"
            f"{tournament.players_number}"
        )
        if len(tournament.players_ids) == int(tournament.players_number)\
                and len(tournament.rounds) == 0:
            print("Le tournoi est prêt à étre joué\n")
        elif len(tournament.rounds) > 0:
            print("Le tournoi est en cours de jeu\n")
            print(f"{'index':<10}{'tour':<30}{'status':<20}")
            print("_"*60)
            for round in tournament.rounds:
                if round.played:
                    status = "terminé"
                else:
                    status = "en cours"
                name = settings.ROUND_BASE_NAME+round.name
                index = tournament.rounds.index(round)
                print(f"{index:<10}{name:<30}{status:<20}")
        else:
            nombre = int(tournament.players_number) -\
                 len(tournament.players_ids)
            print(
                f"\nIl manque {nombre} joueurs"
                f" pour pouvoir jouer le tournoi.")
        print(
            "\n0: retour"
            " | 1: Jouer le tournoi"
            " | 3: selectionner un tour"
            "\nsave: sauvegarder"
            " | load: charger"
        )
        choice = input("?> ")
        return choice


class ViewPlayer:
    """Regroupe les vues de gestion des joueurs"""
    @staticmethod
    def menu_players():
        """Affiche le menu de gestion des joueurs d'un tournoi selectionné"""
        print(
            "\n1: créer un nouveau joueur"
            " | 2: voir les joueurs"
            " | 3: selectionner un joueur"
            " | 0: retour"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def menu_player_selected(player):
        """Affiche le menu de gestion d'un joueur selectionné"""
        score = player.score
        ranking = player.ranking
        gender = player.gender
        birth_date = player.birth_date
        print(
            f"\n== Joueur séléctionné: "
            f"{player.first_name} {player.last_name}")
        print(
            f"{'classement':<15}{'score':^20}{'genre':^10}"
            f"{'date de naissance':^20}")
        print("_"*65)
        print(f"{ranking:<15}{score:^20}{gender:^10}{birth_date:^20}")
        print(
            "\nmodif: modifier"
            " | suppr: supprimer"
            " | 0: retour"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def player_create():
        """Affiche le formulaire de création d'un joueur"""
        response = {}
        response["last_name"] = input("Nom ?> ")
        response["first_name"] = input("Prenom ?> ")
        response["ranking"] = input("Classement ?> ")
        response["birth_date"] = input("Date de naissance ?> ")
        response["gender"] = input("sexe (M/F)?> ")
        return response

    @staticmethod
    def players_show(tournament):
        """Affiche la liste des joueurs d'un tournoi selectionné"""
        players = tournament.players
        tournament.players = sorted(players, key=lambda player: -player.score)
        print(
            f"\n=== Liste des joueurs de {tournament.name} "
            f"({len(tournament.players)}/{tournament.players_number}) ==="
            )
        print(
            f"{'index':<10}"
            f"{'Joueurs':<60}"
            f"{'Classement':^11}"
            f"{'score':^10}"
        )
        print("_"*91)
        for player in tournament.players:
            print_player(player, tournament.players.index(player))
        print("\n")

    @staticmethod
    def player_select():
        """Affiche le formulaire de selection d'un joueur"""
        print("\n=== selectionnez un joueur avec son index :")
        player_index = input("?> ")
        return player_index


class ViewRound:
    """Regroupe les vues concernant les tours"""
    @staticmethod
    def round_select(rounds):
        """Affiche le formulaire de selection d'un tour"""
        print("\n=== Selectionnez un tour avec son index :")
        round_index = input("?> ")
        return round_index

    @staticmethod
    def round_selected(round):
        """Affiche la page d'un tour selectionné"""
        if round.played:
            status = "(terminé)"
        else:
            status = "(en cours)"
        print(
            f"\n=== Tour selectionné : "
            f"{settings.ROUND_BASE_NAME+round.name}"
            f" {status}"
            "\nListe des matches :\n"
        )

        print(
            f"{'index':<10}{'Joueur1':<30} - VS - {'Joueur2':>30}"
            f" {'Vainqueur':>30}")
        print(f"{'_'*109}")
        for match in round.matches:
            if match.winner:
                winner = match.winner
            else:
                winner = "non joué"
            index = round.matches.index(match)
            player1 = f"{match.player1.first_name} {match.player1.last_name}"
            player2 = f"{match.player2.first_name} {match.player2.last_name}"
            print(
                f"{index:<10}{player1:<30} - VS - {player2:>30}"
                f" {winner:>30}")

        print(
            "\n0: retour"
            " | 1: prochain tour"
            " | 3: selectionner un match"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice


class ViewMatch:
    """Regroupe les vues concernant les matches"""
    @staticmethod
    def match_select():
        """Affiche le formulaire de selection d'un match"""
        print("\n=== selectionnez un match avec son index :")
        match_index = int(input("?> "))
        return match_index

    @staticmethod
    def match_selected(match):
        """Affiche la page de gestion d'un match selectionné"""
        print("\n=== Match séléctionné :")
        player1 = f"{match.player1.first_name} {match.player1.last_name}"
        player2 = f"{match.player2.first_name} {match.player2.last_name}"
        if match.winner:
            winner = match.winner
        else:
            winner = "non joué"

        print(
            f"{'Joueur 1': <30}{'':^8}{'Joueur 2':>30}"
            f"{'':<10}{'Vainqueur':<30}")
        print("_"*108)
        print(f"{player1:<30} - VS - {player2:>30}{'':<10}{winner:<30}")

        print(
            "\n0: retour"
            " | 1: enregistrer le resultat"
            "\nsave: sauvegarder"
            " | load: charger")

        choice = input("?> ")
        return choice

    @staticmethod
    def record_match_result(match):
        """Affiche la page d'enregistrement du resultat d'un match
        selectionné"""
        print(
            "\n0: retour"
            " | 1: Joueur 1 vainqueur"
            " | 2: Joueur 2 vainqueur"
            " | 3: nul"
            "\nsave: sauvegarder"
            " | load: charger"
        )
        choice = input("?> ")
        return choice


class ViewReport:
    """Regroupe les vues des rapports"""
    @staticmethod
    def reports():
        """Affiche le menu racine des rapports"""
        print("=== Choisissez une catégorie de rapports")
        print(
            "0: retour"
            " | 1: rapports des joueurs"
            " | 2: rapports des tournois"
            "\nsave: sauvegarder"
            " | load: charger"
        )
        choice = input("?> ")
        return choice

    @staticmethod
    def reports_players(players):
        """Affiche le rapport de tous les joueurs, et son menu"""
        print("=== liste des joueurs :")
        print(
            f"{'joueur':<60}{'né(e) le':^20}{'sexe':^10}{'classement':^10}")
        print("_"*100)
        for player in players:
            name = f"{player.last_name} {player.first_name}"
            print(
                f"{name:<60}{player.birth_date:^20}"
                f"{player.gender:^10}{player.ranking:^10}")
        print(
            "\n0: retour"
            " | 1: trier par classement"
            " | 2: trier par nom"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def reports_tournaments():
        """Affiche le menu des rapports de tournois"""
        print(
            "\n0: retour"
            " | 3: selectionnez un tournoi"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def reports_tournament(tournament):
        """Affiche le rapport d'un tournoi et son menu"""
        print("_"*100)
        print("=== Rapports de tournoi")
        ViewTournament.tournament_show(tournament)
        print(
            "\n0: retour"
            " | 1: voir les tours"
            " | 2: voir les matches"
            " | 3: voir les joueurs"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def reports_rounds(tournament):
        """Affiche le rapport des tours et un menu"""
        print(f"== Liste des tours du tournoi : {tournament.name}")
        print(f"tournoi en {tournament.rounds_number} tours.")
        print(f"{'tour':<30}{'status':<20}")
        print("_"*60)
        for round in tournament.rounds:
            if round.played:
                status = "terminé"
            else:
                status = "en cours"
            name = settings.ROUND_BASE_NAME+round.name
            print(f"{name:<30}{status:<20}")
        print(
            "\n0: retour"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice

    @staticmethod
    def reports_matches(tournament, matches):
        """Affiche le rapport des matches d'un tournoi"""
        print(
            f"{'joueur1':<40}- Vs -{'joueur2':>40}"
            f"{' status':<10}{'vainqueur':^10}")
        print("_"*106)
        for match in matches:
            joueur1 = (
                f"{match.player1.first_name} {match.player1.last_name}"
                f" (classé {match.player1.ranking})")
            joueur2 = (
                f"{match.player2.first_name} {match.player2.last_name}"
                f" (classé {match.player2.ranking})")
            played = "non joué"
            if match.played:
                played = "joué"
            if not match.winner:
                winner = "..."
            else:
                winner = match.winner
            print(
                f"{joueur1:<40}"
                "- Vs -"
                f"{joueur2:>40}"
                f" {played:<10}"
                f"{winner:^10}")

        print(
            "\n0: retour"
            "\nsave: sauvegarder"
            " | load: charger")
        choice = input("?> ")
        return choice


if __name__ == '__main__':
    print("Veuillez ne pas executer ce module directement")
