---
#Ready to Go ?
[Retour d'expérience sur un projet en Golang]
\[goo.gl/OXS5py](http://goo.gl/OXS5py)
---
#This is where it all began
---
/Qui sommes nous ?/L'équipe

L'équipe des développeurs ayant participé au projet est constituée de :

- Michel Casabianca
- Benjamin Chenebault
- Jacques Antoine Massé
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

### Maintenance très complexe et coûteuse

- Développé par un grand nombre de personnes
- Agrégat de design patterns : Observer, Factory, Object pool, Composite
- Très peu, voire aucune documentation
- Beaucoup de problématiques réseau
- Problématiques d'accès concurrent réglés à coups de ConcurrentHashMap, de ScheduledThreadPoolExecutor noyés dans des blocs synchronisés
- Monitorées à partir beans exposés en JMX
---
/Qui sommes nous ?/Conclusion

### Conclusion

Malgré des mois passés à débugger l'application, elle n'a jamais été suffisament stable pour pouvoir y migrer tous nos clients

**Il a donc été envisagé de réécrire l'application**
---
# Etude technique

---
/Etude technique/Périmètre

## Le périmètre de l'étude technique

- Un seul connecteur (frontal HTTP)
- Fonctionnalités principale
  - Parsing XML
  - Authentification par IP
  - Appel d'un serveur par TCP

---
/Etude technique/Critères de choix

## Critères de choix de la technologie

- Simplicité de développement
- Maintenance facile du code
- Performances au runtime
- Consommation ressources CPU/mémoire

---
/Etude technique/Les alternatives

## Alternatives techniques

L'existant a été développé en Java avec utilisation des NIO non bloquantes. Les alternatives envisagées ont été les suivantes :

- Java avec utilisation d'IO synchrones/multithread
- Go avec utilisation des channels et de goroutines

Les deux POCs ont été developpés en parallèle en 10 jours environ

---
/Etude technique/Résultats

## Les résultats des POCS

- Nombre de lignes de code comparable
- Complexité comparable avec un léger avantage à Go
- Tests en charge en faveur de Go (10% environ)

Mesure du nombre du nb de requêtes par seconde et du temps moyen de traitement d'une requête

---
/Etude technique/Nombre de requêtes par seconde

## Nombre de requêtes par seconde

![Nombre de requêtes par seconde](img/nombre-requetes.png)

---
/Etude technique/Temps moyen par requête

## Temps moyen par requête

![Temps moyen de réponse par requête](img/temps-reponse.png)

---
/Etude technique/RAM et CPU

TODO

---
/Etude technique/Résultats

## Résultats

Il est resorti de l'étude technique que :

- L'architecture en Go est plus simple
- Les performances du Go sont légèrement meilleures (d'environ 10%)
- Les consommations RAM & CPU sont en faveur de Go

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
/Bonnes surprises/Montée en compétence

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
/Bonnes surprises/Qualité des APIs

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
/Bonnes surprises/Monitoring

###Monitoring

- Existence du package pprof qui se bind à un serveur http

- Fournit un heap profil 

go tool pprof http://localhost:6060/debug/pprof/heap

- 30-second CPU profile

go tool pprof http://localhost:6060/debug/pprof/profile

- Goroutine blocking profile

go tool pprof http://localhost:6060/debug/pprof/block

On peut laisser un production le serveur HTTP permettant de monitorer le code. Par exemple, on pourra à tout instant afficher l'état de toutes les goroutines.

---
/Bonnes surprises/API de tests

###L'API de tests

Simplissime mais efficace
---
/Bonnes surprises/go test -race

L'option `-race` détecte les risques d'interblocage de l'application
- On peut l'appliquer pour les tests
- Mais aussi au runtime (mais consommateur de ressources)

---
/Bonnes surprises/Stabilité de l'application

Pas de risque de SegFault ni de core dump.
Du à l'absence d'arithmétique de pointeurs

---
/Bonnes surprises/Support et communauté

- Bonne documentation des APIs
- Code source disponible 
- Existende de nombreuses lib sur Github
- Nombreux blogs persos et évènements
- Et super mascotte ;)

---
/Bonnes surprises/Open source et gratuit

Code source très digeste contrairement aux classes du JDK

---
/Les ecueils/Les Erreurs

###La gestion des erreurs est rébarbative

---
/Les ecueils/API de logs

###API de Logs

---
/Les ecueils/Certificats

###Certificats

---
/Les ecueils/Vendorisation
###La vendorisation

- Absence volontaire de package manager natif

- go get clone le last commit des repo GitHub, Bitbucket, Google code

- "There is no need for a central archive of every version of every Go library ever released. Dependencies may move or disappear in the world outside your project. Versioning is a source of significant complexity, especially in large code bases" (Golang FAQ)

- Package managers développé par la communauté : gopack, godep, GoManager, dondur, 

```toml
[deps.memcache]
import = "github.com/bradfitz/gomemcache/memcache"
tag = "1.2"

[deps.mux]
import = "github.com/gorilla/mux"
commit = "23d36c08ab90f4957ae8e7d781907c368f5454dd"
...
```

---
Retour sur les performances et la maintenabilité.
---
/Performances/Développement

- Affranchissement des limitations réseau
- Mocks plus performants qu'implémentations réelles

254 req./s pour la version en GO
139 req./s pour la version en Java

---
/Performances/Préproduction

- Limité par les performances des applications connexes

30 req./s pour la version en GO
30 req./s pour la version en Java (avec drop de paquets)

---
RAM et CPU

- Environnement de préproduction
- A charge égale
- Java : 94% CPU, 8.5% RAM
- Go :   2% CPU,  1.2% RAM

--- 
/Maintenabilité

- Syntaxe plus simple
- Apis plus accessibles
- Pas de hiérarchie d'objets
- Pas de patterns
 
---
/Outils de monitoring

- Monitoring via package pprof
- Dump des Goroutines
- Temps de contention des goroutines
- Profilage
- Pas d'overhead au runtime, utilisé en production
- Outils GNU

---
/Conclusion

- Expérience concluante
- Projet en production

