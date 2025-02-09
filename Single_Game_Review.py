import os.path
import chess_review
import Database_Game_Review_Classes

# Configurations
USE_TIME_LIMIT = True  # Set to False to use depth-based evaluation
TIME_LIMIT = 0.5  # Time in seconds per move (if using time)
DEPTH_LIMIT = 15  # Search depth (if using depth)


def configure_stockfish():
    """Configure Stockfish settings based on time or depth."""
    if USE_TIME_LIMIT:
        chess_review.STOCKFISH_CONFIG = {'time': TIME_LIMIT}
    else:
        chess_review.STOCKFISH_CONFIG = {'depth': DEPTH_LIMIT}


def load_pgn(file_path):
    """Load PGN data from a file."""
    with open(file_path, "r") as file:
        return file.read()


def analyze_game(pgn_data):
    """Run full analysis on the given PGN data."""
    # Parse PGN
    uci_moves, san_moves, fens, time_stamps_list, time_increment, starting_time = chess_review.parse_pgn(pgn_data)

    # Compute centipawn loss (CPL) and estimated ELO
    scores, cpls_white, cpls_black, avg_cpl_white, avg_cpl_black = chess_review.compute_cpl(uci_moves)
    n_moves = len(scores) // 2  # Number of full moves
    white_elo_est = chess_review.estimate_elo(avg_cpl_white, n_moves)
    black_elo_est = chess_review.estimate_elo(avg_cpl_black, n_moves)

    # Compute accuracy scores
    white_acc, black_acc = chess_review.calculate_accuracy(scores)

    # Compute additional metrics
    devs, mobs, tens, conts = chess_review.calculate_metrics(fens)

    # Review the game moves
    review_list, best_review_list, classification_list, uci_best_moves, san_best_moves = chess_review.review_game(
        uci_moves, roast=False)

    return Database_Game_Review_Classes.GameResults(
            san_moves=san_moves,
            scores=scores,
            classification_list=classification_list,
            san_best_moves=san_best_moves,
            review_list=review_list,
            white_elo_est=round(white_elo_est),
            black_elo_est=round(black_elo_est),
            white_acc=round(white_acc),
            black_acc=round(black_acc),
            avg_cpl_white=round(avg_cpl_white),
            avg_cpl_black=round(avg_cpl_black),
            start_time=starting_time,
            time_increment=time_increment,
            time_stamps_list=time_stamps_list)


def display_results(results):
    """Print the results of the chess analysis."""
    print("\n=== Chess Game Analysis ===")
    print(f"Estimated ELO: White - {results.white_elo}, Black - {results.black_elo}")
    print(f"Accuracy: White - {results.white_acc}%, Black - {results.black_acc}%")
    print(f"Average Centipawn Loss: White - {results.avg_cpl_white}, Black - {results.avg_cpl_black}")

    print("\n=== Move Analysis ===")
    for i, move in enumerate(results.san_moves):
        print(
            f"Move {i + 1}: {move} | Score: {results.scores[i]} | Classification: {results.classification_list[i]} | Time: {results.get_time_stamps_list()[i]}")

    print("\n=== Best Move Suggestions ===")
    for i, best_move in enumerate(results.san_best_moves):
        print(f"Move {i + 1}: {results.san_moves[i]} → Suggested: {best_move}")

    print("\n=== Move Reviews ===")
    for i, move in enumerate(results["review_list"]):
        print(f"Move {i + 1}: {move}")


def check_input(pgn):
    if isinstance(pgn, str):
        if os.path.isfile(pgn):
            # If it's a valid file path, load PGN data
            return load_pgn(pgn)
        else:  # Not an existing file
            if "Black" in pgn and "White" in pgn:  # Check that given text is likely a PGN text.
                return pgn
            else:
                raise TypeError("Input must be a valid PGN string or a file path.")
    else:
        raise TypeError("Input must be a valid PGN string or a file path.")


def Game_Review(pgn_data, print_results=True):
    configure_stockfish()
    pgn_data = check_input(pgn_data)
    results = analyze_game(pgn_data)
    if print_results:
        display_results(results)
    return results
