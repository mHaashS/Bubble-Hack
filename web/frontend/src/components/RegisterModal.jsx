import React, { useState } from 'react';
import authService from '../services/authService';
import EmailVerificationPopup from './EmailVerificationPopup';
import './LoginModal.css';

const RegisterModal = ({ isOpen, onClose, onRegisterSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const validateForm = () => {
        if (formData.password !== formData.confirmPassword) {
            setError('Les mots de passe ne correspondent pas');
            return false;
        }
        if (formData.password.length < 6) {
            setError('Le mot de passe doit contenir au moins 6 caractères');
            return false;
        }
        if (formData.username.length < 3) {
            setError('Le nom d\'utilisateur doit contenir au moins 3 caractères');
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('🚀 Début de la soumission du formulaire');
        setLoading(true);
        setError('');

        if (!validateForm()) {
            console.log('❌ Validation du formulaire échouée');
            setLoading(false);
            return;
        }

        console.log('✅ Validation du formulaire réussie, envoi de la requête...');

        try {
            const { confirmPassword, ...registerData } = formData;
            const result = await authService.register(registerData);
            
            console.log('📡 Résultat de l\'inscription:', result);
            
            if (result.success) {
                console.log('✅ Inscription réussie, préparation de la popup...');
                
                // Appeler la fonction de succès avec l'email pour que App.jsx gère la popup
                onRegisterSuccess(result.user, formData.email);
                console.log('📧 Email passé à App.jsx:', formData.email);
                
            } else {
                console.log('❌ Échec de l\'inscription:', result.error);
                setError(result.error);
            }
        } catch (err) {
            console.log('💥 Erreur lors de l\'inscription:', err);
            setError('Erreur d\'inscription. Veuillez réessayer.');
        } finally {
            setLoading(false);
            console.log('🏁 Fin de la soumission du formulaire');
        }
    };

    if (!isOpen) return null;

    return (
        <>
            <div className="modal-overlay" onClick={onClose}>
                <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                    <div className="modal-header">
                        <h2>Inscription</h2>
                        <button className="close-button" onClick={onClose}>×</button>
                    </div>

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                required
                                placeholder="votre@email.com"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="username">Nom d'utilisateur</label>
                            <input
                                type="text"
                                id="username"
                                name="username"
                                value={formData.username}
                                onChange={handleInputChange}
                                required
                                placeholder="Votre nom d'utilisateur"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Mot de passe</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                required
                                placeholder="Votre mot de passe"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="confirmPassword">Confirmer le mot de passe</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleInputChange}
                                required
                                placeholder="Confirmez votre mot de passe"
                            />
                        </div>

                        {error && <div className="error-message">{error}</div>}

                        <button 
                            type="submit" 
                            className="submit-button"
                            disabled={loading}
                        >
                            {loading ? 'Inscription...' : 'S\'inscrire'}
                        </button>
                    </form>

                    <div className="modal-footer">
                        <p>
                            Déjà un compte ?{' '}
                            <button 
                                className="link-button" 
                                onClick={onSwitchToLogin}
                            >
                                Se connecter
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default RegisterModal; 