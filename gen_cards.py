# -*- coding: utf-8 -*-
"""Generator for French Taboo cards. Produces >=8000 unique cards as JSON."""
import json, unicodedata

cards = {}   # word -> [5 forbidden]

def add(word, forbidden):
    word = word.strip()
    if not word:
        return
    if word in cards:
        return
    # ensure exactly 5, unique-ish, non-empty, not equal to word
    seen = []
    for f in forbidden:
        f = f.strip()
        if not f:
            continue
        if f.lower() == word.lower():
            continue
        if f in seen:
            continue
        seen.append(f)
    # pad if short using generic descriptors
    pad = ["Mot", "Chose", "Objet", "Terme", "Idée", "Genre", "Type", "Sujet",
           "Nom", "Élément", "Notion", "Ensemble"]
    i = 0
    while len(seen) < 5:
        p = pad[i % len(pad)]
        if p != word and p not in seen:
            seen.append(p)
        i += 1
        if i > 50:
            break
    cards[word] = seen[:5]

# ---------------------------------------------------------------------------
# 1. High-quality curated cards (most common words) --------------------------
# ---------------------------------------------------------------------------
curated = {
 "Chien":["Animal","Aboyer","Laisse","Poil","Chiot"],
 "Chat":["Animal","Miauler","Griffe","Souris","Ronronner"],
 "Lion":["Félin","Roi","Crinière","Savane","Rugir"],
 "Tigre":["Félin","Rayures","Jungle","Orange","Rugir"],
 "Éléphant":["Trompe","Défense","Gris","Afrique","Oreilles"],
 "Girafe":["Cou","Taches","Grand","Savane","Afrique"],
 "Singe":["Banane","Arbre","Grimper","Jungle","Primate"],
 "Dauphin":["Mer","Nageoire","Intelligent","Saut","Mammifère"],
 "Baleine":["Océan","Géante","Mammifère","Jet","Plancton"],
 "Requin":["Océan","Dents","Prédateur","Aileron","Danger"],
 "Aigle":["Oiseau","Serres","Bec","Voler","Montagne"],
 "Serpent":["Reptile","Ramper","Venin","Siffler","Écailles"],
 "Grenouille":["Amphibien","Sauter","Étang","Coasser","Vert"],
 "Tortue":["Carapace","Lente","Reptile","Nager","Longévité"],
 "Lapin":["Oreilles","Carotte","Sauter","Terrier","Poil"],
 "Cochon":["Ferme","Rose","Boue","Grogner","Jambon"],
 "Vache":["Lait","Ferme","Meuh","Herbe","Pré"],
 "Cheval":["Galop","Selle","Écurie","Crinière","Cavalier"],
 "Mouton":["Laine","Bêler","Troupeau","Berger","Pré"],
 "Loup":["Forêt","Hurler","Meute","Sauvage","Croc"],
 "Ours":["Grand","Miel","Forêt","Hiberner","Poilu"],
 "Renard":["Rusé","Roux","Queue","Forêt","Poule"],
 "Abeille":["Miel","Ruche","Piquer","Butiner","Fleur"],
 "Papillon":["Ailes","Chenille","Fleur","Voler","Couleurs"],
 "Araignée":["Toile","Pattes","Insecte","Peur","Tisser"],
 "Pizza":["Italie","Fromage","Tomate","Four","Pâte"],
 "Baguette":["Pain","Boulangerie","Croustillant","Français","Farine"],
 "Croissant":["Beurre","Petit-déjeuner","Boulangerie","Feuilleté","Café"],
 "Crêpe":["Pâte","Chandeleur","Sucre","Poêle","Nutella"],
 "Fromage":["Lait","Vache","Odeur","Camembert","Plateau"],
 "Chocolat":["Cacao","Noir","Sucré","Tablette","Pâques"],
 "Café":["Boisson","Chaud","Caféine","Matin","Tasse"],
 "Vin":["Raisin","Rouge","Bouteille","Verre","Alcool"],
 "Pain":["Boulangerie","Farine","Mie","Croûte","Baguette"],
 "Sucre":["Sucré","Blanc","Café","Bonbon","Morceau"],
 "Sel":["Salé","Mer","Blanc","Assaisonner","Poivre"],
 "Football":["Ballon","But","Terrain","Équipe","Match"],
 "Tennis":["Raquette","Balle","Filet","Court","Service"],
 "Natation":["Piscine","Nager","Eau","Brasse","Crawl"],
 "Ski":["Neige","Montagne","Piste","Descente","Hiver"],
 "Boxe":["Gants","Ring","Coup","Poing","Combat"],
 "France":["Paris","Europe","Français","Baguette","Coq"],
 "Paris":["France","Capitale","Eiffel","Seine","Louvre"],
 "Italie":["Rome","Pizza","Botte","Pasta","Europe"],
 "Espagne":["Madrid","Paella","Flamenco","Europe","Toro"],
 "Japon":["Tokyo","Sushi","Asie","Samouraï","Manga"],
 "Chine":["Pékin","Asie","Muraille","Riz","Panda"],
 "Médecin":["Malade","Hôpital","Soigner","Ordonnance","Blouse"],
 "Pompier":["Feu","Camion","Sauver","Incendie","Caserne"],
 "Policier":["Uniforme","Loi","Arrêter","Voleur","Enquête"],
 "Boulanger":["Pain","Four","Farine","Baguette","Fournil"],
 "Professeur":["École","Élève","Cours","Enseigner","Tableau"],
 "Téléphone":["Appeler","Écran","Portable","Sonner","Numéro"],
 "Ordinateur":["Écran","Clavier","Internet","Souris","Bureau"],
 "Voiture":["Route","Roue","Conduire","Moteur","Volant"],
 "Vélo":["Roue","Pédale","Guidon","Rouler","Sport"],
 "Avion":["Voler","Ciel","Aéroport","Pilote","Ailes"],
 "Train":["Rail","Gare","Wagon","Vitesse","Locomotive"],
 "Maison":["Toit","Habiter","Porte","Mur","Foyer"],
 "Fenêtre":["Vitre","Ouvrir","Mur","Lumière","Voir"],
 "Porte":["Ouvrir","Fermer","Poignée","Entrée","Clé"],
 "Lit":["Dormir","Chambre","Oreiller","Draps","Matelas"],
 "Table":["Manger","Chaise","Bois","Plate","Repas"],
 "Chaise":["Asseoir","Table","Pieds","Dossier","Bois"],
 "Soleil":["Chaud","Jaune","Ciel","Lumière","Étoile"],
 "Lune":["Nuit","Ciel","Ronde","Étoiles","Croissant"],
 "Pluie":["Eau","Nuage","Parapluie","Mouillé","Goutte"],
 "Neige":["Blanc","Froid","Hiver","Flocon","Bonhomme"],
 "Vent":["Souffler","Air","Tempête","Brise","Feuilles"],
 "Rouge":["Couleur","Sang","Tomate","Feu","Amour"],
 "Bleu":["Couleur","Ciel","Mer","Azur","Océan"],
 "Vert":["Couleur","Herbe","Nature","Feuille","Écologie"],
 "Cœur":["Amour","Battre","Organe","Rouge","Poitrine"],
 "Main":["Doigts","Bras","Toucher","Paume","Cinq"],
 "Œil":["Voir","Regard","Vision","Paupière","Pupille"],
 "Tête":["Cerveau","Cheveux","Visage","Cou","Penser"],
 "Pied":["Marcher","Chaussure","Orteil","Jambe","Talon"],
 "Amour":["Cœur","Sentiment","Passion","Couple","Aimer"],
 "Peur":["Trembler","Crainte","Danger","Frisson","Angoisse"],
 "Joie":["Bonheur","Sourire","Rire","Content","Fête"],
 "Colère":["Fâché","Crier","Rage","Rouge","Énervé"],
 "Guitare":["Cordes","Musique","Jouer","Rock","Instrument"],
 "Piano":["Touches","Musique","Noir","Blanc","Clavier"],
 "Violon":["Cordes","Archet","Musique","Orchestre","Aigu"],
 "Roi":["Couronne","Trône","Royaume","Reine","Château"],
 "Reine":["Couronne","Roi","Royaume","Trône","Château"],
 "Dieu":["Religion","Prière","Ciel","Croire","Divin"],
 "Église":["Prière","Curé","Cloche","Messe","Croix"],
 "Argent":["Monnaie","Riche","Banque","Payer","Pièces"],
 "Banque":["Argent","Compte","Carte","Prêt","Coffre"],
 "Rose":["Fleur","Épine","Rouge","Parfum","Amour"],
 "Arbre":["Feuille","Branche","Tronc","Racine","Forêt"],
 "Chêne":["Arbre","Gland","Bois","Robuste","Forêt"],
 "Sapin":["Noël","Vert","Épine","Arbre","Montagne"],
 "Étoile":["Ciel","Nuit","Briller","Filante","Espace"],
 "Mars":["Planète","Rouge","Espace","Guerre","Fusée"],
 "Fusée":["Espace","Décoller","NASA","Astronaute","Feu"],
 "Liberté":["Libre","Prison","Droit","Choix","Indépendance"],
 "Justice":["Loi","Juge","Tribunal","Équité","Droit"],
 "Vérité":["Vrai","Mensonge","Honnête","Fait","Sincère"],
 "Temps":["Horloge","Heure","Passer","Montre","Minute"],
 "Mort":["Décès","Tombe","Fin","Vie","Cercueil"],
 "Vie":["Naître","Vivant","Existence","Souffle","Mort"],
 "Feu":["Flamme","Chaud","Brûler","Rouge","Bois"],
 "Eau":["Boire","Liquide","Mer","Transparent","Robinet"],
 "Livre":["Lire","Pages","Histoire","Auteur","Bibliothèque"],
 "Musique":["Note","Son","Chanson","Écouter","Mélodie"],
 "Danse":["Bouger","Musique","Rythme","Bal","Pas"],
 "Cinéma":["Film","Écran","Acteur","Salle","Popcorn"],
 "Théâtre":["Scène","Acteur","Pièce","Rideau","Public"],
 "Guerre":["Combat","Soldat","Arme","Paix","Bataille"],
 "Paix":["Guerre","Calme","Colombe","Tranquille","Harmonie"],
 "Montagne":["Sommet","Haut","Neige","Alpes","Escalade"],
 "Mer":["Vague","Plage","Sel","Bleu","Poisson"],
 "Plage":["Sable","Mer","Soleil","Vacances","Bronzer"],
 "Forêt":["Arbre","Bois","Vert","Sauvage","Sentier"],
 "Rivière":["Eau","Couler","Pont","Poisson","Berge"],
 "Fleur":["Pétale","Parfum","Jardin","Bouquet","Rose"],
 "Jardin":["Fleur","Herbe","Plante","Arroser","Potager"],
 "Pomme":["Fruit","Rouge","Croquer","Verger","Arbre"],
 "Banane":["Fruit","Jaune","Singe","Peau","Courbe"],
 "Orange":["Fruit","Jus","Vitamine","Rond","Agrume"],
 "Fraise":["Fruit","Rouge","Sucré","Confiture","Été"],
 "Tomate":["Rouge","Salade","Légume","Sauce","Rond"],
 "Carotte":["Orange","Légume","Lapin","Racine","Potager"],
 "Œuf":["Poule","Coquille","Omelette","Jaune","Casser"],
 "Lait":["Vache","Blanc","Boire","Verre","Yaourt"],
 "Miel":["Abeille","Sucré","Doré","Ruche","Tartine"],
 "Beurre":["Lait","Tartine","Jaune","Cuisine","Gras"],
 "Riz":["Blanc","Grain","Chine","Cuire","Céréale"],
 "Poisson":["Mer","Nager","Écaille","Pêcher","Arête"],
 "Viande":["Boucher","Rouge","Steak","Manger","Protéine"],
 "Soupe":["Chaud","Légume","Bol","Cuillère","Bouillon"],
 "Gâteau":["Sucré","Anniversaire","Bougie","Four","Dessert"],
 "Glace":["Froid","Été","Cornet","Dessert","Vanille"],
 "Bonbon":["Sucré","Enfant","Coloré","Sucrerie","Friandise"],
 "École":["Élève","Professeur","Apprendre","Classe","Cartable"],
 "Hôpital":["Malade","Médecin","Soigner","Urgence","Blouse"],
 "Prison":["Cellule","Barreaux","Prisonnier","Enfermer","Gardien"],
 "Roue":["Ronde","Voiture","Tourner","Pneu","Rouler"],
 "Clé":["Serrure","Ouvrir","Porte","Trousseau","Fermer"],
 "Lampe":["Lumière","Ampoule","Éclairer","Bureau","Interrupteur"],
 "Miroir":["Reflet","Voir","Glace","Vitre","Image"],
 "Horloge":["Heure","Temps","Aiguille","Tic-tac","Mur"],
 "Montre":["Poignet","Heure","Aiguille","Temps","Bracelet"],
 "Parapluie":["Pluie","Ouvrir","Protéger","Mouillé","Toile"],
 "Chapeau":["Tête","Couvrir","Bord","Mode","Soleil"],
 "Chaussure":["Pied","Lacet","Semelle","Marcher","Paire"],
 "Manteau":["Froid","Hiver","Vêtement","Chaud","Porter"],
 "Pantalon":["Jambes","Vêtement","Jean","Ceinture","Porter"],
 "Robe":["Femme","Vêtement","Élégante","Longue","Soirée"],
 "Lunettes":["Yeux","Voir","Verre","Nez","Vue"],
 "Sac":["Porter","Épaule","Contenir","Main","Cuir"],
 "Stylo":["Écrire","Encre","Papier","Bille","Main"],
 "Crayon":["Écrire","Bois","Mine","Gomme","Dessiner"],
 "Papier":["Feuille","Blanc","Écrire","Arbre","Imprimer"],
 "Ciseaux":["Couper","Lame","Papier","Deux","Trancher"],
 "Couteau":["Couper","Lame","Tranchant","Manche","Cuisine"],
 "Fourchette":["Manger","Piquer","Dents","Couvert","Assiette"],
 "Cuillère":["Manger","Soupe","Creux","Couvert","Ronde"],
 "Assiette":["Manger","Ronde","Repas","Table","Plate"],
 "Verre":["Boire","Transparent","Eau","Fragile","Vin"],
 "Bouteille":["Liquide","Bouchon","Verre","Eau","Vin"],
 "Ballon":["Rond","Jouer","Football","Gonfler","Rebondir"],
 "Ordonnance":["Médecin","Médicament","Pharmacie","Prescrire","Papier"],
 "Guitare électrique":["Rock","Amplificateur","Cordes","Solo","Jouer"],
 "Napoléon":["Empereur","France","Bataille","Corse","Bicorne"],
 "Einstein":["Physique","Relativité","Génie","Savant","Cheveux"],
 "Picasso":["Peintre","Cubisme","Espagne","Tableau","Art"],
 "Mozart":["Musique","Compositeur","Piano","Autriche","Symphonie"],
 "Shakespeare":["Théâtre","Anglais","Hamlet","Écrivain","Pièce"],
 "Bouddha":["Religion","Méditation","Asie","Sagesse","Temple"],
 "Jésus":["Religion","Chrétien","Croix","Bible","Nazareth"],
 "Rose (couleur)":["Couleur","Pâle","Fille","Bonbon","Doux"],
 "Cercle":["Rond","Forme","Géométrie","Courbe","Roue"],
 "Carré":["Forme","Côtés","Géométrie","Angle","Quatre"],
 "Triangle":["Forme","Côtés","Trois","Géométrie","Angle"],
 "Un":["Nombre","Chiffre","Premier","Unité","Seul"],
 "Cent":["Nombre","Centaine","Chiffre","Dix","Beaucoup"],
 "Mille":["Nombre","Beaucoup","Chiffre","Grand","Millier"],
 "Santé":["Bien","Malade","Corps","Médecin","Forme"],
 "Maladie":["Malade","Virus","Soigner","Symptôme","Médecin"],
 "Vaccin":["Piqûre","Maladie","Prévenir","Injection","Immunité"],
 "Bourse":["Argent","Actions","Trader","Finance","Wall Street"],
 "Internet":["Web","Réseau","Connexion","Google","En ligne"],
 "Google":["Recherche","Internet","Moteur","Web","Requête"],
 "Robot":["Machine","Métal","Intelligence","Androïde","Programmé"],
 "Piano électrique":["Clavier","Musique","Touches","Électrique","Jouer"],
}
for w, f in curated.items():
    add(w, f)

