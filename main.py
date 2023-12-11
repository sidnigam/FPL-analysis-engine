import requests

def get_league_data(league_id):
    try:
        # Replace this URL with the correct endpoint for league data
        league_url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
        response = requests.get(league_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching league data: {e}")
        return None

def process_gameweek_data(league_data):
    # Assuming league_data contains necessary gameweek info
    # This function needs to be adjusted based on the actual data structure
    highest_scores = {}

    # Example processing (adjust according to actual data structure)
    for gameweek in league_data['gameweeks']:
        scores = [(team['entry_name'], team['points']) for team in gameweek['teams']]
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_scores[gameweek['id']] = scores[:2]

    return highest_scores

def main():
    league_id = "YOUR_LEAGUE_ID"  # Replace with your league ID
    league_data = get_league_data(league_id)
    if league_data:
        highest_scores = process_gameweek_data(league_data)
        for gw, scores in highest_scores.items():
            print(f"Gameweek {gw}: Highest Scores: {scores}")

if __name__ == "__main__":
    main()
