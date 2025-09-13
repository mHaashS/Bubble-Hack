"""
Service Stripe pour la gestion des abonnements et paiements
"""
import stripe
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import models
from crud import crud

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class StripeService:
    def __init__(self):
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    def create_customer(self, user_email: str, user_name: str) -> str:
        """Crée un client Stripe"""
        try:
            customer = stripe.Customer.create(
                email=user_email,
                name=user_name,
                metadata={"user_email": user_email}
            )
            return customer.id
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la création du client Stripe: {str(e)}")
    
    def create_subscription(self, customer_id: str, price_id: str) -> Dict[str, Any]:
        """Crée un abonnement Stripe"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"]
            )
            return subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la création de l'abonnement: {str(e)}")
    
    def create_checkout_session(self, price_id: str, user_email: str, user_name: str, success_url: str, cancel_url: str, customer_id: str = None) -> str:
        """Crée une session de checkout Stripe"""
        try:
            session_params = {
                "payment_method_types": ["card"],
                "line_items": [{
                    "price": price_id,
                    "quantity": 1,
                }],
                "mode": "subscription",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "metadata": {
                    "user_email": user_email,
                    "user_name": user_name
                }
            }
            
            # Utiliser customer_id si fourni, sinon customer_email
            if customer_id:
                session_params["customer"] = customer_id
            else:
                session_params["customer_email"] = user_email
            
            session = stripe.checkout.Session.create(**session_params)
            return session.url
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la création de la session de checkout: {str(e)}")
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Récupère un abonnement Stripe"""
        try:
            return stripe.Subscription.retrieve(subscription_id)
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la récupération de l'abonnement: {str(e)}")
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Annule un abonnement Stripe"""
        try:
            return stripe.Subscription.delete(subscription_id)
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de l'annulation de l'abonnement: {str(e)}")
    
    def create_portal_session(self, customer_id: str, return_url: str) -> str:
        """Crée une session du portail client Stripe"""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            return session.url
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la création de la session du portail: {str(e)}")
    
    def handle_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Traite les webhooks Stripe"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return event
        except ValueError as e:
            raise Exception(f"Payload invalide: {str(e)}")
        except stripe.error.SignatureVerificationError as e:
            raise Exception(f"Signature invalide: {str(e)}")
    
    def get_subscription_quotas(self, subscription_name: str) -> Dict[str, int]:
        """Retourne les quotas selon l'abonnement"""
        quotas = {
            "free": {"daily": 5, "monthly": 5},
            "basic": {"daily": 50, "monthly": 200},
            "premium": {"daily": -1, "monthly": -1}  # -1 = illimité
        }
        return quotas.get(subscription_name.lower(), quotas["free"])

# Instance globale
stripe_service = StripeService()