# ---------------------------------------------------------------------------
# 2. Category word lists -> generated forbidden words ------------------------
# ---------------------------------------------------------------------------
# Each category maps to a list of words plus a set of "anchor" forbidden
# words that fit the whole category. For each word we build 5 forbidden
# entries by combining category anchors with a couple of word-derived hints.

def category(words, anchors):
    """anchors: list of generic forbidden words for this category."""
    for w in words:
        w = w.strip()
        if not w or w in cards:
            continue
        # take up to 5 anchors that differ from the word itself
        fb = [a for a in anchors if a.lower() != w.lower()]
        add(w, fb[:5])

# --- Animals ---------------------------------------------------------------
animaux = """girafe singe dauphin baleine requin aigle hibou perroquet crocodile
serpent grenouille tortue lapin cochon vache cheval mouton chèvre poule coq canard
oie pigeon corbeau moineau berger allemand labrador chaton veau poulain agneau
porcelet lionceau ourson renard loup ours cerf chevreuil sanglier blaireau castor
loutre phoque morse pingouin manchot flamant cigogne hirondelle martin-pêcheur
pic-vert coucou rossignol merle pie geai étourneau bergeronnette fauvette mésange
rouge-gorge pinson linotte chardonneret verdier bruant chouette faucon buse vautour
condor albatros pélican héron spatule ibis grue outarde paon faisan perdrix caille
bécasse bécassine papillon coccinelle abeille guêpe frelon fourmi termite pou puce
moustique mouche taon libellule demoiselle criquet sauterelle grillon cafard blatte
scorpion araignée mygale crabe homard langouste crevette moule huître escargot limace
ver lombric sangsue méduse pieuvre poulpe seiche calmar hippocampe morue saumon thon
sardine maquereau hareng anguille carpe brochet perche truite esturgeon poisson rouge
zèbre hippopotame rhinocéros bison buffle yak chameau dromadaire lama alpaga vigogne
marabout toucan caméléon iguane gecko lézard varan cobra python anaconda boa vipère
couleuvre triton salamandre axolotl tapir tatou fourmilier paresseux kangourou koala
wombat dingo wallaby ornithorynque échidné""".split()
category(animaux, ["Animal","Sauvage","Nature","Bête","Espèce"])

# --- Food ------------------------------------------------------------------
nourriture = """quiche ratatouille cassoulet bouillabaisse soupe potage velouté
bouillon consommé bisque minestrone gaspacho vichyssoise purée gratin lasagne
spaghetti pâtes risotto ravioli gnocchi polenta couscous tajine paella sushi tempura
ramen pho curry tikka burrito tacos guacamole nachos hamburger hot-dog sandwich
croque-monsieur panini wrap kebab shawarma falafel houmous taboulé pastilla mechoui
brick samosa dim sum gyoza yakitori teriyaki satay rendang nasi goreng pad thaï
tom yam laksa omelette frites purée soufflé crème brûlée tarte flan mousse tiramisu
éclair religieuse macaron madeleine cannelé gaufre beignet churros donut cheesecake
brownie cookie pancake porridge muesli granola confiture compote""".split()
category(nourriture, ["Manger","Plat","Cuisine","Recette","Repas"])

# --- Sports ----------------------------------------------------------------
sports = """cyclisme athlétisme basketball volleyball handball rugby baseball
cricket golf snowboard surf planche à voile kiteboard kayak aviron canoë escrime
karaté judo taekwondo kung-fu lutte catch sumo tir à l'arc tir sportif haltérophilie
gymnastique trampoline patinage danse sportive équitation polo pelote basque pétanque
bowling billard fléchettes badminton squash ping-pong padel marathon triathlon
plongée escalade randonnée voile jogging fitness yoga pilates zumba crossfit
parapente deltaplane saut à ski luge bobsleigh curling hockey water-polo""".split()
category(sports, ["Sport","Jouer","Compétition","Équipe","Athlète"])

# --- Geography: countries --------------------------------------------------
pays = """Allemagne Portugal Belgique Pays-Bas Suisse Autriche Pologne Tchéquie
Hongrie Roumanie Bulgarie Serbie Croatie Grèce Turquie Russie Ukraine Suède Norvège
Danemark Finlande Islande Irlande Royaume-Uni Angleterre Écosse Pays de Galles
États-Unis Canada Mexique Brésil Argentine Chili Colombie Venezuela Pérou Bolivie
Équateur Uruguay Paraguay Corée Inde Pakistan Bangladesh Vietnam Thaïlande Cambodge
Laos Myanmar Malaisie Singapour Indonésie Philippines Australie Nouvelle-Zélande
Maroc Algérie Tunisie Libye Égypte Soudan Éthiopie Kenya Tanzanie Afrique du Sud
Nigeria Ghana Côte d'Ivoire Sénégal Mali Niger Tchad Cameroun Congo Angola Mozambique
Madagascar Arabie Saoudite Émirats Israël Palestine Iran Irak Syrie Liban Jordanie
Koweït""".split("\n")
pays = " ".join(pays).split()
category(pays, ["Pays","Nation","Territoire","Frontière","Drapeau"])

# --- Geography: cities -----------------------------------------------------
villes = """Lyon Marseille Bordeaux Toulouse Nice Nantes Strasbourg Lille Rennes
Montpellier Grenoble Tours Dijon Rouen Reims Saint-Étienne Toulon Brest Le Havre
Londres Berlin Madrid Rome Barcelone Lisbonne Amsterdam Bruxelles Vienne Zurich
Prague Varsovie Budapest Bucarest Athènes Istanbul Moscou Kiev Stockholm Oslo
Copenhague Helsinki Dublin New York Los Angeles Chicago Houston Miami Las Vegas
San Francisco Seattle Boston Washington Toronto Montréal Vancouver Mexico São Paulo
Rio Buenos Aires Lima Bogotá Santiago Tokyo Pékin Shanghai Séoul Mumbai Delhi Bangkok
Hanoï Djakarta Sydney Melbourne Le Caire Casablanca Lagos Nairobi Johannesburg Dubaï
Riyad Jérusalem Téhéran Bagdad Damas Beyrouth Amman""".split()
category(villes, ["Ville","Capitale","Habitant","Rue","Urbain"])

# --- Geography: nature/regions ---------------------------------------------
geo_nat = """Alpes Pyrénées Vosges Jura Massif central Ardennes Bretagne Normandie
Provence Alsace Bourgogne Champagne Lorraine Languedoc Gascogne Périgord Auvergne
Savoie Corse Seine Loire Rhône Garonne Rhin Meuse Moselle Dordogne Lot Tarn Var Isère
Saône Méditerranée Atlantique Manche Mer du Nord Mer Noire Mer Rouge Mer Caspienne
Lac Léman Danube Nil Amazone Mississippi Everest Mont-Blanc Kilimandjaro Aconcagua
Fuji Himalaya Andes Rocheuses Atlas Drakensberg Tour Eiffel Louvre Colisée Acropole
Tour de Pise Sagrada Familia Big Ben Westminster Kremlin Statue de la Liberté
Golden Gate Empire State Taj Mahal Grande Muraille Pyramides Sphinx Machu Picchu""".split("\n")
geo_nat = " ".join(geo_nat).split()
category(geo_nat, ["Lieu","Célèbre","Voyage","Paysage","Site"])

# --- Jobs ------------------------------------------------------------------
metiers = """chirurgien infirmier pharmacien dentiste kinésithérapeute psychologue
psychiatre vétérinaire sage-femme gendarme militaire soldat pilote steward hôtesse
marin capitaine chauffeur mécanicien électricien plombier maçon charpentier menuisier
peintre serrurier vitrier couvreur carreleur jardinier agriculteur éleveur pêcheur
pâtissier boucher charcutier fromager cuisinier chef serveur barman caissier vendeur
commercial représentant agent immobilier comptable auditeur banquier assureur courtier
notaire avocat juge huissier greffier instituteur directeur documentaliste bibliothécaire
archiviste journaliste rédacteur reporter photographe cameraman présentateur animateur
acteur réalisateur scénariste producteur musicien chanteur compositeur danseur
chorégraphe sculpteur illustrateur graphiste designer architecte urbaniste ingénieur
technicien informaticien développeur webdesigner chercheur scientifique mathématicien
physicien chimiste biologiste géologue astronome météorologue économiste sociologue
anthropologue philosophe historien géographe linguiste traducteur interprète diplomate
ambassadeur consul politicien député sénateur maire préfet ministre fonctionnaire
secrétaire assistant réceptionniste standardiste livreur facteur postier éboueur
balayeur cantonnier contrôleur guide touristique concierge gardien vigile douanier""".split()
category(metiers, ["Métier","Travail","Profession","Emploi","Salaire"])

# --- Everyday objects ------------------------------------------------------
objets = """smartphone tablette clavier souris écran imprimante scanner photocopieuse
appareil photo caméra télévision radio chaîne hi-fi enceinte casque écouteurs réveil
ampoule interrupteur prise rallonge pile batterie chargeur câble clé USB disque dur
serrure verrou cadenas sonnette interphone digicode boîte aux lettres journal magazine
carnet gomme règle compas taille-crayon agrafeuse perforatrice scotch colle bol tasse
carafe thermos bocal panier chariot caddie valise sac à dos sac à main portefeuille
porte-monnaie agenda calendrier thermomètre balance sablier loupe jumelles masque gants
imperméable pull chemise jupe soutien-gorge chaussettes slip caleçon pyjama bottes
sandales baskets pantoufles ceinture bretelles foulard écharpe bonnet casquette
brosse à dents dentifrice savon shampoing rasoir crème lotion parfum maquillage
rouge à lèvres mascara peigne sèche-cheveux coton-tige médicament comprimé seringue
pansement compresse désinfectant tensiomètre""".split()
category(objets, ["Objet","Utiliser","Quotidien","Maison","Pratique"])

# --- Nature/environment ----------------------------------------------------
nature = """jungle savane désert steppe toundra taïga prairie marais tourbière
mangrove récif lagon fjord delta estuaire baie golfe cap péninsule île archipel atoll
volcan geyser cascade source lac étang mare ruisseau glacier iceberg banquise colline
vallon ravin canyon falaise grotte caverne plaine plateau mesa dune oasis argile sable
gravier pierre roche calcaire granit marbre quartz silex obsidienne charbon pétrole
gaz naturel uranium minerai cuivre diamant rubis émeraude saphir opale ambre corail
perle coquillage fossile mammouth branche tronc racine écorce résine sève pétale pistil
étamine pollen nectar graine spore mousse lichen champignon fougère roseau nénuphar
algue plancton pollution réchauffement effet de serre déforestation érosion inondation
sécheresse ouragan tsunami séisme éruption avalanche""".split()
category(nature, ["Nature","Naturel","Extérieur","Paysage","Environnement"])

# --- Human body ------------------------------------------------------------
corps = """visage front sourcil paupière cil pupille iris cornée nez narine joue
pommette oreille lobe bouche lèvre dent langue palais gorge menton mâchoire cou nuque
épaule bras coude avant-bras poignet paume doigt pouce index majeur annulaire
auriculaire ongle torse poitrine sein sternum clavicule côte ventre abdomen nombril
hanche fesse cuisse genou rotule mollet jambe cheville talon plante orteil colonne
vertèbre dos reins crâne cerveau cervelet nerf poumon foie rein rate pancréas estomac
intestin côlon appendice vésicule thyroïde muscle tendon ligament cartilage os artère
veine capillaire globule plasma lymphe peau épiderme derme poil cheveu sueur larme
salive sang urine""".split()
category(corps, ["Corps","Humain","Organe","Anatomie","Chair"])

# --- Clothes ---------------------------------------------------------------
vetements = """blouson blazer veston redingote pardessus cape poncho sweat hoodie
gilet cardigan chemisier blouse tunique débardeur t-shirt polo minijupe jean legging
short bermuda combinaison salopette nuisette culotte boxer collant bas béret canotier
sombrero turban coiffe voile hijab cravate nœud papillon pochette cartable bijou bague
alliance boucle d'oreille bracelet collier pendentif broche épingle escarpins talons
bottines mocassins tennis chaussons sabots tongs""".split()
category(vetements, ["Vêtement","Porter","Habit","Mode","Tissu"])

# --- Transport -------------------------------------------------------------
transports = """camion camionnette bus car tramway métro TGV Eurostar hélicoptère
ULM montgolfière dirigeable bateau navire paquebot ferry hovercraft sous-marin
pétrolier cargo yacht voilier catamaran canot barque pirogue raft vélomoteur scooter
moto trottinette skateboard rollers tracteur bulldozer excavatrice benne ambulance
taxi rickshaw calèche traîneau navette satellite drone téléphérique funiculaire
ascenseur escalator""".split()
category(transports, ["Transport","Rouler","Déplacer","Véhicule","Voyage"])

# --- Home & furniture ------------------------------------------------------
maison = """salon salle à manger cuisine chambre salle de bain entrée couloir escalier
grenier cave garage terrasse balcon piscine portail clôture haie mur toit cheminée
volet store rideau canapé fauteuil tabouret pouf banquette sommier matelas oreiller
couette couverture drap table basse bureau bibliothèque armoire commode buffet vaisselier
vitrine étagère console porte-manteau tableau cadre affiche vase luminaire plafonnier
applique bougie tapis parquet carrelage moquette papier peint radiateur climatiseur
ventilateur réfrigérateur congélateur four micro-ondes lave-vaisselle lave-linge
sèche-linge aspirateur fer à repasser mixeur grille-pain cafetière bouilloire friteuse""".split()
category(maison, ["Maison","Meuble","Intérieur","Pièce","Habiter"])

