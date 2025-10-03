"""
Player statistics helper functions.
Provides functions to query and aggregate basketball statistics from the database.
"""
import json
import os
import random

from app.dbmodels.models import Player, Shot, Pass, Turnover


def get_player_summary_stats(player_id: str):
    """
    Get comprehensive player summary statistics from the database.

    Aggregates all shots, passes, and turnovers for a given player,
    broken down by action type (Pick & Roll, Isolation, Post-Up, Off-Ball Screen).

    Args:
        player_id (str): The player's unique identifier

    Returns:
        dict: Player statistics including:
            - name, playerID
            - Total stats (shots, points, passes, assists, turnovers)
            - Action counts for each play type
            - Detailed breakdown by action type with shot/pass/turnover data

    Raises:
        Returns error dict if player not found
    """
    try:
        player = Player.objects.get(player_id=int(player_id))
    except Player.DoesNotExist:
        return {"error": f"Player with ID {player_id} not found"}

    # Query all shots, passes, and turnovers for this player from database
    shots = Shot.objects.filter(player=player)
    passes = Pass.objects.filter(player=player)
    turnovers = Turnover.objects.filter(player=player)

    def get_action_stats(action_type):
        """
        Calculate statistics for a specific action type.

        Args:
            action_type (str): The play type (pickAndRoll, isolation, postUp, offBallScreen)

        Returns:
            dict: Aggregated stats for this action type including shot/pass/turnover details
        """
        action_shots = shots.filter(action_type=action_type)
        action_passes = passes.filter(action_type=action_type)
        action_turnovers = turnovers.filter(action_type=action_type)

        # Format shots
        shots_data = [
            {
                "loc": [shot.shot_loc_x, shot.shot_loc_y],
                "points": shot.points
            }
            for shot in action_shots
        ]

        # Format passes
        passes_data = [
            {
                "startLoc": [p.ball_start_loc_x, p.ball_start_loc_y],
                "endLoc": [p.ball_end_loc_x, p.ball_end_loc_y],
                "isCompleted": p.completed_pass,
                "isPotentialAssist": p.potential_assist,
                "isTurnover": p.turnover
            }
            for p in action_passes
        ]

        # Format turnovers (non-passing turnovers)
        turnovers_data = [
            {"loc": [tov.tov_loc_x, tov.tov_loc_y]}
            for tov in action_turnovers
        ]

        return {
            "totalShotAttempts": action_shots.count(),
            "totalPoints": sum(shot.points for shot in action_shots),
            "totalPasses": action_passes.count(),
            "totalPotentialAssists": action_passes.filter(potential_assist=True).count(),
            "totalTurnovers": action_turnovers.count() + action_passes.filter(turnover=True).count(),
            "totalPassingTurnovers": action_passes.filter(turnover=True).count(),
            "shots": shots_data,
            "passes": passes_data,
            "turnovers": turnovers_data
        }

    # Get stats for each action type
    pick_and_roll = get_action_stats("pickAndRoll")
    isolation = get_action_stats("isolation")
    post_up = get_action_stats("postUp")
    off_ball_screen = get_action_stats("offBallScreen")

    # Calculate overall totals
    total_shot_attempts = shots.count()
    total_points = sum(shot.points for shot in shots)
    total_passes = passes.count()
    total_potential_assists = passes.filter(potential_assist=True).count()
    total_turnovers = turnovers.count() + passes.filter(turnover=True).count()
    total_passing_turnovers = passes.filter(turnover=True).count()

    # Count actions by type
    pick_and_roll_count = shots.filter(action_type="pickAndRoll").count() + \
                          passes.filter(action_type="pickAndRoll").count() + \
                          turnovers.filter(action_type="pickAndRoll").count()

    isolation_count = shots.filter(action_type="isolation").count() + \
                      passes.filter(action_type="isolation").count() + \
                      turnovers.filter(action_type="isolation").count()

    post_up_count = shots.filter(action_type="postUp").count() + \
                    passes.filter(action_type="postUp").count() + \
                    turnovers.filter(action_type="postUp").count()

    off_ball_screen_count = shots.filter(action_type="offBallScreen").count() + \
                            passes.filter(action_type="offBallScreen").count() + \
                            turnovers.filter(action_type="offBallScreen").count()

    return {
        "name": player.name,
        "playerID": player.player_id,
        "totalShotAttempts": total_shot_attempts,
        "totalPoints": total_points,
        "totalPasses": total_passes,
        "totalPotentialAssists": total_potential_assists,
        "totalTurnovers": total_turnovers,
        "totalPassingTurnovers": total_passing_turnovers,
        "pickAndRollCount": pick_and_roll_count,
        "isolationCount": isolation_count,
        "postUpCount": post_up_count,
        "offBallScreenCount": off_ball_screen_count,
        "pickAndRoll": pick_and_roll,
        "isolation": isolation,
        "postUp": post_up,
        "offBallScreen": off_ball_screen
    }


