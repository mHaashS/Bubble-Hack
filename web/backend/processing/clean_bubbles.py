import os
import cv2
import torch
import numpy as np
import logging
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo

# Configuration du logging
logger = logging.getLogger(__name__)

# === CONFIGURATION DES CHEMINS ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

print(f"🔧 SCRIPT_DIR: {SCRIPT_DIR}")
print(f"🔧 PROJECT_DIR: {PROJECT_DIR}")

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
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3  # bubble, floating_text, narration_box
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"🔧 Device utilisé: {cfg.MODEL.DEVICE}")
print(f"🔧 CUDA disponible: {torch.cuda.is_available()}")

# Chargement paresseux du modèle
predictor = None

def load_predictor():
    """Charger le modèle Detectron2 de manière paresseuse"""
    global predictor
    if predictor is not None:
        print("✅ Modèle déjà chargé, réutilisation")
        return predictor
    
    try:
        print("🔧 Tentative de chargement du modèle Detectron2...")
        print(f"🔧 Configuration: {cfg.MODEL.WEIGHTS}")
        print(f"🔧 Device: {cfg.MODEL.DEVICE}")
        print(f"🔧 Classes: {cfg.MODEL.ROI_HEADS.NUM_CLASSES}")
        
        # Vérifier la mémoire disponible
        import psutil
        memory = psutil.virtual_memory()
        print(f"🔧 Mémoire disponible: {memory.available / 1024**3:.1f} GB")
        print(f"🔧 Mémoire utilisée: {memory.percent}%")
        
        predictor = DefaultPredictor(cfg)
        logger.info("Modèle Detectron2 chargé avec succès")
        print("✅ Modèle Detectron2 chargé avec succès")
        print(f"🔧 Type du predictor: {type(predictor)}")
        
        # Test rapide du modèle
        print("🔧 Test du modèle avec une image factice...")
        import numpy as np
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_output = predictor(test_image)
        print(f"✅ Test du modèle réussi: {len(test_output['instances'])} détections")
        
        return predictor
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle: {e}")
        print(f"❌ Erreur chargement modèle: {e}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Impossible de charger le modèle Detectron2: {e}")

# === PARAMÈTRES DE NETTOYAGE ===
FILL_COLOR = (255, 255, 255)  # Blanc

CLASS_NAMES = {
    0: "bubble",
    1: "floating_text",
    2: "narration_box"
}

def clean_bubbles(image, outputs):
    """
    Nettoie les bulles de texte détectées dans l'image
    """
    # Autoriser le nettoyage même si le modèle n'est pas chargé lorsque des sorties (outputs) sont fournies
    # Le modèle est uniquement nécessaire pour effectuer la détection, pas pour appliquer des masques déjà fournis.
    if outputs is None:
        print("❌ Erreur: Aucune détection fournie (outputs=None)")
        return image  # Retourner l'image originale si aucune détection n'est possible
    
    try:
        # Vérifier si outputs est valide
        if outputs is None:
            print("❌ Erreur: Aucune détection effectuée")
            return image
        
        # Le reste du code reste identique
        result = image.copy()
        height, width = image.shape[:2]
        
        # Créer un masque pour l'inpainting (utilisé pour "floating_text")
        inpaint_mask = np.zeros((height, width), dtype=np.uint8)
        
        # Traiter chaque instance détectée (supporte dict ou objet MockOutputs)
        instances = None
        if isinstance(outputs, dict) and "instances" in outputs:
            instances = outputs["instances"]
        elif hasattr(outputs, "instances"):
            instances = outputs.instances
        
        if instances is not None:
            # Calculer le nombre d'instances de manière robuste (compat MockInstances)
            try:
                num_instances = len(instances)
            except TypeError:
                # Fallback si l'objet n'implémente pas __len__ (MockInstances)
                if hasattr(instances, "pred_masks") and hasattr(instances.pred_masks, "shape"):
                    num_instances = int(instances.pred_masks.shape[0])
                else:
                    num_instances = 0

            if num_instances == 0:
                print("ℹ️  Aucune bulle détectée dans l'image")
                return result
            
            print(f"🔍 Traitement de {num_instances} bulles détectées")
            
            for i in range(num_instances):
                # Récupérer le masque de l'instance
                mask = instances.pred_masks[i].cpu().numpy().astype(np.uint8)
                # Classe si disponible (0: bubble, 1: floating_text, 2: narration_box)
                class_id = None
                if hasattr(instances, "pred_classes"):
                    try:
                        class_id = int(instances.pred_classes[i].item())
                    except Exception:
                        class_id = 0
                else:
                    class_id = 0
                
                # Redimensionner le masque à la taille de l'image si nécessaire
                if mask.shape != (height, width):
                    mask = cv2.resize(mask, (width, height), interpolation=cv2.INTER_NEAREST)
                
                # Si c'est une bulle/boîte de narration → remplissage blanc OPAQUE (avec bord doux)
                if class_id in (0, 2):
                    mask255 = (mask > 0).astype(np.uint8) * 255
                    # Créer une zone intérieure érodée pour garantir un blanc 100% sans fuite de pixels
                    kernel = np.ones((3, 3), np.uint8)
                    eroded = cv2.erode(mask255, kernel, iterations=1)
                    # Bord = masque - intérieur
                    border = cv2.subtract(mask255, eroded)
                    # Remplir en blanc l'intérieur (opaque)
                    result[eroded > 0] = FILL_COLOR
                    # Appliquer un léger feather uniquement sur le bord pour éviter une coupure nette
                    if np.any(border):
                        soft = cv2.GaussianBlur(border, (5, 5), 0)
                        soft = soft.astype(np.float32) / 255.0
                        white = np.full_like(result, FILL_COLOR, dtype=np.uint8)
                        for c in range(3):
                            result[:, :, c] = (
                                soft * white[:, :, c] + (1.0 - soft) * result[:, :, c]
                            ).astype(np.uint8)
                else:
                    # Texte flottant → inpainting local
                    inpaint_mask = cv2.bitwise_or(inpaint_mask, mask)
        
        # Appliquer l'inpainting si des bulles ont été détectées
        if np.any(inpaint_mask):
            print("🎨 Application de l'inpainting...")
            # Dilater légèrement le masque pour couvrir les contours du texte
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(inpaint_mask, kernel, iterations=1)
            # Rayon augmenté pour éviter les artefacts
            result = cv2.inpaint(result, dilated, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
            print("✅ Inpainting terminé")
        else:
            print("ℹ️  Aucune bulle à nettoyer")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        import traceback
        traceback.print_exc()
        return image  # Retourner l'image originale en cas d'erreur 