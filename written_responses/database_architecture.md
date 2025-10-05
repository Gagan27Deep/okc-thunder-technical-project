
# Database Architecture Description

## Overview
The database implements a star schema design with a normalized relational structure, optimizing for both data integrity and query performance. Six interconnected tables store comprehensive basketball statistics across teams, games, players, and individual actions.

## Schema Design

### Core Entities
- **Teams Table** (`team_id*`): Dimension table storing team metadata
- **Games Table** (`id*`): Dimension table with temporal data (game dates)
- **Players Table** (`player_id*`, `team_id→Teams`): Dimension table linking players to teams

### Fact Tables
- **Shots Table** (`id*`, `player_id→Players`, `game_id→Games`): Records shot attempts with spatial coordinates (x, y in feet from basket center), points scored, foul drawn status, and halfcourt action type (pickAndRoll, isolation, postUp, offBallScreen)
- **Passes Table** (`id*`, `player_id→Players`, `game_id→Games`): Captures pass events with origin/destination coordinates, completion status, assist potential, and turnover flags
- **Turnovers Table** (`id*`, `player_id→Players`, `game_id→Games`): Tracks non-passing turnovers with spatial data and associated action types

## Design Rationale
This normalized architecture achieves 3NF (Third Normal Form), eliminating redundancy from the original nested JSON structure while maintaining complete data fidelity. Strategic foreign key constraints ensure referential integrity across all relationships. The separation of event types (shots/passes/turnovers) into distinct fact tables enables efficient aggregation queries and supports flexible analytics—critical for generating player summary statistics and league-wide rankings. Indexed foreign keys on `player_id` and `game_id` optimize JOIN operations for the API endpoints.
