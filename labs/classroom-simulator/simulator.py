import json
from pathlib import Path

DATA = Path(__file__).with_name("scenarios.json")

def run():
    scenarios = json.loads(DATA.read_text(encoding="utf-8"))
    total = 0
    for s in scenarios:
        print(f"\n{s['title']}\n{s['situation']}")
        for i, o in enumerate(s["options"], 1):
            print(f"{i}. {o['text']}")
        try:
            choice = int(input("Elige: ")) - 1
            selected = s["options"][choice]
        except Exception:
            print("Entrada inválida.")
            continue
        total += selected["score"]
        print("Reflexión:", s["reflection"])
    print("\nPuntaje orientativo:", total)
    print("El puntaje no sustituye la justificación profesional.")

if __name__ == "__main__":
    run()
