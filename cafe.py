import time


class AgentBoisson:
    def __init__(self):
        self.stock = {"cafe": 5, "the": 3, "chocolat": 2}

    def verifier_stock(self, boisson):
        return self.stock.get(boisson, 0) > 0

    def diminuer_stock(self, boisson):
        if self.verifier_stock(boisson):
            self.stock[boisson] -= 1


class AgentPaiement:
    def __init__(self):
        self.prix = {"cafe": 2, "the": 1.5, "chocolat": 2.5}
        self.stock_pieces = {2: 5, 1: 10, 0.5: 20, 0.2: 30, 0.1: 50}

    def verifier_paiement(self, boisson_choisie, mode_paiement, paiement_details):
        if mode_paiement == "carte":
            return self.paiement_par_carte(boisson_choisie)
        elif mode_paiement == "especes":
            return self.paiement_en_especes(boisson_choisie, paiement_details)
        else:
            print(f"[Paiement] Mode de paiement inconnu ({mode_paiement}).")
            return False, None

    def paiement_par_carte(self, boisson):
        prix_boisson = self.prix.get(boisson, 0)
        print(f"[Paiement] Carte acceptée pour {prix_boisson} EUR.")
        return True, 0

    def paiement_en_especes(self, boisson, pieces_client):
        pieces_valides = set(self.stock_pieces.keys())
        for piece in pieces_client.keys():
            if piece not in pieces_valides:
                print(f"[Paiement] Pièce invalide détectée: {piece} EUR.")
                print(
                    "[Paiement] Paiement annulé, veuillez réessayer avec des pièces valides."
                )
                return False, pieces_client

        prix_boisson = self.prix.get(boisson, 0)
        montant_total = sum(
            valeur * quantite for valeur, quantite in pieces_client.items()
        )
        print(f"[Paiement] Montant inséré: {montant_total} EUR.")

        if montant_total < prix_boisson:
            print(f"[Paiement] Paiement insuffisant. {prix_boisson} EUR requis, {montant_total} donné.")
            return False, pieces_client

        for valeur, quantite in pieces_client.items():
            self.stock_pieces[valeur] += quantite

        rendu = round(montant_total - prix_boisson, 2)
        rendu_pieces = self.calculer_rendu_monnaie(rendu)
        if rendu_pieces is None:
            print("[Paiement] Impossible de rendre la monnaie.")
            return False, pieces_client

        print(f"[Paiement] Monnaie rendue: {rendu_pieces}")
        return True, rendu_pieces

    def calculer_rendu_monnaie(self, montant):
        rendu = {}
        reste_a_rendre = montant
        for valeur in sorted(self.stock_pieces.keys(), reverse=True):
            if reste_a_rendre <= 0:
                break
            nb_piece = min(int(reste_a_rendre // valeur), self.stock_pieces[valeur])
            if nb_piece > 0:
                rendu[valeur] = nb_piece
                reste_a_rendre = round(reste_a_rendre - nb_piece * valeur, 2)

        if reste_a_rendre > 0:
            return None

        for valeur, quantite in rendu.items():
            self.stock_pieces[valeur] -= quantite

        return rendu


class AgentPreparation:
    def preparer_boisson(self, boisson):
        print(f"[Préparation] Préparation de votre {boisson}...")
        time.sleep(2)
        print(f"[Préparation] Votre {boisson} est prêt !")


class AgentPrincipal:
    def __init__(self):
        self.agent_boisson = AgentBoisson()
        self.agent_paiement = AgentPaiement()
        self.agent_preparation = AgentPreparation()
        self.etat = "menu"
        self.boisson_choisie = None

    def demarrer(self):
        while True:
            if self.etat == "menu":
                self.afficher_menu()
            elif self.etat == "attente_paiement":
                self.demander_paiement()
            elif self.etat == "validation":
                self.valider_paiement()
            elif self.etat == "preparation":
                self.preparer_boisson()
            elif self.etat == "livraison":
                self.livrer_boisson()

    def afficher_menu(self):
        print("\n=== Menu des boissons ===")
        for boisson, stock in self.agent_boisson.stock.items():
            print(f"- {boisson} ({stock} disponibles)")
        choix = input("Choisissez votre boisson: ").lower()
        if self.agent_boisson.verifier_stock(choix):
            self.boisson_choisie = choix
            self.etat = "attente_paiement"
        else:
            print("Boisson non disponible. Choisissez une autre.")

    def demander_paiement(self):
        mode = input("Mode de paiement (carte/especes): ").lower()
        if mode == "carte":
            self.mode_paiement = mode
            self.paiement_details = None
            self.etat = "validation"
        elif mode == "especes":
            pieces = {}
            print(
                "Insérez vos pièces (format: [valeur] [quantite], exemple: 2 1 pour 1 pièce de 2 EUR). Tapez 'ok' pour terminer."
            )
            while True:
                entree = input("Ajoutez une pièce: ")
                if entree == "ok":
                    break
                try:
                    valeur, quantite = map(float, entree.split())
                    pieces[valeur] = pieces.get(valeur, 0) + int(quantite)
                except:
                    print("Format invalide.")
            self.mode_paiement = mode
            self.paiement_details = pieces
            self.etat = "validation"
        else:
            print("Mode de paiement inconnu.")

    def valider_paiement(self):
        paiement_ok, rendu = self.agent_paiement.verifier_paiement(
            self.boisson_choisie, self.mode_paiement, self.paiement_details
        )
        if paiement_ok:
            self.agent_boisson.diminuer_stock(self.boisson_choisie)
            self.rendu = rendu
            self.etat = "preparation"
        else:
            print("Paiement échoué. Retour au menu.")
            self.etat = "menu"

    def preparer_boisson(self):
        self.agent_preparation.preparer_boisson(self.boisson_choisie)
        self.etat = "livraison"

    def livrer_boisson(self):
        print(f"[Livraison] Voici votre {self.boisson_choisie}.")
        if isinstance(self.rendu, dict) and self.rendu:
            print(f"Rendu monnaie: {self.rendu}")
        self.etat = "menu"


if __name__ == "__main__":
    agent = AgentPrincipal()
    agent.demarrer()
