from PIL import Image, ImageDraw, ImageTk
import io

# Pastel Palette Constants
COLORS = {
    "pink": "#FFB3BA",
    "green": "#BAFFC9",
    "blue": "#BAE1FF",
    "yellow": "#FFFFBA",
    "bg_start": "#FFF0F5",
    "bg_end": "#E6F3FF",
    "text": "#4A4A4A"
}

CATEGORY_COLORS = {
    "Food": COLORS["pink"],
    "Transport": COLORS["blue"],
    "Shopping": "#E6B3FF", # Pastel Purple
    "Utilities": COLORS["yellow"],
    "Entertainment": COLORS["green"],
    "Other": "#FFDFBA" # Pastel Orange
}

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_bg(width, height, start_color, end_color):
    """Generates a vertical gradient background image."""
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return ImageTk.PhotoImage(base)

def create_rounded_rect(width, height, radius, color, alpha=255):
    """Generates a soft rounded rectangle image for use as a container background."""
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    rgb_color = hex_to_rgb(color)
    fill_color = rgb_color + (alpha,)
    
    # Draw rounded rectangle
    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=fill_color
    )
    
    return ImageTk.PhotoImage(img)

def create_color_circle(diameter, color):
    """Generates a simple colored circle for category icons."""
    img = Image.new('RGBA', (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rgb_color = hex_to_rgb(color)
    draw.ellipse([(0, 0), (diameter, diameter)], fill=rgb_color + (200,))
    return ImageTk.PhotoImage(img)
