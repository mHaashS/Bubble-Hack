# Configuration Stripe pour Bubble Cleaner

## 🚀 Configuration initiale

### 1. Variables d'environnement

Ajoutez ces variables à votre fichier `.env` :

```bash
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 2. Initialisation de la base de données

```bash
# Créer les tables
python -m alembic upgrade head

# Initialiser les abonnements
python scripts/init_subscriptions.py
```

### 3. Configuration des produits Stripe

```bash
# Créer les produits et prix dans Stripe
python scripts/setup_stripe.py
```

### 4. Configuration des webhooks

Dans le dashboard Stripe, configurez un webhook avec :
- **URL** : `https://votre-domaine.com/subscription/webhook`
- **Événements** :
  - `checkout.session.completed`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.payment_succeeded`
  - `invoice.payment_failed`

### 5. Test de l'intégration

```bash
# Tester l'intégration Stripe
python scripts/test_stripe_integration.py
```

## 📋 Fonctionnalités implémentées

### ✅ Abonnements
- **Free** : 5 images/jour, 5 images/mois
- **Basic** : 50 images/jour, 200 images/mois (3.99€/mois)
- **Premium** : Illimité (16.99€/mois)

### ✅ API Endpoints
- `GET /subscriptions` - Liste des abonnements
- `GET /subscription/status` - Statut de l'abonnement utilisateur
- `POST /subscription/checkout` - Créer une session de checkout
- `POST /subscription/cancel` - Annuler un abonnement
- `POST /subscription/portal` - Accéder au portail client
- `POST /subscription/webhook` - Webhook Stripe

### ✅ Gestion des quotas
- Quotas quotidiens et mensuels
- Reset automatique des quotas
- Gestion des retraitements par image
- Support des superutilisateurs

## 🔧 Dépannage

### Problèmes courants

1. **Webhook non reçu**
   - Vérifiez l'URL du webhook
   - Vérifiez la signature du webhook
   - Consultez les logs Stripe

2. **Customer_id manquant**
   - L'utilisateur doit d'abord créer un abonnement
   - Vérifiez que le webhook `checkout.session.completed` fonctionne

3. **Quotas non mis à jour**
   - Vérifiez que les webhooks sont bien reçus
   - Vérifiez les logs de l'application

### Logs utiles

```bash
# Vérifier les webhooks reçus
tail -f logs/app.log | grep webhook

# Vérifier les erreurs Stripe
tail -f logs/app.log | grep stripe
```

## 🧪 Tests

### Test manuel avec Stripe CLI

```bash
# Écouter les webhooks localement
stripe listen --forward-to localhost:8000/subscription/webhook

# Déclencher des événements de test
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted
```

### Test des quotas

1. Créez un utilisateur de test
2. Vérifiez les quotas initiaux (Free)
3. Créez un abonnement Basic
4. Vérifiez que les quotas sont mis à jour
5. Testez l'annulation d'abonnement

## 📚 Documentation Stripe

- [Documentation Stripe](https://stripe.com/docs)
- [Webhooks Stripe](https://stripe.com/docs/webhooks)
- [Checkout Stripe](https://stripe.com/docs/checkout)
- [Customer Portal](https://stripe.com/docs/billing/subscriptions/customer-portal)
