import ctypes
import os

# Path to the shared library
# Assuming we are in /home/ryu/code/github.com/ryugen/wp-gen-pyjs
# and kitchn is in ../kitchn
LIB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../kitchn/target/release/libk_ffi.so")
)


class KitchnBridge:
    def __init__(self):
        self.lib = None
        self.ctx = None
        self.load_lib()

    def load_lib(self):
        if not os.path.exists(LIB_PATH):
            print(f"Warning: Kitchn library not found at {LIB_PATH}. Logging disabled.")
            return

        try:
            self.lib = ctypes.CDLL(LIB_PATH)

            # Define signatures
            # kitchn_context_new() -> *mut KitchnContext
            self.lib.kitchn_context_new.restype = ctypes.c_void_p
            self.lib.kitchn_context_new.argtypes = []

            # kitchn_context_free(ctx)
            self.lib.kitchn_context_free.argtypes = [ctypes.c_void_p]

            # kitchn_context_set_app_name(ctx, name)
            self.lib.kitchn_context_set_app_name.argtypes = [
                ctypes.c_void_p,
                ctypes.c_char_p,
            ]

            # kitchn_log(ctx, level, scope, msg)
            self.lib.kitchn_log.argtypes = [
                ctypes.c_void_p,
                ctypes.c_char_p,
                ctypes.c_char_p,
                ctypes.c_char_p,
            ]

            # kitchn_log_preset(ctx, preset_key, msg_override)
            self.lib.kitchn_log_preset.argtypes = [
                ctypes.c_void_p,
                ctypes.c_char_p,
                ctypes.c_char_p,
            ]

            # Initialize context
            self.ctx = self.lib.kitchn_context_new()
            if self.ctx:
                self.set_app_name("wp-gen-pyjs")
            else:
                print("Failed to create Kitchn context.")

        except Exception as e:
            print(f"Error loading Kitchn library: {e}")
            self.lib = None

    def set_app_name(self, name):
        if self.lib and self.ctx:
            c_name = name.encode("utf-8")
            self.lib.kitchn_context_set_app_name(self.ctx, c_name)

    def log(self, level, scope, msg):
        if self.lib and self.ctx:
            c_level = level.encode("utf-8")
            c_scope = scope.encode("utf-8")
            c_msg = msg.encode("utf-8")
            self.lib.kitchn_log(self.ctx, c_level, c_scope, c_msg)
        # Fallback: silently skip (TUI has its own logging)

    def log_preset(self, preset_key, msg_override=None):
        if self.lib and self.ctx:
            c_key = preset_key.encode("utf-8")
            c_msg = msg_override.encode("utf-8") if msg_override else None
            self.lib.kitchn_log_preset(self.ctx, c_key, c_msg)
        # Fallback: silently skip (TUI has its own logging)

    def close(self):
        if self.lib and self.ctx:
            self.lib.kitchn_context_free(self.ctx)
            self.ctx = None


# Global instance
_bridge = None


def get_bridge():
    global _bridge
    if _bridge is None:
        _bridge = KitchnBridge()
    return _bridge


def log_info(msg):
    # Use generic log for now as tui_start/ok/gen/fail are specific events
    get_bridge().log("info", "TUI", msg)


def log_error(msg):
    get_bridge().log("error", "TUI", msg)


def log_debug(msg):
    get_bridge().log("debug", "TUI", msg)


def log_tui_start():
    get_bridge().log_preset("tui_start")


def log_tui_ok():
    get_bridge().log_preset("tui_ok")


def log_tui_theme_ok():
    get_bridge().log_preset("tui_theme_ok")


def log_tui_ai_start(prompt):
    get_bridge().log_preset("tui_ai_start", prompt)


def log_tui_ai_ok():
    get_bridge().log_preset("tui_ai_ok")


def log_tui_pick_ok(color):
    get_bridge().log_preset("tui_pick_ok", color)


def log_tui_save_ok():
    get_bridge().log_preset("tui_save_ok")


def log_tui_gen(msg):
    get_bridge().log_preset("tui_gen", msg)


def log_tui_fail(msg):
    get_bridge().log_preset("tui_fail", msg)
