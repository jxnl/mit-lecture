#!/usr/bin/env python3
"""
LaTeX Auto-Compiler

This script watches for changes in LaTeX files and automatically compiles
the main document when changes are detected.

Usage:
    python watch_and_compile.py [main_file]

    If main_file is not provided, defaults to 'main.tex'
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
except ImportError:
    print("Required package 'watchdog' not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent


class LatexCompiler:
    """Handles the compilation of LaTeX documents."""

    def __init__(self, main_file: str = "main.tex"):
        """
        Initialize the LaTeX compiler.

        Args:
            main_file: Path to the main LaTeX file (default: 'main.tex')
        """
        self.main_file = main_file
        self.main_file_path = Path(main_file)
        self.base_name = self.main_file_path.stem
        self.last_compile_time = 0
        self.compile_cooldown = 2  # seconds

    def compile(self) -> None:
        """Compile the LaTeX document using pdflatex."""
        current_time = time.time()

        # Avoid compiling too frequently
        if current_time - self.last_compile_time < self.compile_cooldown:
            return

        self.last_compile_time = current_time

        print(
            f"\n[{time.strftime('%H:%M:%S')}] Changes detected. Compiling {self.main_file}..."
        )

        try:
            # Run pdflatex twice to resolve references
            for i in range(2):
                process = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", self.main_file],
                    capture_output=True,
                    text=True,
                )

                if process.returncode != 0:
                    print("Error during compilation:")
                    # Extract and print relevant error messages
                    for line in process.stdout.split("\n"):
                        if "error" in line.lower() or "fatal" in line.lower():
                            print(f"  {line.strip()}")
                    return

            print(
                f"[{time.strftime('%H:%M:%S')}] Successfully compiled {self.base_name}.pdf"
            )

        except Exception as e:
            print(f"Compilation failed: {e}")


class LatexFileHandler(FileSystemEventHandler):
    """Handles file system events for LaTeX files."""

    def __init__(self, compiler: LatexCompiler, watched_extensions: List[str]):
        """
        Initialize the file handler.

        Args:
            compiler: The LaTeX compiler instance
            watched_extensions: List of file extensions to watch
        """
        self.compiler = compiler
        self.watched_extensions = watched_extensions

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handle file modification events.

        Args:
            event: The file system event
        """
        if not event.is_directory and self._is_relevant_file(event.src_path):
            self.compiler.compile()

    def _is_relevant_file(self, path: str) -> bool:
        """
        Check if the file is relevant for LaTeX compilation.

        Args:
            path: Path to the file

        Returns:
            True if the file should trigger compilation, False otherwise
        """
        return any(path.endswith(ext) for ext in self.watched_extensions)


def main() -> None:
    """Main function to run the LaTeX auto-compiler."""
    # Get main file from command line args or use default
    main_file = sys.argv[1] if len(sys.argv) > 1 else "main.tex"

    if not os.path.exists(main_file):
        print(f"Error: File '{main_file}' not found.")
        sys.exit(1)

    # Initialize compiler and event handler
    compiler = LatexCompiler(main_file)
    watched_extensions = [".tex", ".bib", ".cls", ".sty"]
    event_handler = LatexFileHandler(compiler, watched_extensions)

    # Set up the observer
    observer = Observer()
    # Watch the current directory and all subdirectories
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    # Initial compilation
    compiler.compile()

    print(
        f"\nWatching for changes in LaTeX files (extensions: {', '.join(watched_extensions)})"
    )
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
