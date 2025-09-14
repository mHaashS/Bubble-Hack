# 🫧 Bubble Hack - Traducteur de Manga IA

> **Transformez vos mangas en quelques clics !** Détection automatique des bulles, traduction intelligente et édition avancée - tout en ligne, sans installation.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/mHaashS/Manga-Bubble-Cleaner)
[![Status](https://img.shields.io/badge/status-live-green.svg)](https://bubblehack.fr)
[![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg)](https://bubblehack.fr)

## ✨ **Pourquoi Bubble Hack ?**

**🎯 Le problème :** Vous avez des mangas en japonais, coréen ou chinois que vous aimeriez lire en français, mais la traduction manuelle prend des heures...

**💡 Ma solution :** Bubble Hack utilise l'intelligence artificielle pour détecter automatiquement les bulles de texte, les traduire et les réinsérer dans l'image - le tout en quelques secondes !

### 🚀 **Fonctionnalités principales**

- **🤖 Détection IA** : Reconnaissance automatique des bulles de texte
- **🌍 Traduction instantanée** : Traduction automatique en français
- **🎨 Édition avancée** : Outils pour ajuster manuellement les bulles et le texte
- **💾 Export multiple** : Export de l'image ou d'un zip
- **🔒 Sécurisé** : Vos images restent privées et sont supprimées après traitement

## 🌐 **Application Web**

### **Accès instantané**
Visitez **[bubblehack.fr](https://bubblehack.fr)** pour utiliser l'application directement dans votre navigateur !

<img width="1899" height="911" alt="Capture d'écran 2025-09-14 181913" src="https://github.com/user-attachments/assets/a9feaadc-32e9-4a3a-81e4-cb1bb908a86f" />
<img width="1899" height="910" alt="Capture d'écran 2025-09-14 182103" src="https://github.com/user-attachments/assets/7bda2148-4333-4051-b1c7-da4ab86f300e" />
<img width="1875" height="902" alt="Capture d'écran 2025-09-14 183155" src="https://github.com/user-attachments/assets/b66b0252-201f-48ab-9bd5-5ee9eb7d6aaa" />
<img width="1899" height="891" alt="Capture d'écran 2025-09-14 182818" src="https://github.com/user-attachments/assets/81d3aaa8-a12e-41a0-8951-d97ba547a577" />
<img width="1884" height="891" alt="Capture d'écran 2025-09-14 182957" src="https://github.com/user-attachments/assets/d997f20b-5142-4194-bb95-f4a7544480ff" />

**✅ Avantages de l'application web :**
- 🚀 **Aucune installation** - Utilisez directement dans votre navigateur
- 📱 **Compatible mobile** - Fonctionne sur tous vos appareils
- 🔄 **Mises à jour automatiques** - Toujours la dernière version
- 👥 **Compte utilisateur** - Gérez vos traductions et abonnements

### **Comment ça marche ?**

1. **📤 Uploadez** vos pages de manga
2. **🤖 L'IA détecte** automatiquement toutes les bulles
3. **🌍 Traduction** instantanée en français
4. **✏️ Éditez** si nécessaire avec les outils
5. **💾 Téléchargez** vos pages traduites

### **Interface moderne**
- **🎨 Thème sombre/clair** - Basculement entre modes clair et sombre
- **📱 Responsive** - S'adapte à la taille de votre écran
- **⚡ Traitement en temps réel** - Suivez l'avancement en direct
- **🛠️ Outils d'édition avancés** - Personnalisez vos traductions

---

## 🎯 **Cas d'usage**

### **📚 Lecteurs de manga**
- Traduisez vos mangas préférés en français
- Lisez sans attendre les traductions officielles
- Découvrez de nouveaux titres dans votre langue

### **🎨 Traducteurs professionnels**
- Accélérez votre workflow de traduction
- Éditez facilement les textes traduits
- Exportez dans tous les formats

### **📖 Éditeurs et scanlators**
- Traitez rapidement de gros volumes
- Maintenez la qualité visuelle des pages
- Optimisez votre temps de production

### **🎓 Étudiants en langues**
- Apprenez en comparant original et traduction
- Améliorez votre compréhension des langues asiatiques
- Pratiquez avec du contenu authentique

---

## 🔒 **Sécurité et Confidentialité**

- **🔐 Chiffrement** : Toutes les données sont chiffrées en transit
- **🗑️ Suppression automatique** : Vos images sont supprimées après traitement
- **👤 Données personnelles** : Nous ne vendons jamais vos informations
- **🛡️ Conformité RGPD** : Respect total de la réglementation européenne
- **🔒 Serveurs sécurisés** : Infrastructure cloud professionnelle

---

## 🔧 **Technologies Utilisées**

### **Frontend (Application Web)**
- **React 18** - Interface utilisateur moderne et réactive
- **Material-UI** - Composants d'interface élégants
- **JavaScript ES6+** - Logique côté client
- **CSS3** - Styles et animations

### **Backend (API)**
- **FastAPI** - API REST moderne et performante
- **Python 3.10** - Langage principal du backend
- **SQLAlchemy** - ORM pour la base de données
- **PostgreSQL** - Base de données relationnelle

### **Intelligence Artificielle**
- **Detectron2** - Détection des bulles avec Mask R-CNN
- **EasyOCR** - Reconnaissance de texte (OCR)
- **OpenAI GPT-3.5** - Traduction automatique
- **OpenCV** - Traitement d'images

### **Infrastructure**
- **Docker** - Conteneurisation
- **Railway** - Hébergement backend
- **Vercel** - Hébergement frontend
- **Stripe** - Paiements et abonnements

---

## 📊 **Comment ça marche ?**

### **1. Détection IA** 🤖
Notre modèle Mask R-CNN entraîné sur des centaines de pages de manga détecte automatiquement les Bulles de dialogue.

### **2. Extraction du texte** 📝
EasyOCR analyse chaque bulle détectée pour extraire le texte original avec une précision de 95%+.

### **3. Traduction intelligente** 🌍
OpenAI GPT-3.5 traduit le texte en conservant le contexte et le style du manga.

### **4. Réinsertion automatique** ✨
Le texte traduit est automatiquement réinséré dans l'image avec :
- **Positionnement précis** dans chaque bulle
- **Ajustement de la taille** de police
- **Centrage automatique** du texte
- **Préservation de l'esthétique** originale

---

## 🚀 **Commencer maintenant**

1. **Visitez** [bubblehack.fr](https://bubblehack.fr)
2. **Créez** votre compte gratuit
3. **Uploadez** votre première page
4. **Profitez** de la traduction automatique !

**C'est tout ! Aucune installation nécessaire.**
