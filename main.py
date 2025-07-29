from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

RAPIDAPI_KEYS = [
    "f5c44b05a2msh2b65270b6b13d1ap193756jsn3c76294b1ce9",
    "key_2_here",
    "key_3_here"
]

RAPIDAPI_HOST = "tiktok-scraper7.p.rapidapi.com"
RAPIDAPI_URL = f"https://{RAPIDAPI_HOST}/"

@app.get("/")
def read_root():
    return {"message": "TikTok HD API is running. Use /tiktok?url=..."}

@app.get("/tiktok")
def get_hd_video(url: str = Query(..., description="TikTok video URL")):
    errors = []

    for key in RAPIDAPI_KEYS:
        try:
            print(f"[INFO] Trying key: {key}")
            response = requests.get(
                RAPIDAPI_URL,
                headers={
                    "x-rapidapi-key": key,
                    "x-rapidapi-host": RAPIDAPI_HOST
                },
                params={"url": url, "hd": "1"},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            hd_url = data.get("data", {}).get("hdplay")
            if not hd_url:
                raise HTTPException(status_code=404, detail="HD video not available")

            return {"hdplay": hd_url}

        except requests.exceptions.RequestException as e:
            print(f"[FAIL] Key failed: {key} — {str(e)}")
            errors.append(f"{key}: {str(e)}")

    # All keys failed
    raise HTTPException(status_code=502, detail=f"All RapidAPI keys failed. Errors: {errors}")
