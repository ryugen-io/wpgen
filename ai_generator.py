import torch
import numpy as np
from PIL import Image
from diffusers import DiffusionPipeline
from sklearn.cluster import KMeans

# Global variable to hold the model so we don't reload it every time
_pipe = None


def get_pipeline():
    global _pipe
    if _pipe is not None:
        return _pipe

    print("Loading AI Model (this may take a while on first run)...")
    # Using LCM-Dreamshaper-v7 for fast generation (SD 1.5 based)
    # It generates good images in 4-8 steps.
    model_id = "SimianLuo/LCM_Dreamshaper_v7"

    try:
        pipe = DiffusionPipeline.from_pretrained(
            model_id,
            custom_pipeline="latent_consistency_txt2img",
            custom_revision="main",
        )

        # Use GPU if available
        if torch.cuda.is_available():
            print("CUDA available. Using GPU.")
            pipe.to("cuda")
        else:
            print("CUDA not available. Using CPU (This might be slow).")
            # CPU is slower but works
            pipe.to("cpu")

        _pipe = pipe
        return _pipe
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def generate_image_from_prompt(prompt, output_path="ai_generated.png", steps=4):
    """
    Generates an image from a text prompt using local Stable Diffusion (LCM).
    """
    pipe = get_pipeline()
    if not pipe:
        return None

    # LCM allows very few steps
    images = pipe(
        prompt=prompt,
        num_inference_steps=steps,
        guidance_scale=8.0,
        lcm_origin_steps=50,
    ).images
    image = images[0]
    image.save(output_path)
    return output_path


def extract_palette(image_path, n_colors=3):
    """
    Extracts the dominant colors from an image using K-Means clustering.
    Returns a list of hex color strings.
    """
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
        image = image.resize((100, 100))  # Resize for speed

        # Convert to numpy array
        img_array = np.array(image)
        pixels = img_array.reshape((-1, 3))

        # Use K-Means
        kmeans = KMeans(n_clusters=n_colors, random_state=42)
        kmeans.fit(pixels)

        colors = kmeans.cluster_centers_

        # Convert to Hex
        hex_colors = []
        for color in colors:
            r, g, b = [int(c) for c in color]
            hex_colors.append(f"#{r:02x}{g:02x}{b:02x}")

        return hex_colors
    except Exception as e:
        print(f"Error extracting colors: {e}")
        # Return fallback
        return ["#000000", "#888888", "#ffffff"][:n_colors]


if __name__ == "__main__":
    # Test
    # print(generate_image_from_prompt("cyberpunk city neon lights"))
    pass
