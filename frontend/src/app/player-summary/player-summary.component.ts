/**
 * Player Summary Component
 *
 * Displays comprehensive basketball statistics for a player, including:
 * - Overall statistics (shots, points, passes, assists, turnovers)
 * - Rankings compared to all players
 * - Shot chart visualization on basketball court
 * - Breakdown by action type (Pick & Roll, Isolation, Post-Up, Off-Ball Screen)
 */
import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';
import {PlayersService} from '../_services/players.service';
import {PlayerSummary} from './player-summary.interface';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {
  /** The player's complete statistics data from the API */
  playerSummary: PlayerSummary | null = null;

  /** Currently selected player ID (default: 0) */
  playerID: number = 0;

  /** Loading state indicator for async data fetching */
  loading: boolean = false;

  /** Error message if data fetch fails */
  error: string | null = null;

  /** Currently selected action type filter (not currently used) */
  selectedActionType: string = 'all';

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) { }

  /**
   * Initialize component - loads data for default player (ID: 0)
   */
  ngOnInit(): void {
    this.loadPlayerData(this.playerID);
  }

  /**
   * Fetch player statistics from the backend API.
   *
   * @param playerID - The player's unique identifier
   */
  loadPlayerData(playerID: number): void {
    this.loading = true;
    this.error = null;

    // Call backend API via PlayersService
    this.playersService.getPlayerSummary(playerID).pipe(untilDestroyed(this)).subscribe({
      next: (data) => {
        this.playerSummary = data.apiResponse;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Failed to load player data';
        this.loading = false;
        console.error(err);
        this.cdr.detectChanges();
      }
    });
  }

  /**
   * Handle player ID change from user input.
   * Triggers a new data fetch for the selected player.
   *
   * @param newID - The new player ID to load
   */
  onPlayerIDChange(newID: number): void {
    this.playerID = newID;
    this.loadPlayerData(newID);
  }

  /**
   * Cleanup on component destroy (handled by @UntilDestroy decorator)
   */
  ngOnDestroy() { }
}