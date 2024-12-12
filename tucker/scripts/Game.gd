# Game.gd
extends Node

var current_character = null
var ai_handler = null

func _ready():
    setup_game()
    connect_to_ai_service()

func setup_game():
    # Load character data
    var character_id = Global.current_character_id
    load_character(character_id)

func connect_to_ai_service():
    # Initialize connection to Python AI service
    ai_handler = preload("res://scripts/AIHandler.gd").new()
    add_child(ai_handler)

func interact_with_npc(npc_name: String, dialogue: String):
    ai_handler.request_response(npc_name, dialogue)
