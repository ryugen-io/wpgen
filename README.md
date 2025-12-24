# WP-Gen-PyJS

A fancy, modern wallpaper generator with a Terminal User Interface (TUI).

## Features
- **Modes:** Solid Color, Linear Gradient, and **Mesh Gradient** (Aurora style).
- **Resolutions:** Generates 1920x1080 and 2560x1440 wallpapers simultaneously.
- **Effects:** Film Grain / Noise for a premium textured look.
- **Overlay:** Composite a transparent logo/image at 7 configurable positions.
- **Interface:** Fully interactive TUI with mouse support.

## Installation

1.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the interactive interface:
```bash
source .venv/bin/activate
python tui.py
```

1.  Select your **Mode** (Solid, Linear, Mesh).
2.  Enter **Hex Colors** (e.g., `#FF0000`).
3.  (Optional) Provide a path to a **Logo/Overlay** image.
4.  Toggle **Noise** for texture.
5.  Click **Generate Wallpapers**.

Files will be saved in the current directory as `wallpaper_1920x1080.png` and `wallpaper_2560x1440.png`.
