import csv

from models.game import game


def is_duplicate_game(game_name: str, seen_names: set) -> bool:
    return game_name in seen_names


def is_complete_game(game: dict, required_keys: list) -> bool:
    return all(key in game for key in required_keys)


def save_games_to_csv(games: list, filename: str):
    if not games:
        print("No games to save.")
        return

    # Use field names from the game model
    fieldnames = game.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)
    print(f"Saved {len(games)} games to '{filename}'.")
