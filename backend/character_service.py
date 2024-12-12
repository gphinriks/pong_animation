# character_service.py
import requests
import json
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CharacterCreate(BaseModel):
    name: str
    background: str
    role: str
    traits: List[str]
    appearance: Dict[str, str]

class Character(BaseModel):
    id: str
    name: str
    background: str
    role: str
    traits: List[str]
    appearance: Dict[str, str]
    stats: Dict[str, int]

# Store characters in memory (replace with database in production)
characters_db = {}

@app.post("/characters/", response_model=Character)
async def create_character(character: CharacterCreate):
    char_id = str(len(characters_db) + 1)
    new_character = Character(
        id=char_id,
        name=character.name,
        background=character.background,
        role=character.role,
        traits=character.traits,
        appearance=character.appearance,
        stats={"strength": 10, "intelligence": 10, "charisma": 10}
    )
    characters_db[char_id] = new_character
    return new_character
