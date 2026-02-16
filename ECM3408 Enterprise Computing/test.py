import requests
import textwrap

GUARDRAILS_URL = "http://localhost:3001/guardrails"
AUBERGE_URL = "http://localhost:3002/auberge"


def print_help():
    print("\nUSAGE")
    print("  <prompt>                Send a prompt to the LLM (default action)")
    print("  ?add <id> <regx> <sub>  Add or update a guardrail rule")
    print("  ?list                   List all active guardrail rules and patterns")
    print("  ?del <id>               Delete a specific guardrail rule")
    print("  ?help                   Show this help menu")
    print("  ?exit                   Exit the CLI")


def format_block(label, text):
    """Formats multi-line text with a header and indentation."""
    prefix = f"[{label}] "
    wrapper = textwrap.TextWrapper(width=80, initial_indent=prefix, subsequent_indent=" " * len(prefix))
    return wrapper.fill(str(text))


def handle_list():
    rsp = requests.get(GUARDRAILS_URL)
    if not rsp.ok:
        print("!! Error: Could not reach guardrail service.")
        return

    ids = rsp.json()
    if not ids:
        print("\n[System] No guardrails defined.")
        return

    print(f"\n{'ID':<5} | {'Regex Pattern':<25} | {'Substitution':<25}")
    print("-" * 60)
    for gid in ids:
        detail = requests.get(f"{GUARDRAILS_URL}/{gid}").json()
        print(f"{str(detail.get('id')):<5} | {str(detail.get('regx')):<25} | {str(detail.get('sub')):<25}")


def handle_prompt(prompt):
    try:
        rsp = requests.post(AUBERGE_URL, json={"prompt": prompt})
        if not rsp.ok:
            print(f"!! Error: {rsp.status_code}")
            return

        data = rsp.json()

        print("\n" + "—" * 40)
        print(format_block("RAW PROMPT", data.get("unsanitised_prompt")))
        print(format_block("CLEAN PROMPT", data.get("prompt")))
        print("-" * 20)
        # Note: 'usanitised_output' used to match your Flask key typo
        print(format_block("RAW OUTPUT", data.get("usanitised_output")))
        print(format_block("CLEAN OUTPUT", data.get("output")))
        print("—" * 40)
    except Exception as e:
        print(f"!! Connection Error: {e}")


def main():
    print("Auberge LLM Proxy CLI")
    print("Type your prompt directly, or ?help for commands.")

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue

            # Command Mode
            if user_input.startswith("?"):
                parts = user_input[1:].split("-", maxsplit=3)
                cmd = parts[0].lower()

                if cmd == "help":
                    print_help()
                elif cmd == "list":
                    handle_list()
                elif cmd == "add" and len(parts) == 4:
                    payload = {"id": int(parts[1]), "regx": parts[2], "sub": parts[3]}
                    requests.put(f"{GUARDRAILS_URL}/{parts[1]}", json=payload)
                    print(f"Added rule {parts[1]}")
                elif cmd == "del" and len(parts) == 2:
                    requests.delete(f"{GUARDRAILS_URL}/{parts[1]}")
                    print(f"Deleted rule {parts[1]}")
                elif cmd == "exit":
                    break
                else:
                    print("Unknown command or incorrect arguments. Type ?help")

            # Prompt Mode
            else:
                handle_prompt(user_input)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
