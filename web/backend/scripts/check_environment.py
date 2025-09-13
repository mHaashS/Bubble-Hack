"""
Script de diagnostic de l'environnement
"""
import sys
import os

print("🔍 Diagnostic de l'environnement Python")
print("=" * 50)

# 1. Vérifier la version Python
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# 2. Vérifier les modules installés
modules_to_check = [
    'stripe',
    'fastapi',
    'sqlalchemy',
    'pydantic',
    'dotenv'
]

print("\n📦 Modules installés:")
for module in modules_to_check:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError:
        print(f"  ❌ {module} - MANQUANT")

# 3. Vérifier les variables d'environnement
print("\n🔐 Variables d'environnement:")
env_vars = ['STRIPE_SECRET_KEY', 'STRIPE_WEBHOOK_SECRET', 'DATABASE_URL']
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Masquer la clé pour la sécurité
        if 'KEY' in var or 'SECRET' in var:
            print(f"  ✅ {var}: {'*' * 20}")
        else:
            print(f"  ✅ {var}: {value}")
    else:
        print(f"  ❌ {var} - NON DÉFINIE")

# 4. Vérifier le fichier .env
print("\n📁 Fichier .env:")
env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_file):
    print(f"  ✅ .env trouvé: {env_file}")
else:
    print(f"  ❌ .env non trouvé: {env_file}")

print("\n" + "=" * 50)
print("Diagnostic terminé!")
