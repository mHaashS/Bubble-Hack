import React, { useState, useEffect } from 'react';
import './EmailVerification.css';
import authService from '../services/authService';

const EmailVerification = () => {
    const [status, setStatus] = useState('loading'); // loading, success, error
    const [message, setMessage] = useState('');
    const [token, setToken] = useState('');

    useEffect(() => {
        // Récupérer le token depuis l'URL
        const urlParams = new URLSearchParams(window.location.search);
        const tokenFromUrl = urlParams.get('token');
        
        if (tokenFromUrl) {
            setToken(tokenFromUrl);
            verifyEmail(tokenFromUrl);
        } else {
            setStatus('error');
            setMessage('Token de vérification manquant');
        }
    }, []);

    const verifyEmail = async (verificationToken) => {
        try {
            setStatus('loading');
            
            const response = await fetch(`http://localhost:8000/verify-email?token=${verificationToken}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();

            if (response.ok) {
                setStatus('success');
                setMessage('Votre email a été vérifié avec succès ! Vous êtes maintenant connecté.');
                
                // Sauvegarder le token et les données utilisateur
                if (data.access_token && data.user) {
                    authService.setToken(data.access_token);
                    authService.setUser(data.user);
                    console.log('✅ Utilisateur connecté automatiquement après vérification:', data.user.username);
                }
                
                // Rediriger vers la page principale après 2 secondes
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                setStatus('error');
                setMessage(data.detail || 'Erreur lors de la vérification de l\'email');
            }
        } catch (error) {
            setStatus('error');
            setMessage('Erreur de connexion. Veuillez réessayer.');
            console.error('Erreur de vérification:', error);
        }
    };

    const handleResendVerification = async () => {
        try {
            setStatus('loading');
            setMessage('Envoi en cours...');
            
            // Demander l'email à l'utilisateur
            const email = prompt('Veuillez entrer votre adresse email :');
            if (!email) return;

            const response = await fetch('http://localhost:8000/resend-verification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (response.ok) {
                setStatus('success');
                setMessage('Un nouvel email de vérification a été envoyé !');
            } else {
                setStatus('error');
                setMessage(data.detail || 'Erreur lors de l\'envoi de l\'email');
            }
        } catch (error) {
            setStatus('error');
            setMessage('Erreur de connexion. Veuillez réessayer.');
            console.error('Erreur d\'envoi:', error);
        }
    };

    return (
        <div className="email-verification-page">
            <div className="verification-card">
                <div className="verification-header">
                    <h1>Vérification d'Email</h1>
                </div>
                
                <div className="verification-content">
                    {status === 'loading' && (
                        <div className="verification-status loading">
                            <div className="loading-spinner"></div>
                            <p>Vérification en cours...</p>
                        </div>
                    )}
                    
                    {status === 'success' && (
                        <div className="verification-status success">
                            <div className="success-icon">✅</div>
                            <p>{message}</p>
                            <p className="redirect-message">Redirection vers la page principale dans 2 secondes...</p>
                        </div>
                    )}
                    
                    {status === 'error' && (
                        <div className="verification-status error">
                            <div className="error-icon">❌</div>
                            <p>{message}</p>
                            <div className="verification-actions">
                                <button 
                                    onClick={handleResendVerification}
                                    className="resend-button"
                                >
                                    Renvoyer l'email de vérification
                                </button>
                                <button 
                                    onClick={() => window.location.href = '/'}
                                    className="home-button"
                                >
                                    Retour à l'accueil
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default EmailVerification;

