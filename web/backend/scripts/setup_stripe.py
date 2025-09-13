"""
Script pour configurer les produits et prix Stripe
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import stripe
from dotenv import load_dotenv

load_dotenv()

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_products_and_prices():
    """Crée les produits et prix Stripe"""
    
    # Produit Basic
    basic_product = stripe.Product.create(
        name="Bubble Cleaner Basic",
        description="Plan basique avec quotas étendus - 50 images/jour, 200 images/mois",
        metadata={"plan": "basic"}
    )
    
    basic_price = stripe.Price.create(
        product=basic_product.id,
        unit_amount=399,  # 3.99€ en centimes
        currency="eur",
        recurring={"interval": "month"},
        metadata={"plan": "basic"}
    )
    
    # Produit Premium
    premium_product = stripe.Product.create(
        name="Bubble Cleaner Premium",
        description="Plan premium avec quotas illimités",
        metadata={"plan": "premium"}
    )
    
    premium_price = stripe.Price.create(
        product=premium_product.id,
        unit_amount=1699,  # 16.99€ en centimes
        currency="eur",
        recurring={"interval": "month"},
        metadata={"plan": "premium"}
    )
    
    print("✅ Produits et prix Stripe créés:")
    print(f"  - Basic: {basic_price.id} (3.99€/mois)")
    print(f"  - Premium: {premium_price.id} (16.99€/mois)")
    
    return {
        "basic_price_id": basic_price.id,
        "premium_price_id": premium_price.id
    }

def update_database_with_stripe_ids(price_ids):
    """Met à jour la base de données avec les vrais IDs Stripe"""
    from database.database import SessionLocal
    from models import models
    
    db = SessionLocal()
    
    try:
        # Mettre à jour l'abonnement Basic
        basic_sub = db.query(models.Subscription).filter(models.Subscription.name == "Basic").first()
        if basic_sub:
            basic_sub.stripe_price_id = price_ids["basic_price_id"]
            print(f"✅ Basic mis à jour: {price_ids['basic_price_id']}")
        
        # Mettre à jour l'abonnement Premium
        premium_sub = db.query(models.Subscription).filter(models.Subscription.name == "Premium").first()
        if premium_sub:
            premium_sub.stripe_price_id = price_ids["premium_price_id"]
            print(f"✅ Premium mis à jour: {price_ids['premium_price_id']}")
        
        db.commit()
        print("✅ Base de données mise à jour avec les IDs Stripe")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la base de données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if not stripe.api_key:
        print("❌ STRIPE_SECRET_KEY non trouvé dans les variables d'environnement")
        sys.exit(1)
    
    try:
        # Créer les produits et prix Stripe
        price_ids = create_stripe_products_and_prices()
        
        # Mettre à jour la base de données
        update_database_with_stripe_ids(price_ids)
        
        print("\n🎉 Configuration Stripe terminée!")
        print("N'oubliez pas de configurer les webhooks dans le dashboard Stripe:")
        print("  - URL: https://votre-domaine.com/subscription/webhook")
        print("  - Événements: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted, invoice.payment_succeeded, invoice.payment_failed")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration Stripe: {e}")
        sys.exit(1)
