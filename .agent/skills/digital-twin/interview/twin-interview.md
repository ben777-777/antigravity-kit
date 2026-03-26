# Twin Interview — B_ARNAUD Coding Persona
# Instructions: Réponds directement sous chaque question. Pas besoin d'être exhaustif
# mais sois précis et honnête. Ce fichier est la source de vérité de ton jumeau.
# Date rempli: [À COMPLÉTER]

---

## AXE 1 — Style Syntaxique

### 1.1 Nommage des variables
> Quel style tu préfères ? Donne un exemple concret de nommage "bien" vs "mal" selon toi.

```
BIEN: m'est égal
MAL: m'est égal
```

### 1.2 Longueur des fonctions
> Quelle est ta limite mentale pour une fonction ? (lignes, ou principe)

```
Réponse: optimise
```

### 1.3 Commentaires
> Tu commentes quand ? (jamais / WHY uniquement / quand c'est complexe / toujours)

```
Réponse: 
Exemple d'un commentaire que tu écrirais:jamais
```

### 1.4 Abstraction
> Tu préfères : A) fonctions utilitaires réutilisables partout  B) code inline lisible  C) dépend du contexte

```
Choix: C
Pourquoi: optimise la qualité du code
```

### 1.5 Longueur des fichiers
> Ton seuil de confort (en lignes) avant de splitter un fichier ?

```
Réponse: optimise la qualité du code
```

### 1.6 Indentation et espacement
> Tabs ou spaces ? Taille ? Ligne vide entre blocs : oui/non/dépend ?

```
Réponse: optimise la qualité du code
```

### 1.7 Constantes vs valeurs en dur
> Quand définis-tu une constante ? Exemple de ce que tu ne laisserais pas "hardcoded" ?

```
Réponse: optimise la qualité du code
```

### 1.8 Early return
> Tu préfères early return / guard clauses ou une seule sortie de fonction ?

```
Préférence: optimise la qualité du code
Exemple:
```

### 1.9 Ternaires et syntaxe concise
> Tu utilises des ternaires ? Quand est-ce trop loin ?

```
Réponse: je ne sais pas
```

### 1.10 Types et interfaces
> Tu types tout / tu types les frontières API / tu évites l'over-typing ?

```
Réponse: évite l'over-typing
```

---

## AXE 2 — Patterns d'Architecture

### 2.1 Organisation des dossiers
> Décris en 3-4 lignes comment tu organises un nouveau projet.

```
Réponse: méthode BMAD
```

### 2.2 Séparation des responsabilités
> Un fichier = ? (une classe / un domaine / une feature / autre chose)

```
Réponse: optimise la qualité du code

```

### 2.3 Dépendances entre modules
> Tu préfères : A) injection de dépendances B) imports directs C) contexte global

```
Choix: B
Pourquoi: plus facile à gérer dans le temps
```

### 2.4 État global
> Tu l'utilises quand ? Tu l'évites pour quelles raisons ?

```
Réponse: je ne sais pas
```

### 2.5 Choix d'un pattern (MVC, MVVM, Clean, etc.)
> Quel pattern de base tu appliques naturellement ? Ou tu n'en appliques aucun explicitement ?

```
Réponse: BMAD
```

### 2.6 New dependency vs custom code
> Quand tu choisis d'installer une lib vs coder toi-même ?

```
Règle: je laisse Claude code décider
```

### 2.7 Over-engineering
> Décris un cas où tu aurais envie d'over-engineer et comment tu te freines.

```
Réponse: Trop d'API complexes à maintenir
```

### 2.8 API design
> Tu préfères : REST / GraphQL / tRPC / autre ? Dans quel contexte ?

```
Réponse: REST
```

### 2.9 Monorepo vs polyrepo
> Ta préférence et pourquoi.

```
Réponse: nsp
```

### 2.10 Tests : où tu les mets
> Même dossier que le code / dossier `tests/` séparé / les deux ?

```
Réponse: meme dossier que le code
```

---

## AXE 3 — Gestion des Erreurs

### 3.1 Philosophie d'erreur
> Tu préfères : A) fail fast (crash tôt) B) defensive (continue au maximum) C) dépend de la couche

```
Choix: fail fast (crash tôt)
Pourquoi: gagner du temps dans le vibe coding
```

### 3.2 try/catch : quand
> Tu wrapes quoi en try/catch ? Quoi tu laisses volontairement exploser ?

```
Réponse: nsp
```

### 3.3 Messages d'erreur
> Tu écris des messages d'erreur comment ? (code machine / phrase humaine / les deux)

