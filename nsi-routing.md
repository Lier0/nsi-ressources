---
layout: page
title: routage
permalink: /routage/
---
# nsi-routing
Synthèse sur le routage

## Modèle OSI vs TCP/IP
![OSI-TCP/IP-newTCP/IP](https://irp.nain-t.net/lib/exe/fetch.php/routage:modeles.gif)
> L'idée étant de comprendre l'indépendance des couches entre elles, avec le matériel en bas et la partie logique en haut.
> Il ne faut pas oublier l'importance de la couche 8 !

Concernant le routage, nous nous plaçons sur la couche réseau du modèle OSI.
Pour aller plus loin et voir le nouveau modèle TCP/IP : https://www.frameip.com/osi/.

## Adressage IP
### Adresse IP
Sur sa version 4, Internet Protocol permet d'identifier une machine sur un réseau IP avec une adresse IP, écrite en décimal pointé (pointé car il y a des points : 192.168.0.1), sur quatre octets.

### Masque de réseau
#### Masque type
De même, il s'écrit en décimal pointé, mais sa fonction est d'identifier l'adresse d'un réseau.
Quelques masques types. Il est courant d'utiliser la notation CIDR plutôt que décimal pointé.
* Adresse IP type : 10.0.0.1
    * CIDR : /8
    * Décimal pointé : 255.0.0.0
* Adresse IP type : 172.16.0.1
    * CIDR : /16
    * Décimal pointé : 255.255.0.0
* Adresse IP type : 192.168.0.1
    * CIDR : /24
    * Décimal pointé : 255.255.255.0
* Adresse IP type : sans, il s'agit généralement de connexion point à point.
    * CIDR : /32
    * Décimal pointé : 255.255.255.255

#### Utilisation du masque
Pour déterminer l'adresse du réseau à partir d'une adresse IP et d'un masque, il faut faire un ET logique entre les deux :
```
10.0.0.1  = 0000 1010 . 0 . 0 . 1
255.0.0.0 = 1111 1111 . 0 . 0 . 0
      AND   ---------------------
10.0.0.0  = 0000 1010 . 0 . 0 . 0
```

Un second exemple avec 192.168.10.128/24
```
192.168.10.128 = 1100 0000 . 1010 1000 . 0000 1010 . 1000 0000
255.255.255.0  = 1111 1111 . 1111 1111 . 1111 1111 . 0000 0000
           AND   ---------------------------------------------
192.168.10.0   = 1100 0000 . 1010 1000 . 0000 1010 . 0000 0000
```

## Routage
Nous allons d'abord voir le routage en général en abordant le routage statique, puis le routage dynamique avec les protocoles RIP et OSPF.
Pour aller plus loin :
- https://www.frameip.com/routage/
- https://www.ictshore.com/free-ccna-course/routing-table-fundamentals/ (en anglais mais les images sont parlantes et nous pouvons ignorer la partie IOS)

Nous voulons envoyer un paquet de notre source à une destination donnée. Nous avons notre IP et notre masque. Cela génère une route stockée dans la table de routage, laquelle contient l'adresse de notre réseau et le masque associé.
Deux cas :
- Si l'IP de destination est dans notre sous réseau, nous allons contacter la destination.
- Sinon, nous envoyons le paquet à la passerelle indiquée sur la route de la destination, ou la passerelle par défaut.

Mais ces deux cas sont gérés par la table de routage, qui est donc composée d'adresse IP de réseaux et de masques. Chaque route indique un réseau et un masque associé. Ainsi lorsque nous envoyons un paquet IP vers une adresse IP de destination, nous regardons la table de routage :
* à chaque route, nous regardons son masque,
* nous faisons un ET logique entre l'IP de destination et le masque de la route, pour obtenir une adresse réseau de destination,
* nous comparons l'adresse du réseau de la route avec l'adresse réseau calculée,
* si elle concorde, nous suivons cette route,
* autrement nous continuons,
* et à défaut, nous prenons la route "default".
Pour illustrer ce paragraphe, nous pouvons consulter l'image à cette adresse : https://www.ictshore.com/wp-content/uploads/2017/02/1029-03-Route_lookup_process.png

> En résumé, si la destination n'est pas dans notre réseau (ce que nous déterminons avec le masque), nous contactons la passerelle qui va bien.

```
A - B - C       |Router               |A     |B     |C     |D     |E
    |   |       |------               |----  |----  |----  |----  |----
    D - E       |dest, gateway        |B, B  |A, A  |A, B  |A, B  |A, D
                                      |C, B  |C, C  |B, B  |B, B  |B, D
                                      |D, B  |D, D  |E, E  |C, B  |C, C
                                      |E, B  |E, C  |D, E  |E, E  |D, D
```
Dans l'exemple ci-dessus :
* Quel est le chemin de A vers E ?
* Quel est le chemin de E vers A ?
* Ces chemins passent-ils par les mêmes routeurs ?

### La métrique d'une route
Nous avons jusqu'à présent occulté la notion de métrique. Celle-ci permet de donner une priorité aux routes. Ainsi, s'il existe deux routes de A vers E, la route avec la plus petite métrique l'emporte. Si les métriques sont identiques alors l'identifiant de l'interface sera différenciateur.
Nous introduisons ici la métrique car par la suite, nous allons voir deux procotoles de routage dynamique :
- RIP, protocole à vecteur de distance, la métrique est liée au nombre de saut.
- OSPF, protocole à vecteur d'état de lien, la métrique est liée à la vitesse en bits par seconde (bps) : débit de référence (souvent 10^8) / débit du lien
Les métriques définies par les protocoles ne sont pas forcement celles que nous verrons sur Linux par exemple, à cause de la distance administrative. Cette valeur définit si un algorithme sera privilégié dans le choix des routes, avec la métrique plus petite possible (110 pour RIP et 120 pour OSPF, cf. https://www.cisco.com/c/fr_ca/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html).

### Routage dynamique - RIP-v2
Routing Information Protocol, permet à un routeur de partager ses routes à ses voisins proches. Ainsi, de proche en proche, les routes vont se propager, sur la base de l'algorithme de Bellman-Ford.
RIP est plutôt utilisé sur des petits réseaux, notamment à cause de la limitation à 15 sauts. Un route RIP doit avoir une métrique inférieure ou égale à 15.

Les principes sont donc :
- nous avons des adresses IP sur nos interfaces,
- lesquelles impliquent des routes relatives aux interfaces,
- nous précisons à RIP les réseaux sur lesquels nous voulons partager les routes associées à ces réseaux.
- Si un routeur reçoit une nouvelle route vers une destination donnée, avec une métrique inférieure à celle déjà présente, alors la route est mise à jour.

Reprenons le schéma précédent, ajoutons les métriques selon RIP :
```
A - B - C     |Router                 |A        |B        |C        |D        |E
    |   |     |------                 |-------  |-------  |-------  |-------  |-------
    D - E     |dest, gateway, metric  |B, B, 1  |A, A, 1  |A, B, 2  |A, B, 2  |A, D, 3
                                      |C, B, 2  |C, C, 1  |B, B, 1  |B, B, 1  |B, D, 2
                                      |D, B, 2  |D, D, 1  |E, E, 1  |C, B, 2  |C, C, 1
                                      |E, B, 3  |E, C, 2  |D, E, 2  |E, E, 1  |D, D, 1
```
> Nous devons retenir que la métrique de RIP est relative au nombre de saut.

### Routage dynamique - OSPF-v2
Open Shortest Path First, permet de partager des routes sur un réseau organisé en zone, autour d'une zone dorsale (backbone, area 0). Les routes se propagent de proche en proche au sein d'une zone, par des résumés vers l'extérieur, sur la base de l'algorithme de Dijkstra.
OSPF est utilisé sur des réseaux plus conséquents, avec une notion backbone.

Reprenons le schéma précédent en modifiant la métrique selon OSPF, dans une même zone, en précisant :
- Tous les liens sont en 100 Mb/s,
- sauf B-C, à 10 Mb/s.
- Débit de ref. à 10^8.
- Soif B-C = 10^8/(10*10^6).
```
A - B - C     |Router                 |A         |B         |C         |D         |E
    |   |     |------                 |--------  |--------  |--------  |--------  |-------
    D - E     |dest, gateway, metric  |B, B,  1  |A, A,  1  |A, B, 11  |A, B,  2  |A, D,  3
                                      |C, B, 11  |C, C, 10  |B, B, 10  |B, B,  1  |A, C, 12
                                      |D, B,  2  |D, D,  1  |E, E,  1  |C, B, 11  |B, D,  2
                                      |E, B,  3  |E, C, 11  |D, E,  2  |C, E,  2  |B, C, 11
                                      |E, B, 12  |E, D,  2  |D, B, 11  |E, E,  1  |C, C,  1
                                                                                  |D, D,  1
```
> Nous devons retenir que la métrique d'OSPF est relative au débit d'un lien.

### RIP ou OSPF
Le choix du protocole dépend de la topologie et des besoins. Les deux sont complémentaires et avoir du RIP en bordure d'OSPF est cohérent.
Nous pouvons consulter ce lien pour un comparatif entre RIP et OSPF : https://community.fs.com/fr/blog/rip-vs-ospf-what-is-the-difference.html.
