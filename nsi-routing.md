# nsi-routing
Synthèse sur le routage

## Modèle OSI vs TCP/IP
![OSI-TCP/IP-newTCP/IP](https://irp.nain-t.net/lib/exe/fetch.php/routage:modeles.gif)
> L'idée étant de comprendre l'indépendance des couches entre elles, avec le matériel en bas et la partie logique en haut.
> Il ne faut pas oublier l'importance de la couche 8 !

Concernant le routage, nous nous plaçons sur la couche réseau du modèle OSI.
Pour aller plus loin et voir le nouveau modèle TCP/IP : ![FrameIP-OSI](https://www.frameip.com/osi/)

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
- ![FrameIP-routage](https://www.frameip.com/routage/)
- ![ictshore](https://www.ictshore.com/free-ccna-course/routing-table-fundamentals/) (en anglais mais les images sont parlantes et nous pouvons ignorer la partie IOS)

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
* Quel est ce chemin E vers A ?
* Ces chemins passent-ils par les mêmes routeurs ?

### La métrique d'une route
Nous avons jusqu'à présent occulté la notion de métrique. Celle-ci permet de donner une priorité aux routes. Ainsi, s'il existe deux routes de A vers E, la route avec la plus petite métrique l'emporte. Si les métriques sont identiques alors l'identifiant de l'interface sera différenciateur.
Nous introduisons ici la métrique car par la suite, nous allons voir deux procotoles de routage dynamiques :
- RIP, protocole à vecteur de distance, la métrique est liée au nombre de saut.
- OSPF, protocole à vecteur d'état de lien, la métrique est liée à la vitesse.
