import cv2
import os
import numpy as np

input_dir = "C:\\Users\\willy\\OneDrive\\Bureau\\test_egalisation"
output_dir_clear = "C:\\Users\\willy\\OneDrive\\Bureau\\sauvegarde"
output_dir_obstructed = "C:\\Users\\willy\\OneDrive\\Bureau\\corbeille"

def brighten_image(img):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calculer la luminosité moyenne de l'image
    mean_brightness = gray.mean()

    # Si l'image est sombre, augmenter la luminosité
    if mean_brightness < 100:
        alpha = 1.5
        beta = 50
        brightened = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)

        return brightened

    else:
        print("L'image n'est pas sombre.")
        return img


def detection_finale(input_dir, output_dir_clear, output_dir_obstructed):
    low_contrast_seuil = 60
    # Parcourir les images dans le dossier d'entrée
    for filename in os.listdir(input_dir):
        # Vérifier que le fichier est une image
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Charger l'image
            image = cv2.imread(os.path.join(input_dir, filename))

            # Augmenter la luminosité de l'image si elle est sombre
            brightened = brighten_image(image)

            # Appliquer la détection finale à l'image
            gray = cv2.cvtColor(brightened, cv2.COLOR_BGR2GRAY)
            canny = cv2.Canny(gray, 30, 150)
            # contrast = cv2.Laplacian(gray, cv2.CV_64F).var()

            rel_path = filename
            abs_path = os.path.abspath(rel_path)

            # Déterminer si l'image est obstruée ou non
            if cv2.countNonZero(canny) > 0:
            # if contrast > low_contrast_seuil:
                # L'image est claire, l'enregistrer dans le dossier de sauvegarde
                cv2.imwrite(os.path.join(output_dir_clear, filename), brightened)
                print(abs_path)
            else:
                # L'image est obstruée, l'enregistrer dans le dossier de corbeil
                cv2.imwrite(os.path.join(output_dir_obstructed, filename), brightened)


detection_finale(input_dir, output_dir_clear, output_dir_obstructed)
