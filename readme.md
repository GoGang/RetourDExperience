---
# Ready to Go ?
[Retour d'expérience sur un projet en Golang]
\[goo.gl/TpHJLq](http://goo.gl/TpHJLq)
---
# This is where it all began
---
/Qui sommes nous ?/Orange (B)

![Groupe Orange](img/groupe-orange.jpg)

Orange est le 3ème opérateur mobile et 1er fournisseur d’accès Internet ADSL en Europe, France Télécom compte parmi les leaders mondiaux des services de télécommunications aux entreprises multinationales.

- 100 000 salariés
- 7,4 millions de Livebox
- 9 millions de clients équipés haut débit, soit 46,3% de part de marché Grand Public
- 26,2 millions de clients mobiles dont 14,6 clients haut débit mobile
- 7,2 millions de clients VOIP
- 1200 boutiques France Télécom
- 736 000 clients Orange TV
- 380 000 clients ont signé pour la Fibre (644 000 foyers connectables)

---
/Qui sommes nous ?/OAB (B)

### Orange Applications for Business

Machine to Machine, Internet des objets, big data... Orange Business Services rassemble dans un même pôle ses expertises : Orange Applications for Business.

![OAB](img/orange-oab.png)

- 2400 collaborateurs (+200 recrutements par an)
- Chiffre d’affaires de 300 millions d’euros en 2013 (sur un CA global de 6,5 milliards d’euros réalisé l’an passé par OBS)

---
/Qui sommes nous ?/L'équipe (B)

L'équipe des développeurs ayant participé au projet est constituée de :

- ### Michel Casabianca
`michel.casabianca@orange.com`
- ### Benjamin Chenebault
`benjamin.chenebault@orange.com`
- ### Jacques Antoine Massé
`jacquesantoine.masse@orange.com`
- ### Sébastien Font
`sebastien.font@orange.com`

---
/Qui sommes nous ?/La plate-forme XMS (B)

### Plate-forme d'envoi et réception SMS/MMS 
#### Entre des éditeurs de services et des usagers mobile

![Bordel ya pas d'image](img/xms.jpg)

- ~ 30 applis en production
- Langages Java, C & Python
- 6 dev, 3 ops   
- Plusieurs centaines de clients
- 900 millions de sms/an

---
/Qui sommes nous ?/Le projet SGS-enabler (B)

### Le frontal d'accès à la plateforme XMS

![Bordel ya pas d'image](img/sgsenabler.jpg)

- Serveur TCP & HTTP

- Module d'authentification

- Routeur

- Load balancer


---
/Qui sommes nous ?/Soucis de maintenance (B)

### Maintenance très complexe et coûteuse

- Développé par un grand nombre de personnes

- Agrégat de design patterns : Observer, Factory, Object pool, Composite, [...]

- Très peu, voire aucune documentation

- Beaucoup de problématiques réseaux

- Problématiques d'accès concurrents réglés avec les classes de `java.util.concurrent`, et des blocs synchronisés

- Monitoré à partir beans exposés en JMX

---

/Qui sommes nous ?/Conclusion (B)

### Conclusion

Malgré des mois passés à débugger l'application, elle n'a jamais été suffisamment stable pour pouvoir y migrer tous nos clients

**Il a donc été envisagé de réécrire l'application**
---

# Etude technique
[Le choix de la technologie]

---
/Etude technique/Périmètre (M)

### Le périmètre de l'étude technique

- Un seul connecteur (frontal HTTP)

- Fonctionnalités principales

  - Parsing XML

  - Authentification par IP

  - Appel d'un serveur par TCP

---
/Etude technique/Critères de choix (M)

### Critères de choix de la technologie

- Simplicité de développement

- Maintenance facile du code

- Performances au runtime

- Consommation ressources CPU/mémoire

---
/Etude technique/Les alternatives (M)

### Alternatives techniques

L'existant a été développé avec l'API Non-blocking I/O du JDK. 

Les cibles envisagées ont été les suivantes :

- Java avec utilisation d'IO synchrones
- Go avec utilisation des channels et de goroutines

Les deux POCs ont été développés en parallèle en 10 jours environ

---
/Etude technique/Résultats (M)

### Les résultats des POCS

- Nombre de lignes de code comparable

- Architecture moins complexe en Go

- Tests en charge en faveur de Go (10% environ)

####Performances mesurées

- Nb de requêtes par seconde

- Temps moyen de traitement d'une requête

---
/Etude technique/Nombre de requêtes par seconde (M)

### Nombre de requêtes par seconde

![Nombre de requêtes par seconde](img/nombre-requetes.png)

---
/Etude technique/Temps moyen par requête (M)

### Temps moyen par requête

![Temps moyen de réponse par requête](img/temps-reponse.png)

---
# Le langage Go
---
/Le Go/Présentation Générale (JA)

### Go est un langage :

- Créé par Google en 2007, v1.0 en mars 2012
	- R.Pike, K.Thompson, R. Griesemer

- Procédural, un peu objet, un peu fonctionnel
 
- Garbage collecté

- Compilé

- Typage fort, statique

- Orienté concurrence

- Open source

---
/Le Go/Channels (JA)

### Les channels

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

- Primitives du langage
- File FIFO
- Très largement utilisée pour gérer la concurrence et les attentes de thread
- "select" permet de poller plusieurs channels

---

/Le Go/Goroutines (JA)

### Les Goroutines
- Exécution d'un appel de fonction en concurrence

- Mot clé "go"

- Primitive du langage

- Faible occupation mémoire (~4ko/goroutine)

- Task switching peu significatif

- Multiplexé sur un ou plusieurs threads de l'OS

---

/Le Go/Exemple (JA)

### Exemple

```go
package main

import (
	"time"
)

func producer(c chan int) {
	for {
		c <- 1
		time.Sleep(100 * time.Nanosecond)
	}
}

func consumer(c chan int) {
	ticker := time.Tick(5 * time.Millisecond)
	result := 0
	for {
		select {
		case val := <-c:
			result = result + val
		case <-ticker:
			println(result)
			return
		}
	}
}
```
---

/Le Go/Exemple (JA)

### Exemple

```go

func main() {
	c := make(chan int)
	go consumer(c)
	go consumer(c)
	go consumer(c)
	producer(c)
}

```

http://play.golang.org/p/kB04dmtTcE


---

/Le Go/Commandes Go (JA)

### Les commandes Go

- En ligne de commande

- go build
	- Compilation

- go run
	- Compilation + exécution

- go test
 
- go dep

[...]

---

/Le Go/Exécutables (JA)

### Les exécutables

- Binaires sans dépendance dynamique

- Volumineux 
    - "Hello world" ~ 1 Mo
    - Notre application ~ 9 Mo
	- Embarque toutes les bibliothèques utilisées

- Plate Formes supportées : 
	- FreeBSD et Linux 32/64 sur x86 et ARM, Windows, MacOS,…

---

/Le Go/Environnements (JA)

### L'environnement de développement

- go code

- Existence de modes pour emacs et vi :
	- go-vim
	- go-snippets, autocomplete, flycheck, etc.

- Liteide
	- Open Source
	- Ecrit en Go

- Plugins Eclipse et IntelliJ peu matures.

- Navigation dans le source, renommage, code appelant, build/tests, etc.

---

# Les écueils

---

/Les écueils/Gestion des Erreurs (M)

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
- Elles peuvent être interceptées
- Ce ne sont cependant pas des exceptions

---
/Les écueils/APIs simplistes (M)

### APIs simplistes

L'API de logs est assez critiquée car elle :

- Ne gère pas des niveaux de logs

- Ne gère pas des fichiers de configuration

- Doit donc être configurée dans le code

L'API de parsing des options en ligne de commande ne respecte par les standards Unix.

---
/Les écueils/Certificats (M)

### Certificats

Nous avons rencontré des difficultés pour la gestion des certificats :

- Des certificats générés sans l'option `ExtendedKeyUsage` (valeur `clientAuth`) ne peuvent servir à authentifier un client

- L'algorithme MD5 n'est pas supporté pour la signature de certificats bien qu'il soit dans la liste des algorithmes supportés par TLS 2.1

Si tous ces choix sont probablement pertinents, ils peuvent poser des problèmes avec l'existant

---
/Les écueils/Gestion des encodages (M)

### Gestion des encodages

Seul l'*UTF-8* et l'*UTF-16* sont supportés.

Ce choix est évident, mais peut rendre difficile la gestion de l'existant.

---
/Les écueils/Versioning (B)

### Le versioning

- `go get` clone le dernier commit des repo GitHub, Bitbucket, Google code

- Absence volontaire de package manager natif

- Package managers développés par la communauté : gopack, godep, GoManager, dondur, 

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

#Les Bonnes Surprises

---
/Bonnes surprises/Montée en compétence (JA)

### Montée en compétence rapide

- La syntaxe est simple 
	- "Langage procédural à accolades"
- Outillage efficace

- Goroutines et channels
	- Patterns de concurrence

- Features avancées
	- Composition de structures
	- Programmation "fonctionnelle"
	- Polymorphisme

---

/Bonnes surprises/Qualité des APIs (JA)

### Qualité des API

- Accessibles et compréhensibles

- API Standard complète
	-  compression, crypto, bases de données, encodage, html, io, log, net, reflection, testing, time, unsafe

- Limite le recours aux API tierces 

- Styles de développement hétérogènes

---
/Bonnes surprises/Monitoring (B)

### Monitoring

- Utilisation du package [pprof](http://golang.org/pkg/net/http/pprof/)

- Génération de heap dump et de cpu profiling

- Le package se bind sur un serveur HTTP

- `go tool pprof`, outil de visualisation des pprofs

![pprof](img/pprof.png)

---
/Bonnes surprises/API de tests (B)

###  L'API de tests

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
        t.Error()
    }
}
```

####Simplissime mais efficace
---
/Bonnes surprises/Accès concurrents (M)

### Accès concurrents

- Possibilité de lancer les tests unitaires avec l'option `-race`. 

Détection des accès concurrents à la mémoire.

- Egalement possible d'appliquer cette option à la compilation pour détecter les accès concurrents au runtime. 

Ceci peut être utile si la couverture de test est faible, mais attention aux performances !

---
/Bonnes surprises/Stabilité de l'application (M)

### Stabilité de l'application

Au cours de nos développements et de nos tests de charge, nous n'avons jamais vu l'application s'arrêter.

- Pas de SegFault ni de core dump

- Les pointeurs existent

- Mais on ne peut les manipuler (pas d'arithmétique de pointeurs)

---

/Bonnes surprises/Support et communauté (JA)

### Support et communauté

- Documentation du langage, des APIs

- Blogs et publications de la core team

- go-nuts, stackoverflow, reddit, go newsletter, irc

- Évènements et captation de conférences

---

/Bonnes surprises/Open source (JA)

### Open source

Google a joué pleinement le jeu de l'Open Source :

- La licence du logiciel est très ouverte (BSD)

- Code source très clair et facilement modifiable

- Nombreuses bibliothèques tierces

- Développement dynamique

---
# Retour sur les performances
---
/Performances/Poste de Développement (M)

### Poste de Développement

- Affranchissement des limitations réseau

- Mocks plus performants qu'implémentations réelles

#### Résultats

- 254 req./s pour la version en GO

- 139 req./s pour la version en Java

---
/Performances/Préproduction (M)

### Préproduction

Limitations dues :

- Au réseau

- Aux performances des applications connexes

#### Résultats

- 30 req./s pour la version en GO

- 30 req./s pour la version en Java (avec perte de paquets)

---
/Performances/RAM & CPU (M)

### RAM et CPU

- Environnement de préproduction

- A charge égale de 30 req./s

- Java : 94% CPU, 8.5% RAM

- Go :   2% CPU,  1.2% RAM

![Gopher](img/gopher.png)

---
# Conclusion

Expérience concluante

Projet en production

Un langage syntaxiquement et conceptuellement simple 

Adapté pour des applications pour lesquelles la performance est un enjeu

Outillage très simple à utiliser

Outils de profiling

Un vrai concurrent à Java...

