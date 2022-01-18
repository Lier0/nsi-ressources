# nsi-routing
Synthèse sur le routage

## Modèle OSI vs TCP/IP
![OSI-TCP/IP-newTCP/IP](https://irp.nain-t.net/lib/exe/fetch.php/routage:modeles.gif)
> L'idée étant de comprendre l'indépendance des couches entre elles, avec le matériel en bas et la partie logique en haut.
> Il ne faut pas oublier l'importance de la couche 8 !

Concernant le routage, nous nous plaçons sur la couche réseau du modèle OSI.

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
* Adresse IP type : sans
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
Le masque est important pour déterminer l'adresse de réseau. Ces informations sont contenues dans la table de routage. Ainsi lorsque nous envoyons un paquet IP vers une adresse IP de destination, nous regardons la table de routage :
* à chaque route, nous regardons son masque,
* nous faisons le ET logique pour obtenir une adresse réseau de destination,
* nous comparons l'adresse du réseau de la route avec l'adresse réseau calculée,
* si elle concorde, nous suivons cette route,
* autrement nous continuons,
* et à défaut, nous prenons la route "default".

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
* Ce chemin suffit-il en TCP ? En UDP ?
* Faut-il un chemin retour et si oui, quel est ce chemin E vers A ?
