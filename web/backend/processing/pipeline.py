import cv2
import numpy as np
import logging
import traceback
from .clean_bubbles import clean_bubbles
from .translate_bubbles import extract_and_translate, predictor as translate_predictor
from .reinsert_translations import draw_translated_text
import base64
from PIL import Image  # Ajouté pour le redimensionnement

logger = logging.getLogger(__name__)

def resize_and_pad_cv2(image_cv2, target_size=(800, 1200), fill_color=(255, 255, 255)):
    """
    Redimensionne une image OpenCV à target_size sans déformation, avec padding si besoin.
    """
    original_height, original_width = image_cv2.shape[:2]
    target_width, target_height = target_size
    # Calcul du ratio d'échelle
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    # Redimensionnement
    resized = cv2.resize(image_cv2, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    # Création du fond
    result = np.full((target_height, target_width, 3), fill_color, dtype=np.uint8)
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    result[paste_y:paste_y+new_height, paste_x:paste_x+new_width] = resized
    return result

def process_image_pipeline(image_bytes: bytes) -> bytes:
    """
    Pipeline complet de traitement d'image pour l'API web
    Prend une image en bytes et retourne l'image traitée en bytes
    """
    try:
        # Convertir les bytes en image OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            logger.error("Impossible de décoder l'image")
            return image_bytes
        
        # Redimensionnement à 800x1200 avec padding
        image = resize_and_pad_cv2(image, target_size=(800, 1200))
        
        logger.info("Début du pipeline de traitement")
        
        # Étape 1: Détection et nettoyage des bulles
        logger.info("Étape 1: Détection et nettoyage des bulles...")
        outputs = clean_predictor(image)
        cleaned_image = clean_bubbles(image, outputs)
        logger.info("Nettoyage terminé")
        
        # Étape 2: Extraction et traduction du texte
        logger.info("Étape 2: Extraction et traduction du texte...")
        translations = extract_and_translate(image, outputs)
        logger.info(f"Traduction terminée: {len(translations)} bulles traitées")
        
        # Étape 3: Réinsertion du texte traduit
        if translations:
            logger.info("Étape 3: Réinsertion du texte traduit...")
            final_image = draw_translated_text(cleaned_image, translations)
            logger.info("Réinsertion terminée")
        else:
            logger.info("Aucune traduction à réinsérer, utilisation de l'image nettoyée")
            final_image = cleaned_image
        
        # Convertir l'image finale en bytes
        _, buffer = cv2.imencode('.png', final_image)
        result_bytes = buffer.tobytes()
        
        logger.info("Pipeline terminé avec succès")
        return result_bytes
        
    except Exception as e:
        logger.error(f"Erreur dans le pipeline: {e}")
        traceback.print_exc()
        # En cas d'erreur, retourner l'image originale
        return image_bytes 

def process_image_pipeline_with_bubbles(image_bytes: bytes):
    """
    Pipeline complet qui retourne l'image traitée, l'image nettoyée ET la liste des bulles (texte, coordonnées, etc.)
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("Impossible de décoder l'image")
            return image_bytes, [], None
        # Redimensionnement à 800x1200 avec padding
        image = resize_and_pad_cv2(image, target_size=(800, 1200))
        logger.info("Début du pipeline de traitement (with bubbles)")
        
        # Charger le modèle de manière paresseuse
        from .clean_bubbles import load_predictor
        try:
            print("🔧 Chargement du modèle Detectron2...")
            predictor = load_predictor()
            print(f"🔧 État du predictor: {predictor}")
        except Exception as e:
            print(f"❌ Erreur: Impossible de charger le modèle Detectron2: {e}")
            raise Exception(f"Modèle Detectron2 requis mais non disponible: {e}")
        
        print("🔧 Exécution de la détection...")
        outputs = predictor(image)
        print(f"✅ Détection terminée: {len(outputs['instances'])} objets détectés")
        cleaned_image = clean_bubbles(image, outputs)
        translations = extract_and_translate(image, outputs)
        if translations:
            final_image = draw_translated_text(cleaned_image, translations)
        else:
            final_image = cleaned_image
        _, buffer_final = cv2.imencode('.png', final_image)
        result_bytes = buffer_final.tobytes()
        _, buffer_cleaned = cv2.imencode('.png', cleaned_image)
        cleaned_base64 = base64.b64encode(buffer_cleaned.tobytes()).decode('utf-8')
        return result_bytes, translations, cleaned_base64
    except Exception as e:
        logger.error(f"Erreur dans le pipeline: {e}")
        traceback.print_exc()
        return image_bytes, [], None 