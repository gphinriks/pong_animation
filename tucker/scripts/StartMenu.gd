extends Control

# Declare tween as a class variable
var tween: Tween

func _ready():
	# Fix node paths
	var start_button = $Background/CenterContainer/Logo/MarginContainer/StartButton
	var load_button = $Background/CenterContainer/Logo/MarginContainer/StartButton/LoadButton
	var logo = $Background/CenterContainer/Logo
	
	# Connect signals
	start_button.connect("pressed", self, "_on_StartButton_pressed")
	start_button.connect("mouse_entered", self, "_on_button_hover")
	start_button.connect("mouse_exited", self, "_on_button_normal")
	load_button.connect("pressed", self, "_on_LoadButton_pressed")
	
	# ... rest of the code ...

	
	# Initialize tween
	tween = Tween.new()
	add_child(tween)
	
	# Set initial transparency
	logo.modulate = Color(1, 1, 1, 0)
	start_button.modulate = Color(1, 1, 1, 0)
	
	# Fade in logo
	tween.interpolate_property(
		logo,
		"modulate",
		Color(1, 1, 1, 0),
		Color(1, 1, 1, 1),
		1.0,
		Tween.TRANS_CUBIC,
		Tween.EASE_IN_OUT
	)
	
	# Fade in button
	tween.interpolate_property(
		start_button,
		"modulate",
		Color(1, 1, 1, 0),
		Color(1, 1, 1, 1),
		1.0,
		Tween.TRANS_CUBIC,
		Tween.EASE_IN_OUT,
		0.5  # Half second delay
	)
	
	tween.start()

func _on_button_hover():
	# Clear any existing tweens
	tween.remove_all()
	
	tween.interpolate_property(
		$CenterContainer/VBoxContainer/StartButton,
		"rect_scale",
		Vector2(1, 1),
		Vector2(1.1, 1.1),
		0.1,
		Tween.TRANS_CUBIC,
		Tween.EASE_OUT
	)
	tween.start()

func _on_button_normal():
	# Clear any existing tweens
	tween.remove_all()
	
	tween.interpolate_property(
		$CenterContainer/VBoxContainer/StartButton,
		"rect_scale",
		Vector2(1.1, 1.1),
		Vector2(1, 1),
		0.1,
		Tween.TRANS_CUBIC,
		Tween.EASE_OUT
	)
	tween.start()

func _on_StartButton_pressed():
	# Change to your game scene
	get_tree().change_scene("res://scenes/Game.tscn")
