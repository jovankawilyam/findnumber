import os
from dotenv import load_dotenv
load_dotenv()

import phonenumbers
import folium
from myphone import number

from phonenumbers import geocoder as ph_geo, carrier

# Parse phone number with error handling
try:
    pepnumber = phonenumbers.parse(number, "ID")
except phonenumbers.NumberParseException as e:
    print("Invalid phone number:", e)
    raise

location = ph_geo.description_for_number(pepnumber, "en")
print(location)

service_provider = phonenumbers.parse(number, "ID")
print(carrier.name_for_number(service_provider, "en"))

from opencage.geocoder import OpenCageGeocode

# Read OpenCage API key from environment variable OPENCAGE_API_KEY
# Do NOT hardcode your API key in source code. Export it in your shell or use a .env file (not committed).
key = os.getenv("OPENCAGE_API_KEY")
if not key:
    print("Warning: OpenCage API key not set. Set OPENCAGE_API_KEY environment variable to geocode the location.")
else:
    try:
        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)
        print(results)
    except Exception as e:
        print("OpenCage geocoding error:", e)
        results = None

    if results:
        best = results[0]
        lat = best['geometry']['lat']
        lng = best['geometry']['lng']

        # Pick a more specific label when available
        components = best.get('components', {})
        preferred = (
            components.get('city')
            or components.get('town')
            or components.get('village')
            or components.get('county')
            or components.get('state')
            or components.get('region')
            or best.get('formatted')
        )

        confidence = best.get('confidence', None)
        print(f"Using location: {preferred}")
        print("OpenCage confidence:", confidence)
        print(lat, lng)

        # Warn if confidence is low (1-4 is typically low for general queries)
        low_confidence = (confidence is not None and confidence <= 3)
        if low_confidence:
            print("Warning: geocoding confidence is low — location may be very approximate.")

        # Put detailed info into the marker popup
        popup_text = f"{preferred} (confidence: {confidence})\nInferred from phone number — may be imprecise"

        # If OpenCage provides bounds, use them to fit the map view. This avoids
        # centering on a country's geographic centroid (which may be in water).
        bounds = best.get('bounds')
        if bounds and 'southwest' in bounds and 'northeast' in bounds:
            sw = bounds['southwest']
            ne = bounds['northeast']
            myMap = folium.Map(location=[(sw['lat'] + ne['lat']) / 2, (sw['lng'] + ne['lng']) / 2])
            myMap.fit_bounds([[sw['lat'], sw['lng']], [ne['lat'], ne['lng']]])
        else:
            myMap = folium.Map(location=[lat, lng], zoom_start=6 if low_confidence else 9)

        folium.Marker([lat, lng], popup=popup_text).add_to(myMap)

        myMap.save("mylocation.html")
        print("Saved mylocation.html")
    else:
        print("No geocoding results for query:", query)
