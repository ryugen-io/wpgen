#!/usr/bin/env python3
"""Generate wallpapers using Kitchn theme colors."""

import os
import generator

# Sweet Dracula colors
colors = {
    "bg": "#161925",
    "primary": "#FF79C6",  # Pink
    "secondary": "#BD93F9",  # Purple
    "success": "#50FA7B",  # Green
    "cyan": "#8BE9FD",
    "magenta": "#DE559C",
    "blue": "#9C6FCF",
    "orange": "#FFB86C",
    "yellow": "#F1FA8C",
}

output_dir = "/home/ryu/Pictures/wpgenwalls"
os.makedirs(output_dir, exist_ok=True)

print("🎨 Generating Kitchn Theme Wallpapers...")

# Solid colors (main palette)
solids = ["primary", "secondary", "cyan", "magenta"]
for name in solids:
    config = {
        "mode": "solid",
        "colors": [colors[name]],
        "output_dir": f"{output_dir}/solid_{name}",
    }
    print(f"  • Solid: {name}")
    generator.generate_wallpaper(config)

# Linear gradients (2-color combos)
gradients = [
    ("primary", "secondary"),  # Pink → Purple
    ("cyan", "magenta"),  # Cyan → Magenta
    ("secondary", "cyan"),  # Purple → Cyan
    ("success", "cyan"),  # Green → Cyan
    ("orange", "primary"),  # Orange → Pink
    ("bg", "secondary"),  # Dark → Purple
    ("magenta", "yellow"),  # Magenta → Yellow
]

for c1_name, c2_name in gradients:
    config = {
        "mode": "gradient_linear",
        "colors": [colors[c1_name], colors[c2_name]],
        "output_dir": f"{output_dir}/gradient_{c1_name}_{c2_name}",
    }
    print(f"  • Gradient: {c1_name} → {c2_name}")
    generator.generate_wallpaper(config)

# Mesh gradients (3-color combos)
meshes = [
    ("primary", "secondary", "cyan"),  # Pink, Purple, Cyan
    ("magenta", "blue", "cyan"),  # Magenta, Blue, Cyan
    ("success", "cyan", "blue"),  # Green, Cyan, Blue
    ("orange", "primary", "magenta"),  # Orange, Pink, Magenta
    ("secondary", "primary", "success"),  # Purple, Pink, Green
    ("bg", "secondary", "cyan"),  # Dark, Purple, Cyan
]

for c1_name, c2_name, c3_name in meshes:
    config = {
        "mode": "gradient_mesh",
        "colors": [colors[c1_name], colors[c2_name], colors[c3_name]],
        "output_dir": f"{output_dir}/mesh_{c1_name}_{c2_name}_{c3_name}",
    }
    print(f"  • Mesh: {c1_name}, {c2_name}, {c3_name}")
    generator.generate_wallpaper(config)

print(f"\n✓ Generated {len(solids) + len(gradients) + len(meshes)} wallpaper sets!")
print(f"📁 Saved to: {output_dir}")
