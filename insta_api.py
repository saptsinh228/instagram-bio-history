#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
import instaloader
# The exception ProfileNotExistsException does exist in instaloader.exceptions
from instaloader.exceptions import ProfileNotExistsException

app = FastAPI()
loader = instaloader.Instaloader()

@app.get("/")
def root():
    return {"message": "Instagram API running"}

@app.get("/profile/{username}")
def get_profile(username: str):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        if not profile.biography:
            raise HTTPException(status_code=404, detail="Bio not found")
        return {
            "bio": profile.biography,
        }
    except ProfileNotExistsException:
        raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
