import random
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def create_solid_background(width, height, color):
    return Image.new("RGB", (width, height), hex_to_rgb(color))


def create_linear_gradient(width, height, start_color, end_color, direction="vertical"):
    base = Image.new("RGB", (width, height), hex_to_rgb(start_color))
    top = Image.new("RGB", (width, height), hex_to_rgb(end_color))
    mask = Image.new("L", (width, height))
    mask_data = []

    if direction == "vertical":
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
    else:  # horizontal
        for y in range(height):
            row = [int(255 * (x / width)) for x in range(width)]
            mask_data.extend(row)

    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def create_mesh_gradient(width, height, colors):
    """
    Creates a trendy mesh/aurora gradient by placing large blurred orbs.
    colors: list of hex strings
    """
    base_color = hex_to_rgb(colors[0])
    img = Image.new("RGB", (width, height), base_color)

    # We need a robust blur, so we draw on a smaller canvas and upscale for speed + smoothness
    scale_factor = 0.1
    small_w, small_h = int(width * scale_factor), int(height * scale_factor)
    small_img = Image.new("RGB", (small_w, small_h), base_color)
    small_draw = ImageDraw.Draw(small_img)

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Draw random large circles
    for i in range(len(rgb_colors)):
        color = rgb_colors[i]
        # Random position
        x = random.randint(-small_w // 2, small_w + small_w // 2)
        y = random.randint(-small_h // 2, small_h + small_h // 2)
        # Random size
        radius = random.randint(small_w // 3, small_w)

        small_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # Heavy blur on the small image
    small_img = small_img.filter(ImageFilter.GaussianBlur(radius=small_w // 4))

    # Resize back up
    img = small_img.resize((width, height), Image.Resampling.BICUBIC)
    return img


def apply_noise(image, intensity=0.05):
    """
    Adds film grain/noise to the image.
    intensity: 0.0 to 1.0
    """
    if intensity <= 0:
        return image

    width, height = image.size
    # Generate noise array
    noise = np.random.normal(0, 255 * intensity, (height, width, 3)).astype(np.float32)

    # Convert image to numpy
    img_arr = np.array(image).astype(np.float32)

    # Add noise
    noisy_img_arr = img_arr + noise
    noisy_img_arr = np.clip(noisy_img_arr, 0, 255).astype(np.uint8)

    return Image.fromarray(noisy_img_arr)


def composite_logo(background, logo_path, position, scale=1.0):
    try:
        logo = Image.open(logo_path).convert("RGBA")
    except Exception as e:
        # Silently fail - TUI handles errors
        return background

    # Resize logo if needed (optional, keeping it simple for now, maybe max 50% of height)
    # Let's say we don't resize unless strictly requested, but user said "previously edited correctly"
    # So we trust the size, but maybe we ensure it's not BIGGER than the BG.

    bg_w, bg_h = background.size
    logo_w, logo_h = logo.size

    # Calculate coordinates
    x, y = 0, 0
    padding = 50  # padding from edges

    if position == "center":
        x = (bg_w - logo_w) // 2
        y = (bg_h - logo_h) // 2
    elif position == "top_center":
        x = (bg_w - logo_w) // 2
        y = padding
    elif position == "top_left":
        x = padding
        y = padding
    elif position == "top_right":
        x = bg_w - logo_w - padding
        y = padding
    elif position == "bottom_center":
        x = (bg_w - logo_w) // 2
        y = bg_h - logo_h - padding
    elif position == "bottom_left":
        x = padding
        y = bg_h - logo_h - padding
    elif position == "bottom_right":
        x = bg_w - logo_w - padding
        y = bg_h - logo_h - padding

    # Paste with alpha
    background.paste(logo, (x, y), logo)
    return background


def generate_wallpaper(config):
    """
    Main entry point.
    config = {
        'mode': 'solid' | 'gradient_linear' | 'gradient_mesh',
        'colors': ['#ffffff', ...],
        'logo_path': 'path/to/logo.png' | None,
        'position': 'center',
        'noise': 0.05,
        'output_dir': '.'
    }
    """
    resolutions = [(1920, 1080), (2560, 1440)]

    for width, height in resolutions:
        mode = config.get("mode", "solid")
        colors = config.get("colors", ["#000000"])

        if mode == "solid":
            img = create_solid_background(width, height, colors[0])
        elif mode == "gradient_linear":
            c1 = colors[0]
            c2 = colors[1] if len(colors) > 1 else colors[0]
            img = create_linear_gradient(width, height, c1, c2)
        elif mode == "gradient_mesh":
            img = create_mesh_gradient(width, height, colors)

        # Apply noise
        noise_level = config.get("noise", 0)
        if noise_level > 0:
            img = apply_noise(img, noise_level)

        # Composite Logo
        logo_path = config.get("logo_path")
        if logo_path:
            pos = config.get("position", "center")
            img = composite_logo(img, logo_path, pos)

        # Save
        output_dir = config.get("output_dir", ".")
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"wallpaper_{width}x{height}.png")
        img.save(filename)
        # Output handled by TUI


if __name__ == "__main__":
    # Test run
    cfg = {
        "mode": "gradient_mesh",
        "colors": ["#ff0000", "#0000ff", "#00ff00"],
        "noise": 0.05,
    }
    generate_wallpaper(cfg)
