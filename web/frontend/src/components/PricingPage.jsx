import React, { useState, useEffect } from 'react';
import SubscriptionCard from './SubscriptionCard';
import subscriptionService from '../services/subscriptionService';
import authService from '../services/authService';
import './PricingPage.css';

const PricingPage = ({ onClose }) => {
    const [subscriptions, setSubscriptions] = useState([]);
    const [currentPlan, setCurrentPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [darkMode, setDarkMode] = useState(false);

    useEffect(() => {
        initializeSubscriptionService();
        loadData();
        
        // Détecter le mode sombre
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        setDarkMode(savedDarkMode);
        
        // Nettoyer l'URL au chargement de la page
        if (window.location.pathname.includes('/subscription/success')) {
            window.history.replaceState({}, document.title, '/');
        }
    }, []);

    const initializeSubscriptionService = () => {
        subscriptionService.setAuthService(authService);
    };

    const loadData = async () => {
        setLoading(true);
        setError(null);

        try {
            // Charger les abonnements disponibles
            const subscriptionsResult = await subscriptionService.getSubscriptions();
            if (!subscriptionsResult.success) {
                throw new Error(subscriptionsResult.error);
            }

            // Charger le statut d'abonnement de l'utilisateur (si connecté)
            if (authService.isAuthenticated()) {
                const statusResult = await subscriptionService.getSubscriptionStatus();
                if (statusResult.success) {
                    setCurrentPlan(statusResult.status);
                    
                    // Filtrer les abonnements selon le plan actuel
                    const filteredSubscriptions = filterSubscriptionsByCurrentPlan(
                        subscriptionsResult.subscriptions, 
                        statusResult.status
                    );
                    setSubscriptions(filteredSubscriptions);
                } else {
                    // Si pas d'abonnement actif, afficher tous les plans
                    setSubscriptions(subscriptionsResult.subscriptions);
                }
            } else {
                // Si pas connecté, afficher tous les plans
                setSubscriptions(subscriptionsResult.subscriptions);
            }
        } catch (err) {
            console.error('Erreur lors du chargement des données:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const filterSubscriptionsByCurrentPlan = (allSubscriptions, currentPlan) => {
        if (!currentPlan || !currentPlan.current_subscription) {
            // Pas d'abonnement actif, afficher tous les plans
            return allSubscriptions;
        }

        const currentPlanName = currentPlan.current_subscription.subscription.name;
        
        switch (currentPlanName) {
            case 'Free':
                // Free : afficher tous les plans
                return allSubscriptions;
            
            case 'Basic':
                // Basic : afficher Basic et Premium seulement
                return allSubscriptions.filter(sub => 
                    sub.name === 'Basic' || sub.name === 'Premium'
                );
            
            case 'Premium':
                // Premium : afficher Premium seulement
                return allSubscriptions.filter(sub => 
                    sub.name === 'Premium'
                );
            
            default:
                // Plan inconnu, afficher tous les plans
                return allSubscriptions;
        }
    };

    const handleSubscribe = (subscription) => {
        console.log('Souscription à:', subscription.name);
        // La logique de souscription est gérée dans SubscriptionCard
    };

    const handleManage = (subscription) => {
        console.log('Gestion de l\'abonnement:', subscription.name);
        // La logique de gestion est gérée dans SubscriptionCard
    };


    if (loading) {
        return (
            <div className="pricing-page">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Chargement des abonnements...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="pricing-page">
                <div className="error-container">
                    <h2>❌ Erreur</h2>
                    <p>{error}</p>
                    <button onClick={loadData} className="retry-button">
                        Réessayer
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="pricing-page">
            <div className={`pricing-card ${darkMode ? 'dark-mode' : ''}`}>
                <button 
                    className="close-button" 
                    onClick={() => {
                        // Nettoyer l'URL avant de fermer
                        window.history.replaceState({}, document.title, '/');
                        onClose();
                    }}
                    title="Fermer"
                >
                    ×
                </button>
                <div className="pricing-content">
                    <div className="pricing-header">
                    <h1>Choisissez votre plan</h1>
                    <p className="pricing-subtitle">
                        Débloquez tout le potentiel de Bubble Cleaner avec nos abonnements
                    </p>
                    
                    {currentPlan && (
                        <div className="current-plan-info">
                            <p>
                                Plan actuel: <strong>{currentPlan.current_subscription?.subscription?.name || 'Free'}</strong>
                            </p>
                        </div>
                    )}
                </div>

                <div className="pricing-grid">
                    {subscriptions.map((subscription) => (
                        <SubscriptionCard
                            key={subscription.id}
                            subscription={subscription}
                            currentPlan={currentPlan}
                            onSubscribe={handleSubscribe}
                            onManage={handleManage}
                            loading={loading}
                            darkMode={darkMode}
                        />
                    ))}
                </div>

                <div className="pricing-footer">
                <div className="features-overview">
                    <h3>Fonctionnalités incluses</h3>
                    <div className="features-grid">
                        <div className="feature-item">
                            <span className="feature-icon">🤖</span>
                            <div>
                                <h4>IA Avancée</h4>
                                <p>Détection automatique des bulles avec l'IA</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">🌍</span>
                            <div>
                                <h4>Traduction</h4>
                                <p>Traduction automatique en plusieurs langues</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">🎨</span>
                            <div>
                                <h4>Édition</h4>
                                <p>Outils d'édition avancés pour personnaliser</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">⚡</span>
                            <div>
                                <h4>Rapidité</h4>
                                <p>Traitement ultra-rapide de vos images</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="security-info">
                    <h3>🔒 Sécurisé et fiable</h3>
                    <p>
                        Paiements sécurisés par Stripe. Annulez à tout moment. 
                        Vos données sont protégées et ne sont jamais partagées.
                    </p>
                </div>
            </div>
                </div>
            </div>
        </div>
    );
};

export default PricingPage;
