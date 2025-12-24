#!/usr/bin/env python3
"""Generate solid wallpapers for ALL Kitchn theme colors."""

import os
import generator

# ALL Sweet Dracula colors
colors = {
    # Base colors
    "bg": "#161925",
    "fg": "#F8F8F2",
    "cursor": "#8BE9FD",
    "selection_bg": "#44475A",
    "selection_fg": "#F8F8F2",
    "tabs": "#11131C",
    "tabs_active": "#BD93F9",
    # Semantic colors
    "primary": "#FF79C6",
    "secondary": "#BD93F9",
    "success": "#50FA7B",
    "error": "#FF5555",
    "warn": "#FFB86C",
    "info": "#8BE9FD",
    "kitchn": "#BD93F9",
    "summary": "#50FA7B",
    # Standard palette
    "black": "#44475A",
    "red": "#DE312B",
    "green": "#2FD651",
    "yellow": "#D0D662",
    "orange": "#FFB86C",
    "blue": "#9C6FCF",
    "magenta": "#DE559C",
    "cyan": "#6AC5D3",
    "white": "#D7D4C8",
    # Bright palette
    "bright_black": "#656B84",
    "bright_red": "#FF5555",
    "bright_green": "#50FA7B",
    "bright_yellow": "#F1FA8C",
    "bright_blue": "#BD93F9",
    "bright_magenta": "#FF79C6",
    "bright_cyan": "#8BE9FD",
    "bright_white": "#F8F8F2",
}

output_dir = "/home/ryu/Pictures/wpgenwalls"
os.makedirs(output_dir, exist_ok=True)

print(f"🎨 Generating {len(colors)} solid color wallpapers...")

for name, color in sorted(colors.items()):
    config = {
        "mode": "solid",
        "colors": [color],
        "output_dir": f"{output_dir}/mono_{name}",
    }
    print(f"  • {name:20s} {color}")
    generator.generate_wallpaper(config)

print(f"\n✓ Generated {len(colors)} mono wallpaper sets ({len(colors) * 3} files)!")
print(f"📁 Saved to: {output_dir}/mono_*")
