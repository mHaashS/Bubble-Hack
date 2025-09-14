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

                    <img src="{get_logo_url()}" alt="Bubble Cleaner" style="height: 60px; width: auto;">

                </div>

                <h2 style="color: #667eea; text-align: center;">Bubble Cleaner - Réinitialisation de mot de passe</h2>

                

                <p>Bonjour {username},</p>

                

                <p>Vous avez demandé la réinitialisation de votre mot de passe pour votre compte Bubble Cleaner.</p>

                

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

            subject="Bubble Cleaner - Réinitialisation de mot de passe",

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

    """Envoyer un email de bienvenue"""

    try:

        conf = get_email_config()

        fm = FastMail(conf)

        

        html_content = f"""

        <html>

        <body>

            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">

                <div style="text-align: center; margin-bottom: 30px;">

                    <img src="{get_logo_url()}" alt="Bubble Cleaner" style="height: 60px; width: auto;">

                </div>

                <h2 style="color: #667eea; text-align: center;">Bienvenue sur Bubble Cleaner !</h2>

                

                <p>Bonjour {username},</p>

                

                <p>Bienvenue sur Bubble Cleaner ! Votre compte a été créé avec succès.</p>

                

                <p>Vous pouvez maintenant :</p>

                <ul>

                    <li>Nettoyer automatiquement les bulles de texte de vos images</li>

                    <li>Traduire le contenu des bulles</li>

                    <li>Éditer manuellement les zones de bulles</li>

                    <li>Gérer vos quotas d'utilisation</li>

                </ul>

                

                <p>Profitez de votre expérience Bubble Cleaner !</p>

                

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">

                

                <p style="color: #6b7280; font-size: 14px; text-align: center;">

                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.

                </p>

            </div>

        </body>

        </html>

        """

        

        message = MessageSchema(

            subject="Bienvenue sur Bubble Cleaner !",

            recipients=[email],

            body=html_content,

            subtype="html"

        )

        

        await fm.send_message(message)

        return True

        

    except Exception as e:

        print(f"Erreur lors de l'envoi de l'email de bienvenue: {e}")

        return False

async def send_verification_email(email: EmailStr, username: str, verification_token: str):
    """Envoyer un email de vérification"""
    try:
        conf = get_email_config()
        fm = FastMail(conf)
        
        # URL de vérification (à adapter selon votre frontend)
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        verification_url = f"{frontend_url}/verify-email?token={verification_token}"
        
        html_content = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <img src="https://bubblehack.fr/logo.svg" alt="Bubble Cleaner" style="height: 60px; width: auto;">
                </div>
                <h2 style="color: #667eea; text-align: center;">Bubble Cleaner - Vérification d'email</h2>
                
                <p>Bonjour {username},</p>
                
                <p>Merci de vous être inscrit sur Bubble Cleaner ! Pour activer votre compte, veuillez vérifier votre adresse email.</p>
                
                <p>Cliquez sur le bouton ci-dessous pour vérifier votre email :</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 12px 24px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              display: inline-block;">
                        Vérifier mon email
                    </a>
                </div>
                
                <p>Si le bouton ne fonctionne pas, vous pouvez copier et coller ce lien dans votre navigateur :</p>
                <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
                
                <p><strong>Ce lien expirera dans 24 heures.</strong></p>
                
                <p>Une fois votre email vérifié, vous pourrez vous connecter et utiliser toutes les fonctionnalités de Bubble Cleaner.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
                
                <p style="color: #6b7280; font-size: 14px; text-align: center;">
                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                </p>
            </div>
        </body>
        </html>
        """
        
        message = MessageSchema(
            subject="Bubble Cleaner - Vérification d'email",
            recipients=[email],
            body=html_content,
            subtype="html"
        )
        
        await fm.send_message(message)
        print(f"✅ Email de vérification envoyé à {email}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email de vérification: {e}")
        
        # En mode développement, simuler l'envoi
        if os.getenv("ENVIRONMENT") == "development":
            print(f"🔧 Mode développement : Email de vérification simulé pour {email}")
            print(f"🔗 Token de vérification : {verification_token}")
            print(f"🔗 URL de vérification : {verification_url}")
            return True
        return False 