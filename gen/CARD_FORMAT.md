# Format des cartes & prompt IA

Documente le format JSON attendu pour une carte Taboo et donne un prompt
prêt à copier-coller dans un assistant IA pour en générer de nouvelles.

## Pipeline

```
gen/cards_NNN.json (un fichier par lot, ~50-100 cartes)
        │  gen/merge.py
        ▼
taboo_cards_fr.json (fusion + dédoublonnage, insensible à la casse)
        │  gen/to_lua.py
        ▼
taboo_cards_fr.lua (format chargé par le jeu, groupé par thème)
```

- `merge.py` : fusionne tous les `gen/cards_*.json` en un seul
  `taboo_cards_fr.json`, en ignorant les mots déjà vus (comparaison
  insensible à la casse sur `word`).
- `add_metadata.py` : ajoute `theme`/`difficulty` aux fichiers qui ne les
  ont pas encore (legacy — les nouveaux fichiers doivent déjà inclure ces
  champs, voir ci-dessous).
- `to_lua.py` : produit le fichier final chargé par `screen.lua`, groupé
  par thème dans l'ordre de `themes.json`.

Pour ajouter un lot de cartes : créer `gen/cards_161.json` (ou le numéro
suivant disponible) au format ci-dessous, puis lancer
`python3 gen/merge.py && python3 gen/to_lua.py` depuis `taboo.koplugin/`.

## Format d'une carte

```json
{
  "word": "Éléphant",
  "forbidden": ["Afrique", "Trompe", "Défense", "Gris", "Savane"],
  "theme": "animaux",
  "difficulty": "easy"
}
```

| Champ | Type | Contrainte |
|---|---|---|
| `word` | string | Le mot à faire deviner. Casse capitalisée (`Éléphant`, pas `éléphant`). Unique dans tout le corpus (insensible à la casse — `merge.py` élimine les doublons). |
| `forbidden` | array de 5 strings | Les mots interdits. Exactement 5. Aucun ne doit être égal à `word` (insensible à la casse) ni se répéter entre eux. |
| `theme` | string | Un des identifiants de [`themes.json`](themes.json) — voir la liste complète dans ce fichier. |
| `difficulty` | string | `"easy"`, `"medium"` ou `"hard"`. |

### Ce qui fait un bon mot interdit

Les 5 mots interdits doivent être les mots qu'un joueur utiliserait
*naturellement* et *en premier* pour décrire le mot principal — c'est ce
qui rend la carte difficile. Éviter :
- les synonymes triviaux du mot lui-même,
- les mots trop génériques (« chose », « objet », « truc ») sauf en
  dernier recours pour compléter à 5,
- les répétitions entre les 5 mots.

### Repère pour `difficulty`

- **easy** — mot très courant, connu de tous (animal domestique, objet du
  quotidien, pays connu…).
- **medium** — mot courant mais moins immédiat (métier spécifique, plat
  moins connu, ville moyenne…).
- **hard** — mot technique, spécialisé ou rare (terme scientifique,
  personnage historique obscur, instrument de musique rare…).

## Prompt IA pour générer un nouveau lot

Copier-coller ce prompt dans un assistant IA en remplaçant `{THEME}`,
`{SOUS-THEME}` et `{N}` par les valeurs voulues. La liste des thèmes
valides est dans [`themes.json`](themes.json).

````text
Tu génères des cartes pour un jeu de Taboo en français.

Génère {N} cartes sur le sous-thème « {SOUS-THEME} » (thème général :
{THEME}). Réponds UNIQUEMENT avec un tableau JSON valide, sans texte
autour, au format suivant pour chaque carte :

{
  "word": "MotPrincipal",
  "forbidden": ["Mot1", "Mot2", "Mot3", "Mot4", "Mot5"],
  "theme": "{THEME}",
  "difficulty": "easy|medium|hard"
}

Règles strictes :
- "word" : un seul mot ou une courte expression, casse capitalisée
  (première lettre en majuscule), en français.
- "forbidden" : exactement 5 mots interdits — les mots qu'un joueur
  utiliserait le plus naturellement pour décrire "word". Aucun ne doit
  être identique à "word" ni se répéter dans la liste. Éviter les mots
  trop génériques.
- "theme" : toujours "{THEME}" (un des identifiants valides :
  fun, alimentation, animaux, arts, cinéma, géographie, histoire,
  jeuxvideo, maison, médecine, métiers, mode, musique, nature, sciences,
  société, sports, technologies, transports).
- "difficulty" : "easy" pour un mot très courant, "medium" pour un mot
  courant mais moins immédiat, "hard" pour un mot technique ou rare.
- Pas de doublons entre les {N} cartes ("word" unique dans le lot).
- Varie les niveaux de difficulté dans le lot (pas uniquement "easy").

Sous-thème précis à couvrir : {SOUS-THEME}
````

Après génération : sauvegarder la réponse dans
`gen/cards_NNN.json` (tableau JSON brut), vérifier que chaque carte a
bien 5 mots interdits distincts, puis lancer
`python3 gen/merge.py && python3 gen/to_lua.py`.
