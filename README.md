# Analyse et Sécurisation du Réseau a l'aide de Wireshark

# Table des Matières

1. [Introduction](#introduction)
2. [Préparation de l'Environnement](#préparation-de-lenvironnement)
3. [Démarrage de la Capture avec Wireshark](#démarrage-de-la-capture-avec-wireshark)
4. [Configurations des Filtres](#configurations-des-filtres)
5. [SYN Scan et Scan de Handshake Complet](#syn-scan-et-scan-de-handshake-complet)
6. [Capture SYN Scan](#capture-syn-scan)
7. [Analyse des Ports Ouverts dans wireshark](#Analyse_des_Ports_Ouverts_dans_wireshark)
8. [Analyse du port spécifique dans wireshark](#analyse-du-port-spécifique-dans-wireshark)
9. [Connaître le Système d'Exploitation Cible](#connaître-le-système-dexploitation-cible)
10. [Follow TCP Stream](#follow-tcp-stream)
11. [Détection et Analyse d'une Attaque ARP Spoofing à l'aide de Wireshark](#détection-et-analyse-dune-attaque-arp-spoofing-à-laide-de-wireshark)
12. [Détection d'une attaque DoS à l'aide de Wireshark](#Détection_d'une_attaque_DoS_à_l'aide_de_Wireshark)
13. [Coclusion](#conclusion)

## Introduction

Dans un monde où la cybercriminalité et les menaces informatiques évoluent constamment, assurer la sécurité d'un réseau informatique est devenu une priorité cruciale pour les organisations de toutes tailles. Les réseaux modernes, souvent vastes et complexes, sont des cibles fréquentes pour diverses formes d'attaques, telles que les intrusions non autorisées, les attaques par déni de service (DoS) et les tentatives de vol de données. Dans ce contexte, la capacité à détecter et à répondre rapidement aux activités suspectes devient un impératif stratégique.

Ce projet, intitulé "Analyse et Sécurisation du Réseau à l'aide de Wireshark", vise à répondre à ces défis en utilisant Wireshark, un outil de capture et d'analyse de paquets de réseau de renommée mondiale. Wireshark est reconnu pour sa puissance et sa flexibilité, permettant aux professionnels de la sécurité informatique de surveiller, d'analyser et de diagnostiquer les problèmes de réseau de manière détaillée. 

## Préparation de l'Environnement

#### Wireshark

Wireshark est un outil de capture et d'analyse de paquets réseau largement utilisé dans les tests de sécurité et l'analyse de réseaux. Pour ce projet, Wireshark est installé par défaut sur les distributions Kali Linux, qui est un système d'exploitation dédié aux tests de sécurité. Kali Linux fournit une suite complète d'outils pour l'analyse et le test de la sécurité réseau, ce qui facilite l'intégration de Wireshark dans l'environnement de test.

#### Préparation du Réseau de Test

Pour assurer une analyse efficace et sécurisée, un environnement de test isolé a été utilisé en employant VMware Workstation. Le réseau de test a été configuré en mode "Host-Only" pour créer un réseau privé virtuel. Cette configuration permet aux machines virtuelles de communiquer uniquement entre elles et avec l'hôte, tout en restant isolées du réseau externe. Les machines virtuelles utilisées dans ce projet sont :

- **Kali Linux** : Fournit les outils nécessaires pour les tests de sécurité et l'analyse réseau.
- **Metasploitable 2** : Une machine virtuelle vulnérable utilisée pour tester les techniques d'exploitation et les outils de sécurité.
- **Windows** 
- **Ubuntu 22.04**

Les étapes de préparation incluent :

1. **Configuration de VMware Workstation :**
   - **Création d'un réseau virtuel "Host-Only" :** VMware a été configuré pour utiliser un réseau "Host-Only", permettant aux machines virtuelles de communiquer entre elles


   ![hostonly](captures/hostonlyconfiguration.png)


   - **Ajout des machines virtuelles :** Les machines virtuelles Kali Linux, Metasploitable 2, Windows XP et Ubuntu 22.04 ont été créées et configurées sur ce réseau "Host-Only". Chaque machine virtuelle a été configurée avec une adresse IP  attribuée par le serveur DHCP du réseau "Host-Only".

1. **Vérification de la Connectivité :**

 - **Test de la communication entre les machines :** l'outil `ping` a été utiliséss pour vérifier que les machines virtuelles pouvaient communiquer entre elles .


    ![ping](captures/ping.png)


## Démarrage de la Capture avec Wireshark

Après avoir préparé l'environnement de test, il est crucial de configurer correctement Wireshark pour capturer les données pertinentes.
Lors du démarrage de wireshark, l'interface réseau correspondant au réseau "Host-Only" a été sélectionnée pour garantir que le trafic capturé provient du réseau de test isolé.

 ![interface](captures/interface.png)

## Configurations des Filtres

Lors de la première exécution de Wireshark, une grande quantité de trafic est observée, comprenant principalement des paquets de diffusion (broadcast) et des protocoles de gestion de réseau tels que ARP, CDP, LLDP et STP.
 
 
 ![brodcast](captures/brodcast.png)

 
Pour se concentrer sur le trafic pertinent et réduire la surcharge d'informations, un filtre a été appliqué :

   ```bash

   !(eth.dst == ff:ff:ff:ff:ff:ff || arp || cdp || lldp || stp )
   ```


  
   ![nobrodcast](captures/nobrodcast.png)

   
   Ce filtre exclut les paquets de diffusion et les protocoles de gestion réseau, permettant ainsi de se focaliser sur le trafic plus significatif pour l'analyse. 

   ### Filtrage par port :


Pour analyser spécifiquement le trafic ICMP, tel que les requêtes et les réponses de ping, les étapes suivantes ont été suivies :

1. **Effectuer le Ping :**
   - Depuis la machine Kali, un terminal a été ouvert.
   - La commande de ping suivante a été exécutée pour envoyer des paquets ICMP Echo Request à la machine Metasploitable :

     ```bash
     ping 192.168.10.123
     ```

2. **Capturer et Analyser le Trafic :**
   - Wireshark a été lancé et l'interface réseau appropriée pour la capture a été sélectionnée.
   - Le filtre `icmp` a été entré dans la barre de filtre de Wireshark pour afficher uniquement les paquets ICMP :

     ```plaintext
     icmp
     ```

  ![icmp](captures/icmp.png)
     

   - La capture a été démarrée. Les paquets ICMP Echo Request envoyés par Kali et les réponses ICMP Echo Reply de Metasploitable ont été visibles.


### Filtrage par Adresses IP : 

Pour se concentrer sur des adresses IP spécifiques dans le réseau, un filtre plus ciblé a été utilisé. Ce filtre permet de restreindre la capture aux paquets envoyés d'une adresse IP source à une adresse IP de destination particulière. Par exemple, pour observer le trafic entre l'adresse IP 192.168.10.219 et l'adresse IP 192.168.10.123, le filtre suivant a été appliqué :

 ```bash
     ip.src == 192.168.10.219 && ip.dst == 192.168.10.123
 ```

  ![ipadd](captures/ipadd.png)

Ce filtre a permis de se concentrer uniquement sur le trafic entre ces deux adresses IP, facilitant ainsi l'analyse des communications spécifiques entre ces machines et éliminant les autres paquets qui ne sont pas pertinents pour cette analyse.

Pour vérifier ce filtre , un test de ping a été effectué depuis la machine Ubuntu, avec l'adresse IP 192.168.10.128, vers la machine Windows, avec l'adresse IP 192.168.10.122. 

 ![ipadd](captures/ubnt.png)
 ![ipadd](captures/vide.png)

 
**Observation :** Wireshark n'a pas capturé les paquets de ce ping. Cela est dû à l'utilisation du filtre qui spécifiait uniquement les paquets entre deux adresses IP spécifiques. En effet, le filtre appliqué limitait la capture aux paquets entre les adresses IP 192.168.10.219 et 192.168.10.123. Par conséquent, les pings effectués entre les adresses IP 192.168.10.128 et 192.168.10.122 ont été exclus de la capture. 

## SYN Scan et Scan de Handshake Complet

Avant d'appliquer le filtre `tcp.flags.syn==1`, il est important de comprendre les différentes méthodes de scan utilisées pour détecter les ports ouverts sur un réseau. Deux méthodes couramment employées sont le **SYN Scan** et le **scan de handshake complet**.

### SYN Scan

Le **SYN Scan** est une technique de scan de ports qui permet d'identifier les ports ouverts sur une machine cible sans établir une connexion TCP complète. Voici un aperçu de cette méthode :

 **Fonctionnement :**
   - Lors d'un SYN Scan, l'outil de scan envoie des paquets TCP avec le drapeau SYN activé à différents ports sur la machine cible.
   - Si un port est ouvert, le serveur répondra avec un paquet SYN-ACK, indiquant qu'il est prêt à établir une connexion.
   - Si le port est fermé, le serveur répondra avec un paquet RST, signalant que la connexion est refusée.
   - Les ports filtrés peuvent ne pas répondre ou répondre avec un paquet ICMP d'erreur.

 ![ipadd](captures/synscan.png)

 
Le SYN Scan est souvent moins détectable car il ne complète pas la connexion TCP. Cela le rend moins visible pour les systèmes de détection d'intrusion.
-Il est généralement plus rapide que les scans complets puisqu'il n'implique pas la finalisation du processus de connexion.

### Scan de Handshake Complet

En revanche, le **scan de handshake complet** (ou **scan TCP connect()**) établit une connexion TCP complète avec la machine cible. Voici comment il fonctionne :

 
   - Le scan débute par l'envoi d'un paquet SYN. Si le port est ouvert, le serveur répondra avec un SYN-ACK, et l'outil de scan enverra un paquet ACK pour compléter le handshake TCP. La connexion est ensuite fermée avec un paquet FIN.
   - Si le port est fermé, le serveur enverra un paquet RST en réponse.
.
    ![ipadd](captures/handshake.png)


   - **Détection :** Le scan de handshake complet établir une connexion complète est plus facile à détecter, ce qui peut rendre le scan plus visible aux systèmes de sécurité.

     ## Capture SYN Scan

Pour capturer et analyser les résultats d'un scan de ports, la commande suivante a été utilisée sur Kali Linux (machine de l'attaquant) pour scanner la machine Metasploitable (machine de vectime) :


 ```bash
     nmap -sS -T4 192.168.10.123
 ```

  ![ipadd](captures/scan.png)


-sS : Effectue un syn scan .

-T4 : Augmente la vitesse du scan pour obtenir les résultats plus rapidement.

Après avoir effectué le scan avec nmap, un filtre a été appliqué dans Wireshark pour isoler les paquets SYN :

 ```bash
     tcp.flags.syn==1
 ```

  ![ipadd](captures/flags.png)


  Lors de l'analyse du trafic réseau capturé pendant un scan de ports, il est important de bien identifier les rôles des machines impliquées : la machine attaquant (qui effectue le scan) et la machine cible (qui reçoit le scan). Voici comment ces rôles sont définis et comment les noms des machines sont modifiés dans Wireshark :

### Définition des Adresses IP

- **Adresse IP de la Machine de l'attaquant :** La machine qui effectue le scan SYN. Dans ce cas, l'adresse IP de la machine attaquante est `192.168.10.219`.
- **Adresse IP de la Machine Cible :** La machine qui est scannée. Dans ce cas, l'adresse IP de la machine cible est `192.168.10.123`.

### Modification des Noms dans Wireshark

Pour faciliter l'analyse dans Wireshark, les noms des machines ont été modifiés comme suit :

1. **Modification du Nom de l'Attaquant**
   - Clic droit sur le premier paquet capturé dans Wireshark.
   - Sélectionner **"Edit Resolved Name"**.
   - Modifier le nom pour refléter l'adresse IP de l'attaquant. Dans ce cas, le nom est changé en **"attacker (192.168.10.219)"**.


2. **Modification du Nom de la Cible**
   - Clic droit sur le premier paquet capturé dans Wireshark.
   - Sélectionner **"Edit Resolved Name"**.
   - Modifier le nom pour refléter l'adresse IP de la cible. Dans ce cas, le nom est changé en **"vectim (192.168.10.123)"**.


      ![ipadd](captures/name.png)

     
    ![ipadd](captures/capture.png)

## Analyse des Ports Ouverts dans wireshark

Pour  analyser spécifiquement les réponses SYN-ACK de la machine cible, un filtre a été appliqué pour isoler ces paquets. Voici les étapes détaillées :
   
### Filtrage des Réponses SYN-ACK

Pour capturer uniquement les réponses SYN-ACK de la machine cible (adresse IP 192.168.10.123), le filtre suivant a été utilisé dans Wireshark :

 ```bash
     tcp.flags.syn==1 and ip.src==192.168.10.123

 ```


![ipadd](captures/openn.png)



Ce filtre permet d'afficher uniquement les paquets SYN-ACK envoyés par la machine cible, indiquant les ports ouverts en réponse aux requêtes SYN de la machine de l'attaquant.


### Analyse des Ports Ouverts

Après avoir appliqué le filtre et capturé les paquets SYN-ACK, il est possible de vérifier les ports ouverts de la machine cible. Dans cet exemple, 22 paquets sont affichés, indiquant que 22 ports sont ouverts.

Pour assurer et visualiser les résultats, les étapes suivantes ont été suivies :

   - Cliquer sur "Statistiques" dans la barre de menu de Wireshark.
   - Sélectionner "Conversations..." pour ouvrir la fenêtre des conversations réseau.
   - Dans la fenêtre des conversations, cliquer sur l'onglet "TCP".


![ipadd](captures/conversations.png)



### Résultat des Ports Ouverts

La fenêtre des conversations TCP affiche toutes les connexions TCP identifiées, y compris les ports ouverts sur la machine cible. Les ports ouverts détectés sont listés, confirmant les résultats du filtre précédent.


## Analyse du Port Spécifique :

Lorsqu'un hacker spécifie un port particulier à attaquer, tel que le port 21, il est crucial d'analyser le trafic associé pour comprendre l'état du port et la réponse du système cible. Dans ce cas, un scan a été effectué sur le port 21 de la machine cible à l'aide de Nmap depuis Kali Linux. 

Le port a été identifié comme ouvert.



Pour analyser ce scan dans Wireshark, le filtre suivant a été utilisé pour capturer les paquets liés à ce port :

 ```bash
     tcp.port==21

 ```

![ipadd](captures/capftp.png)

Wireshark affiche les paquets suivants :

 - Paquet SYN : Envoyé de l'attaquant vers la machine cible (victime), indiquant une tentative de connexion sur le port 21.
 - Paquet SYN-ACK : Réponse de la machine cible à l'attaquant, confirmant que le port 21 est ouvert et prêt à établir une connexion.
 - Paquet RST : Envoyé par l'attaquant à la machine cible pour réinitialiser la connexion, ce qui est une indication que l'attaquant a terminé l'analyse et ne souhaite pas poursuivre la connexion.

Ces trois paquets montrent que le port 21 est ouvert sur la machine cible

### Capture du FTP 

Le hacker décide de se connecter au serveur FTP de la machine cible. Pour ce faire, depuis Kali Linux, la commande suivante est exécutée dans le terminal :

 ```bash
     ftp 192.168.10.123

 ```

![ipadd](captures/capftp2.png)

Lors de cette connexion, l'attaquant entre le nom d'utilisateur et le mot de passe pour accéder au serveur. La connexion est réussie et Wireshark capture l'intégralité de ce processus.

Wireshark capture les échanges entre l'attaquant et le serveur FTP. 

![ipadd](captures/capftp1.png)

Parmi les informations capturées par wireshark :

   - Version du serveur FTP 
   - Nom d'utilisateur (USER) et mot de passe (PASS) 

Pour afficher tous les noms d'utilisateur et mots de passe entrés par l'attaquant pour accéder au serveur FTP, le filtre suivant est utilisé dans Wireshark :

 ```bash
     ftp contains "PASS" || ftp contains "USER"

 ```

![ipadd](captures/capftp3.png)


Ce filtre permet de visualiser spécifiquement les paquets contenant les chaînes FTP "USER" et "PASS", révélant ainsi les identifiants utilisés par l'attaquant.


## Connaître le Système d'Exploitation Cible 

La capacité de déterminer le système d'exploitation de la machine cible peut être essentielle pour une analyse approfondie de la sécurité.

Wireshark permet de réaliser cette identification par empreinte passive (passive fingerprinting) en examinant des valeurs spécifiques dans les en-têtes de paquets réseau. 

Le tableau suivant présente des valeurs courantes utilisées pour l'empreinte passive :

![ipadd](captures/ttl.png)


### Déterminer le Système d'Exploitation a l'aide de Wireshark  

Pour déterminer le système d'exploitation d'une machine cible, j'ai utilisé un exemple de communication Netcat entre deux machines : 

une machine Windows avec l'adresse IP 192.168.10.122 et une machine Ubuntu avec l'adresse IP 192.168.10.128.

Sur la machine Windows, écoutez sur le port 4444 avec la commande PowerShell :

```bash
     ncat -nlvp 4444

 ```

![ipadd](captures/wind.png)

Sur la machine Ubuntu, connectez-vous à la machine Windows en utilisant la commande :
  
```bash
     nc -nv 192.168.10.122 4444

 ```


![ipadd](captures/ubnt.png)

Wireshark capture cette action et permet d'analyser les paquets échangés. En examinant les valeurs des en-têtes des premiers paquets SYN et SYN-ACK, nous pouvons déterminer les systèmes d'exploitation respectifs.

   -Paquet 1 (SYN) envoyé de la machine Ubuntu vers la machine Windows :
        Initial Time to Live : 64
        Don’t Fragment Flag : Set
        Max Segment Size : 1460 Bytes

![ipadd](captures/ttl64.png)

   -Paquet 2 (SYN-ACK) envoyé de la machine Windows vers la machine Ubuntu :
        Initial Time to Live : 128
        Don’t Fragment Flag : Set
        Max Segment Size : 1440 Bytes

![ipadd](captures/ttl128.png)

En utilisant ces valeurs, nous pouvons identifier les systèmes d'exploitation :

   - Ubuntu (Machine 192.168.10.128) :
        TTL = 64, Don’t Fragment Flag = Set, MSS = 1460 Bytes
        Correspond à : Linux

   - Windows (Machine 192.168.10.122) :
        TTL = 128, Don’t Fragment Flag = Set, MSS = 1440 Bytes
        Correspond à : Windows

Ainsi, en analysant seulement deux paquets dans Wireshark, nous avons pu déterminer le système d'exploitation de chaque machine en fonction de leur adresse IP respective.


## Follow TCP Stream

Pour une analyse plus approfondie des actions effectuées par un attaquant, la fonctionnalité "Follow TCP Stream" de Wireshark est très utile. Voici comment cela fonctionne avec un exemple concret.

    
Sur Kali Linux, j'ouvre un terminal et me connecte à la machine Metasploitable2 avec l'adresse IP 192.168.10.123 en utilisant Telnet :

```bash
    telnet 192.168.10.123

 ```

![ipadd](captures/telnet.png)

 Une fois connecté, j'entre le nom d'utilisateur et le mot de passe.

Wireshark capture toutes les communications entre la machine Kali et la machine Metasploitable2 pendant la session Telnet.

![ipadd](captures/telnet2.png)


Pour voir toutes les commandes utilisées par l'attaquant, ainsi que le nom d'utilisateur et le mot de passe, je fais un clic droit sur l'un des paquets Telnet capturés, puis sélectionne Follow > TCP Stream.

La fenêtre "Follow TCP Stream" affiche tout le texte échangé durant la session Telnet.

![ipadd](captures/telnet3.png)

Les commandes entrées par l'attaquant, ainsi que le nom d'utilisateur et le mot de passe utilisés pour se connecter à la machine Metasploitable2, sont visibles.

Cette fonctionnalité permet de visualiser de manière claire et détaillée toutes les actions effectuées par l'attaquant sur la machine cible, facilitant ainsi l'analyse des comportements malveillants.


##    Détection et analyse d'une attaque ARP Spoofing a l'aide de wireshark :

L'ARP spoofing souvent utilisé dans les attaques de l'homme du milieu (MITM) permet à un attaquant d'intercepter le trafic entre deux parties en faisant croire à chacune qu'elle  communique directement avec l'autre.

1) Lorsqu'un appareil cherche à communiquer avec un autre sur un réseau local il envoie une requête ARP pour obtenir son adresse MAC de l'appareil de destination 
2) L'attaquant en falsifiant les réponses ARP se place entre les deux appareils pour 
intercepter tout le trafic. Ainsi chaque appareil pense communiquer directement avec l'autre alors que tout le trafic passe par l'attaquant.
3) L'attaquant intercepte et peut modifier le trafic entre les appareils pour récupérer des informations sensibles.

Dans mon scénario , j’ai une machine d'attaque Kali Linux  une machine ubuntu et une machine windows

 | Machine            | IP Address       | MAC Address            |
 |--------------------|------------------|------------------------|
 | Ubuntu             | 192.168.10.128   | 00:0c:29:3a:e6:63      |         
 | Windows            | 192.168.10.122   | 00:0c:29:79:dc:ec      |
 | Kali (attacker)    | 192.168.10.219   | 00:0c:29:8a:b4:2a      |                                      
                                      
Avant laner l'attaque, nous observons une communication normale entre une machine Windows et une machine Ubuntu, chaque machine utilisant son adresse MAC légitime.

![ipadd](captures/avant.png)


Cependant, une machine Kali est introduite dans le réseau pour lancer une attaque de l'homme du milieu (Man-in-the-Middle) en utilisant Ettercap. Cette attaque repose sur la falsification des tables ARP des machines cibles, leur faisant croire qu'elles communiquent directement entre elles, alors qu'elles communiquent en réalité avec l'attaquant.                                                  


![ipadd](captures/ettercap.png)


Après l'attaque, en ouvrant Wireshark, nous remarquons la présence de trames indiquant que l'adresse MAC 00:0c:29:8a:b4:2a (celle de l'attaquant) est utilisée pour l'adresse IP 192.168.10.219 (adresse de l'attaquant), mais aussi pour la machine Ubuntu ayant l'adresse IP 192.168.10.128. Cette anomalie confirme la présence d'une attaque de type ARP Spoofing.


![ipadd](captures/apres.png)


Pour détecter cette attaque, nous développons un filtre dans Wireshark capable de signaler tous les paquets ARP provenant de l'adresse IP de la machine victime (Ubuntu) mais qui ne correspondent pas à son adresse MAC légitime. Le filtre utilisé est le suivant :


```bash
   ((arp.src.proto_ipv4 == 192.168.10.128) && (arp.opcode == 2)) && !(arp.src.hw_mac == 00:0c:29:3a:e6:63)

 ```

![ipadd](captures/filtre.png)

Ce filtre nous permet de détecter toute tentative de falsification de l'adresse MAC associée à l'adresse IP de la machine Ubuntu, et donc de repérer une attaque ARP Spoofing en cours, mais aussi de surveiller et de prévenir de futures tentatives d'attaques similaires.

## Détection d'une attaque DoS à l'aide de Wireshark

Une attaque de type Denial of Service (DoS) vise à rendre un service ou une machine indisponible en inondant la cible d'un trafic réseau excessif, rendant ainsi ses ressources saturées et incapables de répondre aux demandes légitimes. 

![ipadd](captures/dos.png)

Depuis une machine Kali, j'ai utilisé un script Python qui exécute une attaque DoS sur une machine cible avec l'adresse IP 192.168.10.128


![ipadd](captures/script.png)

ce script envoie un grand nombre de paquets SYN vers la machine cible, saturant ses ressources réseau et provoquant une attaque DoS.


Lors de l'analyse de cette attaque avec Wireshark, nous observons un grand nombre de paquets envoyés à l'adresse IP 192.168.10.128 (la machine Ubuntu). Cela indique qu'une attaque DoS est en cours.


![ipadd](captures/dosattack.png)


Pour mieux comprendre cette attaque, deux filtres différents ont été appliqués dans Wireshark :

```bash
   tcp.flags.syn==1 && tcp.flags.ack==0

 ```

Ce filtre affiche uniquement les paquets SYN sans le drapeau ACK, ce qui correspond à des tentatives de connexion TCP non établies. L'utilisation de ce filtre montre un grand nombre de paquets affichés, indiquant que beaucoup de tentatives de connexion sont en cours, mais aucune n'est terminée.

![ipadd](captures/filtre1.png)


```bash
  tcp.flags.syn==1 && tcp.flags.ack==1

 ```

Ce filtre affiche les paquets où à la fois les drapeaux SYN et ACK sont activés, ce qui signifie que la connexion TCP a été établie. L'application de ce filtre n'affiche aucun paquet, indiquant que la machine cible ne parvient pas à établir une connexion TCP en réponse aux paquets SYN reçus.

![ipadd](captures/filtre2.png)


L'attaque peut également être visualisée dans Wireshark via les I/O Graphs accessibles depuis le menu Statistics. Ce graphe montre une augmentation soudaine du nombre de paquets, ce qui correspond à l'inondation de paquets SYN envoyés lors de l'attaque DoS. Cette visualisation permet de confirmer l'attaque en montrant une nette augmentation du trafic réseau vers la machine cible.

![ipadd](captures/graphe.png)


## Conclusion 

Wireshark est un outil incontournable dans le domaine de l'analyse et de la sécurité des réseaux. Sa capacité à capturer et à analyser le trafic en temps réel permet aux professionnels de la cybersécurité d'obtenir une visibilité approfondie sur l'activité réseau. Grâce à ses puissantes fonctionnalités de filtrage et d'inspection des paquets, Wireshark aide à identifier les anomalies, les tentatives d'intrusion, et d'autres comportements suspects, renforçant ainsi la défense des systèmes informatiques. En somme, Wireshark joue un rôle crucial dans la protection des infrastructures réseau en offrant une analyse détaillée et précise, essentielle pour prévenir et répondre aux menaces de sécurité.
