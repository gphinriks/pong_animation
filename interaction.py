async def game_loop():
    game = GameState()
    while True:
        print("\nWhat would you like to do?")
        print("1. Talk to Sasha")
        print("2. Investigate Police Station")
        print("3. Question Chamberlain")
        print("4. Exit")
        
        choice = input("> ")
        if choice == "1":
            prompt = input("What would you like to ask Sasha? ")
            response = await game.interact_with_npc("sasha", prompt)
            print(f"Sasha: {response}")