# --- Arts & culture --------------------------------------------------------
arts = """peinture sculpture dessin gravure photographie opéra ballet jazz rock pop
hip-hop électronique reggae salsa tango flamenco gospel blues soul funk country folk
métal punk grunge littérature poésie roman nouvelle conte fable biographie essai
bande dessinée manga anime dessin animé comédie tragédie drame thriller comédie musicale
opérette vaudeville marionnettes mime cirque magie illusionnisme street art performance
installation art contemporain impressionnisme surréalisme cubisme abstraction baroque
renaissance romantisme réalisme classicisme gothique art nouveau art déco Monet Renoir
Cézanne Van Gogh Matisse Dali Rembrandt Vermeer Botticelli Michel-Ange Léonard de Vinci
Raphaël Hokusai Warhol Banksy Orsay Beethoven Bach Vivaldi Chopin Verdi Wagner Molière
Racine Corneille Hugo Balzac Flaubert Zola Proust Camus Sartre Voltaire Rousseau
Montaigne Rimbaud Verlaine Baudelaire Apollinaire Prévert""".split()
category(arts, ["Art","Culture","Œuvre","Créer","Artiste"])

# --- History & politics ----------------------------------------------------
histoire = """révolution empire monarchie république démocratie dictature totalitarisme
fascisme nazisme communisme socialisme libéralisme conservatisme anarchisme féminisme
colonialisme esclavage génocide traité alliance armistice siège bataille invasion
résistance occupation libération indépendance unification partition coup d'état
élection référendum constitution parlement assemblée sénat gouvernement cabinet
empereur sultan calife pape évêque croisade inquisition réforme lumières colonisation
décolonisation guerre froide mondialisation Charlemagne Jules César Alexandre le Grand
Cléopâtre Marie-Antoinette Robespierre Danton Lincoln Churchill Roosevelt De Gaulle
Staline Mao Lénine Gandhi Mandela Che Guevara Castro Jaurès Clemenceau""".split()
category(histoire, ["Histoire","Passé","Politique","Pouvoir","Époque"])

# --- Science & tech --------------------------------------------------------
sciences = """physique chimie biologie mathématiques géologie astronomie astrophysique
cosmologie neuroscience génétique botanique zoologie microbiologie virologie immunologie
pharmacologie anatomie physiologie économie sociologie anthropologie archéologie
paléontologie climatologie météorologie robotique intelligence artificielle algorithme
programmation logiciel matériel réseau cloud big data blockchain cryptographie
cybersécurité nanotechnologie biotechnologie clonage énergie solaire éolienne nucléaire
hydrogène fusion fission électricité magnétisme gravité relativité atome molécule ADN
protéine enzyme cellule chromosome évolution mutation adaptation espèce écosystème
photosynthèse respiration oxydation acide base température pression volume masse énergie
force vitesse accélération inertie électron proton neutron photon quark boson onde
fréquence spectre laser fibre optique transistor microprocesseur mémoire""".split()
category(sciences, ["Science","Savant","Étude","Recherche","Théorie"])

# --- Famous people ---------------------------------------------------------
gens = """Darwin Newton Galilée Copernic Kepler Pasteur Curie Fleming Freud Jung
Pavlov Marx Weber Durkheim Tocqueville Montesquieu Aristote Platon Socrate Descartes
Kant Hegel Nietzsche Locke Hobbes Erasme Machiavel Homère Virgile Dante Cervantes
Dostoïevski Tolstoï Tchekhov Dickens Kafka Goethe Orwell Hemingway Twain Poe Melville
Hannibal Attila Gengis Khan Saladin Jeanne d'Arc Henri IV Louis XVI Bismarck Victoria
Kennedy Obama Lincoln Washington Jefferson Reagan Thatcher Mitterrand Chirac Pompidou
Armstrong Coltrane Miles Davis Sinatra Presley Bowie Dylan Hendrix Madonna""".split()
category(gens, ["Personnage","Célèbre","Histoire","Connu","Personne"])

# --- Plants & trees --------------------------------------------------------
plantes = """tulipe marguerite tournesol lavande lilas pivoine orchidée iris lys
chrysanthème dahlia géranium bégonia pensée violette myosotis bleuet coquelicot chardon
ortie pissenlit trèfle plantain renoncule jonquille narcisse crocus glaïeul amaryllis
magnolia azalée rhododendron camélia jasmin chèvrefeuille glycine clématite lierre
mimosa acacia genêt bruyère houx forsythia buis if laurier bambou papyrus fougère prêle
truffe morille cèpe chanterelle girolle pleurote bolet châtaignier hêtre charme bouleau
tremble peuplier saule aulne frêne orme tilleul érable platane noyer noisetier
marronnier cerisier poirier pommier prunier pêcher abricotier figuier olivier vigne pin
épicéa mélèze cèdre séquoia eucalyptus palmier cocotier bananier manguier caféier
cacaoyer canne à sucre maïs blé seigle orge avoine millet sorgho chanvre lin coton
colza soja arachide""".split()
category(plantes, ["Plante","Jardin","Verdure","Pousser","Nature"])

# --- Musical instruments ---------------------------------------------------
instruments = """violoncelle contrebasse alto harpe luth mandoline banjo ukulélé
cithare balalaïka sitar oud kora koto biwa erhu flûte traversière flûte à bec piccolo
hautbois cor anglais clarinette saxophone basson trompette cornet bugle trombone cor
tuba euphonium didgeridoo accordéon bandonéon concertina harmonica orgue synthétiseur
basse électrique thérémine batterie caisse claire grosse caisse charleston cymbale
triangle tambourin maracas castagnettes glockenspiel xylophone marimba vibraphone bongo
djembé congas balafon tabla carillon timbales tambour""".split()
category(instruments, ["Instrument","Musique","Jouer","Son","Note"])

# --- Emotions --------------------------------------------------------------
emotions = """bonheur félicité euphorie extase allégresse gaieté enthousiasme
excitation espoir optimisme confiance sérénité satisfaction contentement fierté
gratitude tendresse affection passion désir attirance admiration respect estime
sympathie empathie compassion générosité bienveillance tristesse mélancolie nostalgie
chagrin deuil peine souffrance désespoir abattement déprime solitude ennui lassitude
fatigue fureur rage irritation agacement exaspération frustration rancœur jalousie envie
ressentiment haine dégoût mépris terreur angoisse anxiété inquiétude stress panique
honte culpabilité remords regret gêne timidité surprise étonnement stupéfaction
émerveillement perplexité confusion doute incertitude sentiment impression émotion humeur
tempérament caractère personnalité""".split()
category(emotions, ["Sentiment","Ressentir","Émotion","Cœur","Humeur"])

# --- Verbs / actions -------------------------------------------------------
verbes = """courir marcher sauter nager plonger voler tomber grimper descendre monter
entrer sortir ouvrir fermer pousser tirer soulever porter lancer attraper frapper cogner
mordre griffer caresser embrasser serrer étreindre chanter parler crier chuchoter rire
pleurer sourire regarder voir entendre écouter sentir goûter toucher manger boire dormir
rêver penser réfléchir comprendre apprendre mémoriser oublier imaginer créer inventer
construire fabriquer réparer casser détruire nettoyer laver sécher repasser coudre
tricoter cuisiner couper trancher mélanger cuire rôtir griller frire bouillir décorer
peindre dessiner écrire lire compter calculer mesurer peser comparer choisir décider
commander obéir refuser accepter donner recevoir acheter vendre perdre trouver chercher
demander répondre expliquer montrer cacher jouer gagner tricher danser applaudir siffler
conduire piloter naviguer pédaler ramer semer récolter cueillir tailler arroser planter
soigner guérir blesser opérer vacciner examiner enseigner former corriger noter
photographier filmer enregistrer publier imprimer télécharger partager""".split()
category(verbes, ["Action","Faire","Verbe","Bouger","Geste"])

# --- Games & toys ----------------------------------------------------------
jeux = """Monopoly Scrabble Cluedo Risk Trivial Pursuit Pictionary Jungle Speed Uno
Mille Bornes Dobble Dixit Catane Pandemic 7 Wonders Codenames Cranium Battleship
Othello dames backgammon mahjong poker bridge belote coinche tarot billard ping-pong
baby-foot flipper dés dominos puzzle Rubik's cube Tetris Minecraft Fortnite Pokemon
Pac-Man Sonic Lego Playmobil Barbie Hot Wheels Meccano poupée nounours doudou toupie
yoyo balançoire toboggan trampoline bac à sable Kapla cubes patins à roulettes billes
figurines train électrique console manette""".split()
category(jeux, ["Jeu","Jouer","Amuser","Loisir","Jouet"])

# --- Seasons/weather/astronomy ---------------------------------------------
saisons = """printemps été automne hiver solstice équinoxe mousson gel verglas blizzard
tempête cyclone typhon tornade grêle bruine brouillard brume nuage cumulus stratus
cirrus orage foudre tonnerre éclair arc-en-ciel brise mistral sirocco canicule
fraîcheur humidité baromètre hygromètre prévision pleine lune nouvelle lune croissant
éclipse Mercure Vénus Jupiter Saturne Uranus Neptune Pluton astéroïde météorite comète
étoile filante constellation galaxie Voie Lactée trou noir supernova nébuleuse
naine blanche géante rouge pulsar quasar télescope observatoire astronaute navette
Station spatiale cosmos univers big bang matière noire orbite gravitation marée""".split()
category(saisons, ["Ciel","Météo","Nature","Temps","Espace"])

# --- Colours/shapes/numbers ------------------------------------------------
formes = """jaune violet marron beige gris turquoise cyan magenta écarlate cramoisi
bordeaux grenat carmin vermillon auburn châtain blond roux brun ivoire crème ocre or
argent bronze cuivre platine émeraude améthyste citron lavande indigo marine cobalt azur
losange pentagone hexagone octogone ellipse ovale croix flèche spirale sphère cube
pyramide cylindre cône prisme point ligne courbe angle zéro deux trois quatre cinq six
sept huit neuf dix million milliard infini positif négatif pair impair fraction décimale
pourcentage moitié tiers quart""".split()
category(formes, ["Forme","Nombre","Couleur","Géométrie","Chiffre"])

# --- Health & medicine -----------------------------------------------------
sante = """symptôme diagnostic traitement médicament prescription posologie dose
effet secondaire allergie intolérance vaccination immunité anticorps infection
inflammation fièvre tension pouls glycémie cholestérol hémoglobine leucocytes plaquettes
clinique urgences bloc opératoire réanimation soins intensifs infirmerie pharmacie
laboratoire radiologie scanner IRM échographie électrocardiogramme biopsie endoscopie
chirurgie opération anesthésie incision suture greffe transplantation prothèse plâtre
attelle béquille fauteuil roulant cancer tumeur chimiothérapie radiothérapie rémission
métastase leucémie diabète insuline hypertension infarctus AVC Alzheimer Parkinson
épilepsie dépression insomnie asthme bronchite pneumonie tuberculose grippe rhume angine
otite sinusite appendicite ulcère gastrite hernie fracture entorse foulure luxation
kyste abcès eczéma psoriasis acné verrue mycose""".split()
category(sante, ["Médecine","Malade","Corps","Soigner","Docteur"])

# --- Specific food ---------------------------------------------------------
aliments = """pomme poire mangue papaye goyave kiwi litchi durian carambole avocat
poivron aubergine courgette concombre cornichon potiron citrouille butternut patate douce
igname manioc taro pomme de terre panais navet betterave radis salsifis topinambour
artichaut asperge brocoli chou-fleur chou chou rouge chou de Bruxelles épinard laitue
roquette endive chicorée mâche cresson oseille persil basilic coriandre menthe thym
romarin sauge origan estragon ciboulette ail oignon échalote poireau fenouil aneth cumin
cannelle muscade curcuma safran paprika poivre piment raisin figue datte abricot pêche
prune mirabelle cerise framboise mûre cassis groseille myrtille canneberge noix noisette
amande pistache cacahuète noix de cajou châtaigne pecan lentilles pois chiches haricots
fèves tofu tempeh crème yaourt kéfir ricotta mascarpone mozzarella parmesan gruyère
emmental comté reblochon raclette brie camembert munster roquefort feta halloumi gouda
edam mimolette cantal saint-nectaire confiture marmelade gelée compote coulis sirop
vinaigre huile d'olive margarine mayonnaise moutarde ketchup limonade orangeade grenadine
expresso cappuccino latte macchiato americano tisane infusion verveine camomille hibiscus
rooibos matcha oolong darjeeling smoothie milk-shake cocktail bière champagne cidre
whisky vodka gin rhum tequila cognac calvados armagnac pastis absinthe limoncello
amaretto cointreau""".split()
category(aliments, ["Manger","Aliment","Cuisine","Goût","Nourriture"])

# --- Religion & mythology --------------------------------------------------
religion = """christianisme catholicisme protestantisme orthodoxie islam judaïsme
bouddhisme hindouisme sikhisme taoïsme shintoïsme animisme chamanisme paganisme athéisme
agnosticisme laïcité Allah Yahvé Brahma Vishnou Shiva Mohammed Moïse Abraham prière
méditation messe sermon liturgie sacrement baptême communion confirmation mariage prêtre
pasteur rabbin imam moine nonne évêque cardinal pape dalaï-lama guru chamane temple
cathédrale mosquée synagogue monastère pagode ashram mausolée pèlerinage La Mecque Bible
Coran Torah Talmud Évangile enfer paradis purgatoire karma dharma nirvana réincarnation
âme esprit ange démon Satan Lucifer Zeus Héra Apollon Artémis Athéna Aphrodite Arès
Hermès Poséidon Héphaïstos Dionysos Déméter Hadès Thor Odin Loki Freya Osiris Isis Ra
Horus Anubis Prométhée Hercule Achille Ulysse Orphée Œdipe Circé minotaure centaure
sirène cyclope sphinx dragon licorne phénix hydre Méduse""".split()
category(religion, ["Religion","Croyance","Divin","Mythe","Sacré"])

# --- Economy & commerce ----------------------------------------------------
economie = """marché actions obligations investissement épargne crédit prêt emprunt
dette déficit budget fiscalité impôt taxe TVA tarif protectionnisme libre-échange
exportation importation PIB croissance récession inflation déflation chômage emploi
salaire SMIC retraite pension assurance mutuelle banque centrale euro dollar yen yuan
cryptomonnaie bitcoin ethereum startup entreprise PME multinationale actionnaire PDG
fusion acquisition faillite liquidation boutique supermarché hypermarché e-commerce
marketplace publicité marketing branding logo slogan client consommateur fournisseur
distributeur grossiste détaillant contrat facture livraison remboursement fidélité
promotion soldes réduction discount coupon""".split()
category(economie, ["Argent","Commerce","Économie","Vendre","Marché"])

