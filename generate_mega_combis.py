#!/usr/bin/env python3
"""Generate MEGA color combinations from Kitchn theme."""

import os
import generator

# Main vibrant colors
colors = {
    "bg": "#161925",
    "fg": "#F8F8F2",
    "primary": "#FF79C6",  # Pink
    "secondary": "#BD93F9",  # Purple
    "success": "#50FA7B",  # Green
    "error": "#FF5555",  # Red
    "warn": "#FFB86C",  # Orange
    "cyan": "#8BE9FD",
    "magenta": "#DE559C",
    "blue": "#9C6FCF",
    "yellow": "#F1FA8C",
    "green": "#2FD651",
    "red": "#DE312B",
    "white": "#D7D4C8",
    "black": "#44475A",
}

output_dir = "/home/ryu/Pictures/wpgenwalls"
os.makedirs(output_dir, exist_ok=True)

# Interesting color pairs for gradients (handpicked combos)
gradient_pairs = [
    # Complementary
    ("primary", "success"),
    ("primary", "cyan"),
    ("secondary", "success"),
    ("secondary", "warn"),
    ("cyan", "warn"),
    ("magenta", "success"),
    ("blue", "warn"),
    ("yellow", "secondary"),
    # Dark to bright
    ("bg", "primary"),
    ("bg", "cyan"),
    ("bg", "success"),
    ("bg", "warn"),
    ("black", "primary"),
    ("black", "cyan"),
    # Vibrant combos
    ("error", "warn"),
    ("error", "yellow"),
    ("success", "yellow"),
    ("cyan", "success"),
    ("magenta", "cyan"),
    ("blue", "cyan"),
    ("red", "yellow"),
    ("green", "cyan"),
    ("primary", "yellow"),
    ("secondary", "cyan"),
]

# Triads for mesh gradients (handpicked)
mesh_triads = [
    # Rainbow vibes
    ("primary", "cyan", "success"),
    ("error", "warn", "yellow"),
    ("magenta", "cyan", "yellow"),
    ("blue", "cyan", "success"),
    # Sunset/Sunrise
    ("error", "warn", "primary"),
    ("warn", "yellow", "fg"),
    ("primary", "warn", "yellow"),
    # Dark to light
    ("bg", "secondary", "primary"),
    ("bg", "blue", "cyan"),
    ("bg", "success", "cyan"),
    ("black", "magenta", "cyan"),
    # Cool tones
    ("secondary", "cyan", "success"),
    ("blue", "cyan", "white"),
    ("secondary", "blue", "cyan"),
    # Warm tones
    ("error", "primary", "warn"),
    ("magenta", "primary", "warn"),
    ("red", "warn", "yellow"),
    # Mixed
    ("success", "cyan", "primary"),
    ("yellow", "cyan", "magenta"),
    ("warn", "cyan", "secondary"),
]

print(f"🎨 Generating {len(gradient_pairs)} gradients + {len(mesh_triads)} meshes...")

# Generate gradients
for c1_name, c2_name in gradient_pairs:
    config = {
        "mode": "gradient_linear",
        "colors": [colors[c1_name], colors[c2_name]],
        "output_dir": f"{output_dir}/grad_{c1_name}_{c2_name}",
    }
    print(f"  🌈 {c1_name} → {c2_name}")
    generator.generate_wallpaper(config)

# Generate meshes
for c1_name, c2_name, c3_name in mesh_triads:
    config = {
        "mode": "gradient_mesh",
        "colors": [colors[c1_name], colors[c2_name], colors[c3_name]],
        "output_dir": f"{output_dir}/mesh_{c1_name}_{c2_name}_{c3_name}",
    }
    print(f"  ✨ {c1_name}/{c2_name}/{c3_name}")
    generator.generate_wallpaper(config)

total_sets = len(gradient_pairs) + len(mesh_triads)
total_files = total_sets * 3
print(f"\n✓ Generated {total_sets} wallpaper sets ({total_files} files)!")
print(f"📁 Saved to: {output_dir}/{{grad,mesh}}_*")
