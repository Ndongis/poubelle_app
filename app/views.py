from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
import requests
import numpy as np
from PIL import Image
import io
import tensorflow as tf

# Charger ton modèle IA (modifier le chemin)
model = tf.keras.models.load_model("my_model.h5")

def preprocess(img):
    img = img.resize((128, 128))
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)

def predict_json(request):
    results = None

    if request.method == "POST" and request.FILES.get("jsonfile"):
        json_file = request.FILES["jsonfile"].read().decode("utf-8")
        data = json.loads(json_file)

        # Le JSON doit contenir une liste : { "images": ["url1", "url2", ...] }
        image_urls = data.get("images", [])

        results = []

        for url in image_urls:
            try:
                # Télécharger l’image
                response = requests.get(url)
                img = Image.open(io.BytesIO(response.content)).convert("RGB")

                # Préprocess & prédiction
                x = preprocess(img)
                pred = model.predict(x)
                predicted_class = int(np.argmax(pred))

                # Ajouter au résultat
                results.append({
                    "url": url,
                    "pred": predicted_class
                })

            except Exception as e:
                results.append({
                    "url": url,
                    "pred": "Erreur"
                })

    return render(request, "predict.html", {"results": results})