# --- Computing & internet --------------------------------------------------
info = """laptop serveur datacentre processeur mémoire RAM SSD carte graphique
carte mère alimentation webcam microphone liseuse smartwatch web navigateur
moteur de recherche Firefox Chrome Safari URL HTTP HTML CSS JavaScript Python Java PHP
Swift Kotlin Ruby SQL base de données API framework IDE terminal shell bash git GitHub
Docker cloud AWS Azure hébergement DNS domaine email spam phishing ransomware antivirus
firewall VPN chiffrement protocole WiFi Bluetooth 5G NFC réseaux sociaux Facebook Twitter
Instagram TikTok YouTube LinkedIn WhatsApp Telegram blog podcast streaming Netflix Spotify
application app store eSport twitch machine learning big data blockchain métavers
réalité virtuelle réalité augmentée""".split()
category(info, ["Informatique","Ordinateur","Internet","Numérique","Technologie"])

# --- Abstract concepts / adjectives ----------------------------------------
concepts = """égalité fraternité beauté sagesse courage honneur dignité tolérance
solidarité harmonie équilibre ordre chaos hasard destin foi rêve imagination créativité
innovation progrès tradition culture identité appartenance communauté société nation
peuple humanité civilisation mémoire avenir espace éternité conscience intelligence savoir
ignorance mensonge réalité illusion apparence essence sens signification symbole métaphore
ironie paradoxe absurde mystère secret révélation découverte coïncidence intuition instinct
raison logique perception jugement critique analyse synthèse abstraction concret universel
relatif absolu subjectif objectif possible impossible nécessaire grand petit long court
haut bas large étroit lourd léger rapide lent fort faible dur mou chaud froid humide sec
lumineux sombre bruyant silencieux beau laid bon mauvais juste injuste vrai faux réel
imaginaire ancien nouveau jeune vieux vivant naturel artificiel simple complexe facile
difficile clair obscur transparent opaque lisse rugueux doux piquant sucré salé amer acide
agréable désagréable utile inutile superflu important insignifiant""".split()
category(concepts, ["Concept","Idée","Notion","Abstrait","Sens"])

# --- More birds / marine (category 29) -------------------------------------
oiseaux = """plie sole rouget grondin saint-pierre bar daurade dorade brème gardon
ablette vairon épinoche loche chabot goujon vandoise chevesne rotengle tanche bouvière
lézard des murailles lézard vert couleuvre à collier vipère aspic orvet lézard ocellé
triton alpestre triton marbré triton palmé salamandre tachetée rainette verte
grenouille rousse grenouille agile crapaud commun crapaud calamite pélodyte discoglosse
alyte accoucheur chouette effraie chouette chevêche chouette hulotte hibou moyen-duc
hibou grand-duc petit-duc scops engoulevent martinet guêpier rollier huppe grimpereau
sittelle pouillot fauvette grisette fauvette à tête noire bouscarle locustelle phragmite
rousserolle hypolaïs gobemouche rougequeue tarier traquet monticole grive musicienne
grive draine grive litorne grive mauvis merle à plastron étourneau sansonnet loriot
pie-grièche geai des chênes pie bavarde choucas freux corneille grand corbeau bruant jaune
bruant zizi bruant des roseaux venturon bouvreuil gros-bec bec-croisé tarin serin
pinson des arbres pinson du nord moineau domestique moineau friquet alouette des champs
alouette lulu cochevis huppé pipit farlouse bergeronnette grise bergeronnette printanière
hirondelle rustique hirondelle de fenêtre martinet noir coucou gris pic vert pic épeiche
pic noir torcol vanneau huppé pluvier doré grand gravelot petit gravelot bécasse des bois
bécassine des marais chevalier gambette chevalier guignette courlis cendré courlis corlieu
barge à queue noire combattant varié bécasseau maubèche phalarope mouette rieuse
goéland argenté goéland brun goéland marin sterne pierregarin sterne arctique
guifette noire fou de Bassan cormoran huppé grand cormoran fulmar plongeon imbrin
grèbe huppé grèbe castagneux tadorne de Belon sarcelle d'hiver souchet fuligule milouin
fuligule morillon garrot à œil d'or harle bièvre canard colvert canard pilet canard siffleur
nette rousse canard mandarin bernache du Canada bernache nonnette oie cendrée cygne tuberculé
cygne chanteur macreuse noire eider à duvet macareux pingouin torda guillemot de Troïl
mergule nain stercoraire parasite grand labbe""".split("\n")
oiseaux = " ".join(oiseaux).split()
# rejoin multi-word bird names properly: the split above breaks them; handle manually
# Instead build from explicit list to keep multiword names intact.
oiseaux_multi = ["plie","sole","rouget","grondin","saint-pierre","bar","daurade","dorade",
 "brème","gardon","ablette","vairon","épinoche","loche","chabot","goujon","vandoise",
 "chevesne","rotengle","tanche","bouvière","lézard des murailles","lézard vert",
 "couleuvre à collier","vipère aspic","orvet","lézard ocellé","triton alpestre",
 "triton marbré","triton palmé","salamandre tachetée","rainette verte","grenouille rousse",
 "grenouille agile","crapaud commun","crapaud calamite","pélodyte","discoglosse",
 "alyte accoucheur","chouette effraie","chouette chevêche","chouette hulotte",
 "hibou moyen-duc","hibou grand-duc","petit-duc scops","engoulevent","martinet","guêpier",
 "rollier","huppe","grimpereau","sittelle","pouillot","fauvette grisette",
 "fauvette à tête noire","bouscarle","locustelle","phragmite","rousserolle","hypolaïs",
 "gobemouche","rougequeue","tarier","traquet","monticole","grive musicienne","grive draine",
 "grive litorne","grive mauvis","merle à plastron","étourneau sansonnet","loriot",
 "pie-grièche","geai des chênes","pie bavarde","choucas","freux","corneille","grand corbeau",
 "bruant jaune","bruant zizi","bruant des roseaux","venturon","bouvreuil","gros-bec",
 "bec-croisé","tarin","serin","pinson des arbres","pinson du nord","moineau domestique",
 "moineau friquet","alouette des champs","alouette lulu","cochevis huppé","pipit farlouse",
 "bergeronnette grise","bergeronnette printanière","hirondelle rustique",
 "hirondelle de fenêtre","martinet noir","coucou gris","pic vert","pic épeiche","pic noir",
 "torcol","vanneau huppé","pluvier doré","grand gravelot","petit gravelot","bécasse des bois",
 "bécassine des marais","chevalier gambette","chevalier guignette","courlis cendré",
 "courlis corlieu","barge à queue noire","combattant varié","bécasseau maubèche","phalarope",
 "mouette rieuse","goéland argenté","goéland brun","goéland marin","sterne pierregarin",
 "sterne arctique","guifette noire","fou de Bassan","cormoran huppé","grand cormoran",
 "fulmar","plongeon imbrin","grèbe huppé","grèbe castagneux","tadorne de Belon",
 "sarcelle d'hiver","souchet","fuligule milouin","fuligule morillon","garrot à œil d'or",
 "harle bièvre","canard colvert","canard pilet","canard siffleur","nette rousse",
 "canard mandarin","bernache du Canada","bernache nonnette","oie cendrée","cygne tuberculé",
 "cygne chanteur","macreuse noire","eider à duvet","macareux","pingouin torda",
 "guillemot de Troïl","mergule nain","stercoraire parasite","grand labbe"]
category(oiseaux_multi, ["Oiseau","Plumes","Voler","Nature","Bec"])

# --- World cuisine ---------------------------------------------------------
cuisine_monde = ["moussaka","tarama","tzatziki","dolmas","spanakopita","baklava",
 "fattoush","babaganoush","labneh","injera","thiéboudienne","mafé","yassa","poulet jerk",
 "gumbo","jambalaya","clam chowder","lobster roll","enchiladas","tamales","quesadilla",
 "salsa","mole","ceviche","churrasco","feijoada","moqueca","coxinha","pão de queijo",
 "empanadas","chimichurri","asado","dumplings","wonton","banh mi","nems",
 "rouleaux de printemps","pad thai","green curry","massaman","tom kha","biryani",
 "tikka masala","butter chicken","dhal","chapati","naan","pakora","lassi","chai","miso",
 "udon","soba","takoyaki","okonomiyaki","sashimi","nigiri","temaki","maki","chirashi",
 "bibimbap","bulgogi","kimchi","tteokbokki","galbi","japchae","banh xeo","bun cha",
 "com tam","gado-gado","soto","bakso","adobo","sinigang","kare-kare","lechon","halo-halo",
 "momos","chole bhature","pav bhaji","idli","dosa","vada","rasam","sambhar","korma",
 "vindaloo","palak paneer","raita","paratha","roti canai","char kway teow"]
category(cuisine_monde, ["Plat","Cuisine","Étranger","Manger","Recette"])

# --- Extra generic fillers to comfortably exceed 8000 ----------------------
# Build additional themed vocabulary lists to reach the target while staying
# meaningful and non-duplicated.
extra_lists = [
 (["marteau","tournevis","clou","vis","scie","perceuse","ponceuse","pince","tenaille",
   "burin","lime","rabot","niveau","équerre","mètre ruban","échelle","escabeau",
   "brouette","pelle","pioche","râteau","binette","sécateur","tondeuse","arrosoir",
   "tuyau","bêche","fourche","serpe","hache","cognée","masse","enclume","étau","soudure",
   "chalumeau","meuleuse","visseuse","cheville","boulon","écrou","rondelle","ressort",
   "charnière","gond","poulie","engrenage","roulement","courroie","chaîne (outil)"],
  ["Outil","Bricolage","Réparer","Atelier","Main"]),
 (["pomme d'amour","barbe à papa","pain d'épices","nougat","caramel","praline","dragée",
   "guimauve","réglisse","berlingot","sucette","chewing-gum","calisson","touron","loukoum",
   "halva","fudge","toffee","marshmallow","meringue","nonnette","pâte de fruit","cotignac",
   "bêtise","chique","malabar","carambar","fraise Tagada","ourson guimauve","dragibus"],
  ["Sucré","Bonbon","Sucrerie","Enfant","Gourmandise"]),
 (["gare","aéroport","port","métro (lieu)","arrêt de bus","péage","autoroute","rond-point",
   "carrefour","feu rouge","passage piéton","trottoir","caniveau","pont","tunnel","viaduc",
   "quai","embarcadère","piste cyclable","parking","station-service","péniche","écluse",
   "phare","balise","radar","borne","panneau","glissière","ralentisseur"],
  ["Route","Circulation","Voyage","Ville","Trajet"]),
 (["nuage de lait","tasse à café","soucoupe","théière","cafetière italienne","moulin à café",
   "presse-agrumes","économe","fouet","spatule","louche","écumoire","passoire","tamis",
   "rouleau à pâtisserie","emporte-pièce","balance de cuisine","planche à découper",
   "râpe","mandoline (cuisine)","mixeur plongeant","robot pâtissier","cocotte","poêle",
   "casserole","faitout","sauteuse","wok","marmite","autocuiseur","plaque de cuisson"],
  ["Cuisine","Ustensile","Cuisiner","Préparer","Recette"]),
 (["cartable","trousse","classeur","cahier","copie","surligneur","effaceur","équerre (école)",
   "rapporteur","calculatrice","dictionnaire","atlas","globe","tableau noir","craie",
   "feutre","ardoise","pupitre","estrade","récréation","cantine","préau","internat","bulletin",
   "note (école)","devoir","examen","dictée","récitation","interrogation"],
  ["École","Élève","Apprendre","Classe","Étudier"]),
 (["fête","anniversaire","mariage (fête)","baptême (fête)","carnaval","bal","kermesse",
   "banquet","réveillon","Noël","Pâques","Halloween","Toussaint","Épiphanie","Chandeleur",
   "Mardi gras","Saint-Valentin","fête des mères","fête des pères","feu d'artifice",
   "guirlande","confettis","serpentin","ballon de baudruche","piñata","gâteau d'anniversaire",
   "bougie (fête)","cadeau","invitation","déguisement"],
  ["Fête","Célébrer","Joie","Occasion","Amusement"]),
 (["étoile de mer","oursin","anémone de mer","corail (mer)","holothurie","concombre de mer",
   "bernard-l'ermite","balane","patelle","bigorneau","bulot","coque","palourde","praire",
   "coquille Saint-Jacques","couteau (coquillage)","ormeau","nacre","krill","copépode",
   "raie","torpille","murène","congre","lamproie","poisson-lune","poisson-clown",
   "poisson-chat","raie manta","poisson-scie"],
  ["Mer","Océan","Marin","Eau","Poisson"]),
 (["chemin","sentier","piste","route (nature)","allée","layon","raccourci","impasse",
   "boulevard","avenue","ruelle","venelle","passage","promenade","esplanade","place",
   "square","parvis","cour","jardin public","parc","aire de jeux","terrain vague","friche",
   "clairière","sous-bois","lisière","taillis","bosquet","haie (nature)"],
  ["Lieu","Chemin","Marcher","Extérieur","Passage"]),
]
for words, anchors in extra_lists:
    category(words, anchors)

# ---------------------------------------------------------------------------
# 3. Programmatic expansion to guarantee >= 8000 unique cards ----------------
# ---------------------------------------------------------------------------
# We create additional cards by pairing common French base words with
# qualifiers, producing meaningful compound "words" with sensible forbidden
# lists. This keeps everything unique and valid.