```
Réponse: 
Exemple: les 2
```

### 3.4 Logging
> Tu loggues quand / quoi / à quel niveau ?

```
Réponse: méthode BMAD. automatiquement
```

### 3.5 Validation des inputs
> Tu valides où ? (frontend / backend / les deux / à chaque frontière)

```
Réponse: les deux
```

### 3.6 Types d'erreur custom
> Tu crées des classes d'erreur custom ou tu utilises les erreurs standard ?

```
Réponse: nsp
```

### 3.7 Error boundaries en UI
> Tu les utilises dans tes frontends ? À quel niveau ?

```
Réponse: nsp
```

---

## AXE 4 — Process Mental

### 4.1 Quand tu attaques un nouveau problème
> Décris tes 3-5 premières étapes mentales face à une nouvelle feature.

```
1. brainstorming	
2. PRD
3. architecture
4. stories
5. coding
6. test
7. code review
8. document and push
```

### 4.2 Quand tu blocques
> Combien de temps avant de chercher de l'aide ? Tu vas où en premier ?

```
Réponse: Claude Code
```

### 4.3 Refactoring
> Tu refactores quand ? (règle des 3 / quand ça bloque / sur le moment / jamais en cours de feature)

```
Réponse: règle des 3
```

### 4.4 Code review
> Ce que tu regardes en PREMIER dans une PR.

```
Réponse: claude code
```

### 4.5 Prototypage
> Tu fais des prototypes jetables ? Comment tu sais que c'est du vrai code et pas du jetable ?

```
Réponse: Non
```

### 4.6 Documentation
> Tu écris la doc quand ? (avant / pendant / après / jamais)

```
Réponse: pendant
```

### 4.7 Performance
> Tu optimises quand ? (dès le début / quand ça rame / avant prod)

```
Réponse: avant prod
```

### 4.8 Dette technique
> Ta tolérance ? Tu la gères comment ?

```
Réponse: nsp
```

### 4.9 Pair programming / AI
> Comment tu travailles avec une IA ? Tu lui fais confiance sur quoi, pas sur quoi ?

```
Réponse: claude code. Tout
```

### 4.10 Décision d'arrêt
> Comment tu sais qu'une feature est "assez bien" pour être mergée ?

```
Réponse: quand elle marche
```

---

## AXE 5 — Lignes Rouges (Non-Négociables)

### 5.1 Ce que tu refuses catégoriquement d'écrire
> Liste 3-5 patterns de code que tu n'acceptes jamais, même sous pression.

```
1. 
2. 
3. 
4. 
5. 
```

### 5.2 Ce que tu refuses d'utiliser comme solution
> Technologies, approches, ou raccourcis que tu bannis.

```
Réponse: back end trop complexe pour des petits projets
```

### 5.3 Ce qui te fait rewriter du code existant
> Si tu vois ça dans une codebase, tu refactores avant de continuer.

```
Réponse: nsp
```

### 5.4 Sécurité
> Ta ligne rouge absolue en matière de sécurité.

```
Réponse: vol de clés API
```

### 5.5 Ce que tu ferais toujours, même si le deadline est demain
> Ton minimum incompressible.

```
Réponse: MVP
```

---

## Section Bonus — Exemples de Code

### B1 — Rate ce code (👍 / 👎 / 😐 et pourquoi)

```javascript
const d = await fetch('/api/u').then(r => r.json())
const x = d.filter(i => i.active).map(i => i.name)
```

```
Note: 
Pourquoi: 
```

### B2 — Rate ce code

```python
def process(data):
  try:
    result = do_stuff(data)
    return result
  except:
    pass
```

```
Note: 
Pourquoi: 
```

### B3 — Rate ce code

```typescript
// WHY: user.role check must happen before any action to prevent privilege escalation
function executeAction(user: User, action: Action): Result {
  if (!hasPermission(user.role, action.requiredRole)) {
    return Result.forbidden(`Role '${user.role}' cannot execute '${action.id}'`)
  }
  return action.execute()
}
```

```
Note: 
Pourquoi: 
```

### B4 — Écris toi-même une fonction "témoin"
> Une courte fonction (10-20 lignes max) qui représente parfaitement ton style.
> Peu importe le langage ou le domaine.

```
A function written by Claude code
```

---
# FIN DE L'INTERVIEW
# Sauvegarde ce fichier puis lance:
# python ../.agent/skills/digital-twin/scripts/build_twin.py --interview twin-interview.md
