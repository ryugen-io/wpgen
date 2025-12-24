import generator
import os


def generate_examples():
    output_dir = "examples"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    presets = [
        {
            "name": "deep_ocean",
            "mode": "gradient_linear",
            "colors": [
                "#0f2027",
                "#203a43",
                "#2c5364",
            ],  # 3rd color ignored by linear currently but good for ref
            "noise": 0.05,
        },
        {
            "name": "sunset_vibes",
            "mode": "gradient_mesh",
            "colors": ["#ff7e5f", "#feb47b", "#ff9966"],
            "noise": 0.08,
        },
        {
            "name": "cotton_candy",
            "mode": "gradient_mesh",
            "colors": ["#a18cd1", "#fbc2eb", "#fad0c4"],
            "noise": 0.0,
        },
        {
            "name": "cyber_neon",
            "mode": "gradient_linear",
            "colors": ["#000000", "#0f9b0f"],  # Black to Green
            "noise": 0.1,
        },
        {
            "name": "midnight_purple",
            "mode": "solid",
            "colors": ["#1a0b2e"],
            "noise": 0.03,
        },
    ]

    print(f"Generating {len(presets)} examples in '{output_dir}'...")

    for p in presets:
        # Hack: The generator currently saves to current dir with fixed names.
        # We need to modify generator.py to accept an output filename or rename after generation.
        # For now, let's just use the generator's internal logic but we will need to rename the output.

        # Actually, looking at generator.py, it hardcodes filenames: "wallpaper_{width}x{height}.png"
        # I should probably update generator.py to accept a prefix or output path,
        # but to be quick and safe, I'll just rename the files after generation.

        config = {
            "mode": p["mode"],
            "colors": p["colors"],
            "noise": p["noise"],
            "logo_path": None,
            "position": "center",
        }

        generator.generate_wallpaper(config)

        # Rename output files
        for res in ["1920x1080", "2560x1440"]:
            src = f"wallpaper_{res}.png"
            dst = os.path.join(output_dir, f"{p['name']}_{res}.png")
            if os.path.exists(src):
                os.rename(src, dst)
                print(f"  -> Created {dst}")


if __name__ == "__main__":
    generate_examples()
