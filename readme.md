---
#Ready to Go ?
[Retour d'expérience sur un projet en Golang]
\[goo.gl/OXS5py](http://goo.gl/OXS5py)
---
#This is where it all began
---
/Qui sommes nous ?/L'équipe

- #Michel Casabianca
 
- #Benjamin Chenebault
 
- #Jacques Antoine Massé
---
/Qui sommes nous ?/La plateform XMS

###Plate-forme d'envoi et réception SMS/MMS entre des éditeurs de service et des usagers mobile 

SCHEMA SIMPLE ICI

- 30 applis en production

- Langages Java, C & Python

- 6 dev, 3 ops   

- Plusieurs centaines de clients

- 900 millions de sms/an

- 23 millions d'€ de CA
---
/Qui sommes nous ?/Le projet SGS-enabler

###Principal frontal d'accès à la plateforme XMS

SCHEMA ICI
---
/Qui sommes nous ?/Soucis de maintenance

###Maintenance très complexe et couteuse

- Développé par un grand nombre de personnes

- Agrégat de design patterns : Observer, Factory, Object pool, Composite

- Très peu, voire aucune documentation

- Beaucoup de problématiques réseau

- Problématiques d'accès concurrent réglés à coups de ConcurrentHashMap, de ScheduledThreadPoolExecutor noyés dans des blocs synchronisés

- Monitorées à partir beans exposés en JMX

- [...]
---
#...
#Vers une réécriture de notre application
---
#Java VS Golang
---
#Survol du langage Go
---
/Le Go/Présentation Générale

### Go est un langage :
## Open source
## Compilé
## Typage fort, statique et inféré
## Orienté concurrence
## Garbage collecté
## Un peu objet, un peu fonctionnel

---
/Le Go/Channels

###Les channels

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

- Primitive du langage
- File FIFO
- Très largement utilisée pour gérer la concurrence et les attentes de thread

---

/Le Go/Les Goroutines

###Les Goroutines

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
- Très légères en terme de ressources (~4ko)
- Multiplexé sur un ou plusieurs threads de l'OS

<http://play.golang.org/p/y6W8I8lJYA>

---
/Le Go/Les Commandes Go

###Les commandes Go

- go build
	- Compilation

- go run
	- Compilation + exécution

- go test
	- Tous les tests, 
	- Un test particulier

- go fmt
	- Formatage
	- Réfactoring (un peu)

- go get
	- Import de bibliothèques
 
- go tool, go vet, go errcheck...
 
## Lancés par un gestionnaire de build ou un script shell

---

/Le Go/Les Exécutables

###Les exécutables

- Binaire sans dépendance dynamique

- Volumineux 
	- "Hello world" ~ 1Mo 
	- Embarque toutes les bibliothèques utilisées

- Plate Formes supportées : 
	- FreeBSD et Linux 32/64 sur x86 et ARM, Windows, MacOS,…

---

/Le Go/Environnements

###L'environnement de développement
- go code

- Existence de modes pour emacs et vi
	- go-vim
	- go-snippets, autocomplete, flycheck, etc.
	
- Plugins Eclise, IntelliJ, etc.
	
- Liteide
	- Open Source
	- écrit en Go

---
#Les Bonnes Surprises
---

/Les bonnes surprises/Numéro 1

###Montée en compétence rapide

- Courbe d'apprentissage douce

- La syntaxe est simple 
	- "Langage procédural à accolades"
- Outillage efficace

- Goroutine et channels
	- Asynchronsime
	- Patterns de concurrence

- Features avancées
	- Composition de structures
	- Programmation "fonctionnelles"
	- Utilisation d'interfaces

---

/Les bonnes surprises/Numéro 2
###Qualité des API

```go
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	res, err := http.Get("http://www.google.com/robots.txt")
	if err != nil {
		log.Fatal(err)
	}
	robots, err := ioutil.ReadAll(res.Body)
	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", robots)
}
```

http://play.golang.org/p/VPwJf7DuUo


---








































Michel Casabianca, Benjamin Chenebault et Jacques Antoine Massé.

---
# Equipe XMS

Plate-forme SMS/MMS entre des éditeurs de service et des usagers mobile
6 dev, 3 devops
~15 applications Java, C, Python
Quelques centaines de clients
900 millions de sms/an

---
# Le projet SGS enabler

Principal frontal d'accès à la plate-forme écrit en Java
Rôle de loadbalancer, authentifications des clients, serveur HTTP & TCP

---
# Soucis de maintenance

Cout de maintenance exorbitants, bugs difficiles à identifier et corriger
Appli obsolète => Nécessité de réécriture
Environ 10 k lignes de code Java
Beaucoup de problèmes de concurrence et de synchronisation du code
Pas assez de documentation

---
# Conclusion : Nécessité de réécrire l'application

Malgré des mois passés à débugger l'application, elle n'a jamais été suffisament stable pour pouvoir migrer tous les clients dessus

---
# Etude technique

Réalisation d'un sous ensemble des fonctionnalités du projet dans le but de décider du choix de la techno.
Périmètre réduit : Acceptation d'une requête HTTP, utilisation de lib XML, authentification par IP, requêtage HTTP, ouverture et envoie de données en TCP. => FAIRE SCHEMA SIMPLE

---
# Critères de choix de la technologie

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
- Typage fort, statique et inféré
- Orienté concurrence
- Garbage collecté

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

La commande Go

- go build
- go run
- go test
- go fmt

---

Les exécutables en Go

- Binaire compilé statiquement donc standalone
- "Hello world" ~ 1Mo (embarque toutes les bibliothèques utilisées)
- Embarque le garbage collector
- Cross compilation possible
- PF supportées : FreeBSD et Linux 32/64 sur x86 et ARM, Windows, MacOS,...

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

Ecueil n°2 : Logging

---

Ecueil n°3 : Certificats

---

Ecueil n°4 : Vendorisation

---

Bonne surprise N°1 : Apprentissage de Go

La montée en compétence est rapide, de l'ordre de la semaine. Le langage est simple:
- La syntaxe est simple
- Goroutine et channels
- Features avancées (champs annonymes)

---

Bonne surprise N°2 : Qualité des API

```go
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	res, err := http.Get("http://www.google.com/robots.txt")
	if err != nil {
		log.Fatal(err)
	}
	robots, err := ioutil.ReadAll(res.Body)
	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", robots)
}
```

http://play.golang.org/p/VPwJf7DuUo

---

Bonne surprise N°3 : Rapidité de développement

Comparable au Python. Cette vistesse est due à :
- La simplicité du langage
- La qualité des APIs

---

Bonne surprise N°4 : Déploiement (binaire sans dépendances)
- Cross compilation possible

---

Bonne surprise N°5 : Monitoring

On peut laisser un production le serveur HTTP permettant de monitorer le code. Par exemple, on pourra à tout instant afficher l'état de toutes les goroutines.

---

Bonne surprise n°6 : L'API de tests
Simplissime mais efficace

---

Bonne surprise n°7 : go test -race
Permet de repérer des risques d'interblocage

---

Bonne surprise n°8 : Stabilité de l'application déployée en production
Pas de risque de SegFault ni de core dump.
Du à l'absence d'arithmétique de pointeurs

---

Bonne surprise n°9 : Support, communication et communauté
- BOnne documentation des APIs
- Code source disponible 
- Existende de nombreuses lib sur Github
- Nombreux blogs persos et évènements
- Et super mascotte ;)

---

Bonne surprise n°10 : Open source et gratuit

Code source très digeste contrairement aux classes du JDK

---

Retour sur les performances et la maintenabilité.

---

Machine de développement
 - Affranchissement des limitations réseau
 - Mocks plus performants qu'implémentations réelles

254 req./s pour la version en GO
139 req./s pour la version en Java

---

Environnement de préproduction
 - Limité par les performances des applications connexes

 - 30 req./s pour la version en GO
 - 30 req./s pour la version en Java (avec drop de paquets)

---

RAM et CPU

 - Environnement de préproduction
 - A charge égale
 - Java : 94% CPU, 8.5% RAM
 - Go :   2% CPU,  1.2% RAM

--- 

Maintenabilité

 - Syntaxe plus simple
 - Apis plus accessibles
 - Pas de hiérarchie d'objets
 - Pas de patterns
 
---

Outils de monitoring

 - Monitoring via package pprof
 - Dump des Goroutines
 - Temps de contention des goroutines
 - Profilage
 - Pas d'overhead au runtime, utilisé en production
 - Outils GNU

---

Conclusion

 - Expérience concluante
 - Projet en production
 - Léger retard dû à des fonctionnalités de l'application hors normse
