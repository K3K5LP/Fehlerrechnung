from PIL import Image, ImageDraw, ImageFont
""" Dieser Code wurde von ChatGPT erstellt
    Falls was nicht funktioniert kein Plan, was hier passiert :)
"""

# A4-Maße bei 300 DPI
A4_BREITE_PX = 3508
A4_HOEHE_PX = 2480
DPI = 600

# Layout
bilder_pro_seite = 6
bilder_gesamt = 6
bilder_pro_zeile = 3
zeilen = 2

# Bildgröße (berechnet auf Basis A4 mit Abstand)
abstand_x, abstand_y = 30, 40
text_hoehe = 30

bild_breite = (A4_BREITE_PX - (bilder_pro_zeile + 1) * abstand_x) // bilder_pro_zeile
bild_hoehe = (A4_HOEHE_PX - (zeilen + 1) * abstand_y - zeilen * text_hoehe) // zeilen

# Schriftart
try:
    schrift = ImageFont.truetype("arial.ttf", 24)
except:
    schrift = ImageFont.load_default()

# Hilfsfunktion für proportional skalierte Bildverkleinerung
def resize_with_aspect(image, target_width, target_height, bg_color=(255, 255, 255)):
    original_width, original_height = image.size
    ratio = min(target_width / original_width, target_height / original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))
    image = image.resize(new_size, Image.LANCZOS)

    new_image = Image.new("RGB", (target_width, target_height), bg_color)
    offset = ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2)
    new_image.paste(image, offset)
    return new_image

# Collage-Seite erzeugen
def erstelle_collage(start_index, seiten_index):
    collage = Image.new('RGB', (A4_BREITE_PX, A4_HOEHE_PX), color='white')
    draw = ImageDraw.Draw(collage)

    bilder_auf_dieser_seite = min(bilder_pro_seite, bilder_gesamt - start_index)

    for i in range(bilder_auf_dieser_seite):
        index = start_index + i + 1
        dateiname = f"Images/Img{index}.png"

        try:
            img = Image.open(dateiname)
            img = resize_with_aspect(img, bild_breite, bild_hoehe)
        except:
            print(f"Fehler beim Laden: {dateiname}")
            continue

        zeile = i // bilder_pro_zeile
        spalte = i % bilder_pro_zeile

        x = abstand_x + spalte * (bild_breite + abstand_x)
        y = abstand_y + zeile * (bild_hoehe + text_hoehe + abstand_y)

        collage.paste(img, (x, y))

        # Text unter dem Bild
        bildname = f"Abbildung Nr: {index}"
        bbox = draw.textbbox((0, 0), bildname, font=schrift)
        text_breite = bbox[2] - bbox[0]
        text_x = x + (bild_breite - text_breite) // 2
        draw.text((text_x, y + 0.85 * bild_hoehe), bildname, fill='black', font=schrift)

    collage.save(f"Collagen/collage_{seiten_index+1}.jpg", dpi=(DPI, DPI))
    print(f"collage_{seiten_index+1}.jpg gespeichert.")

# Hauptlogik
for seite in range((bilder_gesamt + bilder_pro_seite - 1) // bilder_pro_seite):
    start = seite * bilder_pro_seite
    erstelle_collage(start, seite)
