import random
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
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
        # Top to bottom
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
    elif direction == "horizontal":
        # Left to right
        for y in range(height):
            row = [int(255 * (x / width)) for x in range(width)]
            mask_data.extend(row)
    elif direction == "diagonal_tl_br":
        # Top-left to bottom-right
        for y in range(height):
            row = []
            for x in range(width):
                # Distance along diagonal (0 to 1)
                progress = (x / width + y / height) / 2
                row.append(int(255 * progress))
            mask_data.extend(row)
    elif direction == "diagonal_tr_bl":
        # Top-right to bottom-left
        for y in range(height):
            row = []
            for x in range(width):
                progress = ((width - x) / width + y / height) / 2
                row.append(int(255 * progress))
            mask_data.extend(row)
    elif direction == "radial":
        # Radial from center
        center_x, center_y = width // 2, height // 2
        max_dist = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5
        for y in range(height):
            row = []
            for x in range(width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                progress = min(dist / max_dist, 1.0)
                row.append(int(255 * progress))
            mask_data.extend(row)
    else:
        # Default to vertical
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)

    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def create_mesh_gradient(
    width, height, colors, blob_count=None, blur_intensity=1.0, blob_size="medium"
):
    """
    Creates a trendy mesh/aurora gradient by placing large blurred orbs.

    Args:
        width, height: Image dimensions
        colors: list of hex strings
        blob_count: Number of blobs (default: len(colors) * 2)
        blur_intensity: Blur strength 0.1-2.0 (default: 1.0)
        blob_size: 'small', 'medium', 'large' (default: 'medium')
    """
    base_color = hex_to_rgb(colors[0])
    img = Image.new("RGB", (width, height), base_color)

    # We need a robust blur, so we draw on a smaller canvas and upscale for speed + smoothness
    # Increased scale_factor from 0.1 to 0.3 for better quality
    scale_factor = 0.3
    small_w, small_h = int(width * scale_factor), int(height * scale_factor)
    small_img = Image.new("RGB", (small_w, small_h), base_color)
    small_draw = ImageDraw.Draw(small_img)

    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Blob count: default to 2x color count for nice coverage
    if blob_count is None:
        blob_count = len(rgb_colors) * 2

    # Blob size ranges
    size_ranges = {
        "small": (small_w // 6, small_w // 2),
        "medium": (small_w // 3, small_w),
        "large": (small_w // 2, int(small_w * 1.5)),
    }
    min_radius, max_radius = size_ranges.get(blob_size, size_ranges["medium"])

    # Draw random large circles
    for i in range(blob_count):
        color = rgb_colors[i % len(rgb_colors)]
        # Random position (can be off-screen for edge blobs)
        x = random.randint(-small_w // 2, small_w + small_w // 2)
        y = random.randint(-small_h // 2, small_h + small_h // 2)
        # Random size
        radius = random.randint(min_radius, max_radius)

        small_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # Apply blur with configurable intensity
    blur_radius = int((small_w // 4) * blur_intensity)
    blur_radius = max(1, blur_radius)  # Ensure at least 1
    small_img = small_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

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


def apply_blur(image, radius=0):
    """Apply Gaussian blur to image."""
    if radius <= 0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def apply_brightness(image, factor=1.0):
    """Adjust image brightness. 1.0 = original, 0.0 = black, 2.0 = very bright."""
    if factor == 1.0:
        return image
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def apply_contrast(image, factor=1.0):
    """Adjust image contrast. 1.0 = original, 0.0 = gray, 2.0 = high contrast."""
    if factor == 1.0:
        return image
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def apply_saturation(image, factor=1.0):
    """Adjust color saturation. 1.0 = original, 0.0 = grayscale, 2.0 = very saturated."""
    if factor == 1.0:
        return image
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def apply_sharpness(image, factor=1.0):
    """Adjust image sharpness. 1.0 = original, 0.0 = blurred, 2.0 = very sharp."""
    if factor == 1.0:
        return image
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def composite_logo(background, logo_path, position, scale=1.0):
    try:
        logo = Image.open(logo_path).convert("RGBA")
    except Exception:
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
        'output_dir': '.',
        'seed': int | None  # Optional: for reproducible randomness
    }
    """
    resolutions = [(1920, 1080), (2560, 1440), (1920, 1200)]

    # Use a fixed seed for consistent randomness across all resolutions
    # User can override with config['seed'] if desired
    seed = config.get("seed", 42)

    for width, height in resolutions:
        # Reset random state before each resolution to ensure identical patterns
        random.seed(seed)
        np.random.seed(seed)

        mode = config.get("mode", "solid")
        colors = config.get("colors", ["#000000"])

        if mode == "solid":
            img = create_solid_background(width, height, colors[0])
        elif mode == "gradient_linear":
            c1 = colors[0]
            c2 = colors[1] if len(colors) > 1 else colors[0]
            direction = config.get("gradient_direction", "vertical")
            img = create_linear_gradient(width, height, c1, c2, direction)
        elif mode == "gradient_mesh":
            blob_count = config.get("mesh_blob_count")
            blur_intensity = config.get("mesh_blur_intensity", 1.0)
            blob_size = config.get("mesh_blob_size", "medium")
            img = create_mesh_gradient(
                width, height, colors, blob_count, blur_intensity, blob_size
            )

        # Apply effects
        noise_level = config.get("noise", 0)
        if noise_level > 0:
            img = apply_noise(img, noise_level)

        blur_radius = config.get("blur", 0)
        if blur_radius > 0:
            img = apply_blur(img, blur_radius)

        brightness = config.get("brightness", 1.0)
        if brightness != 1.0:
            img = apply_brightness(img, brightness)

        contrast = config.get("contrast", 1.0)
        if contrast != 1.0:
            img = apply_contrast(img, contrast)

        saturation = config.get("saturation", 1.0)
        if saturation != 1.0:
            img = apply_saturation(img, saturation)

        sharpness = config.get("sharpness", 1.0)
        if sharpness != 1.0:
            img = apply_sharpness(img, sharpness)

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
        # Output handled by TUI


if __name__ == "__main__":
    # Test run
    cfg = {
        "mode": "gradient_mesh",
        "colors": ["#ff0000", "#0000ff", "#00ff00"],
        "noise": 0.05,
    }
    generate_wallpaper(cfg)
