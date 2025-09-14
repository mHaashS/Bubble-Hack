from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from pydantic import EmailStr

import os

from typing import Optional

from dotenv import load_dotenv



# Charger les variables d'environnement depuis le fichier .env

load_dotenv()



# Configuration pour l'envoi d'emails

# En développement, on peut utiliser un service comme Mailtrap ou Gmail

# En production, utilisez un service d'email comme SendGrid, AWS SES, etc.



def get_email_config():

    """Configuration pour l'envoi d'emails"""

    return ConnectionConfig(

        MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),

        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),

        MAIL_FROM=os.getenv("MAIL_FROM", "noreply@bubblehack.com"),

        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),

        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),

        MAIL_STARTTLS=True,

        MAIL_SSL_TLS=False,

        USE_CREDENTIALS=True,

        VALIDATE_CERTS=True

    )

def get_logo_url():
    """Obtenir l'URL du logo pour les emails"""
    return os.getenv("EMAIL_LOGO_URL", "https://bubblehack.fr/logo-simple.svg")



async def send_password_reset_email(email: EmailStr, username: str, reset_token: str, reset_url: str):

    """Envoyer un email de récupération de mot de passe"""

    try:

        # Configuration de l'email

        conf = get_email_config()

        fm = FastMail(conf)

        

        # Contenu de l'email

        html_content = f"""

        <html>

        <body>

            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">

                <div style="text-align: center; margin-bottom: 30px;">

                    <img src="{get_logo_url()}" alt="Bubble Hack" style="height: 60px; width: auto;">

                </div>

                <h2 style="color: #667eea; text-align: center;">Bubble Hack - Réinitialisation de mot de passe</h2>

                

                <p>Bonjour {username},</p>

                

                <p>Vous avez demandé la réinitialisation de votre mot de passe pour votre compte Bubble Hack.</p>

                

                <p>Cliquez sur le bouton ci-dessous pour réinitialiser votre mot de passe :</p>

                

                <div style="text-align: center; margin: 30px 0;">

                    <a href="{reset_url}" 

                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 

                              color: white; 

                              padding: 12px 24px; 

                              text-decoration: none; 

                              border-radius: 8px; 

                              display: inline-block;">

                        Réinitialiser mon mot de passe

                    </a>

                </div>

                

                <p>Si le bouton ne fonctionne pas, vous pouvez copier et coller ce lien dans votre navigateur :</p>

                <p style="word-break: break-all; color: #667eea;">{reset_url}</p>

                

                <p><strong>Ce lien expirera dans 24 heures.</strong></p>

                

                <p>Si vous n'avez pas demandé cette réinitialisation, vous pouvez ignorer cet email.</p>

                

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">

                

                <p style="color: #6b7280; font-size: 14px; text-align: center;">

                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.

                </p>

            </div>

        </body>

        </html>

        """

        

        # Création du message

        message = MessageSchema(

            subject="Bubble Hack - Réinitialisation de mot de passe",

            recipients=[email],

            body=html_content,

            subtype="html"

        )

        

        # Envoi de l'email

        await fm.send_message(message)

        print(f"✅ Email envoyé avec succès à {email}")

        return True

        

    except Exception as e:

        print(f"❌ Erreur lors de l'envoi de l'email: {e}")

        # En mode développement, on peut simuler l'envoi

        if os.getenv("ENVIRONMENT") == "development":

            print(f"🔧 Mode développement : Email simulé pour {email}")

            print(f"🔗 Lien de récupération : {reset_url}")

            return True

        return False



