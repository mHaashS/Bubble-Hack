"""
Script pour mettre à jour manuellement les IDs Stripe
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_stripe_ids_manually():
    """Met à jour manuellement les IDs Stripe"""
    
    # IDs générés par setup_stripe.py
    stripe_ids = {
        "Basic": "price_1S6tqmIJLAMOyQF66QNpeoUv",
        "Premium": "price_1S6tqnIJLAMOyQF6mael9cjG"
    }
    
    print("🔄 Mise à jour manuelle des IDs Stripe")
    print("=" * 50)
    
    # Instructions SQL
    print("Exécutez ces commandes SQL dans votre base de données :")
    print()
    
    for plan_name, price_id in stripe_ids.items():
        sql = f"UPDATE subscriptions SET stripe_price_id = '{price_id}' WHERE name = '{plan_name}';"
        print(f"-- {plan_name}")
        print(sql)
        print()
    
    # Instructions alternatives
    print("Ou utilisez un client PostgreSQL :")
    print("1. Connectez-vous à votre base de données")
    print("2. Exécutez les commandes SQL ci-dessus")
    print("3. Vérifiez avec : SELECT name, stripe_price_id FROM subscriptions;")
    
    print("\n✅ IDs Stripe à utiliser :")
    for plan_name, price_id in stripe_ids.items():
        print(f"  - {plan_name}: {price_id}")

if __name__ == "__main__":
    update_stripe_ids_manually()
