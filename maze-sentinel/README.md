# Maze Sentinel

Neon browser arcade prototype focused on maze-chase + route-control gameplay.

## Direction
- Not Pac-Man themed
- Strong neon / premium arcade visuals
- Mobile-friendly touch controls
- Built as the real target for the hourly OpenAI polishing cron

## Files
- `index.html` — playable prototype

## Current systems
- Three drone classes: Scout, Hunter, and Glimmer
- Path-based pursuit so enemies can pressure routes more intelligently
- Hunter drones telegraph a lock-on reticle, then burst into short high-speed surges
- Decoy beacon ability: place a temporary lure on your tile to bend pursuit lines and open safer escape lanes
- Arc-lash combo: trigger a pulse while a decoy is active to fire a crackling trap lane that stuns drones caught along the link
- Compact in-run drone intel row for readability
- District theme rotation: every level-up shifts the arena palette, ambience, and HUD identity for stronger progression feel

## Next polish ideas
- stronger level goals / progression beyond score survival
- richer soundtrack / SFX system
- title screen, progression, unlocks
- smarter drone synergies and telegraphed threat moments
