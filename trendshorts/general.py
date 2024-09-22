import requests


def format_number(n):
    if n < 1000:
        return str(n)
    elif 1000 <= n < 1_000_000:
        return f"{n / 1000:.3f} Thousand".rstrip('0').rstrip('.')
    elif 1_000_000 <= n < 1_000_000_000:
        return f"{n / 1_000_000:.3f} Million".rstrip('0').rstrip('.')
    elif 1_000_000_000 <= n < 1_000_000_000_000:
        return f"{n / 1_000_000_000:.3f} Billion".rstrip('0').rstrip('.')
    else:
        return f"{n / 1_000_000_000_000:.3f} Trillion".rstrip('0').rstrip('.')


def get_bot_info(url):
    response = requests.get(url)
    data = response.json()
    # Extract unique user IDs
    user_ids = set()
    for result in data['result']:
        if 'message' in result:
            user_ids.add(result['message']['from']['id'])
    print(f"Number of unique users: {len(user_ids)}")
