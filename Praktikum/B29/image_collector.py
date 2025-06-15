from PIL import Image, ImageDraw, ImageFont
""" Dieser Code wurde von ChatGPT erstellt
    Falls was nicht funktioniert kein Plan, was hier passiert :)
"""

# A4-Maße bei 300 DPI
A4_BREITE_PX = 2480
A4_HOEHE_PX = 3508
DPI = 600

# Layout
bilder_pro_seite = 17
bilder_gesamt = 51
bilder_pro_zeile = 3
zeilen = 6

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

# Collage-Seite erzeugen
def erstelle_collage(start_index, seiten_index):
    collage = Image.new('RGB', (A4_BREITE_PX, A4_HOEHE_PX), color='white')
    draw = ImageDraw.Draw(collage)

    bilder_auf_dieser_seite = min(bilder_pro_seite, bilder_gesamt - start_index)

    for i in range(bilder_auf_dieser_seite):
        index = start_index + i + 1
        dateiname = f"Images/F{index:04}TEK.jpg"

        try:
            img = Image.open(dateiname)
            img = img.resize((bild_breite, bild_hoehe))
        except:
            print(f"Fehler beim Laden: {dateiname}")
            continue

        zeile = i // bilder_pro_zeile
        spalte = i % bilder_pro_zeile

        x = abstand_x + spalte * (bild_breite + abstand_x)
        y = abstand_y + zeile * (bild_hoehe + text_hoehe + abstand_y)

        collage.paste(img, (x, y))

        # Text unter dem Bild
        bildname = f"Bild Nummer: {index:04}"
        bbox = draw.textbbox((0, 0), bildname, font=schrift)
        text_breite = bbox[2] - bbox[0]
        text_x = x + (bild_breite - text_breite) // 2
        draw.text((text_x, y + bild_hoehe + 5), bildname, fill='black', font=schrift)

    collage.save(f"Collagen/collage_{seiten_index+1}.jpg", dpi=(DPI, DPI))
    print(f"collage_{seiten_index+1}.jpg gespeichert.")

# Hauptlogik
for seite in range((bilder_gesamt + bilder_pro_seite - 1) // bilder_pro_seite):
    start = seite * bilder_pro_seite
    erstelle_collage(start, seite)
