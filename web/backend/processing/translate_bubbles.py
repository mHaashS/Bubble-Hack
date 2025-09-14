import os

import sys

from PIL import Image

if not hasattr(Image, 'ANTIALIAS'):

    Image.ANTIALIAS = Image.Resampling.LANCZOS

import cv2

import torch

import json

import numpy as np

import easyocr

import openai

import logging

from pathlib import Path



# Patch de compatibilité pour Pillow >= 10.0 (utilisé par easyocr)

try:

    from PIL import Image

    if not hasattr(Image, "Resampling"):

        # Pour compatibilité Pillow < 10

        Image.Resampling = Image

    # Image.LANCZOS est toujours disponible dans Pillow >= 10

except ImportError:

    pass



from detectron2.config import get_cfg

from detectron2.engine import DefaultPredictor

from detectron2 import model_zoo



# Configuration du logging

logger = logging.getLogger(__name__)



# === CONFIGURATION DETECTRON2 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))

# Télécharger le modèle depuis Hugging Face si nécessaire
def get_model_path():
    """Obtenir le chemin du modèle, le télécharger depuis Hugging Face si nécessaire"""
    model_path = os.path.join(PROJECT_DIR, "models_ai", "model_final.pth")
    
    if os.path.exists(model_path):
        print(f"✅ Modèle local trouvé: {model_path}")
        return model_path
    
    print("🔧 Modèle local non trouvé, téléchargement depuis Hugging Face...")
    try:
        from huggingface_hub import hf_hub_download
        import time
        
        # Retry avec timeout
        for attempt in range(3):
            try:
                print(f"🔧 Tentative {attempt + 1}/3...")
                model_path = hf_hub_download(
                    repo_id="HaashS/modelev1",
                    filename="model_final.pth",
                    local_dir=os.path.join(PROJECT_DIR, "models_ai"),
                    local_files_only=False,
                    resume_download=True
                )
                print(f"✅ Modèle téléchargé depuis Hugging Face: {model_path}")
                return model_path
            except Exception as e:
                print(f"⚠️  Tentative {attempt + 1} échouée: {e}")
                if attempt < 2:
                    print("🔄 Nouvelle tentative dans 5 secondes...")
                    time.sleep(5)
                else:
                    raise e
    except Exception as e:
        print(f"❌ Erreur téléchargement Hugging Face après 3 tentatives: {e}")
        raise Exception(f"Impossible de télécharger le modèle depuis Hugging Face: {e}")

# Obtenir le chemin du modèle
model_path = get_model_path()
print(f"🔧 Chemin du modèle: {model_path}")

# Vérifier la taille du fichier
file_size = os.path.getsize(model_path)
print(f"🔧 Taille du fichier: {file_size} bytes")

# Vérifier si le fichier est valide
try:
    import torch
    test_model = torch.load(model_path, map_location='cpu', weights_only=False)
    print(f"✅ Modèle valide (taille: {file_size} bytes)")
    cfg.MODEL.WEIGHTS = model_path
    logger.info(f"Chargement du modèle personnalisé: {model_path}")
except Exception as e:
    logger.error(f"Erreur lors de la validation du modèle personnalisé: {e}")
    print(f"❌ Erreur validation modèle personnalisé: {e}")
    raise Exception(f"Impossible de charger le modèle personnalisé: {e}")

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    predictor = DefaultPredictor(cfg)
    logger.info("Modèle Detectron2 chargé avec succès")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle: {e}")
    predictor = None

reader = easyocr.Reader(['en'], gpu=True)



CLASS_NAMES = {0: "bubble", 1: "floating_text", 2: "narration_box"}



# Configuration OCR

CONFIDENCE_THRESHOLD = 0.5



# === OPENAI (nouvelle API) ===

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:

    raise ValueError("OPENAI_API_KEY environment variable is required")



# Initialisation du client OpenAI avec gestion d'erreur robuste

def create_openai_client():

    """Crée un client OpenAI avec gestion d'erreur pour compatibilité"""

    try:

        # Essai standard

        return openai.OpenAI(api_key=api_key)

    except TypeError as e:

        if "proxies" in str(e):

            # Fallback 1: sans http_client

            try:

                return openai.OpenAI(api_key=api_key, http_client=None)

            except:

                pass

        # Fallback 2: avec paramètres minimaux

        try:

            return openai.OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")

        except:

            pass

        # Fallback 3: approche alternative

        try:

            import httpx

            return openai.OpenAI(api_key=api_key, http_client=httpx.Client())

        except:

            pass

        # Si rien ne marche, on lève l'erreur originale

        raise e



client = create_openai_client()



def translate(text):

    if not text.strip():

        return ""

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {"role": "system", "content": "Tu es un traducteur automatique. Ne commente jamais. Donne uniquement la traduction française brute du texte fourni."},

                {"role": "user", "content": f"Traduis ce texte en français : {text}"}

            ],

            max_tokens=150,

            temperature=0.3

        )

        return response.choices[0].message.content.strip()

    except openai.AuthenticationError:

        logger.error("ERREUR: Erreur d'authentification OpenAI. Verifiez votre cle API.")

        return f"[ERREUR: Clé API invalide]"

    except openai.RateLimitError:

        logger.error("ERREUR: Limite de taux depassee. Attendez avant de reessayer.")

        return f"[ERREUR: Limite de taux]"

    except Exception as e:

        logger.error(f"ERREUR: Erreur de traduction: {e}")

        return f"[ERREUR DE TRADUCTION: {str(e)}]"



def clean_ocr(text):

    return text.replace("\n", " ").replace("  ", " ").strip()



def extract_text_easyocr(image):

    results = reader.readtext(image)

    return " ".join([text for _, text, _ in results]).strip()



def extract_and_translate(image, outputs):

    # Gérer à la fois les outputs de Detectron2 et nos MockOutputs

    if hasattr(outputs, 'instances'):

        # MockOutputs

        instances = outputs.instances

    else:

        # Detectron2 outputs

        instances = outputs["instances"]

    

    masks = instances.pred_masks.to("cpu").numpy()

    classes = instances.pred_classes.to("cpu").numpy()

    scores = instances.scores.to("cpu").numpy()



    results = []

    for i, (mask, class_id, score) in enumerate(zip(masks, classes, scores)):

        if score < CONFIDENCE_THRESHOLD:

            continue



        class_name = CLASS_NAMES.get(class_id, "unknown")

        y_indices, x_indices = np.where(mask)

        if len(x_indices) == 0 or len(y_indices) == 0:

            continue

        x_min, x_max = np.min(x_indices), np.max(x_indices)

        y_min, y_max = np.min(y_indices), np.max(y_indices)



        roi = image[y_min:y_max, x_min:x_max]

        ocr_text = extract_text_easyocr(roi)

        ocr_text = clean_ocr(ocr_text)



        logger.info(f"-> BULLE {i+1}: {class_name}, confidence={score:.2f}")

        logger.info(f"   OCR : {ocr_text}")



        if ocr_text.strip() == "":

            continue



        translated_text = translate(ocr_text)



        results.append({

            "index": len(results) + 1,

            "class": class_name,

            "confidence": float(score),

            "ocr_text": ocr_text,

            "translated_text": translated_text,

            "x_min": int(x_min),

            "x_max": int(x_max),

            "y_min": int(y_min),

            "y_max": int(y_max)

        })

    return results 