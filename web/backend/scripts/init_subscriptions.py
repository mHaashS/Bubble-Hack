"""
Script pour initialiser les abonnements dans la base de données
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal, engine
from models import models
from crud import crud

def init_subscriptions():
    """Initialise les abonnements dans la base de données"""
    db = SessionLocal()
    
    try:
        # Créer les tables si elles n'existent pas
        models.Base.metadata.create_all(bind=engine)
        
        # Vérifier si les abonnements existent déjà
        existing_subscriptions = crud.get_all_subscriptions(db)
        if existing_subscriptions:
            print("Les abonnements existent déjà dans la base de données.")
            return
        
        # Créer les abonnements
        subscriptions_data = [
            {
                "name": "Free",
                "description": "Plan gratuit avec quotas limités",
                "price": 0.0,
                "currency": "EUR",
                "stripe_price_id": "price_free"  # ID fictif pour le plan gratuit
            },
            {
                "name": "Basic",
                "description": "Plan basique avec quotas étendus",
                "price": 3.99,
                "currency": "EUR",
                "stripe_price_id": "price_basic_399"  # À remplacer par l'ID Stripe réel
            },
            {
                "name": "Premium",
                "description": "Plan premium avec quotas illimités",
                "price": 16.99,
                "currency": "EUR",
                "stripe_price_id": "price_premium_1699"  # À remplacer par l'ID Stripe réel
            }
        ]
        
        for sub_data in subscriptions_data:
            subscription = models.Subscription(**sub_data)
            db.add(subscription)
        
        db.commit()
        print("✅ Abonnements créés avec succès:")
        for sub_data in subscriptions_data:
            print(f"  - {sub_data['name']}: {sub_data['price']}€/mois")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation des abonnements: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_subscriptions()