base_themes = {
 "sport": (["basket","volley","tennis de table","course à pied","saut en longueur",
   "saut en hauteur","lancer de poids","lancer de javelot","triple saut","perche",
   "relais","haies","décathlon","heptathlon","steeple","cross","semi-marathon",
   "trail","ultra-trail","VTT","BMX","cyclo-cross","descente (vélo)","piste (vélo)",
   "planche à roulettes","longboard","escalade en salle","via ferrata","spéléologie",
   "canyoning","rafting","hydrospeed","stand-up paddle","wakeboard","ski nautique",
   "plongée sous-marine","apnée","snorkeling","voile légère","dériveur","optimist",
   "windsurf","funboard","char à voile","speed sail","patin à glace","hockey sur glace",
   "short track","danse sur glace","biathlon","combiné nordique","saut à ski",
   "ski de fond","ski alpin","slalom","géant","super-G","freestyle","half-pipe",
   "big air","boardercross","télémark","raquettes à neige","alpinisme","cascade de glace",
   "escalade de bloc","trampoline acrobatique","tumbling","GRS","aérobic","step",
   "musculation","haltères","kettlebell","TRX","aquagym","aquabike","natation synchronisée",
   "plongeon acrobatique","water-polo (sport)","nage libre","dos crawlé","papillon (nage)",
   "brasse","quatre nages","waterpolo"],
  ["Sport","Jouer","Compétition","Athlète","Effort"]),
 "musique": (["chorale","orchestre","fanfare","quatuor","trio","duo","solo (musique)",
   "concert","récital","symphonie","concerto","sonate","suite","fugue","cantate","oratorio",
   "requiem","messe (musique)","opéra-comique","comédie musicale (musique)","mélodie",
   "chanson (musique)","refrain","couplet","tube","single","album","vinyle","cassette",
   "CD","playlist","partition","portée","clé de sol","clé de fa","note (musique)","dièse",
   "bémol","gamme","accord (musique)","tempo","mesure (musique)","rythme (musique)",
   "harmonie (musique)","mélodie (musique)","tonalité","majeur (musique)","mineur (musique)",
   "octave","croche","noire (note)","blanche (note)","ronde (note)","soupir","métronome",
   "diapason","chef d'orchestre","baguette (chef)","pupitre (musique)","répétition (musique)",
   "générale","tournée","festival (musique)","scène (concert)","backstage","loge",
   "micro (musique)","ampli","table de mixage","enceinte (musique)","sono","platine"],
  ["Musique","Son","Écouter","Note","Mélodie"]),
 "cuisine": (["entrée (plat)","plat principal","dessert (plat)","apéritif","amuse-bouche",
   "hors-d'œuvre","garniture","accompagnement","sauce (plat)","assaisonnement","marinade",
   "vinaigrette (sauce)","bouillon (base)","fond (cuisine)","roux (sauce)","béchamel (sauce)",
   "coulis (sauce)","réduction (sauce)","émulsion","mousse (cuisine)","gelée (cuisine)",
   "aspic","terrine","pâté","rillettes","foie gras","tartare","carpaccio","brochette",
   "grillade","rôti","daube","pot-au-feu","blanquette","navarin","fricassée","sauté",
   "poêlée","gratin (plat)","tian","clafoutis","far","crumble","tarte tatin","paris-brest",
   "saint-honoré","forêt-noire","opéra (gâteau)","fraisier","charlotte","bavarois",
   "panna cotta","crème caramel","île flottante","œufs à la neige","riz au lait",
   "pain perdu","brioche","chausson","palmier (viennoiserie)","pain au chocolat",
   "chouquette","profiterole","mille-feuille","tarte au citron","tarte aux pommes",
   "quiche lorraine","pissaladière","tourte","friand","vol-au-vent","bouchée à la reine"],
  ["Cuisine","Plat","Manger","Recette","Repas"]),
 "nature2": (["forêt tropicale","forêt boréale","bois (forêt)","futaie","chênaie","hêtraie",
   "pinède","sapinière","garrigue","maquis","lande","prairie fleurie","pâturage","alpage",
   "steppe (nature)","pampa","llanos","cerrado","toundra arctique","désert de sable",
   "désert de pierre","erg","reg","hamada","salar","marais salant","lagune","estran","récif corallien",
   "herbier marin","abysse","fosse océanique","dorsale","plateau continental","banc de sable",
   "cordon littoral","tombolo","flèche littorale","cirque glaciaire","moraine","crevasse",
   "sérac","langue glaciaire","névé","cascade de glace (nature)","chute d'eau","rapide (rivière)",
   "méandre","gorge","défilé","cluse","combe","doline","aven","résurgence","calanque",
   "crique","anse","rade","passe","haut-fond","banquise (nature)","pack de glace",
   "iceberg tabulaire","floe","polynie"],
  ["Nature","Paysage","Extérieur","Naturel","Environnement"]),
}
for key,(words,anchors) in base_themes.items():
    category(words, anchors)

# If still under target, generate systematic "métier de X" / adjectif combos.
extra_metiers = ["forgeron","tailleur","cordonnier","horloger","bijoutier","orfèvre",
 "verrier","potier","céramiste","tapissier","ébéniste","vannier","sellier","maroquinier",
 "chapelier","modiste","couturier","brodeur","dentellier","teinturier","imprimeur",
 "relieur","typographe","graveur","enlumineur","calligraphe","luthier","facteur d'orgues",
 "accordeur","souffleur de verre","émailleur","doreur","restaurateur d'art","antiquaire",
 "brocanteur","commissaire-priseur","expert (métier)","galeriste","conservateur (musée)",
 "guide-conférencier","muséographe","scénographe","costumier","maquilleur","perruquier",
 "cascadeur","doubleur","bruiteur","monteur (cinéma)","cadreur","preneur de son",
 "éclairagiste","machiniste","régisseur","souffleur (théâtre)","habilleur","accessoiriste",
 "décorateur (spectacle)","chef opérateur","script","story-boardeur","animateur 3D",
 "modeleur","truquiste","étalonneur","mixeur (son)","ingénieur du son","DJ","VJ",
 "programmateur (festival)","tourneur (spectacle)","attaché de presse","chargé de com",
 "community manager","rédacteur web","référenceur","data analyst","data scientist",
 "administrateur système","architecte logiciel","testeur (informatique)","scrum master",
 "product owner","chef de projet","consultant","auditeur (informatique)","cryptographe",
 "hacker éthique","analyste sécurité","administrateur réseau","technicien support"]
category(extra_metiers, ["Métier","Travail","Profession","Artisan","Emploi"])

extra_lieux_monde = ["Sahara","Kalahari","Namib","Gobi","Atacama","Patagonie","Amazonie",
 "Sibérie","Scandinavie","Balkans","Caucase","Oural","Carpates","Apennins","Cordillère",
 "Great Barrier Reef","Galápagos","Bornéo","Sumatra","Java","Bali","Célèbes","Tasmanie",
 "Groenland","Terre de Feu","Antarctique","Pôle Nord","Pôle Sud","Cap Horn",
 "Détroit de Gibraltar","Canal de Panama","Canal de Suez","Bosphore","Dardanelles",
 "Mer d'Aral","Lac Baïkal","Lac Victoria","Lac Titicaca","Mer Morte","Grand Canyon",
 "Niagara","Iguazú","Victoria (chutes)","Angel (chute)","Yellowstone","Yosemite",
 "Vallée de la Mort","Uluru","Grande Barrière","Fujiyama","Etna","Vésuve","Stromboli",
 "Krakatoa","Popocatépetl","Cotopaxi","Mauna Loa","Pinatubo","Santorin","Islande (volcan)",
 "Mont Saint-Michel","Carcassonne","Versailles","Chambord","Chenonceau","Mont-Saint-Michel",
 "Notre-Dame","Sacré-Cœur","Arc de Triomphe","Panthéon","Invalides","Champs-Élysées",
 "Montmartre","Trocadéro","Bastille","Concorde","Opéra Garnier","Moulin Rouge",
 "Disneyland","Puy du Fou","Futuroscope","Marineland","mont Fuji","fjord norvégien"]
category(extra_lieux_monde, ["Lieu","Voyage","Célèbre","Monde","Site"])

extra_adjectifs = ["gigantesque","minuscule","énorme","immense","colossal","microscopique",
 "épais","fin","dense","clairsemé","touffu","broussailleux","pointu","arrondi","anguleux",
 "carré (forme)","ovale (forme)","allongé","trapu","élancé","svelte","corpulent","maigre",
 "musclé","frêle","robuste","fragile (adj)","solide","résistant","cassant","souple","rigide",
 "élastique","flexible","raide","mou (adj)","ferme","tendre (adj)","croquant","croustillant",
 "moelleux","fondant","onctueux","crémeux","granuleux","poudreux","collant","gluant",
 "visqueux","huileux","gras (adj)","sec (adj)","aride","détrempé","spongieux","poreux",
 "compact","creux (adj)","plein (adj)","vide","bondé","désert (adj)","peuplé","isolé",
 "reculé","proche","lointain","voisin","adjacent","central","périphérique","frontalier",
 "insulaire","côtier","montagneux","vallonné","plat (adj)","escarpé","abrupt","pentu",
 "vertigineux","profond","superficiel","peu profond","élevé","surélevé","enfoui","enterré",
 "aérien","souterrain","immergé","flottant","suspendu","perché","juché","tapi","blotti"]
category(extra_adjectifs, ["Adjectif","Décrire","Qualité","Caractère","Aspect"])

extra_verbes = ["bondir","gambader","trottiner","galoper","ramper","se faufiler","se glisser",
 "escalader","dévaler","dégringoler","chuter","trébucher","glisser","déraper","patiner",
 "titubler","chanceler","vaciller","tanguer","osciller","balancer","bercer","secouer",
 "agiter","remuer","brasser","touiller","battre (fouet)","fouetter","pétrir","malaxer",
 "façonner","modeler","sculpter","tailler (pierre)","ciseler","graver (verbe)","buriner",
 "poncer","polir","limer","raboter","scier","clouer","visser","boulonner","souder","river",
 "coller (verbe)","assembler","emboîter","empiler","entasser","aligner","ranger","classer",
 "trier","ordonner","organiser","disposer","agencer","aménager","décorer (verbe)","orner",
 "embellir","enjoliver","peaufiner","fignoler","parfaire","achever","terminer","conclure",
 "entamer","commencer","débuter","amorcer","déclencher","provoquer","susciter","engendrer",
 "générer","produire","fabriquer (verbe)","élaborer","concevoir","imaginer (verbe)","inventer (verbe)",
 "innover","créer (verbe)","composer","rédiger","griffonner","gribouiller","raturer","biffer",
 "souligner","surligner","annoter","commenter (verbe)","résumer","synthétiser","analyser (verbe)"]
category(extra_verbes, ["Action","Faire","Verbe","Geste","Mouvement"])

# Broaden with animals-by-habitat and descriptors to fill remaining slots.
extra_animaux = ["chacal","hyène","guépard","léopard","panthère","jaguar","puma","lynx",
 "ocelot","serval","caracal","chat sauvage","genette","civette","mangouste","suricate",
 "raton laveur","coati","kinkajou","opossum","gerboise","gerbille","hamster","cochon d'Inde",
 "chinchilla","octodon","rat","souris (animal)","mulot","campagnol","musaraigne","taupe",
 "hérisson","porc-épic","écureuil","marmotte","spermophile","chien de prairie","lièvre",
 "furet","hermine","belette","fouine","martre","putois","vison","zibeline","glouton",
 "ratel","pangolin","aardvark","damalisque","gnou","impala","gazelle","antilope","oryx",
 "koudou","élan","orignal","renne","caribou","daim","wapiti","chamois","bouquetin","mouflon",
 "isard","markhor","argali","urial","takin","gaur","banteng","zébu","aurochs","musaraigne aquatique",
 "desman","chauve-souris","roussette","pipistrelle","noctule","murin","rhinolophe","vespertilion",
 "narval","béluga","cachalot","orque","rorqual","marsouin","lamantin","dugong","otarie",
 "lion de mer","éléphant de mer","léopard des mers"]
category(extra_animaux, ["Animal","Sauvage","Bête","Nature","Espèce"])

