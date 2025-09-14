import React from 'react';
import './EmailVerificationPopup.css';

const EmailVerificationPopup = ({ isOpen, onClose, email }) => {
  console.log('🎭 EmailVerificationPopup render - isOpen:', isOpen, 'email:', email);
  
  if (!isOpen) {
    console.log('❌ Popup fermée, pas de rendu');
    return null;
  }
  
  console.log('✅ Popup ouverte, rendu en cours...');

  return (
    <div className="email-verification-popup-overlay">
      <div className="email-verification-popup">
        <div className="popup-header">
          <div className="popup-icon">📧</div>
          <h2>Vérification d'email requise</h2>
          <button className="popup-close" onClick={onClose}>×</button>
        </div>
        
        <div className="popup-content">
          <p>
            <strong>Félicitations !</strong> Votre compte a été créé avec succès.
          </p>
          
          <p>
            Pour activer votre compte et commencer à utiliser Bubble Cleaner, 
            veuillez vérifier votre adresse email.
          </p>
          
          <div className="email-info">
            <span className="email-label">Email envoyé à :</span>
            <span className="email-address">{email}</span>
          </div>
          
          <div className="instructions">
            <h3>📋 Instructions :</h3>
            <ol>
              <li>Vérifiez votre boîte de réception</li>
              <li>Cliquez sur le lien de vérification dans l'email</li>
              <li>Vous serez automatiquement connecté</li>
            </ol>
          </div>
          
          <div className="popup-actions">
            <button className="btn-primary" onClick={onClose}>
              J'ai compris
            </button>
          </div>
          
          <div className="help-text">
            <p>
              <small>
                💡 <strong>Astuce :</strong> Vérifiez aussi votre dossier spam si vous ne trouvez pas l'email.
              </small>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailVerificationPopup;
