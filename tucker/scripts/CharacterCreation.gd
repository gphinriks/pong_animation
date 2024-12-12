# CharacterCreation.gd
extends Control

var http_request: HTTPRequest
var character_data = {
	"name": "",
	"background": "",
	"role": "",
	"traits": [],
	"appearance": {}
}

func _ready():
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.connect("request_completed", self, "_on_request_completed")
	setup_ui()

func setup_ui():
	# Name Input
	var name_edit = LineEdit.new()
	name_edit.connect("text_changed", self, "_on_name_changed")
	add_child(name_edit)
	
	# Role Selection
	var role_options = OptionButton.new()
	role_options.add_item("Private Investigator")
	role_options.add_item("Detective")
	role_options.add_item("Reporter")
	role_options.connect("item_selected", self, "_on_role_selected")
	add_child(role_options)
	
	# Appearance Customization
	var appearance_container = VBoxContainer.new()
	add_child(appearance_container)
	
	# Create Character Button
	var create_button = Button.new()
	create_button.text = "Create Character"
	create_button.connect("pressed", self, "_on_create_pressed")
	add_child(create_button)

func _on_name_changed(new_text: String):
	character_data.name = new_text

func _on_role_selected(index: int):
	var roles = ["Private Investigator", "Detective", "Reporter"]
	character_data.role = roles[index]

func _on_create_pressed():
	var json = JSON.print(character_data)
	var headers = ["Content-Type: application/json"]
	http_request.request(
		"http://localhost:8000/characters/",
		headers,
		true,
		HTTPClient.METHOD_POST,
		json
	)

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8())
		if json.result:
			print("Character created successfully!")
			get_tree().change_scene("res://Game.tscn")
	else:
		print("Error creating character")
