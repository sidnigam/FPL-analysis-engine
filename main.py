import requests

def get_league_data(league_id):
    try:
        league_url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
        response = requests.get(league_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching league data: {e}")
        return None

def get_player_gameweek_data(player_id):
    try:
        player_url = f"https://fantasy.premierleague.com/api/entry/{player_id}/history/"
        response = requests.get(player_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching player data for {player_id}: {e}")
        return None

def process_data(league_data):
    gameweek_scores = {}
    player_rank_count = {}
    player_bench_points = {}

    for player in league_data['standings']['results']:
        player_id = player['entry']
        player_name = player['player_name']
        player_gameweek_data = get_player_gameweek_data(player_id)

        if player_gameweek_data and 'current' in player_gameweek_data:
            bench_points = sum(gw_data['points_on_bench'] for gw_data in player_gameweek_data['current'])
            player_bench_points[player_name] = bench_points

            for gw_data in player_gameweek_data['current']:
                gw = gw_data['event']
                points = gw_data['points'] - gw_data['event_transfers_cost']
                gameweek_scores.setdefault(gw, []).append((player_name, points))

    highest_scores = {}
    for gw, scores in gameweek_scores.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_scores[gw] = scores[:3] if len(scores) > 2 else scores

        # Counting the number of times a player is in the top 2
        for score in highest_scores[gw]:
            player_name = score[0]
            player_rank_count[player_name] = player_rank_count.get(player_name, 0) + 1

    return highest_scores, player_rank_count, player_bench_points

def print_formatted_table(data, title, headers):
    print(title)
    print(f"{headers[0]:<10} {headers[1]:<20} {headers[2]}")
    print("-" * 50)
    for key, values in data.items():
        for i, value in enumerate(values):
            if i == 0:
                print(f"{key:<10} {value[0]:<20} {value[1]}")
            else:
                print(f"{' ':<10} {value[0]:<20} {value[1]}")
        print("-" * 50)

def print_rank_count_table(rank_count):
    print("\nNumber of Times Each Player Ranked in Top 3:")
    print(f"{'Player':<20} {'Times Ranked Top 3':<25}")
    print("-" * 30)
    for player, count in rank_count.items():
        print(f"{player:<20} {count:<25}")
    print("-" * 30)

def print_bench_points_table(bench_points):
    print("\nTotal Bench Points for Each Player (Sorted):")
    print(f"{'Player':<20} {'Bench Points':}")
    print("-" * 35)
    for player, points in sorted(bench_points.items(), key=lambda x: x[1], reverse=True):
        print(f"{player:<20} {points}")
    print("-" * 35)

def main():
    league_id = "54617"  # Replace with your league ID 54617 podar; 54609 main
    league_data = get_league_data(league_id)

    if league_data:
        highest_scores, player_rank_count, player_bench_points = process_data(league_data)
        print_formatted_table(highest_scores, "Top 3 Scores Each Gameweek:", ["Gameweek", "Player", "Score"])

        print_rank_count_table(player_rank_count)
        print_bench_points_table(player_bench_points)

if __name__ == "__main__":
    main()
