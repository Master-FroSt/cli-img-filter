import tkinter as tk
from tkinter import filedialog

import questionary
from questionary import Validator, ValidationError
import filters

class NumberValidator(Validator):
    """Validasi tipe data float."""
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a valid number.", cursor_position=len(document.text))


class IntValidator(Validator):
    """Validasi tipe data int."""
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a valid integer.", cursor_position=len(document.text))


def configure_filter(filter_name):
    """Condisional untuk pemilihan filter dengan arrow key."""
    if filter_name == "Brightness":
        action = questionary.select("Action:", choices=["Lighten", "Darken"]).ask()
        if not action: return None
        is_lighten = action == "Lighten"
        pct = questionary.text("Percentage (0-100):", validate=NumberValidator).ask()
        if pct is None: return None
        return {"func": filters.apply_brightness, "kwargs": {"percentage": float(pct), "is_lighten": is_lighten},
                "label": f"Brightness ({action} {pct}%)"}

    elif filter_name == "Grayscale":
        return {"func": filters.apply_grayscale, "kwargs": {}, "label": "Grayscale"}

    elif filter_name == "Black & White":
        threshold = questionary.text("Threshold (0-255) [Default 128]:", default="128", validate=IntValidator).ask()
        if threshold is None: return None
        return {"func": filters.apply_black_and_white, "kwargs": {"threshold": int(threshold)},
                "label": f"B&W (Thresh:{threshold})"}

    elif filter_name == "Invert":
        return {"func": filters.apply_invert, "kwargs": {}, "label": "Invert"}

    elif filter_name == "Isolate Color":
        channel = questionary.select("Channel to isolate:", choices=['R (Merah)', 'G (Hijau)', 'B (Biru)']).ask()
        if not channel: return None
        return {"func": filters.apply_isolate_color, "kwargs": {"channel_choice": channel}, "label": f"Isolate {channel[0]}"}

    elif filter_name == "Erase Color":
        channel = questionary.select("Channel to erase:", choices=['R (Merah)', 'G (Hijau)', 'B (Biru)']).ask()
        if not channel: return None
        return {"func": filters.apply_erase_color, "kwargs": {"channel_choice": channel}, "label": f"Erase {channel[0]}"}

    elif filter_name == "Tint":
        tint = questionary.select("Tint style:", choices=['Sepia', 'Rosewood', 'Patina']).ask()
        if not tint: return None
        return {"func": filters.apply_tint, "kwargs": {"tint_choice": tint}, "label": f"Tint ({tint})"}

    elif filter_name == "Duotone":
        combo = questionary.select("Color combination:", choices=[
            '(Mix, Mix, Invert)', '(Mix, Invert, Mix)', '(Invert, Mix, Mix)',
            '(Mix, Invert, Invert)', '(Invert, Mix, Invert)', '(Invert, Invert, Mix)'
        ]).ask()
        if not combo: return None
        return {"func": filters.apply_duotone, "kwargs": {"combination": combo}, "label": "Duotone"}

    elif filter_name == "Posterize":
        levels = questionary.text("Color levels (e.g. 2, 4, 8) [Default 4]:", default="4", validate=IntValidator).ask()
        if levels is None: return None
        return {"func": filters.apply_posterize, "kwargs": {"levels": int(levels)}, "label": f"Posterize ({levels} lvls)"}

    elif filter_name == "Sepia (Standard)":
        return {"func": filters.apply_sepia_standard, "kwargs": {}, "label": "Sepia"}

    elif filter_name == "Vintage":
        gamma = questionary.text("Gamma (e.g. 1.2) [Default 1.2]:", default="1.2", validate=NumberValidator).ask()
        if gamma is None: return None
        return {"func": filters.apply_vintage, "kwargs": {"gamma": float(gamma)}, "label": f"Vintage (Gamma:{gamma})"}

    elif filter_name == "Brightness & Contrast":
        alpha = questionary.text("Contrast Multiplier (e.g. 1.2) [Default 1.2]:", default="1.2",
                                 validate=NumberValidator).ask()
        if alpha is None: return None
        beta = questionary.text("Brightness Offset (e.g. 10) [Default 10]:", default="10",
                                validate=NumberValidator).ask()
        if beta is None: return None
        return {"func": filters.apply_brightness_contrast, "kwargs": {"alpha": float(alpha), "beta": float(beta)},
                "label": f"B&C (a:{alpha}, b:{beta})"}

    elif filter_name == "Solarize":
        threshold = questionary.text("Threshold (0-255) [Default 128]:", default="128", validate=IntValidator).ask()
        if threshold is None: return None
        return {"func": filters.apply_solarize, "kwargs": {"threshold": int(threshold)},
                "label": f"Solarize (Thresh:{threshold})"}

    elif filter_name == "Monochrome Tint":
        theme = questionary.select("Theme:", choices=['matrix', 'cyanotype', 'blood']).ask()
        if not theme: return None
        return {"func": filters.apply_monochrome_tint, "kwargs": {"theme": theme}, "label": f"Mono ({theme})"}


def browse_file():
    """Opens a native file dialog to select an image."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tk window
    root.attributes('-topmost', True)  # Bring to front
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp;*.bmp")]
    )
    return file_path


def build_filter_chain():
    """Interactive menu to let user dictate the exact order (stack) of filters."""
    available_filters = [
        "Brightness", "Grayscale", "Black & White", "Invert",
        "Isolate Color", "Erase Color", "Tint", "Duotone",
        "Posterize", "Sepia (Standard)", "Vintage",
        "Brightness & Contrast", "Solarize", "Monochrome Tint"
    ]

    filter_chain = []

    while True:
        # Show current chain
        chain_display = " ➔ ".join([f["label"] for f in filter_chain]) if filter_chain else "None"
        print(f"\n\033[96mCurrent Filter Stack:\033[0m {chain_display}")

        choices = ["➕ Add a Filter"]
        if filter_chain:
            choices.extend(["▶️  PROCESS IMAGE", "❌ Clear Stack"])
        choices.append("🔙 Cancel & Return")

        action = questionary.select("What would you like to do?", choices=choices).ask()

        if action == "➕ Add a Filter":
            selected = questionary.select("Select a filter to add:", choices=available_filters).ask()
            if not selected: continue

            config = configure_filter(selected)
            if config:
                filter_chain.append(config)

        elif action == "▶️  PROCESS IMAGE":
            return filter_chain

        elif action == "❌ Clear Stack":
            filter_chain = []

        elif action == "🔙 Cancel & Return" or action is None:
            return None
