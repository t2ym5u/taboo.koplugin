#!/usr/bin/env python3
"""
Adds 'theme' and 'difficulty' fields to all existing cards_NNN.json files.
Difficulty is assigned per-word using a simple heuristic:
  - easy:   very common everyday words
  - medium: moderately common words
  - hard:   technical, specialized or obscure words
Theme is assigned per-file based on content.
"""
import json, os, glob, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Map file numbers (as int) to theme string
FILE_THEMES = {
    1:  "animaux",
    2:  "animaux",
    3:  "animaux",
    4:  "animaux",
    5:  "animaux",
    6:  "animaux",
    7:  "animaux",
    8:  "alimentation",
    9:  "alimentation",
    10: "sports",
    11: "alimentation",
    12: "alimentation",
    13: "alimentation",
    14: "alimentation",
    15: "géographie",
    16: "géographie",
    17: "géographie",
    18: "géographie",
    19: "métiers",
    20: "métiers",
    21: "maison",
    22: "maison",
    23: "mode",
    24: "mode",
    25: "musique",
    26: "musique",
    27: "histoire",
    28: "histoire",
    29: "médecine",
    30: "médecine",
    31: "sciences",
    32: "nature",
    33: "sports",
    34: "technologies",
    35: "arts",
    36: "société",
    37: "société",
    38: "alimentation",
    39: "alimentation",
}

# Words (lowercased) considered EASY — very common everyday words
EASY_WORDS = {
    # animaux
    "chien","chat","vache","cochon","mouton","cheval","poule","lapin","canard","souris",
    "lion","tigre","ours","loup","renard","singe","serpent","grenouille","aigle","hibou",
    "poisson","baleine","dauphin","requin","pieuvre","fourmi","abeille","papillon",
    # alimentation
    "pomme","orange","citron","fraise","cerise","raisin","poire","pêche","banane","melon",
    "tomate","carotte","pomme de terre","salade","oignon","ail","radis","haricot","petit pois",
    "pain","beurre","lait","œuf","fromage","viande","poulet","poisson","riz","sucre","sel",
    "bière","vin","eau","café","thé","jus","chocolat","confiture","miel","gâteau",
    # maison
    "maison","jardin","cuisine","chambre","salon","lit","chaise","table","porte","fenêtre",
    "lampe","tapis","armoire","miroir","verre","assiette","couteau","fourchette","cuillère",
    "four","frigo","télévision","téléphone","voiture","vélo","bus","train","avion","bateau",
    # vêtements
    "chaussure","pantalon","jupe","robe","chapeau","manteau","pull","tee-shirt","jean",
    "sac","montre","lunettes","ceinture","chaussette","gant","écharpe",
    # corps
    "bras","jambe","tête","main","pied","œil","nez","bouche","oreille","dent","cheveux",
    # nature
    "arbre","fleur","herbe","soleil","lune","mer","rivière","montagne","neige","pluie","vent",
    "nuage","ciel","nuit","jour","feu","eau","terre","forêt","lac","plage",
    # métiers
    "médecin","pompier","policier","boulanger","professeur","cuisinier","pilote","soldat",
    # sports
    "football","tennis","natation","vélo","ski","boxe","golf","rugby","basket","volley",
    # géographie
    "france","paris","europe","afrique","asie","amérique","chine","japon","brésil",
    # divers
    "famille","mariage","école","fête","cadeau","voyage","vacances",
    # t-shirt, etc.
    "t-shirt","polo","short","jupe","robe",
}

# Words (lowercased) considered HARD — technical, specialized, obscure
HARD_WORDS = {
    # sciences
    "électrolyse","catalyse","mitochondrie","neurotransmetteur","photosynthèse",
    "mécanique quantique","relativité","thermodynamique","électromagnétisme",
    "chromosome","neurotransmetteur","mitochondrie","agar-agar",
    # médecine
    "kinésithérapeute","ergothérapeute","orthophoniste","gynécologue","dermatologue",
    "cardiologue","neurologue","psychiatre","chimiothérapie","radiothérapie","dialyse",
    "schizophrénie","ostéoporose","artériosclérose","thrombose",
    "grippe","pneumonie","tuberculose","paludisme","leishmaniose",
    # métiers techniques
    "commissaire-priseur","expert-comptable","data scientist","webmaster",
    "vidéaste","chorégraphe","carrossier","couvreur","vitrier","carreleur",
    # musique
    "berimbau","gamelan","kora","sitar","balalaïka","shamisen","darbouka",
    "gayageum","guzheng","erhu","biwa","didgeridoo","vaporwave","theremine",
    "bandonéon","flûte de pan",
    # histoire
    "hammurabi","vercingétorix","hannibal","gengis khan","saladin",
    "montezuma","charlemagne","solon","périclès",
    # arts
    "photomontage","motion design","concept art","stop-motion","lithographie",
    "prestidigitation","électro-acoustique",
    # géographie obscure
    "tourbière","mangrove","toundra",
    # alimentation
    "nuoc-mâm","ras el hanout","garam masala","zaatar","tahini","fenugrec",
    "worcestershire","gélatine","agar-agar","fécule",
    # maison
    "véranda","digicode","interphone","composte",
    # mythologie
    "héphaistos","dionysos","prométhée","minotaure","méduse","gaïa",
    "héra","hadès","déméter","hestia","hermès",
    # religions/philosophie
    "zoroastrisme","animisme","chamanisme","confucianisme","taoïsme",
    "bandonéon","kora","guimbarde",
    # technologie
    "blockchain","cryptographie","machine learning","motion design",
}

def get_difficulty(word):
    w = word.lower()
    if w in EASY_WORDS:
        return "easy"
    if w in HARD_WORDS:
        return "hard"
    # Heuristic: long specialized words tend to be hard
    if len(word) >= 15:
        return "hard"
    if len(word) <= 5:
        return "easy"
    return "medium"

def process_file(path):
    num = int(re.search(r'cards_(\d+)\.json', os.path.basename(path)).group(1))
    theme = FILE_THEMES.get(num, "divers")

    with open(path, encoding="utf-8") as f:
        cards = json.load(f)

    changed = 0
    for card in cards:
        if "theme" not in card:
            card["theme"] = theme
            changed += 1
        if "difficulty" not in card:
            card["difficulty"] = get_difficulty(card.get("word",""))
            changed += 1

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=None, separators=(",", ":"))
            f.write("\n")
        print(f"  Updated {os.path.basename(path)} ({len(cards)} cards, theme={theme})")
    else:
        print(f"  Skipped {os.path.basename(path)} (already tagged)")

files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "cards_*.json")))
print(f"Processing {len(files)} files...")
for path in files:
    process_file(path)
print("Done.")
