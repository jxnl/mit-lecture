# Improving RAG Applications - Presentation

This repository has a presentation made for the MIT Generative AI Course. It uses LaTeX with the beamer class and the Metropolis theme for a modern and clean look.

## Features

- A professional design with modern style.
- Custom colors using a primary blue.
- A clean footline showing the frame number and contact info.
- Easy to compile and update.
- Auto-compilation script that watches for changes and rebuilds the PDF.

## Requirements

- A recent LaTeX distribution (like TeX Live or MiKTeX).
- The Metropolis theme installed.
- Python 3.6+ (for the auto-compiler script).

## How to Compile

### Manual Compilation
1. Open your terminal.
2. Run the command: `xelatex main.tex` (or use another LaTeX tool you like).
3. Open the generated PDF to view the slides.

### Auto-Compilation
For a smoother workflow, use the included auto-compiler script:

1. Make sure the script is executable:
   ```
   chmod +x watch_and_compile.py
   ```

2. Run the script:
   ```
   ./watch_and_compile.py
   ```

3. The script will:
   - Watch for changes in all `.tex`, `.bib`, `.cls`, and `.sty` files
   - Automatically compile the PDF when changes are detected
   - Show compilation errors if they occur

4. Press `Ctrl+C` to stop the script

## Contribution

You can fork this repository and share your improvements. All contributions are welcome!

## License

This project is open source. 

## Project Structure

```
.
├── images/         # Store presentation images here
├── sections/       # Store presentation section files here
├── main.tex        # Main presentation file
├── references.bib  # Bibliography file
├── watch_and_compile.py # Auto-compiler script
└── README.md       # This file
``` 