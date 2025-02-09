# Chess_Games_Review
Analyses chess games - moves and time performance.


Overview

This repository provides a suite of tools to analyze chess games using the Stockfish engine. It allows users to review game moves, classify mistakes, and extract insights from multiple PGN files. The analysis is structured using object-oriented programming with dedicated classes for handling game results and move classifications.

Features

Parses and extracts chess games from PGN files.

Analyzes game moves using Stockfish and categorizes them into classifications such as "blunder," "mistake," and "best move."

Extracts time control information and categorizes games into bullet, blitz, rapid, and classical formats.

Computes player accuracy and move quality statistics.

Outputs results in CSV format for further analysis.

File Structure

Database_Game_Review.py

Handles batch processing of multiple chess games, extracting relevant data, and saving analysis results.

Database_Game_Review_Classes.py

Contains core classes for handling game results and move classifications:

GameResults: Stores information about each game, including move evaluations and time control.

MoveClassification: Categorizes move types and organizes them by time control.

Single_Game_Review.py

Processes a single chess game, utilizing Stockfish to evaluate each move and classify it accordingly.

chess_review.py

Provides helper functions for game analysis, move classification, and Stockfish integration.

Requirements.txt

Lists all dependencies required to run the repository, including:

python-chess: For parsing PGN files and interacting with Stockfish.

pandas: For organizing and exporting game data.

numpy: For numerical computations.

tqdm: For progress tracking.

ipython: For interactive debugging and analysis.

Installation

Clone the repository:

git clone https://github.com/your_username/chess-review.git
cd chess-review

Install dependencies:

pip install -r requirements.txt

Usage

To analyze a batch of PGN games, run Database_Game_Review.py with a valid PGN file.

To analyze a single game, use Single_Game_Review.py with Stockfish.

Modify chess_review.py to fine-tune classification criteria and Stockfish settings.
