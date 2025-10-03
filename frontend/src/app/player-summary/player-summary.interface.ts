/**
 * TypeScript interfaces for basketball player statistics.
 * These match the structure returned by the Django backend API.
 */

/**
 * Complete player summary including all statistics and rankings.
 */
export interface PlayerSummary {
  // Player identification
  name: string;
  playerID: number;

  // Overall statistics
  totalShotAttempts: number;
  totalPoints: number;
  totalPasses: number;
  totalPotentialAssists: number;
  totalTurnovers: number;
  totalPassingTurnovers: number;

  // Action type counts
  pickAndRollCount: number;
  isolationCount: number;
  postUpCount: number;
  offBallScreenCount: number;

  // Rankings (1 = best, higher numbers = worse)
  totalShotAttemptsRank: number;
  totalPointsRank: number;
  totalPassesRank: number;
  totalPotentialAssistsRank: number;
  totalTurnoversRank: number;
  totalPassingTurnoversRank: number;
  pickAndRollCountRank: number;
  isolationCountRank: number;
  postUpCountRank: number;
  offBallScreenCountRank: number;

  // Breakdown by action type
  pickAndRoll: ActionStats;
  isolation: ActionStats;
  postUp: ActionStats;
  offBallScreen: ActionStats;
}

/**
 * Statistics for a specific action type (Pick & Roll, Isolation, Post-Up, Off-Ball Screen).
 */
export interface ActionStats {
  totalShotAttempts: number;
  totalPoints: number;
  totalPasses: number;
  totalPotentialAssists: number;
  totalTurnovers: number;
  totalPassingTurnovers: number;
  shots: Shot[];           // Individual shot details
  passes: Pass[];          // Individual pass details
  turnovers: Turnover[];   // Individual turnover details
}

/**
 * Represents a single shot attempt.
 */
export interface Shot {
  loc: [number, number];   // [x, y] coordinates in feet from basket center
  points: number;          // Points scored (0, 1, 2, 3, or 4)
}

/**
 * Represents a single pass attempt.
 */
export interface Pass {
  startLoc: [number, number];    // [x, y] where pass started
  endLoc: [number, number];      // [x, y] where pass ended
  isCompleted: boolean;          // Whether pass was successfully completed
  isPotentialAssist: boolean;    // Whether pass led to a shot
  isTurnover: boolean;           // Whether pass resulted in turnover
}

/**
 * Represents a single turnover event.
 */
export interface Turnover {
  loc: [number, number];   // [x, y] where turnover occurred
}
