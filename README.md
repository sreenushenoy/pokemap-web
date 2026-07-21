# PokéMap Quest Route Builder

A quality-of-life web tool for Pokémon GO players. Select a city, pick today's quest rewards you're hunting, and download an optimized GPX walking route — no more zigzagging across town.

**Live at:** [pokemap.duckdns.org](https://pokemap.duckdns.org)

---

## What it does

- Pulls **live quest data** from community-run Pokémon GO maps for 5 cities
- Lets you filter by any reward available *today* (coins, stardust, items, Pokémon encounters, mega energy) — filters update automatically as events change
- Shows all matching PokéStops on an interactive dark map
- Groups quests by task condition so you can focus on one type at a time
- Generates **optimized GPX route files** (nearest-neighbor algorithm) so your walk is as efficient as possible
- Resets automatically at midnight and at 11 AM local city time (1 hour after events typically start)

## Cities supported

| City | Map source |
|------|-----------|
| 🇸🇬 Singapore | sgpokemap.com |
| 🇦🇺 Sydney | sydneypogomap.com |
| 🇬🇧 London | londonpogomap.com |
| 🇺🇸 New York City | nycpokemap.com |
| 🇨🇦 Vancouver | vanpokemap.com |

## Credits

Quest data is sourced from these community-maintained Pokémon GO maps:

- **[SGPokéMap](https://sgpokemap.com)** — Singapore
- **[Sydney Pokémon GO Map](https://sydneypogomap.com)** — Sydney
- **[London Pokémon GO Map](https://londonpogomap.com)** — London
- **[NYC PokéMap](https://nycpokemap.com)** — New York City
- **[Vancouver PokéMap](https://vanpokemap.com)** — Vancouver

Pokémon sprites provided by **[PokeAPI](https://pokeapi.co)** (open source, [PokeAPI/sprites](https://github.com/PokeAPI/sprites)).

Pokémon GO is a trademark of Niantic, Inc. and The Pokémon Company. This project is not affiliated with, endorsed by, or connected to Niantic or The Pokémon Company in any way.

## Disclaimer

This tool is a **personal quality-of-life project** built for the Pokémon GO community. It does not scrape, store, or redistribute any map data — it simply acts as a browser-side proxy so your device can fetch and display quest data from the community maps listed above. All quest data belongs to the respective map communities. Please support them and follow their terms of use.

No login, no accounts, no data collection.

---
