import requests
import json
from typing import Dict, List, Optional
import asyncio

# Base Character class
class Character:
    def __init__(self, name, role, status, alignment=None):
        self.name = name
        self.role = role
        self.status = status  # active, missing, deceased
        self.alignment = alignment  # good, evil, unknown
        self.karma = 0  # tracks moral choices
        self.relationships = {}
        self.clues_known = []

# Character definitions
CHARACTERS = {
    "tucker": Character(
        name="Tucker McGinnis",
        role="Private Investigator",
        status="active",
        alignment="player_determined"
    ),
    "susan": Character(
        name="Susan McGinnis",
        role="Nurse",
        status="missing",
        alignment="good"
    ),
    "chamberlain": Character(
        name="John Chamberlain",
        role="Police Director",
        status="active",
        alignment="evil"
    ),
    "monroe": Character(
        name="Peter Monroe",
        role="Former Police Detective",
        status="missing",
        alignment="unknown"
    ),
    "sasha": Character(
        name="Sasha Bojka",
        role="Secretary Assistant",
        status="active",
        alignment="good"
    )
}

# Character Relationships
RELATIONSHIPS = {
    "tucker": {
        "susan": "wife (missing)",
        "monroe": "former partner",
        "sasha": "trusted assistant",
        "chamberlain": "former superior"
    },
    "susan": {
        "tucker": "husband",
        "chamberlain": "discovered his cult involvement"
    },
    "chamberlain": {
        "tucker": "former subordinate",
        "cult": "secret leader"
    }
}

class OllamaCharacterAI:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "codellama:7b"
        self.context = {}

    async def generate_response(self, character_name: str, prompt: str) -> str:
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.model,
                "prompt": self._create_character_prompt(character_name, prompt),
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error generating response: {response.status_code}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def _create_character_prompt(self, character_name: str, prompt: str) -> str:
        character = CHARACTERS.get(character_name.lower())
        if not character:
            return prompt

        character_context = f"""
        You are {character.name}, {character.role} in Rapid Falls, 1963.
        Background: {self._get_character_background(character_name)}
        Current status: {character.status}
        Relationships: {RELATIONSHIPS.get(character_name.lower(), {})}
        
        Respond in character as {character.name}. Maintain the personality and knowledge
        that this character would have in 1963. Keep responses concise and in-character.
        
        User's prompt: {prompt}
        """
        return character_context

    def _get_character_background(self, character_name: str) -> str:
        backgrounds = {
            "susan": """A nurse working nightshifts who discovered a dangerous cult 
                    operating in Rapid Falls. Left to protect her husband Tucker and 
                    investigate the cult's activities.""",
            "chamberlain": """Police Director and secret cult member. Maintains a 
                          respectable public image while conducting dark rituals.""",
            "monroe": """Former police detective and Tucker's ex-partner. Staged his 
                     own kidnapping after a car crash.""",
            "sasha": """Tucker's loyal secretary and assistant. One of his few 
                    remaining allies in Rapid Falls."""
        }
        return backgrounds.get(character_name.lower(), "Background unknown")

class EnhancedCharacter(Character):
    def __init__(self, name, role, status, alignment=None):
        super().__init__(name, role, status, alignment)
        self.ai = OllamaCharacterAI()
        self.conversation_history = []

    async def respond_to(self, prompt: str) -> str:
        response = await self.ai.generate_response(self.name.lower(), prompt)
        self.conversation_history.append({
            "player": prompt,
            "character": response
        })
        return response

class GameState:
    def __init__(self):
        self.karma_points = 0
        self.discovered_clues = []
        self.current_location = None
        self.inventory = []
        self.quest_log = []
        self.ai_handler = OllamaCharacterAI()
        self.initialize_characters()

    def initialize_characters(self):
        self.characters = {
            name: EnhancedCharacter(
                name=char.name,
                role=char.role,
                status=char.status,
                alignment=char.alignment
            )
            for name, char in CHARACTERS.items()
        }

    async def interact_with_npc(self, character_name: str, player_input: str) -> str:
        character = self.characters.get(character_name.lower())
        if not character:
            return "Character not found."
        return await character.respond_to(player_input)

async def game_loop():
    game = GameState()
    while True:
        print("\nWhat would you like to do?")
        print("1. Talk to Sasha")
        print("2. Investigate Police Station")
        print("3. Question Chamberlain")
        print("4. Exit")
        
        choice = input("> ")
        
        if choice == "4":
            break
        elif choice == "1":
            prompt = input("What would you like to ask Sasha? ")
            response = await game.interact_with_npc("sasha", prompt)
            print(f"Sasha: {response}")
        elif choice == "3":
            prompt = input("What would you like to ask Chamberlain? ")
            response = await game.interact_with_npc("chamberlain", prompt)
            print(f"Chamberlain: {response}")

def test_ollama_connection():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("Successfully connected to Ollama")
            print("Available models:", response.json())
            return True
        else:
            print(f"Failed to connect to Ollama: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        return False

if __name__ == "__main__":
    if test_ollama_connection():
        asyncio.run(game_loop())
    else:
        print("Please ensure Ollama is running on localhost:11434")

