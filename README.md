# 🌱 Système de Gestion Intelligente d’Irrigation 🚰


![Université Ibn Zohr](https://img.shields.io/badge/Université-Ibn%20Zohr-blue)

![Année](https://img.shields.io/badge/Année-2024%2F2025-brightgreen)

![Statut](https://img.shields.io/badge/Statut-En%20développement-yellow)

&nbsp;
&nbsp;


## 🎯 Description du Projet

Ce projet, réalisé dans le cadre du module **Systèmes Répartis & Distribués** à la Faculté des Sciences d’Agadir, vise à développer un système distribué pour la gestion intelligente de l’irrigation dans une ferme.  
L’objectif est d’**optimiser la consommation d’eau** et de **minimiser les interventions humaines** grâce à la surveillance continue de l’humidité du sol et à l’automatisation de l’arrosage.

&nbsp;

## 🏗️ Architecture du Système

- **Microcontrôleur (Arduino/ESP32)**  
  📟 Lecture de l’humidité du sol, décision locale d’activation de la pompe (< 30%), envoi des données au serveur CORBA.

- **Serveur CORBA**  
  🖧 Définit les interfaces IDL, reçoit et stocke les données, fait le lien entre microcontrôleurs et interface web.

- **Base de Données (MySQL)**  
  💾 Stocke les mesures d’humidité et l’état de la pompe, accès CRUD optimisé.

- **Interface Web (Flask)**  
  🌐 Affiche l’état du sol, l’historique d’arrosage et les données en temps réel, interagit avec le serveur CORBA.

&nbsp;

## 🛠️ Technologies Utilisées

| Composant         | Technologie                |
|-------------------|---------------------------|
| Microcontrôleur   | Arduino / ESP32 (C++)     |
| Communication     | CORBA (omniORB)           |
| Base de données   | MySQL                     |
| Interface Web     | Flask (Python), HTML/CSS  |

&nbsp;

## 🧑‍💻 Répartition des Tâches

- **Youssef** : Développement C++ sur microcontrôleur, lecture capteurs, envoi CORBA.
- **Personne B** : Implémentation du serveur CORBA, rédaction IDL, liaison microcontrôleur-serveur, stockage des données.
- **Personne C** : Conception de la base de données, création des tables, intégration avec le serveur CORBA, optimisation des requêtes.
- **Alaeddine** : Développement de l’interface web (Flask), création des vues HTML/CSS, connexion avec CORBA, affichage des données.

&nbsp;

## 🧪 Tests & Validation

- **Tests unitaires** : capteur, logique de seuil, appels distants CORBA, insertion/lecture BDD, interface web dynamique.
- **Intégration** : test de la chaîne complète (capteur → serveur → base → interface).
- **Tests réels** : simulation de variations d’humidité sur prototype.

&nbsp;

## 🚀 Perspectives d’Amélioration

- Ajout de notifications (SMS, mail)
- Interface mobile
- Sécurisation des communications (SSL, authentification)

&nbsp;

## 📝 Conclusion

Ce projet offre une expérience complète de mise en œuvre d’un système distribué, répondant à une problématique concrète de gestion des ressources et préparant à l’intégration système en équipe.



&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;


---

**🌾 Bon développement !**