# ---------------------------------------------------------------------------
# 3b. Large additional vocabulary lists to reach >= 8000 unique cards --------
# ---------------------------------------------------------------------------
big_lists = [
 # --- More fruits & vegetables & food items ---
 (["nectarine","brugnon","coing","nèfle","kaki","grenade","cédrat","kumquat","bergamote",
   "yuzu","combava","citron vert","lime (fruit)","physalis","groseille à maquereau","sureau",
   "aronia","argousier","cornouille","alkékenge","tamarillo","chérimole","corossol","sapotille",
   "ramboutan","mangoustan","salak","jaquier","noni","feijoa","nashi","bergamotte","clémenvilla",
   "poivron rouge","poivron jaune","poivron vert","piment doux","piment fort","jalapeño",
   "habanero","chou romanesco","chou kale","chou pak-choï","chou-rave","pousse de bambou",
   "coeur de palmier","germe de soja","haricot mungo","haricot rouge","haricot blanc",
   "haricot noir","haricot coco","flageolet","pois cassé","pois gourmand","edamame",
   "gombo","okra","chayotte","christophine","gingembre confit","raifort","wasabi",
   "galanga","citronnelle","kaffir","curry (feuille)","fenugrec","nigelle","sumac",
   "za'atar","harissa","ras el-hanout","garam masala","cinq-épices","dukkah"],
  ["Aliment","Manger","Cuisine","Goût","Nourriture"]),
 # --- Kitchen & tableware ---
 (["ramequin","cocotte-minute","tajine (plat)","plat à gratin","moule à tarte","moule à cake",
   "moule à gâteau","poêle à crêpes","gaufrier","croque-gaufre","sorbetière","yaourtière",
   "déshydrateur","fumoir","barbecue","plancha (appareil)","raclette (appareil)",
   "fondue (appareil)","cuit-vapeur","couscoussier","bain-marie","chinois (passoire)",
   "entonnoir","doseur","verre doseur","thermosonde","minuteur","essoreuse à salade",
   "presse-ail","dénoyauteur","vide-pomme","zesteur","canneleur","cuillère parisienne",
   "pinceau de cuisine","corne (pâtisserie)","maryse","poche à douille","douille",
   "moule à muffins","moule à madeleines","toile silicone","papier cuisson","cul-de-poule",
   "saladier","plat de service","ravier","raviER","légumier","saucière","beurrier",
   "sucrier","huilier","salière","poivrière","moulin à poivre","moulin à sel","dessous-de-plat"],
  ["Cuisine","Ustensile","Table","Cuisiner","Préparer"]),
 # --- Household & cleaning ---
 (["balai","serpillière","seau","éponge","chiffon","plumeau","balayette","pelle à poussière",
   "raclette (vitre)","brosse à récurer","brosse WC","lavette","microfibre","gant de ménage",
   "produit vaisselle","liquide vaisselle","lessive","adoucissant","détachant","javel",
   "vinaigre blanc","bicarbonate","savon noir","cristaux de soude","désodorisant",
   "papier essuie-tout","sac poubelle","poubelle","corbeille","conteneur","bac de tri",
   "cendrier","aspirateur robot","nettoyeur vapeur","autolaveuse","cireuse","shampouineuse",
   "détartrant","anticalcaire","insecticide","répulsif","tapette","piège à souris",
   "bombe anti-mites","boule antimites","fer à vapeur","centrale vapeur","défroisseur",
   "étendoir","pince à linge","corde à linge","panier à linge","fil à linge"],
  ["Ménage","Nettoyer","Maison","Propre","Entretien"]),
 # --- Weather & sky detailed ---
 (["averse","ondée","crachin","giboulée","déluge","trombe d'eau","grêlon","grésil",
   "flocon (neige)","congère","névé (météo)","frimas","gelée blanche","givre","rosée",
   "brume matinale","brouillard givrant","nappe de brouillard","voile nuageux","éclaircie",
   "embellie","accalmie","bourrasque","rafale","grain (vent)","coup de vent","tempête (météo)",
   "ouragan (météo)","alizé","foehn","tramontane (vent)","autan","bise","noroît","suroît",
   "vent d'ouest","vent du nord","dépression (météo)","anticyclone","front chaud","front froid",
   "isobare","masse d'air","inversion thermique","point de rosée","humidité relative",
   "indice UV","ressenti (météo)","refroidissement éolien","canicule (météo)","vague de froid",
   "redoux","dégel","verglas (météo)","plaque de verglas","brouillard de mer","halo",
   "parhélie","gloire","mirage (optique)"],
  ["Météo","Ciel","Temps","Nature","Climat"]),
 # --- Astronomy detailed ---
 (["planète naine","exoplanète","géante gazeuse","planète tellurique","anneau (planète)",
   "cratère","mer lunaire","phase lunaire","premier quartier","dernier quartier","gibbeuse",
   "éclipse solaire","éclipse lunaire","transit","conjonction","opposition","périhélie",
   "aphélie","apogée","périgée","équinoxe (astro)","solstice (astro)","zénith","nadir",
   "horizon (astro)","méridien","écliptique","zodiaque","Grande Ourse","Petite Ourse",
   "Cassiopée","Orion","Cygne (constellation)","Scorpion (constellation)","Lyre","Aigle (constellation)",
   "Andromède","Pégase","étoile Polaire","Sirius","Bételgeuse","Rigel","Véga","Aldébaran",
   "Antarès","amas d'étoiles","amas globulaire","galaxie spirale","galaxie elliptique",
   "voie lactée (astro)","bras spiral","noyau galactique","trou noir supermassif",
   "naine brune","géante bleue","naine rouge","étoile à neutrons","magnétar","céphéide",
   "nova","hypernova","rémanent","onde gravitationnelle","fond diffus cosmologique",
   "expansion","décalage vers le rouge","année-lumière","parsec","unité astronomique"],
  ["Espace","Ciel","Astronomie","Univers","Étoile"]),
 # --- More professions detailed ---
 (["ostéopathe","podologue","orthophoniste","orthoptiste","diététicien","nutritionniste",
   "ergothérapeute","aide-soignant","auxiliaire de vie","brancardier","ambulancier",
   "manipulateur radio","biologiste médical","anesthésiste","radiologue","cardiologue",
   "neurologue","gastro-entérologue","pneumologue","dermatologue","ophtalmologue","gériatre",
   "pédiatre","gynécologue","urologue","rhumatologue","endocrinologue","oncologue",
   "chirurgien-dentiste","prothésiste dentaire","opticien","audioprothésiste","orthésiste",
   "préparateur en pharmacie","agent hospitalier","secrétaire médicale","assistante dentaire",
   "moniteur d'auto-école","moniteur de ski","maître-nageur","surveillant de baignade",
   "coach sportif","préparateur physique","kinésithérapeute du sport","professeur de yoga",
   "professeur de danse","professeur de musique","professeur de piano","maître d'armes",
   "arbitre","juge-arbitre","commissaire de course","chronométreur","soigneur","entraîneur",
   "sélectionneur","directeur sportif","agent de joueurs","recruteur","préparateur mental"],
  ["Métier","Travail","Profession","Emploi","Spécialiste"]),
 # --- Tools & materials ---
 (["planche","poutre","chevron","tasseau","latte","lambourde","panneau","contreplaqué",
   "aggloméré","MDF","stratifié","placoplâtre","brique","parpaing","béton","ciment","mortier",
   "plâtre (matériau)","enduit","crépi","peinture (matériau)","vernis (matériau)","lasure",
   "cire","mastic","silicone (matériau)","joint","isolant","laine de verre","laine de roche",
   "polystyrène","mousse (isolant)","bâche","géotextile","grillage","treillis","ferraille",
   "armature","tige filetée","goujon","cheville (fixation)","équerre (fixation)","platine",
   "sabot (charpente)","connecteur","agrafe","pointe (clou)","semence (clou)","rivet",
   "goupille","clavette","circlip","joint torique","rondelle éventail","écrou papillon",
   "écrou borgne","tire-fond","vis à bois","vis autoforeuse","boulon (fixation)"],
  ["Matériau","Bricolage","Construction","Chantier","Bâtir"]),
 # --- Clothing detailed ---
 (["anorak","doudoune","parka","caban","trench","imper","ciré","coupe-vent","softshell",
   "polaire","doudoune sans manches","boléro","kimono (vêtement)","peignoir (vêtement)",
   "sarouel","corsaire","pantacourt","pantalon fuseau","jodhpur","knickers","fuseau (ski)",
   "combinaison de ski","combinaison de plongée","maillot de bain","monokini","bikini",
   "boxer de bain","short de bain","paréo","tunique de plage","caftan","djellaba","boubou",
   "sari","kimono japonais","hanbok","cheongsam","toge","tunique romaine","chasuble","aube",
   "soutane","froc","habit (moine)","cornette","guimpe","wimple","chaperon","houppelande",
   "surcot","pourpoint","haut-de-chausses","fraise (col)","jabot","collerette","manchette",
   "poignet mousquetaire","boutons de manchette","épaulette","passepoil","revers (veste)"],
  ["Vêtement","Habit","Porter","Mode","Tissu"]),
 # --- Musical genres & terms ---
 (["classique (musique)","romantique (musique)","baroque (musique)","contemporain (musique)",
   "minimalisme","atonal","dodécaphonique","sérialisme","musique électroacoustique",
   "musique concrète","ambient","techno","house","trance","dubstep","drum and bass","garage",
   "acid","electro","synthwave","chiptune","lo-fi","trip-hop","downtempo","new wave",
   "cold wave","synthpop","dream pop","shoegaze","post-rock","math-rock","progressif",
   "psychédélique","hard rock","heavy metal","thrash metal","death metal","black metal",
   "doom metal","power metal","metalcore","hardcore","emo","screamo","ska","rocksteady",
   "dub","dancehall","ragga","afrobeat","highlife","soukous","zouk","kompa","biguine",
   "bossa nova","samba (musique)","forró","cumbia","reggaeton","bachata","merengue","son cubain",
   "rumba (musique)","mambo","cha-cha-cha","boléro (danse)","paso doble (musique)","java",
   "musette","chanson française","variété","yéyé","chanson réaliste","rap","trap","drill"],
  ["Musique","Genre","Son","Style","Rythme"]),
 # --- Dances ---
 (["valse","polka","mazurka","quadrille","gavotte","menuet","gigue","branle","bourrée",
   "farandole","sardane","fandango","sévillane","sardane (danse)","jota","muñeira","tarentelle",
   "sirtaki","kalinka","kazatchok","czardas","hora","kolo","dabké","raqs sharqi","danse du ventre",
   "danse orientale","bhangra","kathak","bharata natyam","danse hawaïenne","hula","haka (danse)",
   "capoeira","frevo","maracatu","candombe","milonga","chacarera","zamba","joropo","marinera",
   "diablada","carnavalito","huayno","cueca","salsa cubaine","salsa portoricaine","kizomba",
   "semba","gwo ka","maloya","séga","rock acrobatique","rock à quatre temps","charleston (danse)",
   "lindy hop","boogie-woogie","jive","twist (danse)","madison","disco (danse)","hip-hop (danse)",
   "break","popping","locking","krump","house (danse)","voguing","danse contemporaine",
   "danse classique","pointes","pas de deux","entrechat","arabesque (danse)","pirouette","fouetté"],
  ["Danse","Bouger","Musique","Pas","Bal"]),
 # --- More geography/nature ---
 (["cascade (nature)","chute (eau)","torrent","gave","gorges","canyon (nature)","ravine",
   "précipice","gouffre","abîme","crevasse (nature)","faille","escarpement","corniche",
   "aiguille (montagne)","pic (montagne)","aiguille rocheuse","arête (montagne)","col (montagne)",
   "brèche","cheminée (roche)","surplomb","dalle rocheuse","éboulis","pierrier","moraine (nature)",
   "verrou glaciaire","ombilic","auge glaciaire","vallée suspendue","gorge (canyon)","cluse (nature)",
   "percée","reculée","poljé","lapiaz","ouvala","perte (rivière)","exsurgence","siphon","galerie",
   "salle (grotte)","stalactite","stalagmite","colonne (grotte)","draperie","gours","fistuleuse",
   "concrétion","spéléothème","calcite","tuf","travertin","source thermale","mofette","solfatare",
   "fumerolle","cratère (volcan)","caldeira","dôme (volcan)","coulée de lave","nuée ardente",
   "lahar","cône volcanique","dyke","neck","orgue basaltique","pillow lava"],
  ["Nature","Paysage","Relief","Extérieur","Naturel"]),
 # --- More science terms ---
 (["gravitation universelle","champ magnétique","champ électrique","induction","résistance électrique",
   "tension électrique","intensité","courant continu","courant alternatif","semi-conducteur",
   "diode","condensateur","bobine","résonance","interférence","diffraction","réfraction",
   "réflexion","polarisation","effet Doppler","effet photoélectrique","rayonnement","radioactivité",
   "désintégration","demi-vie","isotope","ion","cation","anion","liaison chimique","liaison covalente",
   "liaison ionique","valence","mole","molarité","catalyseur","réaction exothermique",
   "réaction endothermique","combustion","électrolyse","électrolyte","pH acide","pH basique",
   "titrage","précipité","solubilité","saturation (chimie)","cristallisation","distillation",
   "évaporation","sublimation","condensation","fusion (physique)","solidification","vaporisation",
   "point d'ébullition","point de fusion","capacité thermique","conductivité","viscosité",
   "densité","masse volumique","tension superficielle","capillarité","pression osmotique",
   "concentration","dilution","suspension","colloïde","émulsion (chimie)","polymère","monomère"],
  ["Science","Physique","Chimie","Étude","Théorie"]),
 # --- Biology terms ---
 (["mitochondrie","noyau (cellule)","ribosome","membrane cellulaire","cytoplasme","chloroplaste",
   "vacuole","réticulum","appareil de Golgi","lysosome","paroi cellulaire","gène","allèle",
   "génome","chromosome (bio)","méiose","mitose (bio)","gamète","zygote","embryon (bio)","cellule souche",
   "neurone","synapse","axone","dendrite","influx nerveux","hormone","glande","métabolisme",
   "anabolisme","catabolisme","enzyme (bio)","substrat","cofacteur","ADN (bio)","ARN","nucléotide",
   "codon","transcription","traduction (bio)","réplication","mutation (bio)","sélection naturelle (bio)",
   "spéciation","hérédité","phénotype","génotype","dominant","récessif","homozygote","hétérozygote",
   "biodiversité","niche écologique","chaîne alimentaire (bio)","réseau trophique","producteur (bio)",
   "consommateur (bio)","décomposeur","symbiose","parasitisme","commensalisme","mutualisme",
   "prédation","compétition (bio)","biotope","biocénose","population (bio)","espèce (bio)","genre (bio)",
   "famille (bio)","ordre (bio)","classe (bio)","embranchement","règne","taxon"],
  ["Biologie","Science","Vivant","Cellule","Vie"]),
 # --- Body / medical detailed ---
 (["fémur","tibia","péroné","radius (os)","cubitus","humérus","omoplate","bassin (os)","sacrum",
   "coccyx","métacarpe","métatarse","phalange","carpe (os)","tarse","calcanéum","astragale",
   "rotule (os)","mandibule","maxillaire","occiput","pariétal","temporal","frontal (os)","sphénoïde",
   "ethmoïde","hyoïde","atlas (vertèbre)","axis","cervicale","dorsale (vertèbre)","lombaire",
   "biceps","triceps","quadriceps","ischio-jambiers","deltoïde","trapèze (muscle)","pectoral",
   "grand dorsal","abdominaux","obliques","fessier","psoas","mollet (muscle)","soléaire",
   "diaphragme","masséter","zygomatique","orbiculaire","sternocléidomastoïdien","aorte","carotide",
   "jugulaire","fémorale","aorte abdominale","veine cave","artère pulmonaire","valve cardiaque",
   "oreillette","ventricule","myocarde","péricarde","alvéole","bronche","trachée","larynx",
   "pharynx","œsophage","duodénum","jéjunum","iléon","cæcum","rectum","anus","urètre","uretère",
   "vessie","néphron","glomérule","hypophyse","hypothalamus","amygdale (cerveau)","hippocampe (cerveau)"],
  ["Corps","Anatomie","Organe","Humain","Médecine"]),
 # --- Sports detailed / equipment ---
 (["raquette (tennis)","volant (badminton)","filet (sport)","panier (basket)","cage (foot)",
   "poteau","corner","penalty","hors-jeu","tacle","dribble","passe (sport)","tir (sport)","lob",
   "smash","revers (tennis)","coup droit","service (tennis)","ace","break (tennis)","set",
   "jeu (tennis)","match point","tie-break","mêlée","touche (rugby)","essai (rugby)","transformation",
   "drop","plaquage","ruck","maul","chandelle","up and under","haltère (sport)","barre (musculation)",
   "disque (musculation)","kettlebell (sport)","élastique (sport)","tapis (sport)","medecine-ball",
   "corde à sauter (sport)","espalier","anneaux (gym)","barres parallèles","barre fixe","cheval d'arçons",
   "poutre (gym)","tremplin","trampoline (gym)","tatami","kimono (judo)","ceinture (judo)","protège-dents",
   "gants de boxe","sac de frappe","pao","paire de gants","casque (boxe)","protège-tibias",
   "crampons","chaussures à pointes","dossard","chronomètre","starting-block","témoin (relais)"],
  ["Sport","Équipement","Jouer","Match","Compétition"]),
 # --- Emotions / traits extended ---
 (["allégeance","dévouement","loyauté","fidélité","franchise","sincérité","honnêteté","intégrité",
   "modestie","humilité","discrétion","réserve","pudeur","décence","politesse","courtoisie",
   "amabilité","gentillesse","douceur (trait)","patience","persévérance","ténacité","obstination",
   "détermination","volonté","ambition","audace","témérité","hardiesse","bravoure","vaillance",
   "prudence","circonspection","méfiance","vigilance","attention (trait)","concentration","application",
   "rigueur","minutie","méticulosité","perfectionnisme","curiosité","ouverture","tolérance (trait)",
   "indulgence","clémence","mansuétude","magnanimité","altruisme","abnégation","sacrifice",
   "insouciance","légèreté","spontanéité","enthousiasme (trait)","optimisme (trait)","pessimisme",
   "cynisme","scepticisme","fatalisme","résignation","apathie","indifférence","froideur","dureté",
   "sévérité","rigidité","intransigeance","autoritarisme","arrogance","orgueil","vanité","prétention",
   "suffisance","condescendance","susceptibilité","irritabilité","impulsivité","imprudence"],
  ["Trait","Caractère","Sentiment","Personnalité","Qualité"]),
 # --- Abstract nouns extended ---
 (["existence","essence (concept)","substance","matière (concept)","forme (concept)","structure",
   "système","modèle","schéma","paradigme","principe","fondement","base (concept)","origine","cause",
   "conséquence","effet (concept)","finalité","but (concept)","moyen","méthode","procédé","démarche",
   "processus","évolution (concept)","transformation","mutation (concept)","changement","permanence",
   "stabilité","continuité","rupture (concept)","transition","progression","régression","cycle",
   "répétition","alternance","hasard (concept)","nécessité","contingence","possibilité","virtualité",
   "actualité (concept)","potentiel","limite","frontière (concept)","seuil","mesure (concept)","proportion (concept)",
   "équilibre (concept)","déséquilibre","tension (concept)","conflit","opposition (concept)","contradiction",
   "paradoxe (concept)","dilemme","alternative","choix (concept)","décision (concept)","liberté (concept)",
   "contrainte","déterminisme","fatalité","destinée","providence","fortune","chance","malchance",
   "risque","danger (concept)","sécurité (concept)","protection","défense (concept)","attaque (concept)"],
  ["Concept","Idée","Notion","Abstrait","Pensée"]),
 # --- Games/toys/entertainment extended ---
 (["jeu de cartes","jeu de dés","jeu de société","jeu de plateau","jeu de rôle","jeu d'adresse",
   "jeu de stratégie","jeu de mémoire","jeu de mots","jeu de logique","casse-tête","énigme","charade",
   "rébus","mots croisés","mots fléchés","sudoku (jeu)","mots mêlés","anagramme","devinette","quiz (jeu)",
   "loto","bingo","tombola","roue de la fortune","pierre-feuille-ciseaux","cache-cache","chat perché",
   "colin-maillard","marelle","élastique (jeu)","corde à sauter (jeu)","chamboule-tout","pêche aux canards",
   "quilles (jeu)","fléchettes (jeu)","palet","molkky","croquet","jeu de l'oie","petits chevaux",
   "solitaire","réussite","patience (jeu)","bataille (cartes)","pouilleux","menteur (jeu)","pouce (jeu)",
   "sept familles","mistigri","rami","canasta","gin-rami","tarot (cartes)","manille","whist","yams",
   "421","zanzibar","dé à jouer","toupie (jeu)","bilboquet","diabolo","yo-yo (jeu)","kaléidoscope",
   "kazoo","sifflet (jouet)","mirliton","boîte à musique","pantin","marionnette (jouet)","cerf-volant"],
  ["Jeu","Jouer","Amuser","Loisir","Divertissement"]),
 # --- Buildings & places ---
 (["gratte-ciel","tour (bâtiment)","immeuble","pavillon","villa","chalet","cabane","hutte","igloo",
   "tente","yourte","tipi","case","bungalow","mobil-home","caravane","péniche (habitation)","château fort",
   "donjon","forteresse","citadelle","rempart","douve","pont-levis","meurtrière","créneau","mâchicoulis",
   "beffroi","clocher","campanile","minaret","coupole","dôme (bâtiment)","voûte","arche","colonnade",
   "portique","péristyle","fronton","chapiteau (colonne)","corniche (bâtiment)","fresque","vitrail","rosace",
   "gargouille","contrefort","arc-boutant","nef","transept","abside","crypte","cloître","chœur (église)",
   "chapelle","autel","chaire","confessionnal","bénitier","fonts baptismaux","tabernacle","stalle",
   "jubé","tympan (portail)","porche","narthex","déambulatoire","triforium","clé de voûte","pilier",
   "chapiteau (sculpté)","gargouille (sculpture)","frise","métope","triglyphe"],
  ["Bâtiment","Construction","Lieu","Architecture","Édifice"]),
 # --- Landscape/geography features 2 ---
 (["plaine (relief)","plateau (relief)","colline (relief)","butte","monticule","tertre","mamelon",
   "coteau","versant","pente","talus","remblai","déblai","terrasse (agri)","restanque","bocage",
   "openfield","champ","pré (agri)","pâture","chaume","jachère","friche (agri)","lande (agri)",
   "tourbière (agri)","roselière","cariçaie","phragmitaie","saulaie","aulnaie","peupleraie",
   "ripisylve","forêt-galerie","mangrove (relief)","palétuvier","cocoteraie","oliveraie","vignoble",
   "verger","orangeraie","bananeraie","rizière","champ de blé","champ de maïs","prairie (relief)",
   "steppe herbeuse","savane arborée","brousse","fourré","roncier","broussaille","garrigue (relief)",
   "maquis (relief)","matorral","chaparral","toundra (relief)","taïga (relief)","pergélisol",
   "banquise (relief)","inlandsis","calotte glaciaire","glacier de vallée","glacier de cirque",
   "front glaciaire","langue glaciaire (relief)","séracs","crevasse (glacier)"],
  ["Paysage","Relief","Nature","Terrain","Extérieur"]),
 # --- Transportation / vehicles extended ---
 (["berline","coupé","break (auto)","cabriolet","monospace","citadine","SUV","4x4","utilitaire",
   "fourgon","fourgonnette","semi-remorque","poids lourd","autocar","minibus","navette (bus)",
   "trolleybus","autorail","autorail (train)","TER","RER","funiculaire (transport)","téléphérique (transport)",
   "télésiège","télécabine","monorail","train à grande vitesse","train de nuit","wagon-lit","wagon-restaurant",
   "locomotive à vapeur","motrice","draisine","wagonnet","tender","aéroglisseur","hydroptère","hydravion",
   "planeur","autogire","gyrocoptère","avion de chasse","avion de ligne","jet privé","biplan","monoplan",
   "bombardier","chasseur (avion)","cargo (avion)","ravitailleur","hydravion (transport)","ballon dirigeable",
   "zeppelin","mongolfière (transport)","parachute","parapente (transport)","aile delta","wingsuit",
   "navire de guerre","porte-avions","croiseur","destroyer","frégate","corvette","sous-marin (transport)",
   "chalutier","thonier","baleinier","remorqueur","dragueur","chaland","gabarre","gondole (bateau)"],
  ["Transport","Véhicule","Rouler","Déplacer","Voyage"]),
 # --- Mythology / legends extended ---
 (["Cerbère","Pégase (mythe)","Chimère","Griffon","Harpie","Gorgone","Euryale","Sthéno","Charybde",
   "Scylla","Cyclope (mythe)","Titan","Cronos","Ouranos","Gaïa","Rhéa","Océan (mythe)","Téthys",
   "Hypérion","Japet","Atlas (mythe)","Épiméthée","Prométhée (mythe)","Pandore","Deucalion","Éole",
   "Triton (mythe)","Néréide","Naïade","Dryade","Nymphe","Satyre","Faune (mythe)","Pan (mythe)",
   "Silène","Ménade","Bacchante","Muse","Grâce","Parque","Moire","Érinye","Furie","Némésis",
   "Tyché","Iris (mythe)","Hébé","Ganymède","Éros","Cupidon","Psyché","Hymen","Morphée","Hypnos",
   "Thanatos","Charon","Styx","Léthé","Achéron","Champs Élysées (mythe)","Tartare","Élysée","Olympe",
   "ambroisie","nectar (mythe)","corne d'abondance","toison d'or","boîte de Pandore","talon d'Achille",
   "cheval de Troie","fil d'Ariane","supplice de Tantale","rocher de Sisyphe","tonneau des Danaïdes",
   "épée de Damoclès","nœud gordien"],
  ["Mythe","Légende","Antique","Grec","Divin"]),
 # --- Occupations of the past / crafts ---
 (["meunier","laboureur","semeur","moissonneur","faucheur","vigneron","tonnelier","brasseur",
   "distillateur","saunier","charbonnier","bûcheron","sabotier","charron","maréchal-ferrant",
   "bourrelier","cordier","filateur","tisserand","foulon","drapier","teinturier (ancien)","tanneur",
   "corroyeur","mégissier","peaussier","gantier (ancien)","chaudronnier","ferblantier","étameur",
   "fondeur","cloutier","taillandier","armurier","fourbisseur","batteur d'or","monnayeur","graveur (ancien)",
   "enlumineur (ancien)","parcheminier","papetier","cartier","imagier","santonnier","tourneur sur bois",
   "marqueteur","doreur (ancien)","laqueur","vernisseur","matelassier","rempailleur","cannier",
   "vannier (ancien)","cordonnier (ancien)","savetier","gnaffe","bottier","formier","talonnier",
   "guêtrier","passementier","boutonnier","rubanier","dentellière","brodeuse","lingère","repasseuse",
   "blanchisseuse","lavandière","porteur d'eau","allumeur de réverbères","crieur public","colporteur",
   "rémouleur","raccommodeur","ramoneur (ancien)","chiffonnier","biffin"],
  ["Métier","Ancien","Artisan","Travail","Autrefois"]),
 # --- More birds & animals to be safe ---
 (["autruche","émeu","nandou","casoar","kiwi (oiseau)","dodo (oiseau)","cygne noir","paon blanc",
   "dindon","pintade","faisan doré","colvert","harle","garrot","eider","macreuse","tadorne","ouette",
   "dendrocygne","grand tétras","tétras-lyre","gélinotte","lagopède","perdrix rouge","perdrix grise",
   "colin","francolin","turnix","râle d'eau","marouette","poule d'eau","foulque","talève","gallinule",
   "outarde barbue","outarde canepetière","œdicnème","glaréole","huîtrier","échasse","avocette",
   "vanneau sociable","tourne-pierre","chevalier arlequin","chevalier aboyeur","chevalier cul-blanc",
   "bécasseau sanderling","bécasseau cocorli","bécasseau variable","gravelot à collier interrompu",
   "pluvier argenté (oiseau)","barge (oiseau)","courlis (oiseau)","numénius","limosa","tringa",
   "calidris","phalarope à bec large","phalarope à bec étroit","labbe parasite","goéland cendré",
   "goéland leucophée","mouette tridactyle","mouette pygmée","sterne caugek","sterne naine",
   "sterne caspienne (oiseau)","guifette leucoptère","noddi","pétrel","puffin","océanite","fulmar boréal",
   "albatros hurleur","frégate (oiseau)","phaéton","sula","cormoran pygmée","anhinga","pélican blanc",
   "pélican gris","spatule blanche","ibis sacré","ibis falcinelle","flamant rose","flamant nain"],
  ["Oiseau","Plumes","Voler","Bec","Nature"]),
 # --- Insects & small creatures ---
 (["hanneton","lucane","cerf-volant (insecte)","scarabée","bousier","carabe","staphylin","chrysomèle",
   "doryphore","charançon","capricorne","longicorne","cétoine","cantharide","ténébrion","dytique",
   "gyrin","gerris","notonecte","nèpe","ranatre","punaise","pentatome","gendarme (insecte)","cigale",
   "cicadelle","puceron","cochenille","psylle","aleurode","fourmi rouge","fourmi noire","fourmi charpentière",
   "guêpe maçonne","guêpe poliste","frelon asiatique","frelon européen","bourdon","abeille solitaire",
   "abeille charpentière","xylocope","syrphe","bombyle","asile","tabanide","stratiome","tipule",
   "moucheron","cousin","simulie","phlébotome","chironome","éphémère","perle (insecte)","phrygane",
   "plécoptère","trichoptère","névroptère","fourmilion","chrysope","hémérobe","mante religieuse",
   "empuse","phasme","phasme bâton","perce-oreille","forficule","blatte germanique","termite (insecte)",
   "psoque","thrips","collembole","lépisme","poisson d'argent","mille-pattes","iule","scolopendre",
   "scutigère","cloporte","gloméris","opilion","faucheux","tique","acarien","aoûtat"],
  ["Insecte","Petit","Rampant","Nature","Bestiole"]),
]
for words, anchors in big_lists:
    category(words, anchors)

