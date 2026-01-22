import svgwrite
from PIL import Image, ImageDraw

def create_dino_assets():
    # 24x24 grid
    # 'X' is black, ' ' is transparent, 'W' is white (eye)
    dino_grid = [
        "                        ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXX WX       ",
        "           XXXXXXXX     ", # Extended snout
        "           XXXXXXX      ", # Jaw
        "           XXX          ",
        "           XXX          ",
        "          XXXX          ", # Arm starts
        "   XX    XXXXX          ", # Arm
        "  XXXXXXXXXX            ",
        "  XXXXXXXXXXX           ",
        "  XXXXXXXXXXXX          ",
        "  XXXXXXXXXXXX          ",
        "   XXXXXXXXXX           ",
        "    XXXXXXXX            ",
        "    XX    XX            ",
        "    XX    XX            ",
        "    XX     XX           ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
    ]

    # Create SVG
    dwg = svgwrite.Drawing('dino.svg', size=('24px', '24px'))
    for y, row in enumerate(dino_grid):
        for x, char in enumerate(row):
            if char == 'X':
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill='#535353'))
            elif char == 'W':
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill='#FFFFFF'))

    dwg.save()

    # Create PNG for verification
    img = Image.new('RGBA', (240, 240), (255, 255, 255, 0)) # 10x scale
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(dino_grid):
        for x, char in enumerate(row):
            color = None
            if char == 'X':
                color = (83, 83, 83, 255)
            elif char == 'W':
                color = (255, 255, 255, 255)

            if color:
                draw.rectangle([x*10, y*10, x*10+10, y*10+10], fill=color)

    img.save('dino_preview.png')
    print("Assets created.")

if __name__ == "__main__":
    create_dino_assets()
