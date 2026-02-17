# SERP API Usage

## Making a Request

```python
import requests

response = requests.get("https://serpapi.com/search.json", params={
    "q": query,
    "hl": "en",
    "gl": "us",
    "api_key": config['SERP_API_KEY']
})
data = response.json()
```

## Response Structure

The response contains several top-level keys:

| Key | Description |
|-----|-------------|
| `search_metadata` | Request metadata (id, status, timing, raw_html_file) |
| `search_parameters` | Echo of request params (engine, query, domain, language) |
| `search_information` | Query info (total_results, time_taken) |
| `organic_results` | **Main search results list** |
| `sports_results` | Sports-specific widget data (standings, scores) - optional |
| `related_searches` | Related query suggestions |
| `pagination` | Google pagination links |
| `serpapi_pagination` | SerpAPI pagination links |

## Getting Top Search Results (organic_results)

The `organic_results` array contains the main search results. Each result has:

```python
# Get list of top search results
results = data.get('organic_results', [])

for result in results:
    position = result['position']      # Ranking position (1, 2, 3...)
    title = result['title']            # Page title
    link = result['link']              # Direct URL to the page
    snippet = result['snippet']        # Description/preview text
    source = result['source']          # Source website name
    displayed_link = result['displayed_link']  # Formatted URL shown in search
    favicon = result.get('favicon')    # Favicon URL (optional)
```

### Example: Extract Links and Metadata

```python
def get_search_results(query: str, api_key: str, num_results: int = 10) -> list[dict]:
    """
    Search Google via SERP API and return top results.

    Returns list of dicts with: position, title, link, snippet, source
    """
    response = requests.get("https://serpapi.com/search.json", params={
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    })
    data = response.json()

    results = []
    for item in data.get('organic_results', [])[:num_results]:
        results.append({
            'position': item.get('position'),
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
            'source': item.get('source')
        })

    return results
```

### Example: Get Just the URLs

```python
# Simple list of URLs from search results
urls = [r['link'] for r in data.get('organic_results', [])]
```

## Full organic_results Item Structure

```json
{
  "position": 1,
  "title": "NBA Standings - 2025-26 season",
  "link": "https://www.espn.com/nba/standings",
  "redirect_link": "https://www.google.com/url?sa=t&source=web&...",
  "displayed_link": "https://www.espn.com > nba > standings",
  "favicon": "https://serpapi.com/searches/.../images/...",
  "snippet": "Visit ESPN for the complete 2025-26 NBA season standings...",
  "snippet_highlighted_words": ["2025-26 NBA season standings"],
  "source": "ESPN"
}
```

## Other Useful Data

### Sports Results (when available)
For sports queries, `sports_results` may contain structured data:

```python
sports = data.get('sports_results', {})
if sports:
    title = sports.get('title')        # e.g., "NBA standings"
    season = sports.get('season')      # e.g., "2024-25"
    standings = sports.get('league', {}).get('standings', [])
    for team in standings:
        name = team['team']['name']    # e.g., "Cavaliers"
        pos = team['pos']              # e.g., "1"
```

### Related Searches
```python
related = data.get('related_searches', [])
for item in related:
    query = item['query']   # Suggested related search
    link = item['link']     # Google search URL for that query
```

### Pagination
```python
# Get next page of results
next_page = data.get('serpapi_pagination', {}).get('next')
```
