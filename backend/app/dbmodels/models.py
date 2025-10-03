# -*- coding: utf-8 -*-
"""
Django models for basketball statistics database.
Implements a normalized schema with 6 tables for teams, games, players, shots, passes, and turnovers.
"""
from django.db import models


class Team(models.Model):
    """
    Represents a basketball team.

    Attributes:
        team_id (int): Unique identifier for the team (primary key)
        name (str): Name of the team
    """
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Game(models.Model):
    """
    Represents a basketball game.

    Attributes:
        id (int): Unique identifier for the game (primary key)
        date (date): Date when the game was played
    """
    id = models.IntegerField(primary_key=True)
    date = models.DateField()

    class Meta:
        db_table = 'games'

    def __str__(self):
        return f"Game {self.id} on {self.date}"


class Player(models.Model):
    """
    Represents a basketball player.

    Attributes:
        player_id (int): Unique identifier for the player (primary key)
        name (str): Name of the player
        team (ForeignKey): Reference to the player's team
    """
    player_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')

    class Meta:
        db_table = 'players'

    def __str__(self):
        return self.name


class Shot(models.Model):
    """
    Represents a shot attempt by a player in a game.

    Attributes:
        id (int): Unique identifier for the shot (primary key)
        player (ForeignKey): Reference to the player who took the shot
        game (ForeignKey): Reference to the game where shot occurred
        points (int): Points scored (0, 1, 2, 3, or 4)
        shooting_foul_drawn (bool): Whether a shooting foul was drawn
        shot_loc_x (float): X coordinate of shot location (feet from basket)
        shot_loc_y (float): Y coordinate of shot location (feet from basket)
        action_type (str): Type of action (pickAndRoll, isolation, postUp, offBallScreen)
    """
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='shots', db_column='player_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='shots', db_column='game_id')
    points = models.IntegerField()
    shooting_foul_drawn = models.BooleanField()
    shot_loc_x = models.FloatField()
    shot_loc_y = models.FloatField()
    action_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'shots'

    def __str__(self):
        return f"Shot {self.id} by {self.player.name}"


class Pass(models.Model):
    """
    Represents a pass attempt by a player in a game.

    Attributes:
        id (int): Unique identifier for the pass (primary key)
        player (ForeignKey): Reference to the player who made the pass
        game (ForeignKey): Reference to the game where pass occurred
        completed_pass (bool): Whether the pass was completed successfully
        potential_assist (bool): Whether the pass led to a shot (potential assist)
        turnover (bool): Whether the pass resulted in a turnover
        ball_start_loc_x (float): X coordinate where pass started (feet)
        ball_start_loc_y (float): Y coordinate where pass started (feet)
        ball_end_loc_x (float): X coordinate where pass ended (feet)
        ball_end_loc_y (float): Y coordinate where pass ended (feet)
        action_type (str): Type of action (pickAndRoll, isolation, postUp, offBallScreen)
    """
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='passes', db_column='player_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='passes', db_column='game_id')
    completed_pass = models.BooleanField()
    potential_assist = models.BooleanField()
    turnover = models.BooleanField()
    ball_start_loc_x = models.FloatField()
    ball_start_loc_y = models.FloatField()
    ball_end_loc_x = models.FloatField()
    ball_end_loc_y = models.FloatField()
    action_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'passes'

    def __str__(self):
        return f"Pass {self.id} by {self.player.name}"


class Turnover(models.Model):
    """
    Represents a turnover by a player in a game.

    Attributes:
        id (int): Unique identifier for the turnover (primary key)
        player (ForeignKey): Reference to the player who committed the turnover
        game (ForeignKey): Reference to the game where turnover occurred
        tov_loc_x (float): X coordinate where turnover occurred (feet)
        tov_loc_y (float): Y coordinate where turnover occurred (feet)
        action_type (str): Type of action (pickAndRoll, isolation, postUp, offBallScreen)
    """
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='turnovers', db_column='player_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='turnovers', db_column='game_id')
    tov_loc_x = models.FloatField()
    tov_loc_y = models.FloatField()
    action_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'turnovers'

    def __str__(self):
        return f"Turnover {self.id} by {self.player.name}"
