import Database_Game_Review_Classes
import Single_Game_Review
import re
import numpy as np
import pandas as pd


def get_player_color(pgn_data, player_name):
    """Determine the color of the specified player."""
    if player_name in pgn_data:
        if f"""[White "{player_name}"]""" in pgn_data:
            return 0  # Player is white
        return 1  # Player is black
    else:
        raise KeyError("Player name not in PGN!")


def extract_player_results(game_results, color, start_time, increment):
    """Extract player-specific move classifications timestamps and turn times.

        Args:
            game_results (obj): A GameResults object containing game classification results.
            color (int): 0 for White, 1 for Black.
            start_time (int): Initial time control in seconds.
            increment (int): Time increment per move in seconds.

        Returns:
            dict: Contains classification list, time stamps list, and turn time list.
        """
    player_classification_list = []
    player_time_stamps_list = []
    player_turn_time_list = []

    current_time = start_time + increment

    for j, move in enumerate(game_results.classification_list):
        if j % 2 == color:
            player_classification_list.append(move)

            turn_stamp = game_results.get_time_stamps_list()[j]
            player_time_stamps_list.append(turn_stamp)
            player_turn_time_list.append(current_time - turn_stamp)
            current_time = turn_stamp + increment

    return {
        "classification_list": player_classification_list,
        "time_stamps_list": player_time_stamps_list,
        "turn_time_list": player_turn_time_list
    }


def extract_games_from_pgn(file_path):
    """Extract individual games from a PGN file.

        Args:
            file_path (str): Path to the PGN file.

        Returns:
            list: A list of game strings extracted from the PGN file.
        """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split at every `[Event "Some Event"]` header while keeping the delimiter
    games = re.split(r'(?=\[Event\s+".*?"\])', content)

    # Remove empty entries and strip whitespace
    games = [game.strip() for game in games if game.strip()]

    return games


def classify_time_stamps(player_results, move_classification_obj):
    """Classify moves based on strength and add them to respective time stamps lists.

        Args:
            player_results (dict): Dictionary containing move classifications and times.
            move_classification_obj (obj): MoveClassification object where categorized times are stored.
        """
    blunder_list = []
    mistake_list = []
    inaccuracy_list = []
    good_list = []
    excellent_list = []
    best_list = []
    book_list = []

    for j, move in enumerate(player_results["classification_list"]):
        time = player_results["turn_time_list"][j]
        if move == "blunder" and time: blunder_list.append(time)
        elif move == "mistake" and time: mistake_list.append(time)
        elif move == "inaccuracy" and time: inaccuracy_list.append(time)
        elif move == "good" and time: good_list.append(time)
        elif move == "excellent" and time: excellent_list.append(time)
        elif move == "best" and time: best_list.append(time)
        elif move == "book" and time: book_list.append(time)

    move_classification_obj.categories["blunder"].extend(blunder_list)
    move_classification_obj.categories["mistake"].extend(mistake_list)
    move_classification_obj.categories["inaccuracy"].extend(inaccuracy_list)
    move_classification_obj.categories["good"].extend(good_list)
    move_classification_obj.categories["excellent"].extend(excellent_list)
    move_classification_obj.categories["best"].extend(best_list)
    move_classification_obj.categories["book"].extend(book_list)
    move_classification_obj.this_time_control_was_analysed = True


def determine_time_control(start_time):
    if start_time <= 60:
        return "bullet"
    if start_time <= 300:
        return "blitz"
    if start_time <= 1800:
        return "rapid"
    return "classic"


def extract_time_control(game_data):
    # Look for the 'TimeControl' field and extract the value
    match = re.search(r'\[TimeControl "([^"]+)"\]', game_data)
    if match:
        time_control = match.group(1)
        # Split the time control into main time and increment
        start_time, increment = time_control.split('+')
        return int(start_time), int(increment)
    else:
        return None, None


def display_and_save_player_results(game_num, move_classification_objects_list):
    print(f"-------------- Games Reviewed {game_num} --------------")

    categories = ["book", "blunder", "mistake", "inaccuracy", "good", "excellent", "best"]

    for obj in move_classification_objects_list:
        if not obj.this_time_control_was_analysed:
            continue
        print(f"-------------- {obj.time_control_str} Games --------------")
        for category in categories:
            times = np.array(obj.categories[category], dtype=np.float64)

            if np.all(np.isnan(times)):  # Check if all values are NaN
                print(f"Average time spent for making {category}: No valid data")
                continue

            avg = np.nanmean(times)  # Compute avg while ignoring NaN values
            print(f"Average time spent for making {category}: {avg:.1f}")

        # Save data:
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in obj.categories.items()]))
        df.to_csv(f"{obj.time_control_str}_games.csv", index=False)
    print("CSV files saved successfully!")


if __name__ == "__main__":
    games_path = "chess_com_games_2025-02-07.pgn"
    player_name = "Yoavzz"  # my username in Chess.com

    games = extract_games_from_pgn(games_path)
    total_games = len(games)

    bullet = Database_Game_Review_Classes.MoveClassification("Bullet")
    blitz = Database_Game_Review_Classes.MoveClassification("Blitz")
    rapid = Database_Game_Review_Classes.MoveClassification("Rapid")
    classic = Database_Game_Review_Classes.MoveClassification("Classic")

    for i, game in enumerate(games):
        start_time, increment = extract_time_control(game)
        time_control = determine_time_control(start_time)
        if not start_time:  # No time data in this game
            total_games -= 1
            continue
        print(f"-------------- Reviewing Game {i + 1}/{total_games} --------------")

        results = Single_Game_Review.Game_Review(game, print_results=False)
        player_color = get_player_color(game, player_name)
        player_results = extract_player_results(results, player_color, start_time, increment)

        match time_control:
            case "bullet": classify_time_stamps(player_results, bullet)
            case "blitz": classify_time_stamps(player_results, blitz)
            case "rapid": classify_time_stamps(player_results, rapid)
            case "classic": classify_time_stamps(player_results, classic)

    display_and_save_player_results(total_games, [bullet, blitz, rapid, classic])

