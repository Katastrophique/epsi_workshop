from gpt4all import GPT4All

def main():
    print("Chargement du modèle GPT4All léger...")

    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

    print("Modèle chargé !")
    print("Bienvenue dans l'IA représentant l'EPSI Lyon.")
    print("Tapez 'quit' pour sortir.\n")

    # Contexte initial
    context = "Tu es une IA représentant l'EPSI Lyon. Tu connais les programmes, campus, événements, et peux répondre aux questions des futurs étudiants."

    while True:
        prompt = input("Vous : ")
        if prompt.lower() in ["quit", "exit"]:
            print("Au revoir !")
            break

        # Ajouter le contexte au prompt
        full_prompt = context + "\nQuestion: " + prompt
        response = model.generate(full_prompt)
        print(f"EPSI IA : {response}\n")

if __name__ == "__main__":
    main()
