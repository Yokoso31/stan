import svgwrite
import base64
import os

def create_dino_assets():
    # Base Dino (Standing/Jump)
    dino_base = [
        "                        ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXX WX       ",
        "           XXXXXXXX     ",
        "           XXXXXXX      ",
        "           XXX          ",
        "           XXX          ",
        "          XXXX          ",
        "   XX    XXXXX          ",
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

    # Run Frame 1 (Left leg up)
    dino_run1 = [
        "                        ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXX WX       ",
        "           XXXXXXXX     ",
        "           XXXXXXX      ",
        "           XXX          ",
        "           XXX          ",
        "          XXXX          ",
        "   XX    XXXXX          ",
        "  XXXXXXXXXX            ",
        "  XXXXXXXXXXX           ",
        "  XXXXXXXXXXXX          ",
        "  XXXXXXXXXXXX          ",
        "   XXXXXXXXXX           ",
        "    XXXXXXXX            ",
        "    XX    XX            ",
        "    XX                  ", # Right leg only
        "    XX                  ",
        "    XX                  ",
        "                        ",
        "                        ",
        "                        ",
    ]

    # Run Frame 2 (Right leg up - looks like back leg raised)
    dino_run2 = [
        "                        ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXXXXX       ",
        "           XXX WX       ",
        "           XXXXXXXX     ",
        "           XXXXXXX      ",
        "           XXX          ",
        "           XXX          ",
        "          XXXX          ",
        "   XX    XXXXX          ",
        "  XXXXXXXXXX            ",
        "  XXXXXXXXXXX           ",
        "  XXXXXXXXXXXX          ",
        "  XXXXXXXXXXXX          ",
        "   XXXXXXXXXX           ",
        "    XXXXXXXX            ",
        "    XX    XX            ",
        "          XX            ", # Left leg only
        "          XX            ",
        "           XX           ",
        "                        ",
        "                        ",
        "                        ",
    ]

    def save_svg_base64(grid, filename):
        dwg = svgwrite.Drawing(filename, size=('24px', '24px'))
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == 'X':
                    dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill='#535353'))
                elif char == 'W':
                    dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill='#FFFFFF'))
        dwg.save()

        with open(filename, 'rb') as f:
            data = f.read()
            b64 = base64.b64encode(data).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"

    b64_base = save_svg_base64(dino_base, 'dino_base.svg')
    b64_run1 = save_svg_base64(dino_run1, 'dino_run1.svg')
    b64_run2 = save_svg_base64(dino_run2, 'dino_run2.svg')

    print("FRAME_BASE='" + b64_base + "'")
    print("FRAME_RUN1='" + b64_run1 + "'")
    print("FRAME_RUN2='" + b64_run2 + "'")

if __name__ == "__main__":
    create_dino_assets()
