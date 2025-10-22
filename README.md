# 🍽️ Optimisation+ | Plateforme BI Restaurant

Application Streamlit de démonstration pour l'analyse de données en restauration, conçue par des experts pour les restaurateurs québécois.

## 🎯 Fonctionnalités principales

### 📊 Mon Tableau de bord
- **4 KPIs essentiels** : Coût Principal, Ticket moyen, Marge nette, Couverts/jour
- **Statut opérationnel** : Rotation des tables, Performance menu, Taux d'occupation
- **Statut financier** : Coût principal, Marge nette, Coût nourriture, Coût main d'œuvre
- **Actions prioritaires automatiques** basées sur vos données réelles
- **Opportunités identifiées** avec calcul de potentiel de revenus

### ⚙️ Suivi des opérations
- Choix de période : **Aujourd'hui | Cette semaine | 4 semaines roulantes**
- Système de **feux de circulation** (VERT/JAUNE/ROUGE)
- **Prévision prochaine journée** (par heure) : 11h-22h
- **Alertes prédictives** automatiques (affluence, météo, événements)
- Liens vers sections détaillées (Inventaire, Menu, Effectifs)

### 📈 Analyses
**4 sous-sections :**

#### 🍕 Performance du menu
- **Classification intelligente** des plats :
  - ⭐ **Vedettes** : Haute popularité + Haute marge → Conserver
  - 👥 **Populaires** : Haute popularité + Faible marge → Augmenter prix
  - 💎 **Potentiels** : Faible popularité + Haute marge → Promouvoir
  - ⚠️ **À revoir** : Faible popularité + Faible marge → Retirer
- Analyse par catégorie (Entrées, Viandes, Poissons, Pâtes, Pizzas, Burgers)
- Calcul automatique du potentiel de revenus avec ajustements de prix
- Tableau détaillé avec marges et revenus par plat

#### 👥 Effectifs
- Répartition des coûts par poste (Serveurs, Cuisiniers, Aide-cuisine, Plongeurs, Bar, Gérance)
- 4 métriques clés : Coût total, % Coût travail, Taux rotation, Productivité
- **Optimisation des horaires** :
  - Périodes bien staffées vs sous-staffées
  - Recommandations d'économies concrètes
  - Actions requises avec calcul de ROI

#### 📦 Inventaires
- Section préparée pour gestion des stocks
- Alertes de réapprovisionnement
- Analyse du gaspillage

#### 👤 Clients
- Répartition Livraison/Bar/Salle
- Temps de service moyen
- Efficacité du marketing

### 💰 Suivi des coûts et revenus
**3 sous-sections :**

#### 💰 Profitabilité
- Vue d'ensemble Revenus vs Coûts
- Performance financière détaillée
- Métriques : Marge brute, Coût nourriture, Coût personnel

#### 📈 Revenus
- **Prévisions 30 jours** avec intervalle de confiance (94.3% précision)
- Tendances hebdomadaires
- Identification du meilleur jour prévu
- Économies identifiées grâce aux prévisions

#### 💸 Coûts
- Répartition des coûts de main d'œuvre
- Ratio coûts vs revenus (heures pointe vs creuses)
- Efficacité de la planification (85%)

## 🚀 Installation et lancement

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation

```bash
# Cloner le répertoire
cd votre-dossier

# Activer l'environnement virtuel
# Windows (Git Bash)
source venv/Scripts/activate

# Linux/macOS
source venv/bin/activate

# Installer les dépendances
pip install streamlit pandas numpy plotly

# Lancer l'application
streamlit run dashboard_expert.py
```

L'application sera accessible à l'adresse: http://localhost:8501

## 📱 Utilisation

### Filtres disponibles (Sidebar)
- **Période d'analyse**: Aujourd'hui, Cette semaine, 4 semaines roulantes
- **Métrique principale**: Revenus, Couverts, Ticket moyen, Marge
- **KPIs en temps réel**: Revenus 7j, Couverts 7j, Ticket moyen

### Navigation
1. **📊 Mon Tableau de bord** : Vue d'ensemble avec actions prioritaires
2. **⚙️ Suivi des opérations** : Prévisions et alertes quotidiennes
3. **📈 Analyses** : Performance menu, Effectifs, Inventaires, Clients
4. **💰 Suivi coûts et revenus** : Profitabilité, Revenus, Coûts

## 🎓 Points de vente pour le pitch

### KPIs essentiels simplifiés
- ✅ **Coût Principal** : 58.2% (cible < 60%) - Food + Labor combinés
- ✅ **Ticket moyen** : 52.50$ - Montant moyen par client
- ✅ **Marge nette** : 17.8% (cible 15-20%) - Profit réel
- ✅ **Couverts/jour** : 68 clients - Volume d'activité

### ROI démontrable
- **+2,400$/mois** avec optimisation des horaires staffing
- **-780$/mois** en réduction du gaspillage alimentaire
- **+3-5%** de marge globale avec optimisation menu
- **3,840$/mois** d'économies grâce aux prévisions précises (94.3%)

### Avantages compétitifs
- ✅ Interface **100% en français** adaptée au Québec
- ✅ KPIs **simplifiés** (4 au lieu de 7+)
- ✅ Données **réalistes** (patterns québécois)
- ✅ Classification menu **en français** (Vedettes, Populaires, Potentiels, À revoir)
- ✅ Actions **automatiques** basées sur vos données
- ✅ Calculs **intelligents** (potentiel revenus, ROI, seuil rentabilité)

