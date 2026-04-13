from PIL import Image

img = Image.open("imagenes/Edu1.ico").convert("RGBA")  # tu imagen original
img.save("logo.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (256,256)])
print("Icono creado correctamente 👍")