from gpt4all import GPT4All
import json
import os
from datetime import datetime

class EPSIChatbot:
    def __init__(self):
        print("🔄 Chargement du modèle GPT4All...")
        self.model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
        print("✅ Modèle chargé avec succès!")
        
        # Charger la base de connaissances
        self.knowledge_base = self.load_knowledge_base()
        self.faq = self.load_faq()
        self.conversation_history = []
        
    def load_knowledge_base(self):
        """Charge la base de connaissances depuis le fichier JSON"""
        try:
            with open('knowledge_base.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Fichier knowledge_base.json introuvable. Utilisation des données par défaut.")
            return self.get_default_knowledge_base()
    
    def load_faq(self):
        """Charge les FAQ depuis le fichier JSON"""
        try:
            with open('faq.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Fichier faq.json introuvable. Utilisation des FAQ par défaut.")
            return self.get_default_faq()
    
    def get_default_knowledge_base(self):
        """Base de connaissances par défaut"""
        return {
            "general": {
                "nom": "EPSI Lyon",
                "type": "École d'ingénierie informatique",
                "ville": "Lyon, quartier Part-Dieu",
                "description": "L'EPSI forme des experts en informatique et systèmes d'information"
            },
            "programmes": {
                "bachelor": [
                    "Bachelor Développement (Bac+3)",
                    "Bachelor Infrastructure & Réseaux (Bac+3)",
                    "Bachelor Cybersécurité (Bac+3)"
                ],
                "mastere": [
                    "Mastère Expert en Informatique et Systèmes d'Information (Bac+5)",
                    "Mastère Architecture Logicielle (Bac+5)",
                    "Mastère Cybersécurité (Bac+5)"
                ],
                "modalites": "Formation en initial ou en alternance dès la 3ème année"
            },
            "admission": {
                "post_bac": "Candidature via Parcoursup ou directement sur le site EPSI",
                "processus": "Étude du dossier + entretien de motivation",
                "admissions_paralleles": "Possibilité d'intégrer en 3ème ou 4ème année",
                "prerequis": "Bac général ou technologique, passion pour l'informatique"
            },
            "alternance": {
                "debut": "Possible dès la 3ème année (Bachelor 3 ou Mastère 1)",
                "rythme": "3 semaines en entreprise / 1 semaine à l'école",
                "avantages": [
                    "Frais de scolarité pris en charge par l'entreprise",
                    "Salaire mensuel",
                    "Expérience professionnelle concrète",
                    "Facilite l'insertion professionnelle"
                ]
            },
            "campus": {
                "localisation": "Lyon Part-Dieu, proche des transports",
                "equipements": [
                    "Salles informatiques équipées",
                    "Espace coworking",
                    "Laboratoires techniques",
                    "Salles de réunion pour projets"
                ]
            },
            "debouches": {
                "metiers": [
                    "Développeur Full-Stack",
                    "DevOps Engineer",
                    "Architecte logiciel",
                    "Expert Cybersécurité",
                    "Data Engineer",
                    "Chef de projet IT",
                    "Consultant IT"
                ],
                "secteurs": [
                    "ESN (Entreprises de Services Numériques)",
                    "Startups tech",
                    "Grands groupes",
                    "Banques et assurances",
                    "E-commerce"
                ]
            },
            "vie_etudiante": {
                "bde": "Bureau Des Étudiants actif organisant des événements réguliers",
                "evenements": [
                    "Hackathons et challenges de programmation",
                    "Conférences avec des professionnels",
                    "Soirées et événements festifs",
                    "Projets collaboratifs inter-promotions"
                ],
                "partenariats": "Réseau d'entreprises partenaires pour stages et alternances"
            }
        }
    
    def get_default_faq(self):
        """FAQ par défaut"""
        return {
            "tarif": "Pour connaître les tarifs précis de l'EPSI Lyon, je vous invite à contacter directement le service admissions ou à consulter le site officiel epsi.fr. Les tarifs varient selon le programme et le mode de formation (initial ou alternance).",
            "contact": "Vous pouvez contacter l'EPSI Lyon par téléphone ou via le formulaire de contact sur epsi.fr. Le campus est situé dans le quartier Part-Dieu à Lyon.",
            "portes ouvertes": "L'EPSI Lyon organise plusieurs journées portes ouvertes dans l'année. Consultez le site epsi.fr rubrique 'Événements' pour connaître les prochaines dates.",
            "stages": "Des stages sont prévus à chaque année du cursus. En Bachelor, plusieurs stages de 2 à 6 mois. En Mastère, des stages longue durée ou l'alternance.",
            "logement": "L'EPSI peut vous accompagner dans votre recherche de logement à Lyon. Des partenariats existent avec des résidences étudiantes proches du campus.",
            "international": "L'EPSI propose des opportunités de stages à l'international et des partenariats avec des universités étrangères pour des échanges académiques."
        }
    
    def find_relevant_context(self, question):
        """Trouve le contexte pertinent selon la question"""
        question_lower = question.lower()
        relevant_sections = []
        
        # Mapping des mots-clés vers les sections
        keywords_map = {
            "programmes": ["programme", "formation", "bachelor", "mastère", "mastere", "cursus", "diplôme", "etudes"],
            "admission": ["admission", "candidature", "inscription", "entrer", "parcoursup", "intégrer", "integrer"],
            "campus": ["campus", "locaux", "où", "ou", "situé", "adresse", "batiment", "equipement"],
            "debouches": ["débouché", "debouche", "métier", "metier", "emploi", "carrière", "carriere", "travail", "job"],
            "vie_etudiante": ["vie étudiante", "vie etudiante", "bde", "événement", "evenement", "association", "sortie"],
            "alternance": ["alternance", "rythme", "entreprise", "salaire", "contrat"]
        }
        
        # Chercher les sections pertinentes
        for section, keywords in keywords_map.items():
            if any(keyword in question_lower for keyword in keywords):
                if section in self.knowledge_base:
                    relevant_sections.append(f"### {section.upper()}\n{json.dumps(self.knowledge_base[section], ensure_ascii=False, indent=2)}")
        
        # Si aucune section spécifique, retourner l'info générale
        if not relevant_sections:
            relevant_sections.append(f"### INFORMATIONS GÉNÉRALES\n{json.dumps(self.knowledge_base.get('general', {}), ensure_ascii=False, indent=2)}")
        
        return "\n\n".join(relevant_sections)
    
    def check_faq(self, question):
        """Vérifie si la question correspond à une FAQ"""
        question_lower = question.lower()
        for key, answer in self.faq.items():
            if key in question_lower:
                return answer
        return None
    
    def generate_response(self, question):
        """Génère une réponse à la question"""
        # Vérifier d'abord les FAQ
        faq_response = self.check_faq(question)
        if faq_response:
            return faq_response
        
        # Construire le prompt avec contexte pertinent
        relevant_context = self.find_relevant_context(question)
        
        system_prompt = """Tu es une IA représentant l'EPSI Lyon, école d'ingénierie informatique.
Tu dois répondre de manière précise, amicale et professionnelle aux questions des futurs étudiants.
Utilise UNIQUEMENT les informations fournies ci-dessous pour répondre.
Si tu ne trouves pas l'information, dis-le honnêtement et invite à contacter l'école.

Règles importantes:
- Sois précis et concis
- Utilise un ton amical mais professionnel
- Ne pas inventer d'informations
- Reste positif sur l'école
"""
        
        full_prompt = f"""{system_prompt}

INFORMATIONS DISPONIBLES:
{relevant_context}

Question de l'étudiant: {question}

Réponse (sois naturel et direct):"""
        
        # Générer la réponse
        response = self.model.generate(
            full_prompt,
            max_tokens=250,
            temp=0.7,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.2
        )
        
        # Sauvegarder dans l'historique
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": response
        })
        
        return response.strip()
    
    def save_history(self):
        """Sauvegarde l'historique des conversations"""
        if self.conversation_history:
            with open('conversation_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Historique sauvegardé ({len(self.conversation_history)} conversations)")
    
    def run(self):
        """Lance le chatbot"""
        print("\n" + "="*60)
        print("🎓 Bienvenue sur le ChatBot de l'EPSI Lyon!")
        print("="*60)
        print("Je peux répondre à vos questions sur:")
        print("  • Les programmes de formation")
        print("  • Les admissions et candidatures")
        print("  • Le campus et les équipements")
        print("  • Les débouchés professionnels")
        print("  • La vie étudiante")
        print("  • L'alternance")
        print("\nTapez 'quit' ou 'exit' pour quitter")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("💬 Vous: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ["quit", "exit", "quitter", "sortir"]:
                    print("\n👋 Merci de votre visite! À bientôt à l'EPSI Lyon!")
                    self.save_history()
                    break
                
                print("\n🤖 EPSI IA: ", end="", flush=True)
                response = self.generate_response(question)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir!")
                self.save_history()
                break
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
                print("Veuillez réessayer.\n")

def main():
    try:
        chatbot = EPSIChatbot()
        chatbot.run()
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("Assurez-vous que le modèle 'orca-mini-3b-gguf2-q4_0.gguf' est téléchargé.")

if __name__ == "__main__":
    main()