### Cas d'usage concrets
1. **Menu intelligent** : Classification automatique → Plats Vedettes (marge 72%)
2. **Optimisation staffing** : Économies 1,920$/mois sur heures creuses
3. **Prévisions affluence** : Alertes automatiques forte affluence (+45%)
4. **Ajustements prix** : Potentiel +3,200$/mois identifié automatiquement
5. **Rotation tables** : Suivi midi (1.8x) et soir (2.2x) vs cibles

## 💡 Données réalistes de l'industrie

### Patterns hebdomadaires authentiques
- **Vendredi** : 130% (soirée forte)
- **Samedi** : 125% (weekend)
- **Jeudi** : 105% (début weekend)
- **Dimanche** : 100% (brunch)
- **Mercredi** : 90%
- **Mardi** : 80%
- **Lundi** : 75% (journée faible)

### Services réalistes
- **Rush midi** : 12h-13h30 (pic à 12h30) - 42 couverts/heure
- **Creux** : 15h-17h - 5-15 couverts/heure
- **Rush soir** : 18h-21h (pic à 19h-20h) - 65-85 couverts/heure

### Coûts standards industrie
- **Food Cost** : 28-32% des revenus (cible < 32%)
- **Labor Cost** : 30-35% des revenus (cible < 35%)
- **Prime Cost** : < 60% (Food + Labor) - Indicateur #1 santé financière
- **Autres coûts** : ~15% (loyer, électricité, etc.)

### Menu par catégories avec marges réelles
- 🥗 **Entrées** : Marge 78-80% (très rentable)
- 🥩 **Viandes** : Marge 55-65% (moyenne)
- 🐟 **Poissons** : Marge 52% (moyenne-faible)
- 🍝 **Pâtes** : Marge 70-72% (très rentable)
- 🍕 **Pizzas** : Marge 75% (très rentable)
- 🍔 **Burgers** : Marge 68% (bonne)

## 🔧 Personnalisation

Les données sont générées de façon réaliste pour la démo. Pour une utilisation réelle :

1. Remplacer la fonction `generate_data()` par connexion à votre base de données
2. Intégrer vos API (POS, inventaire, météo, etc.)
3. Ajuster les seuils selon vos objectifs (ex: Prime Cost cible, marges)
4. Personnaliser les couleurs et le branding
5. Configurer les alertes automatiques

## 📊 Intégrations possibles

- **Systèmes POS** : Lightspeed, Square, Toast, Clover
- **Inventaire** : Mycawan, MarketMan, SimpleOrder
- **RH/Paie** : Planday, 7shifts, Homebase, Agendrix (Québec)
- **Météo** : OpenWeather API, Weather.com
- **Réseaux sociaux** : Meta Business Suite, Google My Business

## 📈 Métriques techniques

- **Technologies** : Streamlit, Plotly, Pandas, NumPy
- **Responsive** : Optimisé pour desktop et tablette
- **Performance** : Chargement < 2 secondes
- **Langue** : 100% français québécois
- **Données** : Patterns réalistes basés sur l'industrie

## 🎯 Structure du code

```
dashboard_expert.py
├── Configuration & CSS
├── Génération de données réalistes
│   ├── Patterns hebdomadaires (Ven > Sam > Jeu > Dim...)
│   ├── Rush hours (midi 12h30, soir 19h-20h)
│   ├── Coûts réels (Food 28-32%, Labor 30-35%)
│   └── Menu par catégories avec marges
├── Calcul KPIs essentiels
│   ├── Prime Cost (Food + Labor)
│   ├── Rotation tables (midi/soir)
│   ├── Seuil rentabilité
│   └── Marges et profitabilité
├── Sidebar (Filtres)
├── Onglet 1: Mon Tableau de bord
│   ├── 4 KPIs principaux
│   ├── Statut opérations & finances
│   └── Actions prioritaires & opportunités
├── Onglet 2: Suivi des opérations
│   ├── Prévision prochaine journée
│   └── Alertes prédictives
├── Onglet 3: Analyses
│   ├── Performance menu (Classification)
│   ├── Effectifs (Optimisation horaires)
│   ├── Inventaires
│   └── Clients
└── Onglet 4: Suivi coûts et revenus
    ├── Profitabilité
    ├── Revenus (Prévisions 30j)
    └── Coûts (Main d'œuvre)
```

## 🎯 Prochaines étapes après la démo

1. **Audit des données** : Identifier les sources disponibles (POS, inventaire, RH)
2. **POC (2-4 semaines)** : Intégration avec données réelles du restaurant
3. **Formation** : 2-3h pour l'équipe de direction
4. **Déploiement** : Mise en production progressive
5. **Support** : Accompagnement continu et optimisations

## 📞 Support

Pour toute question ou démo personnalisée, contactez notre équipe d'experts en BI restaurant.

---

## 🆕 Dernières améliorations (Version Expert Française)

### Version actuelle : 2.0 - Expert Restaurant Québécois

✅ **100% en français** - Terminologie adaptée aux restaurateurs québécois
✅ **KPIs simplifiés** - 4 indicateurs essentiels au lieu de 7+
✅ **Données réalistes** - Patterns hebdomadaires et rush hours authentiques
✅ **Classification menu française** - Vedettes, Populaires, Potentiels, À revoir
✅ **Actions intelligentes** - Recommandations automatiques basées sur vos données
✅ **Graphique simplifié** - Matrice profitabilité × popularité retirée
✅ **Optimisation horaires** - Déplacée dans Analyses > Effectifs
✅ **Calculs automatiques** - Potentiel revenus, ROI, seuil rentabilité

---

**Optimisation+** - Transformez vos données en décisions rentables 🚀

*Par et pour les restaurateurs québécois* 🇨🇦🍽️