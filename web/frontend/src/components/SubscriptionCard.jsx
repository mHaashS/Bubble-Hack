import React, { useState } from 'react';
import subscriptionService from '../services/subscriptionService';
import './SubscriptionCard.css';

const SubscriptionCard = ({ 
    subscription, 
    currentPlan, 
    onSubscribe, 
    onManage,
    loading = false,
    darkMode = false
}) => {
    const [isLoading, setIsLoading] = useState(false);
    const isCurrentPlan = currentPlan && currentPlan.current_subscription?.subscription?.name === subscription.name;
    const isFree = subscription.name === 'Free';
    const quotas = subscriptionService.getQuotasForPlan(subscription.name);

    const handleSubscribe = async () => {
        if (isFree) return;
        
        setIsLoading(true);
        try {
            // Vérifier si l'utilisateur a déjà un abonnement actif
            const hasActiveSubscription = currentPlan && currentPlan.current_subscription;
            
            if (hasActiveSubscription) {
                // Upgrade/downgrade ou gestion : rediriger vers le portail Stripe
                const result = await subscriptionService.createPortalSession();
                if (result.success) {
                    subscriptionService.redirectToPortal(result.portalUrl);
                } else {
                    if (result.error && result.error.includes('No configuration provided')) {
                        alert('Le portail de gestion des abonnements n\'est pas encore configuré. Veuillez contacter le support.');
                    } else {
                        alert(`Erreur: ${result.error}`);
                    }
                }
            } else {
                // Nouvel abonnement : créer une session de checkout
                const result = await subscriptionService.createCheckoutSession(subscription.name);
                if (result.success) {
                    subscriptionService.redirectToCheckout(result.checkoutUrl);
                } else {
                    alert(`Erreur: ${result.error}`);
                }
            }
        } catch (error) {
            console.error('Erreur lors de la souscription:', error);
            alert('Erreur lors de la souscription');
        } finally {
            setIsLoading(false);
        }
    };


    const renderQuotas = () => {
        if (quotas.unlimited) {
            return (
                <div className="quotas">
                    <div className="quota-item unlimited">
                        <span className="quota-icon">📅</span>
                        <span className="quota-text">∞/jour</span>
                    </div>
                    <div className="quota-item unlimited">
                        <span className="quota-icon">📊</span>
                        <span className="quota-text">∞/mois</span>
                    </div>
                </div>
            );
        }

        return (
            <div className="quotas">
                <div className="quota-item">
                    <span className="quota-icon">📅</span>
                    <span className="quota-text">
                        {subscriptionService.formatQuotaDisplay(quotas.daily)} images/jour
                    </span>
                </div>
                <div className="quota-item">
                    <span className="quota-icon">📊</span>
                    <span className="quota-text">
                        {subscriptionService.formatQuotaDisplay(quotas.monthly)} images/mois
                    </span>
                </div>
            </div>
        );
    };

    const getButtonText = () => {
        if (isLoading && !isFree) return 'Chargement...';
        if (isCurrentPlan) return 'Gérer l\'abonnement';
        if (isFree) return 'Gratuit';
        
        // Vérifier si l'utilisateur a déjà un abonnement actif
        const hasActiveSubscription = currentPlan && currentPlan.current_subscription;
        
        if (hasActiveSubscription) {
            // Si l'utilisateur a un abonnement actif mais ce n'est pas le plan actuel
            // Déterminer si c'est un upgrade ou downgrade
            const currentPlanName = currentPlan.current_subscription.subscription.name;
            const currentPlanPrice = getPlanPrice(currentPlanName);
            const thisPlanPrice = subscription.price;
            
            if (thisPlanPrice > currentPlanPrice) {
                return 'Améliorer l\'abonnement';
            } else {
                return 'Changer d\'abonnement';
            }
        } else {
            return `S'abonner - ${subscriptionService.formatPrice(subscription.price)}`;
        }
    };
    
    const getPlanPrice = (planName) => {
        const planPrices = {
            'Free': 0,
            'Basic': 3.99,
            'Premium': 16.99
        };
        return planPrices[planName] || 0;
    };

    const getButtonAction = () => {
        if (isCurrentPlan && !isFree) return handleSubscribe; // Utiliser handleSubscribe qui redirige vers le portail
        if (isFree) return null;
        return handleSubscribe;
    };

    return (
        <div className={`subscription-card ${isCurrentPlan ? 'current' : ''} ${isFree ? 'free' : ''} ${subscription.name.toLowerCase()} ${darkMode ? 'dark-mode' : ''}`}>
            <div className="card-header">
                <h3 className="plan-name">{subscription.name}</h3>
                <div className="plan-price">
                    {isFree ? (
                        <span className="price-free">Gratuit</span>
                    ) : (
                        <>
                            <span className="price-amount">
                                {subscriptionService.formatPrice(subscription.price)}
                            </span>
                            <span className="price-period">/mois</span>
                        </>
                    )}
                </div>
            </div>

            <div className="card-body">
                <p className="plan-description">{subscription.description}</p>
                
                {renderQuotas()}

                <div className="plan-features">
                    {subscription.name === 'Free' && (
                        <>
                            <div className="feature">✅ Traitement d'images de base</div>
                            <div className="feature">✅ Détection automatique des bulles</div>
                            <div className="feature">✅ Traduction automatique</div>
                        </>
                    )}
                    {subscription.name === 'Basic' && (
                        <>
                            <div className="feature">✅ Tout du plan Free</div>
                            <div className="feature">✅ Quotas étendus</div>
                            <div className="feature">✅ Support prioritaire</div>
                            <div className="feature">✅ Retraitements avancés</div>
                        </>
                    )}
                    {subscription.name === 'Premium' && (
                        <>
                            <div className="feature">✅ Tout du plan Basic</div>
                            <div className="feature">✅ Quotas illimités</div>
                            <div className="feature">✅ Support premium</div>
                            <div className="feature">✅ Fonctionnalités avancées</div>
                        </>
                    )}
                </div>
            </div>

            <div className="card-footer">
                <button
                    className={`subscription-button ${isCurrentPlan ? 'current' : ''} ${isFree ? 'free' : ''} ${subscription.name.toLowerCase()}`}
                    onClick={getButtonAction()}
                    disabled={(isLoading || loading) && !isFree}
                >
                    {getButtonText()}
                </button>
                
            </div>
        </div>
    );
};

export default SubscriptionCard;
