from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frame(video_url, output_path):
    clip = VideoFileClip(video_url)
    frame = clip.get_frame(0)  # Obtener el primer frame del video
    clip.close()
    image = Image.fromarray(frame)  # Convertir el array numpy a una imagen PIL
    image.save(output_path)  # Guardar la imagen

# Llamar a la función con el enlace del video y la ruta de salida para la imagen
extract_frame("https://mediapopa.s3.amazonaws.com/26cd00f9ecc94f4987ae6e7ae6726684.mp4", "screenshot.jpg")
