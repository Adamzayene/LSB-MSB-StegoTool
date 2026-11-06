#!/usr/bin/env python3
import argparse
from PIL import Image
from colorama import init, Fore
import numpy as np
import sys
# ANSI escape sequences for colors
RESET = "\033[0m"
LIGHT_BLUE = "\033[94m"
LIGHT_GREEN = "\033[92m"
LIGHT_YELLOW = "\033[93m"

def print_banner():
    banner = f"""{LIGHT_BLUE}
 888      .d8888b.  888888b.         .d8888b.           888b     d888  .d8888b.  {LIGHT_YELLOW}888888b.   
 888     d88P  Y88b 888  "88b       d88P  "88b          8888b   d8888 d88P  Y88b  {LIGHT_GREEN}888  "88b  
 888     Y88b.      888  .88P       Y88b. d88P          88888b.d88888 Y88b.      {LIGHT_BLUE}888  .88P  
 888      "Y888b.   8888888K.        "Y8888P"           888Y88888P888  "Y888b.   {LIGHT_YELLOW}8888888K.  
 888         "Y88b. 888  "Y88b      .d88P88K.d88P       888 Y888P 888     "Y88b. {LIGHT_GREEN}888  "Y88b 
 888           "888 888    888      888"  Y888P"        888  Y8P  888       "888 {LIGHT_BLUE}888    888 
 888     Y88b  d88P 888   d88P      Y88b .d8888b        888   "   888 Y88b  d88P {LIGHT_YELLOW}888   d88P 
 88888888 "Y8888P"  8888888P"        "Y8888P" Y88b      888       888  "Y8888P"  {LIGHT_GREEN}8888888P"  
                                                                                            
                            LSB & MSB StegoTool
                                 by Adam Zayene
{RESET}"""
    print(banner)

# Initialize colorama
init(autoreset=True)

def text_to_bin(text):
    """Convert text to binary representation."""
    return ''.join(format(ord(char), '08b') for char in text)

def hide_text_in_image(image_path, text, output_path, is_msb_else_lsb):
    """Hide text in an image using LSB or MSB method."""
    image = Image.open(image_path).convert("RGB")
    image.load()
    pixels = np.frombuffer(image.tobytes(), dtype=np.uint8).copy()  # shape = (H, W, RGB) -> (3*H*W,)
    # Prepare the binary text with an end-of-text marker
    binary_text = np.unpackbits(np.frombuffer(text.encode("latin-1") + b"\xff\xfe", dtype=np.uint8))
    workspace = pixels[:binary_text.size]
    if is_msb_else_lsb:
        binary_text <<= 7
        workspace &= 127  # Modify the most significant bit
    else:
        workspace &= 254  # Modify the least significant bit
    workspace |= binary_text
    pixels = pixels.reshape((image.height, image.width, 3))
    out = Image.fromarray(pixels)
    out.save(output_path)
    print(Fore.GREEN + f"Image saved with hidden text in: {output_path}")

def extract_text_from_image(image_path, is_msb_else_lsb):
    """Extract hidden text from an image using LSB or MSB method."""
    image = Image.open(image_path).convert("RGB")
    image.load()
    pixels = np.frombuffer(image.tobytes(), dtype=np.uint8).copy()  # shape = (H, W, RGB) -> (3*H*W,)
    if is_msb_else_lsb:
        pixels >>= 7  # Extract the most significant bit
    else:
        pixels &= 1  # Extract the least significant bit
    pixels = np.packbits(pixels)
    # Check for the end-of-text marker
    windows = np.lib.stride_tricks.sliding_window_view(pixels, 2)
    stop = np.argmax(np.all(windows == (255, 254), axis=1)) or pixels.size
    return pixels[:stop].tobytes().decode("latin-1")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Hide or extract text in an image using LSB or MSB.")

    # Add options (flags)
    parser.add_argument("-i", "--image", required=True, help="Path to the original image")
    parser.add_argument("-e", "--text", help="Text to hide")
    parser.add_argument("-o", "--output", help="Path to save the image with hidden text")
    parser.add_argument("-m", "--method", choices=["lsb", "msb"], default="lsb",
                        help="Hiding method: 'lsb' for least significant bit or 'msb' for most significant bit (default is lsb)")
    parser.add_argument("-x", "--extract", action="store_true", help="Extract hidden text from the image")

    args = parser.parse_args()
    is_msb_else_lsb = args.method == "msb"

    # Execute hide or extract functionality
    if args.extract:
        if args.image:
            hidden_text = extract_text_from_image(args.image, is_msb_else_lsb)
            print(Fore.CYAN + f"Extracted text: {hidden_text}")
        else:
            print(Fore.RED + "Error: Please specify the image path with -i or --image")
    else:
        text = args.text
        if text is None:
            print("Reading text from stdin: ")
            text = sys.stdin.read()
        if args.output:
            hide_text_in_image(args.image, text, args.output, is_msb_else_lsb)
        else:
            print(Fore.RED + "Error: Please specify both the text to hide (-e) and the output path (-o).")

if __name__ == "__main__":
    main()
