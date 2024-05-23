import base64
from django.core.files.base import ContentFile

def convert_image_to_base64(image):
    return base64.b64encode(image.read()).decode('utf-8')

def convert_base64_to_image(base64_string, name):
    format, imgstr = base64_string.split(';base64,') 
    ext = format.split('/')[-1] 
    return ContentFile(base64.b64decode(imgstr), name=f"{name}.{ext}")