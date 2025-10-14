// App.js - React Native Quiz: "Quel type de sorcier es-tu ?"
// Single-file React Native app (JavaScript)
// Conçu pour être simple, clair et commenté.
// Pas de backend — toutes les données sont locales.

import React, { useState, useRef, useEffect } from 'react';
import {
  SafeAreaView,
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  StatusBar,
  ScrollView,
} from 'react-native';

// ---------- CONFIGURATION ----------
// Définir ici les 4 types de sorciers
const WIZARD_TYPES = {
  ELEMENTALIST: 'Elementalist',
  NECROMANCER: 'Necromancer',
  ILLUSIONIST: 'Illusionist',
  HEALER: 'Healer',
};

// 20 questions. Chaque question a 4 réponses.
// Chaque réponse indique `type` (profil associé) et `points` (entier)
// On peut ajuster les points pour pondérer certaines réponses.
const QUESTIONS = [
  {
    q: "Quelle activité préfères-tu pendant ton temps libre ?",
    a: [
      { text: 'Aller en randonnée et sentir la nature', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Lire des textes anciens sur la vie et la mort', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Créer des illusions et blagues pour amuser', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Soigner un animal ou un ami blessé', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Ton objet favori serait :',
    a: [
      { text: 'Une amulette en pierre élémentaire', type: WIZARD_TYPES.ELEMENTALIST, points: 3 },
      { text: 'Un grimoire vieux et poussiéreux', type: WIZARD_TYPES.NECROMANCER, points: 3 },
      { text: 'Un masque changeant d’apparence', type: WIZARD_TYPES.ILLUSIONIST, points: 3 },
      { text: 'Une trousse de plantes médicinales', type: WIZARD_TYPES.HEALER, points: 3 },
    ],
  },
  {
    q: 'En cas de conflit tu :',
    a: [
      { text: 'Utilises la force de la nature', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Cherches un moyen de lier ou neutraliser', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Détournes l’attention avec des illusions', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Essayes de résoudre pacifiquement et soigner les rancœurs', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Quelle est ta saison préférée ?',
    a: [
      { text: 'L’été — feu et dynamisme', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'L’automne — fin et souvenir', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Printemps — renouveau et surprises', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Printemps aussi — guérison et croissance', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'Ton lieu préféré pour étudier la magie :',
    a: [
      { text: 'Au sommet d’une montagne', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Dans un cimetière ancien (à distance respectueuse)', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Dans un théâtre ou une salle d’art', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Dans un jardin d’herbes médicinales', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Laquelle de ces phrases te décrit le mieux ?',
    a: [
      { text: 'Je me sens connecté aux éléments', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Je suis fasciné par le cycle vie-mort', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'J’aime jouer avec la perception', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Je veux aider et apaiser les autres', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Ton animal totem serait :',
    a: [
      { text: 'Aigle (éléments & hauteur)', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'Corbeau (mystère)', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Chat (furtif & joueur)', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Cerf (apaisant & curatif)', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'Si tu pouvais lancer un sort en un mot, tu choisirais :',
    a: [
      { text: 'Tempest', type: WIZARD_TYPES.ELEMENTALIST, points: 3 },
      { text: 'Shade', type: WIZARD_TYPES.NECROMANCER, points: 3 },
      { text: 'Mirage', type: WIZARD_TYPES.ILLUSIONIST, points: 3 },
      { text: 'Balm', type: WIZARD_TYPES.HEALER, points: 3 },
    ],
  },
  {
    q: 'Le pouvoir le plus tentant selon toi :',
    a: [
      { text: 'Contrôler les tempêtes', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Parler aux âmes', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Faire croire ce que tu veux aux autres', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Guérir une maladie incurable', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Ton style vestimentaire :',
    a: [
      { text: 'Robes et ornements inspirés par la terre et le ciel', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'Vêtements sombres et mystérieux', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Tenues colorées et changeantes', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Tissus simples, pratiques, fleuris', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'Quelle couleur te parle le plus ?',
    a: [
      { text: 'Bleu & Vert (éléments)', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'Noir & Gris', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Pourpre & Or', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Blanc & Vert pâle', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'En groupe, tu es généralement :',
    a: [
      { text: 'L’instigateur d’activités', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Celui qui observe et apprend', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Le comique / farceur', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Le soutien, celui qui aide', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Ton rêve le plus cher :',
    a: [
      { text: 'Maîtriser la nature', type: WIZARD_TYPES.ELEMENTALIST, points: 3 },
      { text: 'Comprendre les mystères de la mort', type: WIZARD_TYPES.NECROMANCER, points: 3 },
      { text: 'Créer l’illusion parfaite', type: WIZARD_TYPES.ILLUSIONIST, points: 3 },
      { text: 'Guérir le monde', type: WIZARD_TYPES.HEALER, points: 3 },
    ],
  },
  {
    q: 'Quel est ton rapport au pouvoir ?',
    a: [
      { text: 'Protection et équilibre', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Connaissance, même risquée', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'S’amuser et expérimenter', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Responsabilité envers les autres', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Dans un duel magique tu préfères :',
    a: [
      { text: 'Lancer des attaques élémentaires puissantes', type: WIZARD_TYPES.ELEMENTALIST, points: 3 },
      { text: 'Désarmer moralement l’adversaire', type: WIZARD_TYPES.NECROMANCER, points: 3 },
      { text: 'Tromper les sens pour gagner', type: WIZARD_TYPES.ILLUSIONIST, points: 3 },
      { text: 'Soigner ses alliés pour contrer l’ennemi', type: WIZARD_TYPES.HEALER, points: 3 },
    ],
  },
  {
    q: 'Ton livre préféré parle de :',
    a: [
      { text: 'Les forces naturelles et leurs lois', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'Rituels et anciennes invocations', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Arts scénographiques et illusions', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Herboristerie et savoir médical', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'Quel est ton rapport au risque ?',
    a: [
      { text: 'Je prends des risques calculés', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Je m’aventure dans l’inconnu', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'Je teste des ruses et surprises', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'Je préfère protéger avant tout', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Tu rencontres une créature blessée, tu :',
    a: [
      { text: 'Étudies son lien avec l’environnement', type: WIZARD_TYPES.ELEMENTALIST, points: 2 },
      { text: 'Cherches si elle porte des signes de malédiction', type: WIZARD_TYPES.NECROMANCER, points: 2 },
      { text: 'L’emportes pour créer un spectacle', type: WIZARD_TYPES.ILLUSIONIST, points: 2 },
      { text: 'La soignes et la remets en liberté', type: WIZARD_TYPES.HEALER, points: 2 },
    ],
  },
  {
    q: 'Si un inconnu te demande un secret, tu :',
    a: [
      { text: 'Lui réponds s’il respecte l’équilibre', type: WIZARD_TYPES.ELEMENTALIST, points: 1 },
      { text: 'Évalues ses intentions', type: WIZARD_TYPES.NECROMANCER, points: 1 },
      { text: 'Mène une petite farce avant', type: WIZARD_TYPES.ILLUSIONIST, points: 1 },
      { text: 'Racontes quelque chose pour le rassurer', type: WIZARD_TYPES.HEALER, points: 1 },
    ],
  },
  {
    q: 'Ton apothéose idéale serait :',
    a: [
      { text: 'Un orage contrôlé qui purifie', type: WIZARD_TYPES.ELEMENTALIST, points: 3 },
      { text: 'Une cérémonie liant passé et présent', type: WIZARD_TYPES.NECROMANCER, points: 3 },
      { text: 'Un spectacle où tout semble réel', type: WIZARD_TYPES.ILLUSIONIST, points: 3 },
      { text: 'Une grande guérison collective', type: WIZARD_TYPES.HEALER, points: 3 },
    ],
  },
];

// ---------- UTILITAIRES ----------
function initializeTotals() {
  return Object.keys(WIZARD_TYPES).reduce((acc, k) => {
    acc[WIZARD_TYPES[k]] = { points: 0, count: 0 };
    return acc;
  }, {});
}

// ---------- APP COMPONENTS ----------
export default function App() {
  const [screen, setScreen] = useState('HOME'); // HOME | QUIZ | RESULT
  const [currentIndex, setCurrentIndex] = useState(0);
  const [totals, setTotals] = useState(initializeTotals());
  const [lastGained, setLastGained] = useState({ type: null, points: 0 });
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // animate progress bar when index changes
    const progress = (currentIndex) / QUESTIONS.length;
    Animated.timing(progressAnim, {
      toValue: progress,
      duration: 350,
      useNativeDriver: false,
    }).start();
  }, [currentIndex]);

  function handleStart() {
    setTotals(initializeTotals());
    setCurrentIndex(0);
    setLastGained({ type: null, points: 0 });
    setScreen('QUIZ');
  }

  function handleAnswer(answer) {
    // Update totals with points and counts
    setTotals(prev => {
      const next = { ...prev };
      next[answer.type] = {
        points: next[answer.type].points + answer.points,
        count: next[answer.type].count + 1,
      };
      return next;
    });

    // Small feedback: store last gained to display
    setLastGained({ type: answer.type, points: answer.points });

    // Move to next question or result
    if (currentIndex + 1 < QUESTIONS.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setScreen('RESULT');
    }
  }

  function computeResult() {
    // Determine the winner. Primary: points total. Secondary tie-breaker: count. If still tie, choose first alphabetically.
    const entries = Object.entries(totals).map(([type, v]) => ({ type, points: v.points, count: v.count }));

    entries.sort((a, b) => {
      if (b.points !== a.points) return b.points - a.points;
      if (b.count !== a.count) return b.count - a.count;
      return a.type.localeCompare(b.type);
    });

    const winner = entries[0];
    return { winner, breakdown: entries };
  }

  if (screen === 'HOME') {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" />
        <View style={styles.homeBox}>
          <Text style={styles.title}>Quel type de sorcier es-tu ?</Text>
          <Text style={styles.subtitle}>Réponds à 20 questions pour découvrir ton profil magique.</Text>

          <TouchableOpacity style={styles.startButton} onPress={handleStart}>
            <Text style={styles.startButtonText}>Commencer le test</Text>
          </TouchableOpacity>

          <View style={styles.infoBox}>
            <Text style={styles.infoTitle}>Gamification</Text>
            <Text style={styles.infoText}>Points par réponse, barre de progression, feedback immédiat et écran de résultat détaillé.</Text>
          </View>
        </View>
      </SafeAreaView>
    );
  }

  if (screen === 'QUIZ') {
    const q = QUESTIONS[currentIndex];
    const progressInterpolated = progressAnim.interpolate({ inputRange: [0, 1], outputRange: ['0%', '100%'] });

    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="dark-content" />
        <View style={styles.quizHeader}>
          <Text style={styles.questionCounter}>Question {currentIndex + 1} / {QUESTIONS.length}</Text>
          <View style={styles.progressBackground}>
            <Animated.View style={[styles.progressFill, { width: progressInterpolated }]} />
          </View>
        </View>

        <View style={styles.questionBox}>
          <Text style={styles.questionText}>{q.q}</Text>
        </View>

        <View style={styles.answersBox}>
          {q.a.map((ans, i) => (
            <TouchableOpacity
              key={i}
              style={styles.answerButton}
              onPress={() => handleAnswer(ans)}
            >
              <Text style={styles.answerText}>{ans.text}</Text>
              <Text style={styles.answerPoints}>+{ans.points} pts</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.feedbackBox}>
          {lastGained.type && (
            <Text style={styles.feedbackText}>Dernier gain: {lastGained.points} pts pour {lastGained.type}</Text>
          )}
        </View>

      </SafeAreaView>
    );
  }

  // RESULT SCREEN
  const result = computeResult();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentContainerStyle={styles.resultContainer}>
        <Text style={styles.resultTitle}>Résultat</Text>
        <Text style={styles.resultSubtitle}>Ton type de sorcier est :</Text>

        <View style={styles.winnerBox}>
          <Text style={styles.winnerType}>{result.winner.type}</Text>
          <Text style={styles.winnerScore}>Points: {result.winner.points} — Réponses associées: {result.winner.count}</Text>

          <Text style={styles.winnerDesc}>{getDescriptionForType(result.winner.type)}</Text>
        </View>

        <View style={styles.breakdownBox}>
          <Text style={styles.breakdownTitle}>Détail des scores</Text>
          {result.breakdown.map((b, idx) => (
            <View key={idx} style={styles.breakdownRow}>
              <Text style={styles.breakdownType}>{b.type}</Text>
              <Text style={styles.breakdownPoints}>{b.points} pts ({b.count} réponses)</Text>
            </View>
          ))}
        </View>

        <TouchableOpacity style={styles.restartButton} onPress={() => setScreen('HOME')}>
          <Text style={styles.restartButtonText}>Recommencer</Text>
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}

// Description text for each wizard type
function getDescriptionForType(type) {
  switch (type) {
    case WIZARD_TYPES.ELEMENTALIST:
      return "Elementalist — Tu es en harmonie avec les forces naturelles. Tes sorts tirent leur puissance des éléments : terre, feu, eau, air. Courageux et impulsif, tu protèges l’équilibre du monde.";
    case WIZARD_TYPES.NECROMANCER:
      return "Necromancer — Tu es fasciné par le cycle de la vie et de la mort. Ton savoir porte sur l’au-delà et les secrets anciens. Tu recherches la connaissance, parfois au prix du danger.";
    case WIZARD_TYPES.ILLUSIONIST:
      return "Illusionist — Tu joues avec la perception et la réalité. Créatif et joueur, tu préfères la ruse, la tromperie bienveillante et les spectacles magiques.";
    case WIZARD_TYPES.HEALER:
      return "Healer — Empathique et généreux, tu utilises la magie pour soigner et restaurer. Tu mets le bien-être des autres avant tout et inspires confiance.";
    default:
      return "Profil inconnu.";
  }
}

// ---------- STYLES ----------
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f172a' },
  homeBox: { padding: 24, alignItems: 'center', justifyContent: 'center', flex: 1 },
  title: { fontSize: 28, fontWeight: '700', color: '#fff', marginBottom: 8, textAlign: 'center' },
  subtitle: { fontSize: 14, color: '#cbd5e1', marginBottom: 20, textAlign: 'center' },
  startButton: { backgroundColor: '#7c3aed', paddingVertical: 14, paddingHorizontal: 28, borderRadius: 12, marginTop: 12 },
  startButtonText: { color: '#fff', fontWeight: '700' },
  infoBox: { marginTop: 24, backgroundColor: '#071029', padding: 12, borderRadius: 10, width: '100%' },
  infoTitle: { color: '#94a3b8', fontWeight: '700' },
  infoText: { color: '#cbd5e1', marginTop: 6 },

  quizHeader: { padding: 16, backgroundColor: '#fff', borderBottomLeftRadius: 18, borderBottomRightRadius: 18 },
  questionCounter: { fontSize: 12, color: '#334155', textAlign: 'center' },
  progressBackground: { height: 8, backgroundColor: '#e6edf3', borderRadius: 8, overflow: 'hidden', marginTop: 8 },
  progressFill: { height: 8, backgroundColor: '#22c55e' },

  questionBox: { padding: 20, marginTop: 20 },
  questionText: { fontSize: 20, color: '#fff', textAlign: 'center' },

  answersBox: { paddingHorizontal: 16, marginTop: 8 },
  answerButton: { backgroundColor: '#12203a', padding: 14, borderRadius: 10, marginVertical: 8, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  answerText: { color: '#e6eef8', flex: 1, marginRight: 10 },
  answerPoints: { color: '#94a3b8', fontSize: 12 },

  feedbackBox: { padding: 12, alignItems: 'center' },
  feedbackText: { color: '#cbd5e1' },

  resultContainer: { padding: 20 },
  resultTitle: { fontSize: 26, fontWeight: '800', color: '#fff', textAlign: 'center' },
  resultSubtitle: { fontSize: 14, color: '#94a3b8', textAlign: 'center', marginBottom: 12 },
  winnerBox: { backgroundColor: '#071029', padding: 16, borderRadius: 12, marginVertical: 12 },
  winnerType: { color: '#7c3aed', fontSize: 22, fontWeight: '800', textAlign: 'center' },
  winnerScore: { color: '#cbd5e1', marginTop: 6, textAlign: 'center' },
  winnerDesc: { color: '#e6eef8', marginTop: 10, textAlign: 'center' },

  breakdownBox: { marginTop: 12, backgroundColor: '#071029', padding: 12, borderRadius: 10 },
  breakdownTitle: { color: '#94a3b8', marginBottom: 8, fontWeight: '700' },
  breakdownRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 6 },
  breakdownType: { color: '#e6eef8' },
  breakdownPoints: { color: '#94a3b8' },

  restartButton: { backgroundColor: '#7c3aed', padding: 12, marginTop: 16, borderRadius: 10, alignItems: 'center' },
  restartButtonText: { color: '#fff', fontWeight: '700' },
});

/*
  ---------- DOCUMENTATION ET EXPLICATION DE LA GAMIFICATION ----------

  Ci-dessous se trouve le document expliquant la gamification, la logique du test, les chemins possibles
  et la description synthétique des 4 types de sorciers.

  Tu trouveras ces informations également dans l'éditeur du projet.
*/

// ---------- DOCUMENTATION (Markdown) ----------

/*
# Document de Gamification — "Quel type de sorcier es-tu ?"

## Objectif
Fournir un quiz ludique (20 questions) qui identifie le profil de sorcier du joueur parmi 4 archétypes : Elementalist, Necromancer, Illusionist, Healer.

L’application est pensée pour être simple, cross-platform (React Native), sans backend et adaptée à une intégration future (son, animations, partage).

## Principes de gamification intégrés

1. **Points par réponse** : Chaque réponse donne un certain nombre de points (+1 à +3). Cela crée un système de récompense numérique immédiat.

2. **Barre de progression** : Le joueur voit sa progression (question 1/20 etc.) via une barre animée, ce qui stimule l’engagement et l’achèvement.

3. **Feedback immédiat** : Après chaque réponse, le jeu affiche quel profil a gagné des points (+X pts pour TYPE). Ce micro-feedback renforce la connexion entre action et résultat.

4. **Résultat final clair et détaillé** : À la fin, le profil dominant est affiché avec une description, son score et une ventilation des points par profil.

5. **Rejouabilité** : Le bouton "Recommencer" permet de refaire le test pour améliorer son score ou explorer d’autres chemins.

## Mécanique de scoring et logique (comment c’est calculé)

- **Structure des réponses** : Chaque réponse a deux éléments importants : `type` (le profil auquel la réponse est associée) et `points` (le nombre de points attribués pour cette réponse).

- **Agrégation** : Pendant le quiz, l’application accumule deux mesures pour chaque type :
  - `points` : somme des points attribués pour ce type.
  - `count` : nombre de réponses choisies qui sont associées à ce type.

- **Détermination du profil gagnant** :
  1. On classe d’abord par `points` (celui qui a le plus de points gagne).
  2. En cas d’égalité sur les points, on utilise `count` (plus de réponses associées au profil gagne).
  3. En dernier recours (égalité parfaite), on utilise un ordre alphabétique stable pour décider (cela garantit une sortie déterministe).

Cette combinaison points / count permet d’avoir à la fois une granularité (pondération avec `points`) et une robustesse (nombre de réponses soutenant un profil).

## Chemins possibles

- Chaque question offre 4 choix correspondant chacun à un profil. Il y a donc `4^20` chemins théoriques — mais le design des questions vise à guider vers un profil dominant selon les tendances des réponses.

- Quelques scénarios typiques :
  - **Convergence forte** : Si l’utilisateur choisit majoritairement des réponses liées à un même profil (ex. Elementalist) — points élevés et count élevé — résultat très clair.
  - **Mix équilibré** : Si l’utilisateur répond varié, le score peut être serré : le tie-breaker par `count` ou la pondération `points` décidera.
  - **Stratégique** : L’utilisateur peut cibler des réponses à forte valeur (points 3) pour influencer le résultat même s’il ne choisit pas ce profil à chaque fois.

## Description synthétique des 4 types

1. **Elementalist**
   - *Essence*: Maîtrise des forces naturelles (terre, feu, eau, air).
   - *Qualités*: Dynamique, protecteur, connecté à l’environnement.
   - *Style*: Robes ornées, rituels en extérieur, sorts éléments puissants.

2. **Necromancer**
   - *Essence*: Compréhension des cycles de vie/mort et des secrets anciens.
   - *Qualités*: Curieux, réservé, prêt à explorer l’interdit pour la connaissance.
   - *Style*: Étude des rituels, grimoire, approche mystique.

3. **Illusionist**
   - *Essence*: Manipulation de la perception et de la réalité.
   - *Qualités*: Créatif, joueur, taquin, adepte des tromperies esthétiques.
   - *Style*: Spectacles, jeux psychologiques, ruse et charme.

4. **Healer**
   - *Essence*: Magie centrée sur la guérison et le soutien.
   - *Qualités*: Empathique, responsable, altruiste.
   - *Style*: Herboristerie, soins, rituels de restauration.

## Intégration UX / UI proposée

- **Palette** : Fond sombre, accents colorés (violet, vert) pour faire ressortir les éléments interactifs.
- **Micro-interactions** : Animation de la barre de progression, animation légère du texte de feedback.
- **Sons** : Prévoir des petits effets sonores pour réponse correcte / progression (optionnel, nécessite expo-av ou lib similaire).
- **Accessibilité** : Texte lisible, boutons larges, contrastes suffisants.

## Étapes d’évolution possibles

- Ajouter des **profils secondaires** (top 2) et des conseils personnalisés.
- Permettre de **partager** le résultat sur les réseaux sociaux (image + description).
- Ajouter des **badges** ou des succès (ex. "Elementalist Novice" après X points) pour renforcer la gamification.
- Ajouter de l’**audio** et des **animations/confettis** sur les résultats pour augmenter la satisfaction utilisateur.

## Notes techniques

- L’application fournie est un prototype front-end fonctionnel en React Native — peut être démarrée via Expo si souhaité (en plaçant le code dans App.js d’un projet Expo).
- Pas de stockage persistant inclus (mais on peut facilement ajouter AsyncStorage pour sauvegarder le dernier résultat).

---

Merci ! Si tu veux, je peux :
- Te fournir une version prête pour Expo (package.json + instructions),
- Ajouter sons et effets (avec expo-av),
- Transformer les descriptions en images partageables,
- Ou réduire / augmenter le nombre de questions.

*/
