import param
import panel as pn
import secrets
import httpx
import webbrowser
from xeauth.settings import config
from .oauth import XeAuthSession, NotebookSession
from .certificates import certs
import time

def login(client_id=config.DEFAULT_CLIENT_ID, scopes=[], audience=config.DEFAULT_AUDIENCE,
            open_browser=False, print_url=False):
    if isinstance(scopes, str):
        scopes = scopes.split(" ")
    scopes = list(scopes)
    session = XeAuthSession(client_id=client_id, scopes=scopes, audience=audience)
    # return session
    session.login(open_browser=open_browser, print_url=print_url)
    return session

def notebook_login(client_id=config.DEFAULT_CLIENT_ID, scopes=[],
                    audience=config.DEFAULT_AUDIENCE, open_browser=True):
    pn.extension()
    if isinstance(scopes, str):
        scopes = scopes.split(" ")
    scopes = list(scopes)
    session = NotebookSession(client_id=client_id, scopes=scopes, audience=audience)
    session.login_requested(None)
    if open_browser:
        session.authorize()
    return session

def cli_login(client_id=config.DEFAULT_CLIENT_ID, scopes=[], 
                audience=config.DEFAULT_AUDIENCE):
    if isinstance(scopes, str):
        scopes = scopes.split(" ")
    scopes = list(scopes)
    session = login(client_id=client_id, scopes=scopes, audience=audience, print_url=True)
    print("logged in as:")
    print(session.profile)
    print(f"Access token: {session.access_token}")
    print(f"ID token: {session.id_token}")

def validate_claims(token, **claims):
    return certs.validate_claims(token, **claims)