async def send_welcome_email(email: EmailStr, username: str):
    """Envoyer un email de bienvenue via Mailgun API"""
    try:
        import requests
        
        # Configuration Mailgun
        mailgun_domain = os.getenv("MAILGUN_DOMAIN", "bubblehack.fr")
        mailgun_api_key = os.getenv("MAILGUN_API_KEY", "your-api-key")
        
        # URL de l'API Mailgun (utilise le domaine EU)
        api_url = f"https://api.eu.mailgun.net/v3/{mailgun_domain}/messages"
        
        # Données de l'email
        data = {
            "from": f"Bubble Hack <noreply@{mailgun_domain}>",
            "to": f"{username} <{email}>",
            "subject": "Bienvenue sur Bubble Hack !",
            "text": f"""
Bonjour {username},

Bienvenue sur Bubble Hack ! Votre compte a été créé avec succès.

Vous pouvez maintenant :
- Nettoyer automatiquement les bulles de texte de vos images
- Traduire le contenu des bulles
- Éditer manuellement les zones de bulles
- Gérer vos quotas d'utilisation

Profitez de votre expérience Bubble Hack !

Cordialement,
L'équipe Bubble Hack
            """,
            "html": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bienvenue sur Bubble Hack</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://bubblehack.fr/logo.svg" alt="Bubble Hack" style="height: 60px; width: auto;">
    </div>
    
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #333;">🎉 Bienvenue sur Bubble Hack !</h1>
    </div>
    
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="color: #333; margin-top: 0;">Bonjour {username},</h2>
        <p style="color: #666; line-height: 1.6;">
            Félicitations ! Votre compte Bubble Hack a été créé avec succès. 
            Vous pouvez maintenant profiter de toutes nos fonctionnalités.
        </p>
    </div>
    
    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #2d5a2d; margin-top: 0;">✨ Ce que vous pouvez faire :</h3>
        <ul style="color: #666; line-height: 1.8;">
            <li><strong>🧹 Nettoyer automatiquement</strong> les bulles de texte de vos images</li>
            <li><strong>🌍 Traduire le contenu</strong> des bulles dans votre langue</li>
            <li><strong>✏️ Éditer manuellement</strong> les zones de bulles</li>
            <li><strong>📊 Gérer vos quotas</strong> d'utilisation</li>
        </ul>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="https://bubblehack.fr" 
           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; 
                  padding: 15px 30px; 
                  text-decoration: none; 
                  border-radius: 5px; 
                  font-weight: bold; 
                  display: inline-block;">
            🚀 Commencer maintenant
        </a>
    </div>
    
    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="color: #999; font-size: 12px;">
            Cordialement,<br>
            L'équipe Bubble Hack
        </p>
    </div>
</body>
</html>
            """
        }
        
        print(f"📧 Envoi email de bienvenue via Mailgun API vers {email}")
        print(f"🌐 Domaine Mailgun: {mailgun_domain}")
        
        # Envoi via l'API Mailgun
        response = requests.post(
            api_url,
            auth=("api", mailgun_api_key),
            data=data,
            timeout=30
        )
        
        print(f"📡 Réponse Mailgun (bienvenue): {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Email de bienvenue envoyé à {email}")
            return True
        else:
            print(f"❌ Erreur API Mailgun (bienvenue): {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email de bienvenue: {e}")
        return False

async def send_verification_email(email: EmailStr, username: str, verification_token: str):
    """Envoyer un email de vérification via Mailgun API"""
    try:
        import requests
        
        # Configuration Mailgun
        mailgun_domain = os.getenv("MAILGUN_DOMAIN", "bubblehack.fr")
        mailgun_api_key = os.getenv("MAILGUN_API_KEY", "your-api-key")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        
        # URL de l'API Mailgun (utilise le domaine EU)
        api_url = f"https://api.eu.mailgun.net/v3/{mailgun_domain}/messages"
        
        # URL de vérification
        verification_url = f"{frontend_url}/verify-email?token={verification_token}"
        
        # Données de l'email
        data = {
            "from": f"Bubble Hack <noreply@{mailgun_domain}>",
            "to": f"{username} <{email}>",
            "subject": "Vérification de votre compte Bubble Hack",
            "text": f"""
Bonjour {username},

Bienvenue sur Bubble Hack ! 

Pour activer votre compte, cliquez sur le lien suivant :
{verification_url}

Ce lien est valide pendant 24 heures.

Si vous n'avez pas créé de compte, ignorez cet email.

Cordialement,
L'équipe Bubble Hack
            """,
            "html": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vérification de votre compte</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://bubblehack.fr/logo.svg" alt="Bubble Hack" style="height: 60px; width: auto;">
    </div>
    
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #333;">🎉 Bienvenue sur Bubble Hack !</h1>
    </div>
    
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="color: #333; margin-top: 0;">Bonjour {username},</h2>
        <p style="color: #666; line-height: 1.6;">
            Merci de vous être inscrit sur Bubble Hack ! Pour activer votre compte et commencer à nettoyer vos bulles de manga, 
            cliquez sur le bouton ci-dessous :
        </p>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="{verification_url}" 
           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; 
                  padding: 15px 30px; 
                  text-decoration: none; 
                  border-radius: 5px; 
                  font-weight: bold; 
                  display: inline-block;">
            ✅ Vérifier mon compte
        </a>
    </div>
    
    <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-top: 20px;">
        <p style="color: #856404; margin: 0; font-size: 14px;">
            <strong>⚠️ Important :</strong> Ce lien est valide pendant 24 heures. 
            Si vous n'avez pas créé de compte, ignorez cet email.
        </p>
    </div>
    
    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="color: #999; font-size: 12px;">
            Cordialement,<br>
            L'équipe Bubble Hack
        </p>
    </div>
</body>
</html>
            """
        }
        
        print(f"📧 Envoi email via Mailgun API vers {email}")
        print(f"🌐 Domaine Mailgun: {mailgun_domain}")
        print(f"🔗 URL de vérification: {verification_url}")
        
        # Envoi via l'API Mailgun
        response = requests.post(
            api_url,
            auth=("api", mailgun_api_key),
            data=data,
            timeout=30
        )
        
        print(f"📡 Réponse Mailgun: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Email de vérification envoyé à {email}")
            return True
        else:
            print(f"❌ Erreur API Mailgun: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email de vérification: {e}")
        
        # En mode développement, on peut continuer sans email
        if os.getenv("ENVIRONMENT") == "development":
            print(f"🔧 Mode développement: Email simulé pour {email}")
            print(f"🔗 Token de vérification: {verification_token}")
            return True
        
        return False 