# Image Compressor Pro

A professional, standalone desktop application for batch compressing images (JPEG, PNG, WebP) to a user-specified target file size. Built with Python, Tkinter, and Pillow, it features a modern, user-friendly interface and is distributed as a single `.exe` for Windows.

## Features
- **Modern UI**: Sleek, Material Design-inspired interface with `ttkbootstrap`.
- **Flexible Input/Output**: Select custom input and output folders via file dialogs.
- **Smart Compression**: Reduces image quality iteratively (95 to 10) while preserving resolution. Converts PNG to JPEG for better compression if needed.
- **Configuration Support**:
  - `exclude.txt`: List filenames to skip (one per line).
  - `config.csv`: Set custom target sizes per file (columns: `filename`, `target_kb`).
- **Progress Tracking**: Real-time log and progress bar for user feedback.
- **Detailed Reporting**: Exports a CSV report (`compression_report.csv`) with compression stats.
- **Standalone Executable**: No installation required; runs on Windows 10/11.

## Screenshots
*(Add screenshots here: e.g., main UI, compression in progress, sample report)*

## System Requirements
- **OS**: Windows 10/11 (64-bit).
- **Disk Space**: ~70 MB for the `.exe`.
- **No Python Required**: The `.exe` includes all dependencies.

## Usage
1. Download `ImageCompressorPro.exe` from the [Releases](https://github.com/sezanX/ImageCompressor-tools/releases/tag/v-1.0) section or a provided link.
2. Double-click to run the `.exe` (no installation needed).
3. Click "Browse" to select an **input folder** containing images (JPEG, PNG, WebP).
4. Click "Browse" to select an **output folder** for compressed images.
5. (Optional) Adjust "Target Size (KB)" (default: 250 KB).
6. Click **Start Compression**.
7. Monitor progress in the log area. A `compression_report.csv` will be saved in the output folder.

### Optional Configuration Files
Place these in the input folder:
- **exclude.txt** (skip specific files):
  ```
  image1.jpg
  image2.png
  ```
- **config.csv** (custom target sizes):
  ```csv
  filename,target_kb
  image1.jpg,100
  image2.png,300
  ```

## Supported Formats
- **Input**: JPEG, PNG, WebP.
- **Output**: JPEG (optimized).

## Building from Source (For Developers)
1. Install dependencies:
   ```bash
   pip install Pillow ttkbootstrap pyinstaller
   ```
2. Save the script as `image_compressor.py`.
3. Run: `python image_compressor.py`.
4. To build the `.exe`:
   ```bash
   py -m PyInstaller --onefile --windowed --name "ImageCompressorPro" --hidden-import=PIL --hidden-import=ttkbootstrap image_compressor.py
   ```

## Troubleshooting
- **No images found**: Ensure the input folder contains `.jpg`, `.jpeg`, `.png`, or `.webp` files.
- **Permission errors**: Run the `.exe` as administrator or check folder permissions.
- **Large .exe size**: Normal due to bundled Python, Pillow, and ttkbootstrap (~70 MB).

## License
MIT License. Free to use and modify.

## Author
Developed by **SezanX**  
GitHub: [https://github.com/sezanX](https://github.com/sezanX)  
© 2025 Sezan Mahmood

## Contact
- **GitHub**: [sezanX](https://github.com/sezanX)
- **Report Issues**: Open an issue on the [GitHub repository](https://github.com/sezanX/ImageCompressorPro) or contact via email (add if desired).

---

*Powered by Python, Pillow, and ttkbootstrap. Built with ❤️ by SezanX.*
