/**
 * Service de gestion des abonnements Stripe
 */

const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? 'https://api.bubblehack.fr'
    : 'http://localhost:8000';

class SubscriptionService {
    constructor() {
        this.authService = null; // Sera injecté depuis authService
    }

    // Injecter le service d'authentification
    setAuthService(authService) {
        this.authService = authService;
    }

    // Headers pour les requêtes authentifiées
    getAuthHeaders() {
        if (!this.authService) {
            throw new Error('AuthService non initialisé');
        }
        return this.authService.getAuthHeaders();
    }

    // Récupérer tous les abonnements disponibles
    async getSubscriptions() {
        try {
            const response = await fetch(`${API_BASE_URL}/subscriptions`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de la récupération des abonnements');
            }

            const subscriptions = await response.json();
            return { success: true, subscriptions };
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des abonnements:', error);
            return { success: false, error: error.message };
        }
    }

    // Récupérer le statut d'abonnement de l'utilisateur
    async getSubscriptionStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/subscription/status`, {
                method: 'GET',
                headers: this.getAuthHeaders(),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de la récupération du statut d\'abonnement');
            }

            const status = await response.json();
            return { success: true, status };
        } catch (error) {
            console.error('❌ Erreur lors de la récupération du statut d\'abonnement:', error);
            return { success: false, error: error.message };
        }
    }

    // Créer une session de checkout pour un abonnement
    async createCheckoutSession(subscriptionName) {
        try {
            const response = await fetch(`${API_BASE_URL}/subscription/checkout`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify({
                    subscription_name: subscriptionName
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de la création de la session de checkout');
            }

            const result = await response.json();
            return { success: true, checkoutUrl: result.checkout_url };
        } catch (error) {
            console.error('❌ Erreur lors de la création de la session de checkout:', error);
            return { success: false, error: error.message };
        }
    }

    // Annuler l'abonnement actuel
    async cancelSubscription() {
        try {
            const response = await fetch(`${API_BASE_URL}/subscription/cancel`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de l\'annulation de l\'abonnement');
            }

            const result = await response.json();
            return { success: true, message: result.message };
        } catch (error) {
            console.error('❌ Erreur lors de l\'annulation de l\'abonnement:', error);
            return { success: false, error: error.message };
        }
    }

    // Créer une session du portail client Stripe
    async createPortalSession() {
        try {
            const response = await fetch(`${API_BASE_URL}/subscription/portal`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de la création de la session du portail');
            }

            const result = await response.json();
            return { success: true, portalUrl: result.portal_url };
        } catch (error) {
            console.error('❌ Erreur lors de la création de la session du portail:', error);
            return { success: false, error: error.message };
        }
    }

    // Rediriger vers Stripe Checkout
    redirectToCheckout(checkoutUrl) {
        if (checkoutUrl) {
            window.location.href = checkoutUrl;
        } else {
            throw new Error('URL de checkout non fournie');
        }
    }

    // Rediriger vers le portail client Stripe
    redirectToPortal(portalUrl) {
        if (portalUrl) {
            window.location.href = portalUrl;
        } else {
            throw new Error('URL du portail non fournie');
        }
    }

    // Formater le prix pour l'affichage
    formatPrice(price, currency = 'EUR') {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: currency,
        }).format(price);
    }

    // Obtenir les quotas selon l'abonnement
    getQuotasForPlan(planName) {
        const quotas = {
            'Free': { daily: 5, monthly: 5, unlimited: false },
            'Basic': { daily: 50, monthly: 200, unlimited: false },
            'Premium': { daily: -1, monthly: -1, unlimited: true }
        };
        return quotas[planName] || quotas['Free'];
    }

    // Formater l'affichage des quotas
    formatQuotaDisplay(quotaValue, isUnlimited = false) {
        if (isUnlimited || quotaValue === -1 || quotaValue === 999999) {
            return '∞';
        }
        return quotaValue.toString();
    }

    // Vérifier si un plan est illimité
    isUnlimited(planName) {
        const quotas = this.getQuotasForPlan(planName);
        return quotas.unlimited;
    }

}

// Instance singleton
const subscriptionService = new SubscriptionService();
export default subscriptionService;
