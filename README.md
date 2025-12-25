# findnumber

This small script parses a phone number (from `myphone.py`) and attempts to geocode the country/city name using the OpenCage Geocoder API, then saves a simple `mylocation.html` map if coordinates are found.

Important: do NOT commit your API keys to source control. Use environment variables or a local `.env` file.

Quick start

1. Create and activate the project's virtual environment (if you haven't already):

```bash
# macOS / zsh example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # optional if you have such file
```

2. Install dependencies (we installed these earlier in the venv):

```bash
pip install phonenumbers opencage folium python-dotenv
```

3. Provide your OpenCage API key safely:

- Preferred: export the key in your shell session (temporary):

```bash
export OPENCAGE_API_KEY="<your_real_opencage_api_key>"
python main.py
```

- Alternative: create a local `.env` file (never commit this file):

```bash
cp .env.example .env
# Edit .env and replace YOUR_OPENCAGE_API_KEY_HERE with your real key
python main.py
```

If the key is not found the script will print a warning and skip geocoding.

How to rotate (revoke and regenerate) your OpenCage API key

1. Sign in to your OpenCage account at https://opencagedata.com/
2. Open the API key / dashboard page (usually named "API Keys" or "Account -> API keys").
3. Revoke or delete the old key (if it was accidentally leaked or committed).
4. Create/generate a new key and copy it.
5. Update your local environment:
   - If using shell export, update the `OPENCAGE_API_KEY` environment variable.
   - If using `.env`, update the `.env` file with the new key.
6. Test the script again.

Security note: if you previously committed a real API key to a repository, treat it as compromised: rotate (revoke) it immediately in the OpenCage dashboard so the old key cannot be abused.
