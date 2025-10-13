"""
IA représentant l'EPSI Lyon - version locale légère
Script prêt à exécuter
"""

# Installer les librairies nécessaires si pas déjà installées
# pip install gpt4all

from gpt4all import GPT4All

def main():
    print("Chargement du modèle GPT4All léger...")
    
    # Charger le modèle local (le plus petit)
    model = GPT4All("gpt4all-lora-quantized")  # modèle léger, adapté pour CPU
    
    print("Modèle chargé !")
    print("Bienvenue dans l'IA représentant l'EPSI Lyon.")
    print("Tapez 'quit' pour sortir.\n")
    
    while True:
        prompt = input("Vous : ")
        if prompt.lower() in ["quit", "exit"]:
            print("Au revoir !")
            break
        
        response = model.generate(prompt)
        print(f"EPSI IA : {response}\n")

if __name__ == "__main__":
    main()