def get_ranks(player_id: str, player_summary: dict):
    """
    Calculate rankings for a player's statistics against all other players.

    Ranks are calculated by counting how many players have better (higher) values
    for each statistic. Rank 1 means the player has the highest value for that stat.

    Args:
        player_id (str): The player's unique identifier
        player_summary (dict): The player's statistics from get_player_summary_stats()

    Returns:
        dict: Rankings for all statistics (1 = best, higher numbers = worse ranking)
            - totalShotAttemptsRank, totalPointsRank, totalPassesRank, etc.
    """
    from django.db.models import Count, Sum, Q

    # Get all players for comparison
    all_players = Player.objects.all()

    def calculate_rank(stat_name, player_value):
        """
        Calculate rank for a specific statistic.

        Args:
            stat_name (str): Name of the statistic to rank
            player_value (int): The player's value for this statistic

        Returns:
            int: Rank (1-indexed, 1 is best)
        """
        if stat_name == 'totalShotAttempts':
            # Count shots for each player and rank
            better_count = Player.objects.annotate(
                shot_count=Count('shots')
            ).filter(shot_count__gt=player_value).count()

        elif stat_name == 'totalPoints':
            # Sum points for each player and rank
            better_count = 0
            for p in all_players:
                total = Shot.objects.filter(player=p).aggregate(Sum('points'))['points__sum'] or 0
                if total > player_value:
                    better_count += 1

        elif stat_name == 'totalPasses':
            better_count = Player.objects.annotate(
                pass_count=Count('passes')
            ).filter(pass_count__gt=player_value).count()

        elif stat_name == 'totalPotentialAssists':
            better_count = Player.objects.annotate(
                assist_count=Count('passes', filter=Q(passes__potential_assist=True))
            ).filter(assist_count__gt=player_value).count()

        elif stat_name == 'totalTurnovers':
            better_count = Player.objects.annotate(
                tov_count=Count('turnovers') + Count('passes', filter=Q(passes__turnover=True))
            ).filter(tov_count__gt=player_value).count()

        elif stat_name == 'totalPassingTurnovers':
            better_count = Player.objects.annotate(
                pass_tov_count=Count('passes', filter=Q(passes__turnover=True))
            ).filter(pass_tov_count__gt=player_value).count()

        elif stat_name == 'pickAndRollCount':
            better_count = 0
            for p in all_players:
                count = (Shot.objects.filter(player=p, action_type='pickAndRoll').count() +
                        Pass.objects.filter(player=p, action_type='pickAndRoll').count() +
                        Turnover.objects.filter(player=p, action_type='pickAndRoll').count())
                if count > player_value:
                    better_count += 1

        elif stat_name == 'isolationCount':
            better_count = 0
            for p in all_players:
                count = (Shot.objects.filter(player=p, action_type='isolation').count() +
                        Pass.objects.filter(player=p, action_type='isolation').count() +
                        Turnover.objects.filter(player=p, action_type='isolation').count())
                if count > player_value:
                    better_count += 1

        elif stat_name == 'postUpCount':
            better_count = 0
            for p in all_players:
                count = (Shot.objects.filter(player=p, action_type='postUp').count() +
                        Pass.objects.filter(player=p, action_type='postUp').count() +
                        Turnover.objects.filter(player=p, action_type='postUp').count())
                if count > player_value:
                    better_count += 1

        elif stat_name == 'offBallScreenCount':
            better_count = 0
            for p in all_players:
                count = (Shot.objects.filter(player=p, action_type='offBallScreen').count() +
                        Pass.objects.filter(player=p, action_type='offBallScreen').count() +
                        Turnover.objects.filter(player=p, action_type='offBallScreen').count())
                if count > player_value:
                    better_count += 1

        else:
            return 1

        return better_count + 1  # Rank is count of better players + 1

    return {
        "totalShotAttemptsRank": calculate_rank('totalShotAttempts', player_summary.get('totalShotAttempts', 0)),
        "totalPointsRank": calculate_rank('totalPoints', player_summary.get('totalPoints', 0)),
        "totalPassesRank": calculate_rank('totalPasses', player_summary.get('totalPasses', 0)),
        "totalPotentialAssistsRank": calculate_rank('totalPotentialAssists', player_summary.get('totalPotentialAssists', 0)),
        "totalTurnoversRank": calculate_rank('totalTurnovers', player_summary.get('totalTurnovers', 0)),
        "totalPassingTurnoversRank": calculate_rank('totalPassingTurnovers', player_summary.get('totalPassingTurnovers', 0)),
        "pickAndRollCountRank": calculate_rank('pickAndRollCount', player_summary.get('pickAndRollCount', 0)),
        "isolationCountRank": calculate_rank('isolationCount', player_summary.get('isolationCount', 0)),
        "postUpCountRank": calculate_rank('postUpCount', player_summary.get('postUpCount', 0)),
        "offBallScreenCountRank": calculate_rank('offBallScreenCount', player_summary.get('offBallScreenCount', 0)),
    }
