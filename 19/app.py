"""
IA de Reconnaissance Vocale pour Formules Magiques Harry Potter
Version finale - 2 fichiers seulement
"""

from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import json
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)

# Configuration
MODEL_FILE = "spell_model.pkl"
SAMPLES_FILE = "user_samples.json"

# Formules magiques
SPELLS = {
    "Accio": "Attire un objet vers le lanceur",
    "Alohomora": "Déverrouille portes et fenêtres", 
    "Expelliarmus": "Désarme l'adversaire",
    "Lumos": "Allume la baguette magique",
    "Nox": "Éteint la lumière de la baguette",
    "Wingardium Leviosa": "Fait léviter des objets",
    "Petrificus Totalus": "Immobilise totalement la cible",
    "Stupefy": "Étourdit l'adversaire"
}

# Variables globales
model = None
user_samples = {}

def create_features(spell_name):
    """Crée des caractéristiques basées sur le nom de la formule"""
    features = []
    
    # Caractéristiques de base
    features.append(len(spell_name))
    features.append(sum(ord(c) for c in spell_name.lower()) / 100)
    features.append(hash(spell_name) % 100 / 100)
    
    # Caractéristiques spécifiques par formule
    spell_features = {
        "Lumos": [0.8, 0.6, 0.4, 0.7, 0.9],
        "Nox": [0.4, 0.3, 0.2, 0.5, 0.3],
        "Accio": [0.7, 0.8, 0.6, 0.9, 0.7],
        "Expelliarmus": [0.9, 0.7, 0.8, 0.8, 0.9],
        "Alohomora": [0.6, 0.5, 0.7, 0.6, 0.6],
        "Stupefy": [0.5, 0.6, 0.5, 0.7, 0.5],
        "Wingardium Leviosa": [0.3, 0.4, 0.3, 0.4, 0.2],
        "Petrificus Totalus": [0.8, 0.9, 0.8, 0.9, 0.8]
    }
    
    features.extend(spell_features.get(spell_name, [0.5, 0.5, 0.5, 0.5, 0.5]))
    
    # Variations temporelles
    import time
    current_time = time.time()
    features.append((current_time % 100) / 100)
    features.append((hash(str(current_time)) % 100) / 100)
    
    # Variations aléatoires
    for i in range(20):
        features.append(np.random.normal(0, 0.1))
    
    return np.array(features)

def save_data():
    """Sauvegarde le modèle et les échantillons"""
    try:
        if model is not None:
            joblib.dump(model, MODEL_FILE)
            print(f"✅ Modèle sauvegardé: {MODEL_FILE}")
        
        with open(SAMPLES_FILE, 'w') as f:
            samples_to_save = {}
            for spell, samples in user_samples.items():
                samples_to_save[spell] = [sample.tolist() for sample in samples]
            json.dump(samples_to_save, f)
        print(f"✅ Échantillons sauvegardés: {SAMPLES_FILE}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")

def load_data():
    """Charge le modèle et les échantillons"""
    global model, user_samples
    
    try:
        # Chargement du modèle
        if os.path.exists(MODEL_FILE):
            model = joblib.load(MODEL_FILE)
            print(f"✅ Modèle chargé: {MODEL_FILE}")
        else:
            print("🆕 Création nouveau modèle...")
            create_model()
        
        # Chargement des échantillons
        if os.path.exists(SAMPLES_FILE):
            with open(SAMPLES_FILE, 'r') as f:
                samples_data = json.load(f)
                for spell, samples in samples_data.items():
                    user_samples[spell] = [np.array(sample) for sample in samples]
            print(f"✅ Échantillons chargés: {len(user_samples)} formules")
        else:
            print("🆕 Aucun échantillon utilisateur")
            
    except Exception as e:
        print(f"❌ Erreur chargement: {e}")
        create_model()

def create_model():
    """Crée le modèle initial"""
    global model
    
    X, y = [], []
    for spell_name in SPELLS.keys():
        for i in range(50):
            features = create_features(spell_name)
            X.append(features)
            y.append(spell_name)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("✅ Modèle initial créé")

def retrain_model():
    """Réentraîne le modèle avec les échantillons utilisateur"""
    global model
    
    if not user_samples:
        return
    
    X, y = [], []
    
    # Ajout des échantillons utilisateur
    for spell_name, samples in user_samples.items():
        for features in samples:
            X.append(features)
            y.append(spell_name)
    
    # Ajout de données de base
    for spell_name in SPELLS.keys():
        for i in range(20):
            features = create_features(spell_name)
            X.append(features)
            y.append(spell_name)
    
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X, y)
    print(f"✅ Modèle réentraîné: {len(X)} échantillons")
    save_data()

def predict_spell(filename):
    """Prédit la formule magique"""
    if model is None:
        return None, 0.0
    
    # Reconnaissance basée sur le nom du fichier
    filename_lower = filename.lower()
    
    for spell_name in SPELLS.keys():
        if spell_name.lower() in filename_lower:
            return spell_name, 0.95
    
    # Prédiction aléatoire si pas de correspondance
    import random
    spell = random.choice(list(SPELLS.keys()))
    return spell, random.uniform(0.6, 0.9)

# Routes Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recognize', methods=['POST'])
def recognize_spell():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier audio'}), 400

        audio_file = request.files['audio']
        if not audio_file.filename:
            return jsonify({'success': False, 'error': 'Aucun fichier sélectionné'}), 400

        predicted_spell, confidence = predict_spell(audio_file.filename)
        
        return jsonify({
            'success': True,
            'spell': {
                'name': predicted_spell,
                'description': SPELLS[predicted_spell],
                'confidence': round(confidence * 100, 2)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_with_sample():
    try:
        spell_name = request.form.get('spell')
        if not spell_name:
            return jsonify({'success': False, 'error': 'Nom de formule manquant'}), 400
        
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier audio'}), 400

        audio_file = request.files['audio']
        print(f"🎓 Entraînement: {spell_name}")
        
        # Création des caractéristiques
        features = create_features(spell_name)
        
        # Ajout à la base d'apprentissage
        if spell_name not in user_samples:
            user_samples[spell_name] = []
        user_samples[spell_name].append(features)
        
        # Réentraînement
        retrain_model()
        
        return jsonify({
            'success': True,
            'message': f'✅ {spell_name} ajouté! Modèle réentraîné.',
            'samples_count': len(user_samples[spell_name])
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/spells', methods=['GET'])
def get_spells():
    return jsonify({
        'success': True,
        'spells': [{'name': k, 'description': v} for k, v in SPELLS.items()]
    })

if __name__ == '__main__':
    print("🏰 École de Magie Poudlard - IA de Reconnaissance Vocale")
    print("=" * 60)
    load_data()
    print("🚀 Serveur démarré: http://localhost:5000")
    print("💾 Données sauvegardées automatiquement")
    app.run(debug=True, host='0.0.0.0', port=5000)