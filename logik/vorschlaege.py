import requests

def duckduckgo_search(query):
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        search_results = response.json()
        return search_results.get('RelatedTopics', [])[0]["FirstURL"]
    else:
        print('Error:', response.status_code)
        return None
    