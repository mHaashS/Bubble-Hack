#!/usr/bin/env python3
"""
Script pour créer un logo optimisé pour les emails
"""

from PIL import Image
import os

def create_email_logo():
    """Créer un logo optimisé pour les emails"""
    
    # Chemin vers le logo ICO existant
    ico_path = "../frontend/public/icone-bubble-hack-rond-light.ico"
    
    try:
        # Ouvrir l'image ICO
        with Image.open(ico_path) as img:
            print(f"✅ Logo ICO chargé: {img.size}")
            
            # Convertir en RGBA pour garder la transparence
            img = img.convert("RGBA")
            
            # Créer une version pour les emails (120x40)
            email_logo = img.resize((120, 40), Image.Resampling.LANCZOS)
            
            # Sauvegarder en PNG
            email_logo_path = "../frontend/public/logo-email.png"
            email_logo.save(email_logo_path, "PNG", optimize=True)
            
            print(f"✅ Logo email créé: {email_logo_path}")
            print(f"📏 Dimensions: {email_logo.size}")
            
            # Créer aussi une version plus grande (200x60)
            large_logo = img.resize((200, 60), Image.Resampling.LANCZOS)
            large_logo_path = "../frontend/public/logo-email-large.png"
            large_logo.save(large_logo_path, "PNG", optimize=True)
            
            print(f"✅ Logo large créé: {large_logo_path}")
            print(f"📏 Dimensions: {large_logo.size}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("📝 Note: Assurez-vous que Pillow est installé (pip install Pillow)")

if __name__ == "__main__":
    create_email_logo()

