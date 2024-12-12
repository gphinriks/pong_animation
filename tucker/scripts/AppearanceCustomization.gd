# AppearanceCustomization.gd
extends Control

signal appearance_updated(data)

var appearance_data = {
    "hair_style": "",
    "hair_color": "",
    "face_shape": "",
    "eye_color": ""
}

func _ready():
    setup_appearance_options()

func setup_appearance_options():
    # Hair Style
    var hair_options = OptionButton.new()
    for style in ["Short", "Long", "Curly", "Straight"]:
        hair_options.add_item(style)
    hair_options.connect("item_selected", self, "_on_hair_style_selected")
    add_child(hair_options)
    
    # Hair Color
    var color_picker = ColorPickerButton.new()
    color_picker.connect("color_changed", self, "_on_hair_color_changed")
    add_child(color_picker)

func _on_hair_style_selected(index: int):
    var styles = ["Short", "Long", "Curly", "Straight"]
    appearance_data.hair_style = styles[index]
    emit_signal("appearance_updated", appearance_data)
