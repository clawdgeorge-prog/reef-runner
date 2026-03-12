# Quantum Vault

Quantum Vault is now a simpler, more mobile-first neon arcade maze game.

## Core loop
- Collect every shard in the maze
- The exit opens when the maze is clear
- Escape to advance to the next district
- Use Pulse Burst as a simple defensive panic button when charged

## What changed in this pass
- Simplified the run into **one obvious objective**: clear all shards, then reach the exit
- Removed the busier side systems from the active loop:
  - no optional cores
  - no expiring caches
  - no surge pickups
  - no jackpot detours
  - no gate-jam micromanagement
  - no difficulty picker clutter in the UI
- Rebuilt the HUD and sidebar to focus on just the essentials:
  - score
  - best score
  - level
  - lives
  - shard progress
  - burst charge
- Kept controls forgiving and thumb-friendly with swipe / drag steering, D-pad buttons, and a dedicated Burst button
- Improved presentation with richer backgrounds, stronger glow, cleaner composition, smoother trails, nicer pickup/exit animation, better popups, and a more polished top banner
- Simplified scoring into a more arcade-friendly model:
  - shard pickups
  - short streak bonus
  - level-clear bonus
  - life bonus
  - local top-score board
- Kept the game instantly replayable after each loss

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe / drag or use the D-pad, tap Burst to stun nearby drones when charged

## Notes
- Fully self-contained; no external assets required
- Scores and leaderboard are stored in local browser storage
- Best results come from clearing efficiently, staying alive, and chaining shard pickups
