# wpgen

A fancy, modern wallpaper generator with a Terminal User Interface (TUI).

## Features

### Generation Modes
- **Solid Color** - Clean, single-color backgrounds
- **Linear Gradient** - 5 direction options (vertical, horizontal, diagonal TL→BR, diagonal TR→BL, radial)
- **Mesh Gradient** - Apple-style aurora/blob gradients with customizable blob count, size, and blur intensity

### Resolutions
Generates wallpapers in three resolutions simultaneously:
- 1920x1080 (Full HD)
- 2560x1440 (QHD)
- 1920x1200 (WUXGA)

### Effects & Adjustments
- **Noise/Grain** (0.0-0.2) - Film grain texture
- **Blur** (0-10) - Gaussian blur
- **Brightness** (0.5-2.0) - Adjust brightness
- **Contrast** (0.5-2.0) - Adjust contrast
- **Saturation** (0.0-2.0) - Adjust color intensity
- **Sharpness** (0.0-2.0) - Adjust sharpness

### Additional Features
- **Logo Overlay** - Composite transparent logos at 7 positions (center, corners, edges)
- **AI Generation** - Optional AI-powered wallpaper generation
- **Custom Output Directory** - Specify where to save wallpapers
- **Kitchn Theme Integration** - Automatically matches your system theme via Kitchn

### Interface
- Fully interactive TUI built with Textual
- Mouse and keyboard support
- Real-time status logging
- Dynamic UI that shows/hides relevant options

## Installation

### Quick Install (Recommended)
Run the installation script to create a standalone binary:
```bash
chmod +x install.sh
./install.sh
```

This will compile wpgen to `~/.local/bin/wpgen` using PyInstaller.

### Manual Installation
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Binary
After installation, simply run:
```bash
wpgen
```

### Using Python Directly
```bash
source .venv/bin/activate
python tui.py
```

### TUI Workflow
1. Select your **Mode** (Solid, Linear Gradient, Mesh Gradient)
2. Enter **Hex Colors** (e.g., `#FF79C6`)
3. For gradients:
   - **Linear**: Choose direction (vertical/horizontal/diagonal/radial)
   - **Mesh**: Adjust blob count, blur intensity, and blob size
4. (Optional) Adjust **Effects**: noise, blur, brightness, contrast, saturation, sharpness
5. (Optional) Enable **Logo** overlay and select position
6. (Optional) Enable **AI Generation**
7. (Optional) Set **Output Directory** (defaults to current directory)
8. Click **Generate Wallpapers**

## Kitchn Integration

wpgen integrates with [Kitchn](https://github.com/yourusername/kitchn) theme management:

1. The TUI automatically uses your Kitchn theme colors
2. Generate wallpapers from theme colors using provided scripts:
   ```bash
   python generate_kitchn_walls.py    # Curated combinations
   python generate_all_mono.py        # All solid colors
   python generate_mega_combis.py     # Massive variety pack
   ```

To update the theme integration:
```bash
kitchn stock wp-gen-tui.ing
```

## Output

Wallpapers are saved as:
- `wallpaper_1920x1080.png`
- `wallpaper_2560x1440.png`
- `wallpaper_1920x1200.png`

## License

MIT
