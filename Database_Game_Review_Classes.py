
class GameResults:
    """
        Represents the results of a chess game, including move evaluations, time control data, and player performance.

        Attributes:
            san_moves (list[str]): List of moves in Standard Algebraic Notation (SAN).
            scores (list[int | float]): List of engine evaluations after each move.
            classification_list (list[str]): List of move classifications (e.g., "blunder", "good").
            san_best_moves (list[str]): List of best moves suggested by the engine.
            review_list (list[str]): List of additional review comments for each move.
            white_elo (int): Estimated Elo rating of the white player.
            black_elo (int): Estimated Elo rating of the black player.
            white_acc (float): Accuracy score of the white player.
            black_acc (float): Accuracy score of the black player.
            avg_cpl_white (float): Average centipawn loss for white.
            avg_cpl_black (float): Average centipawn loss for black.
            time_control (list[int, int, list[float]]): A list containing start time, increment, and timestamps.

        Methods:
            get_start_time() -> int:
                Returns the game's start time in seconds.

            get_time_increment() -> int:
                Returns the game's time increment per move in seconds.

            get_time_stamps_list() -> list[float]:
                Returns the list of time stamps for each move.
        """
    def __init__(self,
                 san_moves,
                 scores,
                 classification_list,
                 san_best_moves,
                 review_list,
                 white_elo_est,
                 black_elo_est,
                 white_acc,
                 black_acc,
                 avg_cpl_white,
                 avg_cpl_black,
                 start_time,
                 time_increment,
                 time_stamps_list,
                 ) -> None:

        self.san_moves = san_moves
        self.scores = scores
        self.classification_list = classification_list
        self.san_best_moves = san_best_moves
        self.review_list = review_list
        self.white_elo = white_elo_est
        self.black_elo = black_elo_est
        self.white_acc = white_acc
        self.black_acc = black_acc
        self.avg_cpl_white = avg_cpl_white
        self.avg_cpl_black = avg_cpl_black
        self.time_control = [start_time, time_increment, time_stamps_list]

    def get_start_time(self):
        """Returns the game's start time in seconds."""
        return self.time_control[0]

    def get_time_increment(self):
        """Returns the game's time increment per move in seconds."""
        return self.time_control[1]

    def get_time_stamps_list(self):
        """Returns the list of time stamps for each move."""
        return self.time_control[2]


class MoveClassification:
    """
        Stores and categorizes moves based on classification types (e.g., blunders, mistakes, best moves) for a given time control.

        Attributes:
            categories (dict[str, list[float]]): A dictionary mapping move classifications to lists of recorded times.
            this_time_control_was_analysed (bool): Indicates if this time control category has been analysed.
            time_control_str (str): The time control category (e.g., "Bullet", "Blitz", "Rapid", "Classic").

        Methods:
            __getitem__(key: str) -> list[float]:
                Retrieves the list of recorded times for a given move classification.

            __setitem__(key: str, value: list[float]) -> None:
                Sets the list of recorded times for a given move classification.

            __repr__() -> str:
                Returns a string representation of the MoveClassification object.
        """
    def __init__(self, time_control):
        self.categories = {
            "blunder": [],
            "mistake": [],
            "inaccuracy": [],
            "good": [],
            "excellent": [],
            "best": [],
            "book": [],
        }
        self.this_time_control_was_analysed = False

        time_control_categories = ["Bullet", "Blitz", "Rapid", "Classic"]
        if time_control not in time_control_categories:
            raise KeyError("Valid time control categories include bullet, blitz, rapid, classic.")
        self.time_control_str = time_control

    def __getitem__(self, key):
        """Retrieves the list of recorded times for a given move classification."""
        if key in self.categories:
            return self.categories[key]
        raise KeyError(f"Invalid key: {key}. Valid keys: {list(self.categories.keys())}")

    def __setitem__(self, key, value):
        """Sets the list of recorded times for a given move classification."""
        if key in self.categories:
            self.categories[key] = value
        else:
            raise KeyError(f"Invalid key: {key}. Valid keys: {list(self.categories.keys())}")

    def __repr__(self):
        """Returns a string representation of the MoveClassification object."""
        return f"MoveClassification(time_control={self.time_control_str}, categories={self.categories})"
