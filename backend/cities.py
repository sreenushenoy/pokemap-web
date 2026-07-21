CITIES = {
    "sg":  {"name": "Singapore", "flag": "🇸🇬", "base_url": "https://sgpokemap.com"},
    "syd": {"name": "Sydney",    "flag": "🇦🇺", "base_url": "https://sydneypogomap.com"},
    "lon": {"name": "London",    "flag": "🇬🇧", "base_url": "https://londonpogomap.com"},
    "nyc": {"name": "NYC",       "flag": "🇺🇸", "base_url": "https://nycpokemap.com"},
    "van": {"name": "Vancouver", "flag": "🇨🇦", "base_url": "https://vanpokemap.com"},
}

# Common reward presets — label shown in UI, filter code sent to pokemap API
REWARD_PRESETS = {
    "coins":     {"label": "10 PokéCoins",   "filter": "8,10,0"},
    "luckyegg":  {"label": "1 Lucky Egg",    "filter": "2,1,301"},
    "stardust":  {"label": "Stardust",       "filter": None},  # multiple values, resolved dynamically
    "encounter": {"label": "Pokémon Encounter", "filter": None},
}
