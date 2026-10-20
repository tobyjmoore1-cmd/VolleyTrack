
matches = [
    {
        "player": "Toby",
        "opponent": "North Georgia",
        "sets_played": 3,
        "kills": 12,
        "attack_errors": 4,
        "attack_attempts": 32,
        "assists": 25,
        "digs": 8,
        "aces": 2,
        "blocks": 1
    },
    {
        "player": "Toby",
        "opponent": "Georgia Tech",
        "sets_played": 2,
        "kills": 7,
        "attack_errors": 2,
        "attack_attempts": 18,
        "assists": 18,
        "digs": 6,
        "aces": 1,
        "blocks": 0
    }
]


def calculate_hitting_percentage(match):
    kills = match["kills"]
    attack_errors = match["attack_errors"]
    attack_attempts = match["attack_attempts"]

    if attack_attempts == 0:
        return None

    return (kills - attack_errors) / attack_attempts


def calculate_assists_per_set(match):
    assists = match["assists"]
    sets_played = match["sets_played"]

    if sets_played == 0:
        return None

    return assists / sets_played


def calculate_season_assists_per_set(matches):
    total_assists = sum(match["assists"] for match in matches)
    total_sets_played = sum(match["sets_played"] for match in matches)

    if total_sets_played == 0:
        return None

    return total_assists / total_sets_played


def calculate_season_hitting_percentage(matches):
    total_kills = sum(match["kills"] for match in matches)
    total_attack_errors = sum(match["attack_errors"] for match in matches)
    total_attack_attempts = sum(match["attack_attempts"] for match in matches)

    if total_attack_attempts == 0:
        return None

    return (total_kills - total_attack_errors) / total_attack_attempts


if __name__ == "__main__":

    # Individual match statistics
    for match in matches:
        hitting_percentage = calculate_hitting_percentage(match)
        assists_per_set = calculate_assists_per_set(match)

        print(f"\nOpponent: {match['opponent']}")

        if hitting_percentage is None:
            print("Hitting Percentage: N/A")
        else:
            print(f"Hitting Percentage: {hitting_percentage:.3f}")

        if assists_per_set is None:
            print("Assists Per Set: N/A")
        else:
            print(f"Assists Per Set: {assists_per_set:.2f}")

    # Season statistics
    season_assists_per_set = calculate_season_assists_per_set(matches)
    season_hitting_percentage = calculate_season_hitting_percentage(matches)

    if season_assists_per_set is None:
        print("\nSeason Assists Per Set: N/A")
    else:
        print(f"\nSeason Assists Per Set: {season_assists_per_set:.2f}")

    if season_hitting_percentage is None:
        print("Season Hitting Percentage: N/A")
    else:
        print(f"Season Hitting Percentage: {season_hitting_percentage:.3f}")
