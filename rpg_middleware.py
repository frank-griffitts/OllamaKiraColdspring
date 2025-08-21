import requests
import re
import random

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"  # or "rpg-gm" if you created a custom Modelfile

def roll_dice(command: str) -> str:
    """
    Parse dice commands like 'roll 1d20' or 'roll 3d6'
    """
    match = re.match(r"roll (\d+)d(\d+)", command.lower())
    if not match:
        return "Invalid dice format. Try: roll 1d20 or roll 3d6."

    num_dice, dice_sides = int(match.group(1)), int(match.group(2))
    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls)
    return f"🎲 You rolled {rolls} (total = {total})"

def query_ollama(prompt: str) -> str:
    """
    Send a prompt to the Ollama API and return the model's response.
    """
    response = requests.post(
        OLLAMA_API_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False}
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json().get("response", "").strip()

def main():
    print("=== Kira Coldspring RPG Middleware ===")
    print("Type 'quit' to exit.")
    print("Use 'roll XdY' for dice rolls (e.g., roll 1d20).")

    while True:
        user_input = input("\nPlayer: ")

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower().startswith("roll"):
            print(roll_dice(user_input))
        else:
            story = query_ollama(user_input)
            print(f"GM: {story}")

if __name__ == "__main__":
    main()
