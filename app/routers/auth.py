from fastapi import APIRouter, Request
from dotenv import load_dotenv
import requests, os

router = APIRouter()

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

@router.post("/code")
async def auth_code(request: Request):
    # Accept JSON or form for convenience
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        code = body.get("code")
    else:
        form = await request.form()
        code = form.get("code") or form.get("credential")

    if not code:
        return {"error": "missing_code"}

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": "postmessage",        # REQUIRED for popup code flow
        "grant_type": "authorization_code",
    }

    token_res = requests.post(TOKEN_URL, data=data)
    token_data = token_res.json()
    if "access_token" not in token_data:
        return {"error": "token_exchange_failed", "details": token_data}

    access_token = token_data["access_token"]

    # Optional: confirm identity / get profile
    userinfo = requests.get(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # TODO: persist refresh_token = token_data.get("refresh_token")
    # TODO: set a session/JWT and return a success response your UI expects
    return {
        "user": userinfo,
        "scope": token_data.get("scope"),
        "expires_in": token_data.get("expires_in"),
        "has_refresh_token": bool(token_data.get("refresh_token")),
    }
