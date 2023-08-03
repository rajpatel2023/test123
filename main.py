from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth


config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="RAJ")


@app.get("/")
async def Home(request: Request):
    user = request.session.get("user")
    if user is not None:
        return user
    return {"error": "Un-authorized"}


@app.get("/login", tags=["Authentication"])
async def login(request: Request):
    # absolute url for callback(Google authorized and send to this urls)
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]
    request.session["user"] = userinfo
    return RedirectResponse(url="/")


@app.get("/logout", tags=["Authentication"])
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


def test_function():
    assert ("200", "200")
