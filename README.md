# PageXml to Binary Mask Converter

This Python script converts PageXml files into binary masks for text lines using OpenCV and BeautifulSoup.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd PageXml-to-Binary-Mask-Converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Arguments

- `-i, --InputDir`: Input directory containing PageXml files (default: "Dataconverstion").
- `-o, --OutputDir`: Output directory for saving binary mask files (default: "ProcessedData").
- `-d, --DeletePrevious`: Delete the previous output directory (default: True).

### Example

Convert PageXml files in the `Dataconverstion` directory to binary masks and save them in `ProcessedData`:
```bash
python convert.py -i Dataconverstion -o ProcessedData -d True
```

## Requirements

- Python 3.x
- BeautifulSoup
- numpy
- OpenCV (cv2)
- Pillow (PIL)
- tqdm

