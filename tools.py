# # tools.py
# from agents import function_tool
# import requests
# from difflib import get_close_matches


# @function_tool
# def get_country_info(country_name: str) -> dict:
#     """Get capital, population, languages, flag and map location of a country using RESTCountries API"""
#     url = "https://restcountries.com/v3.1/all"
#     try:
#         res = requests.get(url)
#         data = res.json()

#         # 🔠 Spelling correction
#         country_names = [c["name"]["common"] for c in data]
#         closest = get_close_matches(country_name, country_names, n=1)
#         if not closest:
#             return {"error": "Country not found. Try again."}

#         matched = closest[0]
#         country_data = next(item for item in data if item["name"]["common"] == matched)

#         capital = country_data.get("capital", ["N/A"])[0]
#         population = f'{country_data.get("population", 0):,}'
#         languages = ", ".join(country_data.get("languages", {}).values())
#         flag_url = country_data.get("flags", {}).get("png", "")
#         latlng = country_data.get("latlng", [0, 0])
#         map_link = f"https://www.google.com/maps/search/?api=1&query={latlng[0]},{latlng[1]}"

#         return {
#             "country": matched,
#             "capital": capital,
#             "population": population,
#             "languages": languages,
#             "flag_url": flag_url,
#             "map_link": map_link
#         }

#     except Exception as e:
#         return {"error": str(e)}
from agents import function_tool
import requests
from difflib import get_close_matches

@function_tool
def get_country_info(country_name: str) -> dict:
    """Get capital, population, languages, flag and map location of a country using RESTCountries API"""
    url = "https://restcountries.com/v3.1/all"
    try:
        res = requests.get(url)
        data = res.json()

        # Spelling correction (case-insensitive)
        country_names = [c["name"]["common"] for c in data]
        country_lookup = {name.lower(): name for name in country_names}
        closest = get_close_matches(country_name.lower(), country_lookup.keys(), n=1)
        if not closest:
            return {"error": "Country not found. Try again."}

        matched = country_lookup[closest[0]]
        country_data = next(item for item in data if item["name"]["common"] == matched)

        capital = country_data.get("capital")
        capital = capital[0] if capital else "N/A"

        population = f'{country_data.get("population", 0):,}'

        languages_dict = country_data.get("languages", {})
        languages = ", ".join(languages_dict.values()) if languages_dict else "N/A"

        flag_url = country_data.get("flags", {}).get("png") or "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/World_map_blank_without_borders.svg/640px-World_map_blank_without_borders.svg.png"

        latlng = country_data.get("latlng", [0, 0])
        map_link = f"https://www.google.com/maps/search/?api=1&query={latlng[0]},{latlng[1]}"

        return {
            "country": matched,
            "capital": capital,
            "population": population,
            "languages": languages,
            "flag_url": flag_url,
            "map_link": map_link
        }

    except Exception as e:
        return {"error": f"❌ API Error: {str(e)}"}