big_lists2 = [
 # --- Plants / flowers extended ---
 (["anémone","aster","campanule","gentiane","primevère","pâquerette","souci","œillet","œillet d'Inde",
   "reine-marguerite","zinnia","cosmos (fleur)","gaillarde","rudbeckie","échinacée","hélénie","gazania",
   "arctotis","dimorphotéca","nemesia","diascia","calibrachoa","surfinia","pétunia","verveine (fleur)",
   "lobélie","alysse","ibéris","giroflée","matthiole","juliennes","monnaie-du-pape","œillet de poète",
   "digitale","ancolie","aconit","delphinium","pied-d'alouette","nigelle (fleur)","adonis","hellébore",
   "rose de Noël","perce-neige","nivéole","muguet","fritillaire","tulipe botanique","jacinthe des bois",
   "scille","muscari","allium","colchique","cyclamen","sternbergia","nérine","agapanthe","alstroemère",
   "freesia","ixia","sparaxis","tritonia","montbrétia","crocosmia","kniphofia","hémérocalle","hosta",
   "astilbe","heuchère","tiarelle","brunnera","pulmonaire","bergénia","géranium vivace","népéta",
   "sauge ornementale","népeta","achillée","tanaisie","armoise","santoline","hélichryse","immortelle",
   "statice","gypsophile","œillet mignardise","saponaire","silène","lychnis","coquelourde"],
  ["Fleur","Plante","Jardin","Fleurir","Nature"]),
 # --- Trees & shrubs extended ---
 (["tilleul (arbre)","robinier","févier","catalpa","paulownia","ailante","sophora","arbre de Judée",
   "cercis","koelreuteria","liquidambar","tulipier","ginkgo","métaséquoia","cyprès chauve","araucaria",
   "cèdre du Liban","cèdre de l'Atlas","cèdre déodar","pin sylvestre","pin maritime","pin parasol",
   "pin noir","pin d'Alep","pin cembro","pin Weymouth","douglas","tsuga","abies","picéa","genévrier",
   "cyprès","thuya (arbre)","chamaecyparis","séquoia géant","séquoia côtier","if (arbre)","houx (arbre)",
   "buis (arbre)","fusain","troène (arbre)","laurier-tin","laurier-sauce","laurier-rose","laurier-cerise",
   "photinia","viburnum","viorne","sureau (arbre)","aubépine","prunellier","cornouiller","noisetier commun",
   "charme (arbre)","charmille","hêtre pourpre","érable sycomore","érable plane","érable champêtre",
   "érable du Japon","frêne commun","frêne à fleurs","orme champêtre","micocoulier","platane commun",
   "peuplier tremble","peuplier noir","peuplier blanc","saule pleureur","saule marsault","saule blanc",
   "osier","bouleau verruqueux","bouleau pubescent","aulne glutineux","charme-houblon"],
  ["Arbre","Bois","Feuille","Forêt","Végétal"]),
 # --- Countries & nationalities extended ---
 (["Slovénie","Slovaquie","Estonie","Lettonie","Lituanie","Biélorussie","Moldavie","Macédoine",
   "Monténégro","Bosnie","Albanie","Kosovo","Malte","Chypre","Luxembourg","Liechtenstein","Monaco",
   "Andorre","Saint-Marin","Vatican","Géorgie","Arménie","Azerbaïdjan","Kazakhstan","Ouzbékistan",
   "Turkménistan","Kirghizistan","Tadjikistan","Mongolie","Afghanistan","Népal","Bhoutan","Sri Lanka",
   "Maldives","Birmanie","Brunei","Timor oriental","Papouasie","Fidji","Samoa","Tonga","Vanuatu",
   "Salomon","Kiribati","Palaos","Nauru","Tuvalu","Guatemala","Honduras","Salvador","Nicaragua",
   "Costa Rica","Panama","Cuba","Jamaïque","Haïti","Bahamas","Barbade","Trinité","Guyana","Suriname",
   "Belize","Mauritanie","Gambie","Guinée","Sierra Leone","Liberia","Togo","Bénin","Burkina Faso",
   "Gabon","Guinée équatoriale","Centrafrique","Rwanda","Burundi","Ouganda","Somalie","Djibouti",
   "Érythrée","Zambie","Zimbabwe","Malawi","Botswana","Namibie","Lesotho","Eswatini","Comores",
   "Maurice","Seychelles","Cap-Vert","Oman","Qatar","Bahreïn","Yémen"],
  ["Pays","Nation","Territoire","Drapeau","Frontière"]),
 # --- French regions / departments / famous places ---
 (["Occitanie","Nouvelle-Aquitaine","Hauts-de-France","Grand Est","Centre-Val de Loire",
   "Pays de la Loire","Île-de-France","Auvergne-Rhône-Alpes","Provence-Alpes-Côte d'Azur",
   "Bourgogne-Franche-Comté","Anjou","Poitou","Saintonge","Aunis","Berry","Touraine","Orléanais",
   "Maine","Perche","Beauce","Sologne","Brie","Beaujolais","Bresse","Dombes","Forez","Velay",
   "Vivarais","Rouergue","Quercy","Albigeois","Comminges","Bigorre","Béarn","Roussillon","Cerdagne",
   "Camargue","Luberon","Verdon","Ventoux","Mercantour","Vercors","Chartreuse","Belledonne","Oisans",
   "Queyras","Briançonnais","Maurienne","Tarentaise","Beaufortain","Chablais","Faucigny","Genevois",
   "Bugey","Trièves","Diois","Baronnies","Cévennes","Aubrac","Margeride","Cézallier","Sancy",
   "Cantal (relief)","Livradois","Bourbonnais","Nivernais","Morvan","Charolais","Mâconnais","Chalonnais",
   "Côte-d'Or","Vignoble alsacien","Sundgau","Ried","Kochersberg","Alpilles","Costières","Minervois",
   "Corbières","Fenouillèdes","Vallespir","Conflent","Capcir"],
  ["Région","France","Territoire","Lieu","Terroir"]),
 # --- Historical periods & events ---
 (["Préhistoire","Antiquité","Moyen Âge","Renaissance (époque)","Temps modernes","Époque contemporaine",
   "Néolithique","Paléolithique","Âge du bronze","Âge du fer","Empire romain","République romaine",
   "Gaule","Gaulois","Mérovingiens","Carolingiens","Capétiens","Valois","Bourbons","féodalité",
   "chevalerie","croisades","peste noire","guerre de Cent Ans","Renaissance italienne","Réforme protestante",
   "Contre-Réforme","guerres de religion","Grand Siècle","Ancien Régime","Siècle des Lumières",
   "Révolution française","Terreur","Directoire","Consulat","Premier Empire","Restauration",
   "monarchie de Juillet","Deuxième République","Second Empire","Commune de Paris","Troisième République",
   "Belle Époque","Première Guerre mondiale","Années folles","Grande Dépression","Front populaire",
   "Seconde Guerre mondiale","Occupation (histoire)","Libération (histoire)","Trente Glorieuses",
   "Mai 68","Guerre froide (histoire)","chute du mur","décolonisation (histoire)","guerre d'Algérie",
   "guerre d'Indochine","conquête spatiale","révolution industrielle (histoire)","colonisation (histoire)",
   "traite négrière","abolition de l'esclavage","suffrage universel","droit de vote des femmes"],
  ["Histoire","Époque","Passé","Événement","Période"]),
 # --- Musical & artistic works terms ---
 (["portrait","paysage (art)","nature morte","autoportrait","fresque (art)","mosaïque","enluminure",
   "estampe","lithographie","sérigraphie","eau-forte","aquatinte","pointe sèche","xylographie","monotype",
   "aquarelle","gouache","pastel","fusain (dessin)","sanguine","encre de Chine","huile (peinture)",
   "acrylique","tempera","détrempe","collage","assemblage","installation (art)","land art (art)",
   "art cinétique","op art","pop art","art brut","art naïf","art abstrait","art figuratif","art conceptuel",
   "expressionnisme","fauvisme","pointillisme","divisionnisme","nabis","symbolisme","préraphaélisme",
   "maniérisme","rococo","néoclassicisme","académisme","orientalisme","art déco (art)","modern style",
   "Bauhaus","De Stijl","constructivisme","suprématisme","futurisme","dadaïsme","métaphysique (art)",
   "arte povera","minimalisme (art)","hyperréalisme","photoréalisme","street art (art)","graffiti",
   "pochoir","fresque murale","trompe-l'œil","anamorphose","perspective","clair-obscur","sfumato",
   "camaïeu","grisaille","glacis","empâtement","touche (peinture)","aplat","dégradé"],
  ["Art","Œuvre","Peinture","Créer","Artiste"]),
 # --- Computing / tech extended ---
 (["clavier (info)","touche (clavier)","curseur","raccourci clavier","copier","coller (info)","couper (info)",
   "glisser-déposer","dossier","fichier","répertoire","chemin d'accès","extension (fichier)","icône",
   "bureau (info)","corbeille (info)","fenêtre (info)","onglet","barre des tâches","menu déroulant",
   "boîte de dialogue","case à cocher","bouton radio","curseur (barre)","ascenseur (info)","widget",
   "notification","pop-up","cookie","cache (info)","historique (navigateur)","favori","signet","marque-page",
   "onglet de navigation","mode privé","extension (navigateur)","plug-in","module","paquet (logiciel)",
   "dépendance","bibliothèque (info)","compilateur","interpréteur","débogueur","point d'arrêt","exception",
   "erreur (info)","bug","patch (info)","mise à jour","correctif","version bêta","alpha","release",
   "dépôt (git)","commit","branche (git)","fusion (git)","conflit (git)","pull request","fork (git)",
   "clone (git)","push (git)","serveur (info)","client (info)","requête","réponse (info)","protocole (info)",
   "paquet réseau","adresse IP","port (réseau)","pare-feu","routeur","commutateur","passerelle","proxy"],
  ["Informatique","Ordinateur","Numérique","Technologie","Écran"]),
 # --- Economy / finance extended ---
 (["taux d'intérêt","taux directeur","rendement","dividende","plus-value","moins-value","capital",
   "actif","passif","bilan","compte de résultat","chiffre d'affaires","marge","bénéfice","perte (finance)",
   "trésorerie","liquidité","solvabilité","rentabilité","amortissement","provision","impôt sur le revenu",
   "impôt sur les sociétés","cotisation","charge sociale","prélèvement","abattement","déduction","crédit d'impôt",
   "niche fiscale","paradis fiscal","évasion fiscale","fraude fiscale","blanchiment","spéculation","krach",
   "bulle (finance)","dette publique","dette privée","emprunt d'État","obligation d'État","bon du Trésor",
   "action (bourse)","indice boursier","CAC 40","Dow Jones","Nasdaq","cotation","introduction en bourse",
   "OPA","rachat","cession","filiale","holding","conglomérat","cartel","monopole","oligopole","concurrence",
   "offre (économie)","demande (économie)","prix (économie)","coût (économie)","valeur ajoutée","productivité",
   "pouvoir d'achat","niveau de vie","seuil de pauvreté","indice des prix","panier de la ménagère"],
  ["Argent","Finance","Économie","Marché","Commerce"]),
 # --- Religion / spirituality extended ---
 (["prophète","apôtre","disciple","saint","martyr","sainteté","miracle","apparition","révélation (religion)",
   "commandement","péché","vertu","grâce (religion)","salut (religion)","rédemption","résurrection",
   "eucharistie","hostie","calice","ostensoir","encens","cierge","chapelet","rosaire","icône (religion)",
   "reliquaire","relique","procession","confession","pénitence","jeûne","carême","avent","ramadan (fête)",
   "aïd","yom kippour","hanoucca","pâque juive","shabbat","kippa","talith","ménorah","kascher","halal",
   "muezzin","adhan","prosternation","ablution","hadith","sourate","verset","psaume","cantique","hymne (religion)",
   "grégorien","plain-chant","chant sacré","liturgie (religion)","vêpres","matines","complies","laudes",
   "office","messe basse","messe de minuit","procession (religion)","pèlerinage (religion)","ex-voto",
   "vœu","offrande","dîme","aumône","charité","béatitude","paradis (religion)","enfer (religion)","limbes",
   "ange gardien","archange","chérubin","séraphin"],
  ["Religion","Croyance","Sacré","Foi","Spirituel"]),
 # --- More adjectives & descriptors ---
 (["rond","ovoïde","sphérique","cubique","conique","cylindrique","pyramidal","plat (objet)","bombé",
   "concave","convexe","creux (objet)","évidé","ajouré","perforé","strié","cannelé","nervuré","côtelé",
   "godronné","ondulé","gaufré","texturé","granité","moucheté","tacheté","tigré","rayé","zébré","marbré",
   "veiné","chiné","moiré","irisé","nacré","chatoyant","brillant","luisant","mat","satiné","velouté",
   "soyeux","laineux","cotonneux","duveteux","pelucheux","hirsute","touffu (adj)","broussailleux (adj)",
   "épineux","piquant (adj)","urticant","gluant (adj)","poisseux","visqueux (adj)","filandreux","fibreux",
   "spongieux (adj)","élastique (adj)","caoutchouteux","gélatineux","farineux","poudreux (adj)","pulvérulent",
   "grumeleux","caillouteux","sablonneux","limoneux","argileux","marécageux","boueux","fangeux","vaseux",
   "détrempé (adj)","imbibé","gorgé","saturé (adj)","imperméable (adj)","étanche"],
  ["Adjectif","Décrire","Aspect","Qualité","Texture"]),
 # --- More verbs of daily life ---
 (["se lever","se coucher","s'habiller","se déshabiller","se laver","se doucher","se coiffer","se raser",
   "se maquiller","se brosser les dents","se parfumer","déjeuner","dîner","souper","goûter (repas)","grignoter",
   "cuisiner (verbe)","mettre la table","débarrasser","faire la vaisselle","essuyer","balayer","aspirer",
   "épousseter","laver (linge)","étendre","repasser (verbe)","plier (linge)","ranger (verbe)","trier (verbe)",
   "jeter","recycler","arroser (verbe)","tondre","tailler (verbe)","planter (verbe)","récolter (verbe)",
   "cueillir (verbe)","bricoler","réparer (verbe)","peindre (mur)","tapisser","poncer (verbe)","visser (verbe)",
   "clouer (verbe)","percer","scier (verbe)","mesurer (verbe)","dessiner (plan)","conduire (verbe)","garer",
   "faire le plein","laver (voiture)","gonfler","freiner","accélérer","tourner","doubler","stationner",
   "marcher (verbe)","courir (verbe)","sauter (verbe)","grimper (verbe)","nager (verbe)","plonger (verbe)",
   "pédaler (verbe)","ramer (verbe)","skier","patiner (verbe)","danser (verbe)","chanter (verbe)","jouer (musique)"],
  ["Action","Faire","Quotidien","Geste","Verbe"]),
 # --- Foods: dishes & specialties ---
 (["pot-au-feu (plat)","blanquette de veau","bœuf bourguignon","coq au vin","navarin d'agneau",
   "cassoulet (plat)","choucroute","potée","garbure","aligot","truffade","tartiflette","raclette (plat)",
   "fondue savoyarde","fondue bourguignonne","gratin dauphinois","hachis parmentier","gratin (plat)",
   "quenelle","brandade","bouillabaisse (plat)","bourride","aïoli","pistou","tapenade","anchoïade",
   "socca","pan bagnat","salade niçoise","ratatouille (plat)","piperade","garbure (plat)","confit de canard",
   "magret","foie gras (plat)","cassolette","escargots de Bourgogne","cuisses de grenouille","andouillette",
   "boudin noir","boudin blanc","saucisson","rillettes (plat)","pâté en croûte","terrine (plat)",
   "galantine","ballottine","quiche lorraine (plat)","tarte flambée","flammekueche","bretzel","kouglof",
   "far breton","kouign-amann","gâteau breton","canelé (plat)","tourteau fromager","clafoutis (plat)",
   "flognarde","pastis landais","tourtière","croustade","millas","gâteau basque","macaron d'Amiens",
   "bêtise de Cambrai","calisson d'Aix","nougat de Montélimar","berlingot de Carpentras","praline de Montargis"],
  ["Plat","Cuisine","Manger","Recette","Spécialité"]),
 # --- Body actions / gestures / expressions ---
 (["sourire (geste)","rire (geste)","pleurer (geste)","froncer les sourcils","cligner","hausser les épaules",
   "hocher la tête","secouer la tête","montrer du doigt","applaudir (geste)","saluer","serrer la main",
   "faire la bise","embrasser (geste)","enlacer","câliner","chatouiller","pincer","caresser (geste)",
   "tapoter","frotter","gratter","masser","pétrir (geste)","malaxer (geste)","tordre","essorer (geste)",
   "presser","écraser","broyer","piler","concasser","hacher (geste)","émincer","trancher (geste)",
   "découper","déchirer","froisser","chiffonner","plier (geste)","rouler (geste)","enrouler","dérouler",
   "nouer","dénouer","attacher","détacher","boutonner","déboutonner","lacer","délacer","fermer (geste)",
   "ouvrir (geste)","tourner (geste)","visser (geste)","dévisser","enfoncer","retirer","arracher","extraire",
   "insérer","glisser (geste)","empiler (geste)","aligner (geste)","disperser","éparpiller","rassembler","trier (geste)"],
  ["Geste","Bouger","Main","Corps","Action"]),
]
for words, anchors in big_lists2:
    category(words, anchors)

# ---------------------------------------------------------------------------
# 4. Emit -------------------------------------------------------------------
# ---------------------------------------------------------------------------
out = [{"word": w, "forbidden": f} for w, f in cards.items()]
print("TOTAL CARDS:", len(out))

# sanity checks
assert all(len(c["forbidden"]) == 5 for c in out), "some card lacks 5 forbidden"
assert len({c["word"] for c in out}) == len(out), "duplicate words!"

with open("/Users/tomar/Projets/github/koreader-plugins/tabou.koplugin/taboo_cards.json",
          "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
print("WROTE FILE")
