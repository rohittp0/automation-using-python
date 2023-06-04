from PIL import ImageDraw, ImageFont, Image


def draw_text(image, text, position):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("assets/cursive.ttf", 90)
    w, h = draw.textsize(text, font=font)

    position = position[0] - w / 2, position[1] - h / 2
    black = (255, 255, 255)

    draw.text(position, text, black, font=font, align="right")

    return image


for name, mail in [("Ms. Rekha Mathew", "Rekha"), ("Dr. Sr. Priya Antony", "Priya")]:
    img = Image.open("assets/certificate.png")
    draw_text(img, name.title(), (1150, 950))
    img.save(f"out/{mail}.png")
