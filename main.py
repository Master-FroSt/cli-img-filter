import os
import sys
import numpy as np
from PIL import Image
import questionary
import cli

def process_and_save(image_path, filter_chain):
    """Loads image, applies the sequential stack, and saves to /out."""
    print(f"\n⏳ Loading image: {image_path}...")
    try:
        # Load and convert to RGB (to avoid issues with RGBA in NumPy matrix multiplications)
        img = Image.open(image_path).convert('RGB')
        pixels = np.array(img)

        # Apply filters in exact order
        for f in filter_chain:
            print(f"   Applying: {f['label']}...")
            pixels = f["func"](pixels, **f["kwargs"])

        # Ensure output directory exists
        os.makedirs("out", exist_ok=True)

        # Generate Smart Filename
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        filter_names = "_".join([f["label"].split()[0].lower() for f in filter_chain])
        out_filename = f"{name}_{filter_names}{ext}"
        out_path = os.path.join(os.getcwd(), "out", out_filename)

        # Save image
        out_img = Image.fromarray(pixels)
        out_img.save(out_path)

        print(f"\n✅ \033[92mSUCCESS!\033[0m Image processed successfully.")
        print(f"📁 Saved to: \033[94m\033[4m{out_path}\033[0m\n")
        return True

    except Exception as e:
        print(f"\n❌ \033[91mERROR:\033[0m Failed to process image. {e}\n")
        return False


def main():
    print("========================================")
    print("🎨 NumPy Image Filter CLI Studio")
    print("========================================")

    last_image_path = None

    while True:
        choices = ["🖼️  Process New Image"]
        if last_image_path:
            choices.append("🔁 Re-process Last Image")
        choices.append("🚪 Exit")

        main_action = questionary.select("\nMain Menu:", choices=choices).ask()

        if main_action == "🚪 Exit" or main_action is None:
            print("Goodbye! 👋")
            sys.exit(0)

        elif main_action == "🖼️  Process New Image":
            print("\nOpening file browser...")
            file_path = cli.browse_file()
            if not file_path:
                print("⚠️  No file selected.")
                continue
            last_image_path = file_path

        # Build the chain
        print(f"\nSelected Image: {last_image_path}")
        chain = cli.build_filter_chain()

        # Execute
        if chain:
            process_and_save(last_image_path, chain)
        else:
            print("⚠️  Processing cancelled.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye! 👋")
        sys.exit(0)