RetourExperience
================

Retour d'expérience projet Go

Soumission à Bdx.io
-------------------

Présentation de 50' dans le thème *Langages / Fraleworks / Tooling*.

### Titre

Retour d'expérience sur la mise en oeuvre du Go au sein d'Orange

### Résumé

Notre équipe à mis en oeuvre le langage de programmation Go dans un projet de serveur haute performance dans l'infrastructure SMS d'Orange. Au cours de cette présentation, nous détaillerons :

- Le contexte du projet et ses contraintes.
- Rapide présentation du Go.
- Les raisons du choix de Go.
- Ecueils et bonnes surprises lors du développement.
- Retour sur les performances et la maintenabilité.

### Message pour le comité de sélection

Cette conférence sera présentée par l'équipe ayant développé le projet, à savoir :

- Michel Casabianca
- Benjamin Chenebault
- Jacques Antoine Massé

Elle pourrait être couplée à un atelier d'1h50 sur le langage de programmation Go.

---

Plan
====
- Qui sommes nous ?
  - Orange
  - Equipe XMS
- Le contexte du projet et ses contraintes (3 min)
  - Présentation de l'environnement
  - Technos mises en oeuvre dans le projet
  - Les difficultés du projet
  - Conclusion : nécessité de réécrire l'appli
- Etude Technique
  - Java
  - Go
  - Réalisation de POCS
    - Critères de choix
    - Protocole de test
    - Graphes de benches
  - Conclusion de l'étude technique
    - Choix du Go
- Rapide présentation du Go.
  - Concurrence
  - Outils de développement (commande go)
  - Environnements de développement
- Ecueils et bonnes surprises lors du développement.
  - Difficultés
    - Pattern 'APPEL+CheckERROR' 
    - Logging
    - Certificats
    - Réapprentissage de pratiques de dév
    - Gestion des erreurs perfectible (besoin de discipline, très reberbatif, et pas de typage des erreurs)
    - Vendorisation
  - Bonnes surprises
    - Apprentissage de Go 
    - Qualité des API
    - Rapidité de développement
    - Déploiement (binaire sans dépendances)
    - Monitoring
    - Librairie standard (dont serveurs http)
    - API de tests
    - go test -race
    - Pas de problèmes rencontrés en PROD, appli stable
    - Support, communication et communauté
    - Open source donc gratuit
- Retour sur les performances et la maintenabilité.
  - Résultats des benches go/legacy
  - Outils de monitoring mis en production

---

Qui sommes nous ?

Michel Casabianca, Benjamin Chenebault et Jacques Antoine Massé.

---

Equipe XMS

Plate-forme SMS/MMS entre des éditeurs de service et des usagers mobile
6 dev, 3 devops
~15 applications Java, C, Python
Quelques centaines de clients
900 millions de sms/an

---

Le projet SGS enabler

Principal frontal d'accès à la plate-forme écrit en Java
Rôle de loadbalancer, authentifications des clients, serveur HTTP & TCP

---

Soucis de maintenance

Cout de maintenance exorbitants, bugs difficiles à identifier et corriger
Appli obsolète => Nécessité de réécriture
Environ 10 k lignes de code Java
Beaucoup de problèmes de concurrence et de synchronisation du code
Pas assez de documentation

---

Conclusion : Nécessité de réécrire l'application

Malgré des mois passés à débugger l'application, elle n'a jamais été suffisament stable pour pouvoir migrer tous les clients dessus

---

Etude technique

Réalisation d'un sous ensemble des fonctionnalités du projet dans le but de décider du choix de la techno.
Périmètre réduit : Acceptation d'une requête HTTP, utilisation de lib XML, authentification par IP, requêtage HTTP, ouverture et envoie de données en TCP. => FAIRE SCHEMA SIMPLE

---

Critères de choix de la technologie

Performances
Simplicité de développement et de lecture de code
Consommation ressources CPU/mémoire

---

Les alternatives

Développement en Java avec utilisation d'IO synchrones/multithread (VS NIO dans implémentation legacy)
Développement en Go avec l'utilisation des channels et des go routines

Réalisation des 2 POCs en parallèle sur 10 jours de développement.

---

Les résultats des POCS

Nombre de lignes de code comparable
Complexité comparable avec un léger avantage à Go
Protocole de test : Test de montée en charge et de vieillissement de l'application
Mesure du nombre du nb de requêtes par seconde et du temps moyen de traitement d'une requête

---

Les résultats des POCS

LES GRAPHES NB REQUETE/SEC ICI

---

Les résultats des POCS

LES GRAPHES temps moyen par requete ICI

---

Les résultats des POCS

LES GRAPHES RAM ET CPU ICI

---

Conclusion de l'étude technique

Architecture du programme en Go simplifiée
Les performances en Go sont meilleures d'environ 10%
Consommation RAM/CPU en faveur de Go

---

Présentation de Go

Go est un langage :
- Open source
- Compilé
- Typé statiquement
- Orienté concurrence
- Garbage collecté

---

Les goroutines

```go
package main

func producer(c chan string) {
	c <- "hello"
}

func consumer(c chan string) {
	println(<-c)
}

func main() {
	c := make(chan string)
	go consumer(c)
	producer(c)
}
```

- Primitives du langage
- Très légères en terme de ressources (4ko)
- Multiplexé sur un thread de l'OS

<http://play.golang.org/p/y6W8I8lJYA>

---

Les channels

```go
package main

func main() {
	c := make(chan int, 1)
	c <- 42
	val := <-c
	println(val)
}
```

<http://play.golang.org/p/Kq0Ih_NwIH>

- File d'attente intégrée au langage
- FIFO
- Très largement utilisée pour gérer la concurrence et les attentes de thread

---

La commande Go

- go build
- go run
- go test
- go fmt

---

Les exécutables en Go

-Binaire compilé statiquement donc standalone
-"Hello world" ~ 1Mo (embarque toutes les bibliothèques utilisées)
-Embarque le garbage collector
-Cross compilation possible
-Pf supportées : FreeBSD et Linux 32/64 sur x86 et ARM, Windows, MacOS,...

---

L'environnement de développement

- Existence de modes pour emacs et vi
- Existence de plugins Eclise et IntelliJ
- Liteide écrit en Go

---

Ecueils et bonnes surprises

---

Ecueil n°1 : la gestion des erreurs peut sembler réberbatifs

---

Ecueil n°2 : Le 


