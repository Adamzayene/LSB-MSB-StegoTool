# LSB-MSB-StegoTool
LSB & MSB StegoTool is a Python-based application that allows users to hide and extract text within image files using Least Significant Bit (LSB) and Most Significant Bit (MSB) steganography techniques. This tool is designed for both educational and practical purposes in the field of data hiding and information security.

## Features

- **Text Hiding**: Hide messages in image files using LSB or MSB methods.
- **Text Extraction**: Retrieve hidden messages from images.
- **Flexible Usage**: Easily specify input images, output files, and hiding methods via command-line arguments.
- **User-Friendly Interface**: Colorful banners and informative messages enhance user experience.
- **Open Source**: Free to use and modify, with a focus on educational purposes.

## Requirements

- Python 3.x
- Pillow library (for image processing)
- Colorama library (for colored terminal output)

You can install the required libraries using pip:

```bash
pip install pillow colorama
```
## Options

- `-i` or `--image`: 
  - **Description**: Path to the original image.
  
- `-e` or `--text`: 
  - **Description**: Text to hide within the image.

- `-o` or `--output`: 
  - **Description**: Path to save the image with the hidden text.

- `-m` or `--method`: 
  - **Description**: Hiding method. Choose either `lsb` for least significant bit or `msb` for most significant bit.
  - **Default**: `lsb`.
-  `-x` or `--extract`: 
  - **Description**: Flag to indicate that you want to extract text from the image.
    
## Usage

To use **LSB & MSB StegoTool**, you can execute it from the command line with the following options:

### Hiding Text

```bash
python stego_tool.py -i <image_path> -e "<text_to_hide>" -o <output_image_path> -m <method>
```
### Extracting Text

To extract hidden text from an image, you can execute the tool from the command line with the following options:

```bash
python stego_tool.py -i <image_path> -x -m <method>
```
## Example

### Hiding Text

To hide text within an image, use the following command:

```bash
python stego_tool.py -i input_image.png -e "Hello, World!" -o output_image.png -m lsb
```
### Extracting Text

To extract hidden text from an image, use the following command:

```bash
python stego_tool.py -i output_image.png -x -m lsb
```
