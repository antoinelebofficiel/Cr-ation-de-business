# Frappe froide — liste CSV

Les pubs créent de la demande. La liste **crée** le marché. 1 008 indépendants avec téléphone dans `cibles-commerces.csv`. C’est 10× plus de volume que d’attendre Facebook.

Filtrer : `chaine = non` + `tel` non vide. Trier par zone du jour (voir tournées dans `01-offre.md`).
Ordre opérationnel : l’îlot du jour dans `mecanisme/carnet.csv` (T01 le jour 1, T02 le jour 2). Hors îlot = hors tournée.

Ignorer les sièges nationaux, banques régie, grandes enseignes déjà taguées `chaine = oui`. Un concessionnaire ou un salon de coiffure indépendant = cible prioritaire (vitrines + passage fréquent).

---

## Appel à froid (25 secondes)

> {Commerce} bonjour, {Toi} de Clartéo — on lave les vitrines sur {Ville}. Je passe déjà {demain} dans la rue, je vous glisse un premier passage à 49 € sans engagement ?

Si standardiste :

> Le gérant, 20 secondes. C’est pour la devanture.

Si « envoyez un mail » :

> Je n’envoie pas de plaquette. Un passage, vous voyez. Je suis sur {Ville} {jour} à {heure}. Oui ou non ?

Noter dans le Sheet : NRP / refus / rappel / OK créneau.

Quota Lun–Ven : **60 appels + 25 portes**. Sam : **20 portes**, 0 appel bureau.
Semaine : `equipe/00-SEMAINE.txt`. Recrutement AE : `equipe/recrutement.txt`.

---

## Porte (8 secondes + carte)

> Clartéo, vitrines. 49 € le premier, pas de contrat. Je vous prends {créneau tournée} ?

Tu as déjà la photo de LEUR vitrine sur ton téléphone (tu l’as prise en arrivant). Tu la montres :

> Là, aujourd’hui. Demain matin, ça.

C’est le close visuel. Tu ne discutes pas.

25 portes Lun–Ven, 20 le samedi. Centre d’abord. Zones commerciales : indépendants en périphérie des galeries, pas les enseignes. Après le oui vitrine : locaux, même jour.
