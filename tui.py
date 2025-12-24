from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    Input,
    Button,
    Label,
    RadioButton,
    RadioSet,
    Switch,
    Static,
    Select,
    Log,
)
from textual.validation import Regex
import os
import subprocess
import generator
import ai_generator
import kitchn_bridge

try:
    import tui_theme_config

    HAS_THEME = True
except ImportError:
    HAS_THEME = False
    print("Warning: tui_theme_config not found. Using default Textual theme.")


class WallpaperGenApp(App):
    # Disable all Textual auto-features that might capture output
    ENABLE_COMMAND_PALETTE = False

    # Override notify to suppress all notifications
    def notify(self, *args, **kwargs):
        pass

    def _suppress_fd_output(self, func, *args, **kwargs):
        """Temporarily redirect fd 1/2 to suppress C/Rust library output."""
        # Save original fds
        stdout_fd = os.dup(1)
        stderr_fd = os.dup(2)

        # Redirect to devnull
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)

        try:
            result = func(*args, **kwargs)
        finally:
            # Restore original fds
            os.dup2(stdout_fd, 1)
            os.dup2(stderr_fd, 2)
            os.close(devnull)
            os.close(stdout_fd)
            os.close(stderr_fd)

        return result

    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 40%;
        height: 100%;
        background: $panel;
        padding: 1 2;
        border-right: heavy $accent;
    }

    #main_content {
        width: 60%;
        height: 100%;
        padding: 2;
        align: center middle;
    }

    .section-title {
        text-style: bold;
        color: $accent;
        margin-top: 1;
        margin-bottom: 1;
    }

    Input {
        margin-bottom: 1;
    }

    Button {
        width: 100%;
        margin-top: 2;
    }
    
    #status_log {
        background: $surface;
        border: solid $secondary;
        height: 50%;
        width: 100%;
        padding: 1;
        color: $text;
    }
    
    .toggle-row {
        height: 3;
        align: left middle;
        margin-bottom: 1;
    }
    
    .separator {
        height: 1;
        background: $accent;
        margin: 1 0;
    }

    .color-row {
        height: 3;
        margin-bottom: 1;
    }
    .color-input {
        width: 80%;
    }
    .btn-small {
        width: 20%;
        min-width: 4;
        margin-top: 0;
        height: 100%;
    }

    #logo_section {
        margin-bottom: 1;
    }

    Select {
        margin-bottom: 1;
    }
    """

    TITLE = "WP-Gen-PyJS"
    SUB_TITLE = "Fancy Wallpaper Generator"

    def compose(self) -> ComposeResult:
        with Container(id="sidebar"):
            # AI Toggle
            with Horizontal(classes="toggle-row"):
                yield Label("Enable AI: ", classes="section-title")
                yield Switch(value=False, id="ai_toggle")

            # AI Section
            with Container(id="ai_section"):
                yield Label("Prompt", classes="section-title")
                yield Input(
                    placeholder="Describe your vibe (e.g. 'Cyberpunk City')",
                    id="ai_prompt",
                )
                yield Button(
                    "Magic Generate (Colors + Image)", variant="warning", id="ai_btn"
                )
                yield Static(classes="separator")

            # Manual Section
            yield Label("Mode", classes="section-title")
            with RadioSet(id="mode_select"):
                yield RadioButton("Solid Color", value=True, id="mode_solid")
                yield RadioButton("Linear Gradient", id="mode_linear")
                yield RadioButton("Mesh Gradient", id="mode_mesh")

            yield Label("Colors (Hex)", classes="section-title")
            with Horizontal(classes="color-row"):
                yield Input(
                    placeholder="#000000",
                    id="color1",
                    classes="color-input",
                    validators=[Regex(r"^#(?:[0-9a-fA-F]{3}){1,2}$")],
                )
                yield Button("🎨", id="pick1", classes="btn-small")

            with Horizontal(classes="color-row", id="row_color2"):
                yield Input(
                    placeholder="#FFFFFF",
                    id="color2",
                    classes="color-input",
                    validators=[Regex(r"^#(?:[0-9a-fA-F]{3}){1,2}$")],
                )
                yield Button("🎨", id="pick2", classes="btn-small")

            with Horizontal(classes="color-row", id="row_color3"):
                yield Input(
                    placeholder="#FF00FF",
                    id="color3",
                    classes="color-input",
                    validators=[Regex(r"^#(?:[0-9a-fA-F]{3}){1,2}$")],
                )
                yield Button("🎨", id="pick3", classes="btn-small")

            with Horizontal(classes="toggle-row"):
                yield Label("Enable Logo: ", classes="section-title")
                yield Switch(value=False, id="logo_switch")

            with Container(id="logo_section"):
                yield Label("Overlay Image (Path)", classes="section-title")
                yield Input(placeholder="/path/to/logo.png", id="logo_path")

                yield Label("Position", classes="section-title")
                yield Select.from_values(
                    [
                        "center",
                        "top_center",
                        "top_left",
                        "top_right",
                        "bottom_center",
                        "bottom_left",
                        "bottom_right",
                    ],
                    value="center",
                    id="pos_select",
                )

            yield Label("Output Directory", classes="section-title")
            yield Input(
                placeholder="Leave empty for current directory",
                id="output_dir",
            )

            yield Label("Effects", classes="section-title")
            with Horizontal():
                yield Label("Noise/Grain: ")
                yield Switch(value=False, id="noise_switch")

            yield Button("Generate Wallpapers", variant="primary", id="gen_btn")

        with Container(id="main_content"):
            yield Label("Status Log", classes="section-title")
            yield Log(id="status_log")

    def on_mount(self) -> None:
        self.query_one("#status_log").write("Ready to generate...")
        self._suppress_fd_output(kitchn_bridge.log_tui_start)

        # Apply Kitchn Theme if available
        if HAS_THEME:
            for key, value in tui_theme_config.CSS_VARIABLES.items():
                # Textual uses variable names without '$' in set_variable
                self.screen.styles.set_variable(key, value)
            self._suppress_fd_output(kitchn_bridge.log_tui_theme_ok)

        self._suppress_fd_output(kitchn_bridge.log_tui_ok)

        # Initial state for solid mode
        self.query_one("#row_color2").display = False
        self.query_one("#row_color3").display = False
        # Initial state for logo
        self.query_one("#logo_section").display = False
        # Initial state for AI (disabled by default)
        self.query_one("#ai_section").display = False

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "ai_toggle":
            self.query_one("#ai_section").display = event.value
        elif event.switch.id == "logo_switch":
            self.query_one("#logo_section").display = event.value

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        # Show/Hide color inputs based on mode
        mode = event.pressed.id
        # We toggle the ROWS now
        r2 = self.query_one("#row_color2")
        r3 = self.query_one("#row_color3")

        if mode == "mode_solid":
            r2.display = False
            r3.display = False
        elif mode == "mode_linear":
            r2.display = True
            r3.display = False
        elif mode == "mode_mesh":
            r2.display = True
            r3.display = True

    @work(exclusive=False, thread=True)
    def pick_color_worker(self, target_input_id: str) -> None:
        try:
            # hyprpicker returns hex color directly (e.g., '#RRGGBB')
            # Works natively on Wayland
            # Suppress all output to prevent TUI interference
            result = subprocess.run(
                ["hyprpicker", "-a"], capture_output=True, text=True
            )

            if result.returncode != 0:
                return  # User cancelled

            hex_color = result.stdout.strip()

            # Update UI safely
            def update_input():
                self.query_one(f"#{target_input_id}").value = hex_color
                self._suppress_fd_output(kitchn_bridge.log_tui_pick_ok, hex_color)

            self.call_from_thread(update_input)

        except Exception:
            # User cancelled or error
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:
            bid = event.button.id
            if bid == "gen_btn":
                self.generate()
            elif bid == "ai_btn":
                self.generate_ai()
            elif bid == "pick1":
                self.pick_color_worker("color1")
            elif bid == "pick2":
                self.pick_color_worker("color2")
            elif bid == "pick3":
                self.pick_color_worker("color3")
        except Exception as e:
            err = f"CRITICAL ERROR: {str(e)}"
            self.write_log(err)
            self._suppress_fd_output(kitchn_bridge.log_error, err)

    def write_log(self, message: str) -> None:
        """Helper to write to log safely (can be called from threads)."""
        self.call_from_thread(self.query_one("#status_log").write, message)
        # Also log to Kitchn
        self._suppress_fd_output(kitchn_bridge.log_info, message)

    def update_ui_colors(self, colors: list[str]) -> None:
        """Helper to update color inputs safely."""
        self.query_one("#color1").value = colors[0]
        if len(colors) > 1:
            self.query_one("#color2").value = colors[1]
        if len(colors) > 2:
            self.query_one("#color3").value = colors[2]

    def set_mesh_mode(self) -> None:
        """Helper to set mesh mode safely."""
        self.query_one("#mode_mesh").value = True

    @work(exclusive=True, thread=True)
    def generate_ai(self):
        # Must access UI elements via call_from_thread or query before work starts?
        # Textual queries are thread-safeish for reading usually, but better to read via worker if possible.
        # However, accessing `self.query_one` inside a worker IS allowed for reading properties in many cases,
        # but standard practice is to read data *before* or pass it in.
        # But `generate_ai` is triggered by button, so we need to read the prompt inside here.

        # Safe pattern: Schedule a function to read the prompt, but that's async.
        # Simpler: Reading values from main thread widgets inside a worker is generally safe in Textual
        # as long as we don't write. Let's try reading.

        # Actually, let's read the prompt via app.call_from_thread if we want to be 100% strict,
        # but checking docs, reading widget properties is often fine.
        # For safety, I'll access it directly. If it fails, I'll wrap it.

        # Wait, if I read `self.query_one("#ai_prompt").value`, it might be fine.

        try:
            # We need to get the prompt.
            # Note: `self.query_one` is thread-safe.
            prompt = self.query_one("#ai_prompt").value

            if not prompt:
                self.write_log("Please enter a prompt for AI generation.")
                return

            self.write_log(
                f"AI Generating for '{prompt}'...\n(This might take a while on first run)"
            )
            self._suppress_fd_output(kitchn_bridge.log_tui_ai_start, prompt)

            # 1. Generate Image
            # We save to a temporary location
            ai_image_path = "ai_generated_temp.png"
            path = ai_generator.generate_image_from_prompt(prompt, ai_image_path)

            if not path:
                self.write_log("Error: AI Model failed to load or run.")
                self._suppress_fd_output(kitchn_bridge.log_tui_fail, "AI Model failed")
                return

            self.write_log("Image generated! Extracting colors...")

            # 2. Extract Colors
            colors = ai_generator.extract_palette(path, n_colors=3)
            self.write_log(f"Colors found: {colors}")

            # 3. Update UI
            self.call_from_thread(self.update_ui_colors, colors)
            self.call_from_thread(self.set_mesh_mode)

            self.write_log(
                "UI updated! Click 'Generate Wallpapers' to render final output."
            )
            self._suppress_fd_output(kitchn_bridge.log_tui_ai_ok)

        except Exception as e:
            self.write_log(f"AI Error: {str(e)}")
            self._suppress_fd_output(kitchn_bridge.log_tui_fail, str(e))

    @work(exclusive=True, thread=True)
    def generate(self):
        self.write_log("Starting generation...")

        # Reading UI state inside worker
        # This is the tricky part. It's better to gather inputs on the main thread and pass them to the worker.
        # But since `on_button_pressed` calls this directly, we are already in the worker context if we decorate it.
        # A better pattern: The event handler (main thread) gathers data, then calls the worker with that data.

        # Refactoring to: on_button_pressed gathers data -> calls self.run_generation_worker(data)

        # HOWEVER, for now, let's stick to reading from worker as it usually works for simple properties in Textual.
        # If it crashes, I will refactor.

        try:
            mode_radio = self.query_one("#mode_select").pressed_button
            if not mode_radio:
                mode = "solid"
            else:
                mode = mode_radio.id.replace("mode_", "")
                if mode == "linear":
                    mode = "gradient_linear"
                if mode == "mesh":
                    mode = "gradient_mesh"

            c1 = self.query_one("#color1").value or "#000000"
            c2 = self.query_one("#color2").value or "#333333"
            c3 = self.query_one("#color3").value or "#666666"

            colors = [c1]
            if mode == "gradient_linear":
                colors.append(c2)
            elif mode == "gradient_mesh":
                colors.extend([c2, c3])

            logo_enabled = self.query_one("#logo_switch").value
            logo_path = self.query_one("#logo_path").value

            final_logo_path = None
            if logo_enabled:
                if logo_path and not os.path.exists(logo_path):
                    self.write_log(f"Error: Logo file not found at {logo_path}")
                    return
                final_logo_path = logo_path

            position = self.query_one("#pos_select").value
            noise_enabled = self.query_one("#noise_switch").value
            noise_level = 0.05 if noise_enabled else 0.0

            output_dir = self.query_one("#output_dir").value.strip()
            if not output_dir:
                output_dir = "."

            config = {
                "mode": mode,
                "colors": colors,
                "logo_path": final_logo_path,
                "position": position,
                "noise": noise_level,
                "output_dir": output_dir,
            }

            self.write_log(f"Mode: {mode}\nColors: {colors}\nProcessing...")
            self._suppress_fd_output(kitchn_bridge.log_tui_gen, f"Mode: {mode}")

            generator.generate_wallpaper(config)

            self.write_log("Success! Saved wallpapers")
            self._suppress_fd_output(kitchn_bridge.log_tui_save_ok)

        except Exception as e:
            self.write_log(f"Error:\n{str(e)}")
            self._suppress_fd_output(kitchn_bridge.log_tui_fail, str(e))


if __name__ == "__main__":
    app = WallpaperGenApp()
    app.run()
