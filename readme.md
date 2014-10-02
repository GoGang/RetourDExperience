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
	- Ecrit en Go

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

- Utilisation du package [pprof](http://golang.org/pkg/net/http/pprof/)

- Aucune instrumentation de code nécessaire

- Génération de heap dump et de cpu profiling

- Le package se bind sur un serveur HTTP

- `go tool pprof`, outil de visualisation des pprofs


On peut laisser un production le serveur HTTP permettant de monitorer le code. 
Par exemple, on pourra ainsi à tout instant afficher l'état de toutes les goroutines.

---
/Bonnes surprises/API de tests

### L'API de tests

Cette API est tout à fait comparable à un JUnit :

```go
package main

import "testing"

func Add(x, y int) int {
    return x+y
}

func TestAdd(t *testing.T) {
    if Add(1, 2) != 3 {
        t.Error("Bad luck!")
    }
}
```

- Elle est plus simple (pas de `assert`)
- Elle dispose d'outil pour lancer les tests d'un package

- Utilisation du package [testing](http://golang.org/pkg/testing/)

- Par convention, les fichiers de tests sont nommés XXX_test.go

- `go test` permet d'exécuter les tests

- Il existe deux types de test :
    - Les tests unitaires : `TestXxx(*testing.T)`
    - Les benchmarks : `BenchmarkXxx(*testing.B)`
    
```go
import "testing"

func TestFunctionTralala(t *testing.T) {
    if "tralala" != "tralala" {
        t.Fail()
    }
}
```

Simplissime mais efficace
---
/Bonnes surprises/Accès concurrents

### Accès concurrents

Il est possible de lancer les tests unitaires avec l'option `-race`. Go est alors capable de détecter les acceès concurrents à la mémoire.

Mais il est aussi possible d'appliquer cette option à la compilation pour détecter les accès concurrents au runtime. Ceci peut être utile si la couverture de test est faible, mais attention aux performances.

---
/Bonnes surprises/Stabilité de l'application

### Stabilité de l'application

Au cours de nos développements et de nos tests de charge, nous n'avons jamais vu planter notre logiciel :

- Pas de SegFault ni de core dump.
- Parceque pas d'arithmétique de pointeurs

---
/Bonnes surprises/Support et communauté

### Support et communauté

- Bonne documentation des APIs
- Code source disponible 
- Existende de nombreuses lib sur Github
- Nombreux blogs persos et évènements
- Et super mascotte ;)

---
/Bonnes surprises/Open source

### Open source

Google a joué pleinement le jeu de l'Open Source :

- La licence du logiciel est très ouverte (de type BSD)
- Code source très clair et facilement modifiable
- Développement dynamique

---
/Les ecueils/Gestion des Erreurs

### La gestion des erreurs est rébarbative

Source Go typique :

```go
f, err := os.Open("filename.ext")
if err != nil {
    log.Fatal(err)
}
```

Cette gestion des erreurs :

- Est répétitive
- On ne peut gérer des erreurs *en bloc*
- On ne peut typer les erreurs

Il est possible de lancer des *paniques* :

- Elles sont propagées
- Peuvent être interceptées
- Ce ne sont cependant pas des exceptions

---
/Les ecueils/API de logs

### API de Logs

L'API de logs est assez critiquée car elle :

- Ne gère pas des niveaux de logs
- Ne gère pas des fichiers de configuration
- Doit donc être configurée dans le code

---
/Les ecueils/Certificats

### Certificats

Nous avons rencontré des difficultés pour la gestion des certificats :

- Des certificats générés sans l'option XXX ne peuvent servir à authentifier un client
- L'algorithme MD5 n'est pas supporté pour la signature de certificats

Si tous ces choix sont probablement pertinents, ils peuvent poser des problèmes avec l'existant

TODO : vérifier les options exactes

---
/Les ecueils/Gestion des encodages

### Gestion des encodages

Seul l'*UTF-8* et l'*UTF-16* sont supportés.

Nous sommes tous d'accord que ce choix est évident, cependant cela peut rendre difficile la gestion de l'existant.

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
# Retour sur les performances et la maintenabilité.
---
/Performances/Poste de Développement

### Poste de Développement

- Affranchissement des limitations réseau
- Mocks plus performants qu'implémentations réelles

Les résultats sont les suivants :

- 254 req./s pour la version en GO
- 139 req./s pour la version en Java

---
/Performances/Préproduction

### Préproduction

- Limité par les performances des applications connexes

Les résultats sont les suivants :

- 30 req./s pour la version en GO
- 30 req./s pour la version en Java (avec drop de paquets)

---
/Performances/RAM & CPU

### RAM et CPU

- Environnement de préproduction
- A charge égale
- Java : 94% CPU, 8.5% RAM
- Go :   2% CPU,  1.2% RAM

--- 
/Performances/Maintenabilité

### Maintenabilité

- Syntaxe plus simple
- Apis plus accessibles
- Pas de hiérarchie d'objets
- Pas de patterns
 
---
/Performances/Outils de monitoring

### Outils de monotoring

- Monitoring via package pprof
- Pas d'overhead au runtime, utilisé en production
- Script de supervision pour surveiller les goroutines
- Temps de contention des goroutines

IMAGE HOBBIT

---
# Conclusion

Expérience concluante

Projet en production

- Un langage syntaxiquement et conceptuellement simple 
- Adapté pour des applications pour lesquelles la performance est un enjeu
- Outillage très simple à utilisé
- Outils de profiling
- Un vrai plaisir... ;)

