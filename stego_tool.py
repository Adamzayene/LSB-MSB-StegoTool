import argparse
from PIL import Image
from colorama import init, Fore, Style
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

def bin_to_text(binary):
    """Convert binary string back to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_text_in_image(image_path, text, output_path, method):
    """Hide text in an image using LSB or MSB method."""
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    # Prepare the binary text with an end-of-text marker
    binary_text = text_to_bin(text) + '1111111111111110'
    data_index = 0

    for y in range(image.height):
        for x in range(image.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Modify each color channel (R, G, B)
                if data_index < len(binary_text):
                    bit = int(binary_text[data_index])
                    if method == "lsb":
                        pixel[i] = (pixel[i] & ~1) | bit  # Modify the least significant bit
                    elif method == "msb":
                        pixel[i] = (pixel[i] & 0b01111111) | (bit << 7)  # Modify the most significant bit
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(binary_text):
                break
        if data_index >= len(binary_text):
            break

    image.save(output_path)
    print(Fore.GREEN + f"Image saved with hidden text in: {output_path}")

def extract_text_from_image(image_path, method):
    """Extract hidden text from an image using LSB or MSB method."""
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    binary_text = ""

    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            for i in range(3):  # Extract each color channel (R, G, B)
                if method == "lsb":
                    binary_text += str(pixel[i] & 1)  # Extract the least significant bit
                elif method == "msb":
                    binary_text += str((pixel[i] >> 7) & 1)  # Extract the most significant bit
                # Check for the end-of-text marker
                if binary_text.endswith('1111111111111110'):
                    return bin_to_text(binary_text[:-16])

    return bin_to_text(binary_text)

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

    # Execute hide or extract functionality
    if args.extract:
        if args.image:
            hidden_text = extract_text_from_image(args.image, args.method)
            print(Fore.CYAN + f"Extracted text: {hidden_text}")
        else:
            print(Fore.RED + "Error: Please specify the image path with -i or --image")
    else:
        if args.text and args.output:
            hide_text_in_image(args.image, args.text, args.output, args.method)
        else:
            print(Fore.RED + "Error: Please specify both the text to hide (-e) and the output path (-o).")

if __name__ == "__main__":
    main()
