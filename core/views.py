from django.shortcuts import render
from django.conf import settings
import os
from ultralytics import YOLO
import numpy as np
model = YOLO(os.path.join(settings.BASE_DIR, "app", "best.pt"))
n=np.array([1])
def upload_and_predict(request):
    prediction = None
    yolo_image_url = None

    if request.method == "POST":
        image = request.FILES.get("image")

        if image:
            # Sauvegarder l'image
            original_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(original_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Prédiction YOLO
            results = model.predict(original_path,imgsz=320)
            result = results[0]

            # Récupérer la classe détectée
            if result.boxes is not None and len(result.boxes) > 0:
                cls_id = int(result.boxes.cls[0])
                prediction = result.names[cls_id]
            else:
                prediction = "Aucun objet détecté"

            # Sauvegarder l'image annotée
            output_path = os.path.join(settings.MEDIA_ROOT, "yolo_" + image.name)
            result.save(filename=output_path)

            yolo_image_url = settings.MEDIA_URL + "yolo_" + image.name
    print(yolo_image_url)
    return render(request, "upload.html", {
        "prediction": prediction,
        "yolo_image_url": yolo_image_url
    })
