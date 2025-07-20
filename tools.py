import requests
from typing import Optional, Dict
from agents import function_tool

@function_tool
def get_country_info(country_name: str) -> Dict[str, Optional[str]]:
    """
    Returns detailed information about a given country using the REST Countries API.
    """
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        if response.status_code != 200:
            return {"error": "Country not found or API error."}
        
        data = response.json()[0]

        country = data.get("name", {}).get("common", "Unknown")
        capital = data.get("capital", ["Unknown"])[0]
        population = f"{data.get('population', 'Unknown'):,}"
        languages = ", ".join(data.get("languages", {}).values()) or "Unknown"
        flag_url = data.get("flags", {}).get("png")
        map_link = data.get("maps", {}).get("googleMaps", "")

        return {
            "country": country,
            "capital": capital,
            "population": population,
            "languages": languages,
            "flag_url": flag_url,
            "map_link": map_link
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
