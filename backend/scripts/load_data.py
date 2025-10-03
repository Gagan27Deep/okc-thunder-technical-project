#!/usr/bin/env python
"""
Data loading script for OKC Thunder Basketball Stats Database
Loads data from JSON files in backend/raw_data/ into PostgreSQL database
Can be run multiple times without creating duplicates
"""

import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from app.dbmodels.models import Team, Game, Player, Shot, Pass, Turnover


def load_teams(data_dir):
    """
    Load teams from teams.json into the database.

    Uses update_or_create() to make the operation idempotent - running this
    multiple times will not create duplicate teams.

    Args:
        data_dir (str): Path to directory containing JSON data files
    """
    print("Loading teams...")
    teams_file = os.path.join(data_dir, 'teams.json')

    with open(teams_file, 'r') as f:
        teams_data = json.load(f)

    for team_data in teams_data:
        # Create team if it doesn't exist, or update if it does
        Team.objects.update_or_create(
            team_id=team_data['team_id'],
            defaults={'name': team_data['name']}
        )

    print(f"Loaded {len(teams_data)} teams")


def load_games(data_dir):
    """
    Load games from games.json into the database.

    Uses update_or_create() to make the operation idempotent.

    Args:
        data_dir (str): Path to directory containing JSON data files
    """
    print("Loading games...")
    games_file = os.path.join(data_dir, 'games.json')

    with open(games_file, 'r') as f:
        games_data = json.load(f)

    for game_data in games_data:
        # Create game if it doesn't exist, or update if it does
        Game.objects.update_or_create(
            id=game_data['id'],
            defaults={'date': game_data['date']}
        )

    print(f"Loaded {len(games_data)} games")


def load_players(data_dir):
    """
    Load players and their associated shots, passes, and turnovers from players.json.

    This function processes the nested JSON structure where each player object contains
    arrays of shots, passes, and turnovers. Uses update_or_create() for idempotency.

    Args:
        data_dir (str): Path to directory containing JSON data files
    """
    print("Loading players and stats...")
    players_file = os.path.join(data_dir, 'players.json')

    with open(players_file, 'r') as f:
        players_data = json.load(f)

    for player_data in players_data:
        # Create or update player record
        player, created = Player.objects.update_or_create(
            player_id=player_data['player_id'],
            defaults={
                'name': player_data['name'],
                'team_id': player_data['team_id']
            }
        )

        # Load all shots for this player
        for shot_data in player_data.get('shots', []):
            Shot.objects.update_or_create(
                id=shot_data['id'],
                defaults={
                    'player_id': player.player_id,
                    'game_id': shot_data['game_id'],
                    'points': shot_data['points'],
                    'shooting_foul_drawn': shot_data['shooting_foul_drawn'],
                    'shot_loc_x': shot_data['shot_loc_x'],
                    'shot_loc_y': shot_data['shot_loc_y'],
                    'action_type': shot_data['action_type']
                }
            )

        # Load all passes for this player
        for pass_data in player_data.get('passes', []):
            Pass.objects.update_or_create(
                id=pass_data['id'],
                defaults={
                    'player_id': player.player_id,
                    'game_id': pass_data['game_id'],
                    'completed_pass': pass_data['completed_pass'],
                    'potential_assist': pass_data['potential_assist'],
                    'turnover': pass_data['turnover'],
                    'ball_start_loc_x': pass_data['ball_start_loc_x'],
                    'ball_start_loc_y': pass_data['ball_start_loc_y'],
                    'ball_end_loc_x': pass_data['ball_end_loc_x'],
                    'ball_end_loc_y': pass_data['ball_end_loc_y'],
                    'action_type': pass_data['action_type']
                }
            )

        # Load all turnovers for this player
        for tov_data in player_data.get('turnovers', []):
            Turnover.objects.update_or_create(
                id=tov_data['id'],
                defaults={
                    'player_id': player.player_id,
                    'game_id': tov_data['game_id'],
                    'tov_loc_x': tov_data['tov_loc_x'],
                    'tov_loc_y': tov_data['tov_loc_y'],
                    'action_type': tov_data['action_type']
                }
            )

    print(f"Loaded {len(players_data)} players with their stats")


def main():
    """
    Main function to orchestrate data loading.

    Loads data in the correct order to respect foreign key dependencies:
    1. Teams (no dependencies)
    2. Games (no dependencies)
    3. Players (depends on Teams)
    4. Shots, Passes, Turnovers (depends on Players and Games)

    Prints summary statistics after loading is complete.
    """
    # Get the directory containing raw data files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), 'raw_data')

    print(f"Loading data from: {data_dir}")
    print("=" * 50)

    # Load data in order (respecting foreign key dependencies)
    load_teams(data_dir)
    load_games(data_dir)
    load_players(data_dir)  # Also loads shots, passes, and turnovers

    print("=" * 50)
    print("Data loading complete!")

    # Print summary statistics
    print("\nDatabase Summary:")
    print(f"  Teams: {Team.objects.count()}")
    print(f"  Games: {Game.objects.count()}")
    print(f"  Players: {Player.objects.count()}")
    print(f"  Shots: {Shot.objects.count()}")
    print(f"  Passes: {Pass.objects.count()}")
    print(f"  Turnovers: {Turnover.objects.count()}")


if __name__ == '__main__':
    main()
