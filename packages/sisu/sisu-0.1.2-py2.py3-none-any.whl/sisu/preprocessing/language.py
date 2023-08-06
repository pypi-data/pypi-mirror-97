#!/usr/http://localhost:8888/edit/notebooks/summarizer/language_filtering.py#bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of newdle
# Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

from collections import defaultdict
from sisu.preprocessing.tokenizer import words

EN_STOP_WORDS = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act",
                 "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again",
                 "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am",
                 "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore",
                 "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren",
                 "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away",
                 "awfully", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before",
                 "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below",
                 "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "ca",
                 "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come",
                 "comes", "contain", "containing", "contains", "could", "couldnt", "date", "did", "didn't", "different",
                 "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "each", "ed",
                 "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough",
                 "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything",
                 "everywhere", "ex", "except", "far", "few", "ff", "fifth", "first", "five", "fix", "followed",
                 "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further",
                 "furthermore", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes",
                 "gone", "got", "gotten", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having",
                 "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers",
                 "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however",
                 "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important",
                 "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't",
                 "it", "itd", "it'll", "its", "itself", "i've", "just", "keep", "keeps", "kept", "kg", "km", "know",
                 "known", "knows", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest",
                 "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd",
                 "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime",
                 "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly",
                 "mr", "mrs", "much", "mug", "must", "my", "myself", "na", "name", "namely", "nay", "nd", "near",
                 "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new",
                 "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally",
                 "nos", "not", "noted", "nothing", "now", "nowhere", "obtain", "obtained", "obviously", "of", "off",
                 "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or",
                 "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
                 "overall", "owing", "own", "page", "pages", "part", "particular", "particularly", "past", "per",
                 "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp",
                 "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides",
                 "put", "que", "quickly", "quite", "qv", "ran", "rather", "rd", "re", "readily", "really", "recent",
                 "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research",
                 "respectively", "resulted", "resulting", "results", "right", "run", "said", "same", "saw", "say",
                 "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen",
                 "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should",
                 "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar",
                 "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan",
                 "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically",
                 "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially",
                 "successfully", "such", "sufficiently", "suggest", "sup", "sure", "take", "taken", "taking", "tell",
                 "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the",
                 "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered",
                 "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've",
                 "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though",
                 "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to",
                 "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts",
                 "twice", "two", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "un", "unto", "up",
                 "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually",
                 "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "want", "wants", "was", "wasnt",
                 "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever",
                 "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby",
                 "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who",
                 "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing",
                 "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "yes", "yet",
                 "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "zero", "al",
                 "herse", "himse", "itse", "myse", 'didn', 'doesn', 'don', 'hasn', 'haven', 'isn', 'll', 'shouldn',
                 've']
"""
List of common English words.
"""

FR_STOP_WORDS = ["a", "à", "â", "abord", "afin", "ah", "ai", "aie", "ainsi", "allaient", "allo", "allô", "allons",
                 "après", "assez", "attendu", "au", "aucun", "aucune", "aujourd", "aujourdhui", "auquel", "aura",
                 "auront", "aussi", "autre", "autres", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait",
                 "avant", "avec", "avoir", "ayant", "bah", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr", "ça",
                 "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là",
                 "celui", "celui-ci", "celui-là", "cent", "cependant", "certain", "certaine", "certaines", "certains",
                 "certes", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chaque", "cher", "chère",
                 "chères", "chers", "chez", "chiche", "chut", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième",
                 "cinquième", "clac", "clic", "combien", "comme", "comment", "compris", "concernant", "contre", "couic",
                 "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors", "delà", "depuis", "derrière", "des",
                 "dès", "désormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement",
                 "devant", "devers", "devra", "différent", "différente", "différentes", "différents", "dire", "divers",
                 "diverse", "diverses", "dix", "dix-huit", "dixième", "dix-neuf", "dix-sept", "doit", "doivent", "donc",
                 "dont", "douze", "douzième", "dring", "du", "duquel", "durant", "e", "effet", "eh", "elle",
                 "elle-même", "elles", "elles-mêmes", "en", "encore", "entre", "envers", "environ", "es", "ès", "est",
                 "et", "etant", "étaient", "étais", "était", "étant", "etc", "été", "etre", "être", "eu", "euh", "eux",
                 "eux-mêmes", "excepté", "f", "façon", "fais", "faisaient", "faisant", "fait", "feront", "fi", "flac",
                 "floc", "font", "g", "gens", "h", "ha", "hé", "hein", "hélas", "hem", "hep", "hi", "ho", "holà", "hop",
                 "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "huitième", "hum", "hurrah", "i", "il", "ils",
                 "importe", "j", "je", "jusqu", "jusque", "k", "l", "la", "là", "laquelle", "las", "le", "lequel",
                 "les", "lès", "lesquelles", "lesquels", "leur", "leurs", "longtemps", "lorsque", "lui", "lui-même",
                 "m", "ma", "maint", "mais", "malgré", "me", "même", "mêmes", "merci", "mes", "mien", "mienne",
                 "miennes", "miens", "mille", "mince", "moi", "moi-même", "moins", "mon", "moyennant", "n", "na", "ne",
                 "néanmoins", "neuf", "neuvième", "ni", "nombreuses", "nombreux", "non", "nos", "notre", "nôtre",
                 "nôtres", "nous", "nous-mêmes", "nul", "o", "o|", "ô", "oh", "ohé", "olé", "ollé", "on", "ont", "onze",
                 "onzième", "ore", "ou", "où", "ouf", "ouias", "oust", "ouste", "outre", "p", "paf", "pan", "par",
                 "parmi", "partant", "particulier", "particulière", "particulièrement", "pas", "passé", "pendant",
                 "personne", "peu", "peut", "peuvent", "peux", "pff", "pfft", "pfut", "pif", "plein", "plouf", "plus",
                 "plusieurs", "plutôt", "pouah", "pour", "pourquoi", "premier", "première", "premièrement", "près",
                 "proche", "psitt", "puisque", "q", "qu", "quand", "quant", "quanta", "quant-à-soi", "quarante",
                 "quatorze", "quatre", "quatre-vingt", "quatrième", "quatrièmement", "que", "quel", "quelconque",
                 "quelle", "quelles", "quelque", "quelques", "quelquun", "quels", "qui", "quiconque", "quinze", "quoi",
                 "quoique", "r", "revoici", "revoilà", "rien", "s", "sa", "sacrebleu", "sans", "sapristi", "sauf", "se",
                 "seize", "selon", "sept", "septième", "sera", "seront", "ses", "si", "sien", "sienne", "siennes",
                 "siens", "sinon", "six", "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous",
                 "stop", "suis", "suivant", "sur", "surtout", "t", "ta", "tac", "tant", "te", "té", "tel", "telle",
                 "tellement", "telles", "tels", "tenant", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc",
                 "toi", "toi-même", "ton", "touchant", "toujours", "tous", "tout", "toute", "toutes", "treize",
                 "trente", "très", "trois", "troisième", "troisièmement", "trop", "tsoin", "tsouin", "tu", "u", "un",
                 "une", "unes", "uns", "v", "va", "vais", "vas", "vé", "vers", "via", "vif", "vifs", "vingt", "vivat",
                 "vive", "vives", "vlan", "voici", "voilà", "vont", "vos", "votre", "vôtre", "vôtres", "vous",
                 "vous-mêmes", "vu", "w", "x", "y", "z", "zut", "alors", "aucuns", "bon", "devrait", "dos", "droite",
                 "début", "essai", "faites", "fois", "force", "haut", "ici", "juste", "maintenant", "mine", "mot",
                 "nommés", "nouveaux", "parce", "parole", "personnes", "pièce", "plupart", "seulement", "soyez",
                 "sujet", "tandis", "valeur", "voie", "voient", "état", "étions"]
"""
List of common French words.
"""

ES_STOP_WORDS = ["algún", "alguna", "algunas", "alguno", "algunos", "ambos", "ampleamos", "ante", "antes", "aquel",
                 "aquellas", "aquellos", "aqui", "arriba", "atras", "bajo", "bastante", "bien", "cada", "cierta",
                 "ciertas", "cierto", "ciertos", "como", "con", "conseguimos", "conseguir", "consigo", "consigue",
                 "consiguen", "consigues", "cual", "cuando", "dentro", "desde", "donde", "dos", "el", "ellas", "ellos",
                 "empleais", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era",
                 "eramos", "eran", "eras", "eres", "es", "esta", "estaba", "estado", "estais", "estamos", "estan",
                 "estoy", "fin", "fue", "fueron", "fui", "fuimos", "gueno", "ha", "hace", "haceis", "hacemos", "hacen",
                 "hacer", "haces", "hago", "incluso", "intenta", "intentais", "intentamos", "intentan", "intentar",
                 "intentas", "intento", "ir", "la", "largo", "las", "lo", "los", "mientras", "mio", "modo", "muchos",
                 "muy", "nos", "nosotros", "otro", "para", "pero", "podeis", "podemos", "poder", "podria", "podriais",
                 "podriamos", "podrian", "podrias", "por", "por qué", "porque", "primero", "puede", "pueden", "puedo",
                 "quien", "sabe", "sabeis", "sabemos", "saben", "saber", "sabes", "ser", "si", "siendo", "sin", "sobre",
                 "sois", "solamente", "solo", "somos", "soy", "su", "sus", "también", "teneis", "tenemos", "tener",
                 "tengo", "tiempo", "tiene", "tienen", "todo", "trabaja", "trabajais", "trabajamos", "trabajan",
                 "trabajar", "trabajas", "trabajo", "tras", "tuyo", "ultimo", "un", "una", "unas", "uno", "unos", "usa",
                 "usais", "usamos", "usan", "usar", "usas", "uso", "va", "vais", "valor", "vamos", "van", "vaya",
                 "verdad", "verdadera", "verdadero", "vosotras", "vosotros", "voy", "yo", "él", "ésta", "éstas", "éste",
                 "éstos", "última", "últimas", "último", "últimos", "a", "añadió", "aún", "actualmente", "adelante",
                 "además", "afirmó", "agregó", "ahí", "ahora", "al", "algo", "alrededor", "anterior", "apenas",
                 "aproximadamente", "aquí", "así", "aseguró", "aunque", "ayer", "buen", "buena", "buenas", "bueno",
                 "buenos", "cómo", "casi", "cerca", "cinco", "comentó", "conocer", "consideró", "considera", "contra",
                 "cosas", "creo", "cuales", "cualquier", "cuanto", "cuatro", "cuenta", "da", "dado", "dan", "dar", "de",
                 "debe", "deben", "debido", "decir", "dejó", "del", "demás", "después", "dice", "dicen", "dicho",
                 "dieron", "diferente", "diferentes", "dijeron", "dijo", "dio", "durante", "e", "ejemplo", "ella",
                 "ello", "embargo", "encuentra", "esa", "esas", "ese", "eso", "esos", "está", "están", "estaban",
                 "estar", "estará", "estas", "este", "esto", "estos", "estuvo", "ex", "existe", "existen", "explicó",
                 "expresó", "fuera", "gran", "grandes", "había", "habían", "haber", "habrá", "hacerlo", "hacia",
                 "haciendo", "han", "hasta", "hay", "haya", "he", "hecho", "hemos", "hicieron", "hizo", "hoy", "hubo",
                 "igual", "indicó", "informó", "junto", "lado", "le", "les", "llegó", "lleva", "llevar", "luego",
                 "lugar", "más", "manera", "manifestó", "mayor", "me", "mediante", "mejor", "mencionó", "menos", "mi",
                 "misma", "mismas", "mismo", "mismos", "momento", "mucha", "muchas", "mucho", "nada", "nadie", "ni",
                 "ningún", "ninguna", "ningunas", "ninguno", "ningunos", "no", "nosotras", "nuestra", "nuestras",
                 "nuestro", "nuestros", "nueva", "nuevas", "nuevo", "nuevos", "nunca", "o", "ocho", "otra", "otras",
                 "otros", "parece", "parte", "partir", "pasada", "pasado", "pesar", "poca", "pocas", "poco", "pocos",
                 "podrá", "podrán", "podría", "podrían", "poner", "posible", "próximo", "próximos", "primer", "primera",
                 "primeros", "principalmente", "propia", "propias", "propio", "propios", "pudo", "pueda", "pues", "qué",
                 "que", "quedó", "queremos", "quién", "quienes", "quiere", "realizó", "realizado", "realizar",
                 "respecto", "sí", "sólo", "se", "señaló", "sea", "sean", "según", "segunda", "segundo", "seis", "será",
                 "serán", "sería", "sido", "siempre", "siete", "sigue", "siguiente", "sino", "sola", "solas", "solos",
                 "son", "tal", "tampoco", "tan", "tanto", "tenía", "tendrá", "tendrán", "tenga", "tenido", "tercera",
                 "toda", "todas", "todavía", "todos", "total", "trata", "través", "tres", "tuvo", "usted", "varias",
                 "varios", "veces", "ver", "vez", "y", "ya"]
"""
List of common Spanish words.
"""

DE_STOP_WORDS = ["ab", "aber", "ach", "acht", "achte", "achten", "achter", "achtes", "ag", "alle", "allein", "allem",
                 "allen", "aller", "allerdings", "alles", "allgemeinen", "als", "also", "am", "an", "andere", "anderen",
                 "andern", "anders", "au", "auch", "auf", "aus", "ausser", "außer", "ausserdem", "außerdem", "bald",
                 "bei", "beide", "beiden", "beim", "beispiel", "bekannt", "bereits", "besonders", "besser", "besten",
                 "bin", "bis", "bisher", "bist", "da", "dabei", "dadurch", "dafür", "dagegen", "daher", "dahin",
                 "dahinter", "damals", "damit", "danach", "daneben", "dank", "dann", "daran", "darauf", "daraus",
                 "darf", "darfst", "darin", "darüber", "darum", "darunter", "das", "dasein", "daselbst", "dass", "daß",
                 "dasselbe", "davon", "davor", "dazu", "dazwischen", "dein", "deine", "deinem", "deiner", "dem",
                 "dementsprechend", "demgegenüber", "demgemäss", "demgemäß", "demselben", "demzufolge", "den", "denen",
                 "denn", "denselben", "der", "deren", "derjenige", "derjenigen", "dermassen", "dermaßen", "derselbe",
                 "derselben", "des", "deshalb", "desselben", "dessen", "deswegen", "d.h", "dich", "die", "diejenige",
                 "diejenigen", "dies", "diese", "dieselbe", "dieselben", "diesem", "diesen", "dieser", "dieses", "dir",
                 "doch", "dort", "drei", "drin", "dritte", "dritten", "dritter", "drittes", "du", "durch", "durchaus",
                 "dürfen", "dürft", "durfte", "durften", "e", "eben", "ebenso", "ehrlich", "ei", "ei,", "eigen",
                 "eigene", "eigenen", "eigener", "eigenes", "ein", "einander", "eine", "einem", "einen", "einer",
                 "eines", "einige", "einigen", "einiger", "einiges", "einmal", "eins", "elf", "en", "ende", "endlich",
                 "entweder", "er", "Ernst", "erst", "erste", "ersten", "erster", "erstes", "es", "etwa", "etwas",
                 "euch", "f", "früher", "fünf", "fünfte", "fünften", "fünfter", "fünftes", "für", "g", "gab", "ganz",
                 "ganze", "ganzen", "ganzer", "ganzes", "gar", "gedurft", "gegen", "gegenüber", "gehabt", "gehen",
                 "geht", "gekannt", "gekonnt", "gemacht", "gemocht", "gemusst", "genug", "gerade", "gern", "gesagt",
                 "geschweige", "gewesen", "gewollt", "geworden", "gibt", "ging", "gleich", "gott", "gross", "groß",
                 "grosse", "große", "grossen", "großen", "grosser", "großer", "grosses", "großes", "gut", "gute",
                 "guter", "gutes", "h", "habe", "haben", "habt", "hast", "hat", "hatte", "hätte", "hatten", "hätten",
                 "heisst", "her", "heute", "hier", "hin", "hinter", "hoch", "ich", "ihm", "ihn", "ihnen", "ihr", "ihre",
                 "ihrem", "ihren", "ihrer", "ihres", "im", "immer", "indem", "infolgedessen", "ins", "irgend", "ist",
                 "ja", "jahr", "jahre", "jahren", "je", "jede", "jedem", "jeden", "jeder", "jedermann", "jedermanns",
                 "jedoch", "jemand", "jemandem", "jemanden", "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "k",
                 "kam", "kann", "kannst", "kaum", "kein", "keine", "keinem", "keinen", "keiner", "kleine", "kleinen",
                 "kleiner", "kleines", "kommen", "kommt", "können", "könnt", "konnte", "könnte", "konnten", "kurz", "l",
                 "lang", "lange", "leicht", "leide", "lieber", "los", "m", "machen", "macht", "machte", "mag", "magst",
                 "mahn", "man", "manche", "manchem", "manchen", "mancher", "manches", "mann", "mehr", "mein", "meine",
                 "meinem", "meinen", "meiner", "meines", "mensch", "menschen", "mich", "mir", "mit", "mittel", "mochte",
                 "möchte", "mochten", "mögen", "möglich", "mögt", "morgen", "muss", "muß", "müssen", "musst", "müsst",
                 "musste", "mussten", "n", "na", "nach", "nachdem", "nahm", "natürlich", "neben", "nein", "neue",
                 "neuen", "neun", "neunte", "neunten", "neunter", "neuntes", "nicht", "nichts", "nie", "niemand",
                 "niemandem", "niemanden", "noch", "nun", "nur", "o", "ob", "oben", "oder", "offen", "oft", "ohne",
                 "Ordnung", "p", "q", "r", "recht", "rechte", "rechten", "rechter", "rechtes", "richtig", "rund", "s",
                 "sa", "sache", "sagt", "sagte", "sah", "satt", "schlecht", "Schluss", "schon", "sechs", "sechste",
                 "sechsten", "sechster", "sechstes", "sehr", "sei", "seid", "seien", "sein", "seine", "seinem",
                 "seinen", "seiner", "seines", "seit", "seitdem", "selbst", "sich", "sie", "sieben", "siebente",
                 "siebenten", "siebenter", "siebentes", "sind", "solang", "solche", "solchem", "solchen", "solcher",
                 "solches", "soll", "sollen", "sollte", "sollten", "sondern", "sonst", "sowie", "später", "statt",
                 "tag", "tage", "tagen", "tat", "teil", "tel", "tritt", "trotzdem", "tun", "u", "über", "überhaupt",
                 "übrigens", "uhr", "um", "und", "und?", "uns", "unser", "unsere", "unserer", "unter", "v",
                 "vergangenen", "viel", "viele", "vielem", "vielen", "vielleicht", "vier", "vierte", "vierten",
                 "vierter", "viertes", "vom", "von", "vor", "w", "wahr?", "während", "währenddem", "währenddessen",
                 "wann", "war", "wäre", "waren", "wart", "warum", "was", "wegen", "weil", "weit", "weiter", "weitere",
                 "weiteren", "weiteres", "welche", "welchem", "welchen", "welcher", "welches", "wem", "wen", "wenig",
                 "wenige", "weniger", "weniges", "wenigstens", "wenn", "wer", "werde", "werden", "werdet", "wessen",
                 "wie", "wieder", "will", "willst", "wir", "wird", "wirklich", "wirst", "wo", "wohl", "wollen", "wollt",
                 "wollte", "wollten", "worden", "wurde", "würde", "wurden", "würden", "x", "y", "z", "z.b", "zehn",
                 "zehnte", "zehnten", "zehnter", "zehntes", "zeit", "zu", "zuerst", "zugleich", "zum", "zunächst",
                 "zur", "zurück", "zusammen", "zwanzig", "zwar", "zwei", "zweite", "zweiten", "zweiter", "zweites",
                 "zwischen", "zwölf", "euer", "eure", "hattest", "hattet", "jedes", "mußt", "müßt", "sollst", "sollt",
                 "soweit", "weshalb", "wieso", "woher", "wohin"]
"""
List of common German words.
"""

LANG_EXAMPLES = {'en': "My taylor is rich.",
                 "fr": "La vie est belle.",
                 'es': "Hasta la vista aqui.",
                 'de': "Der Erlkönig tut mir leid."}
"""Small sentences written in different languages."""


THRESHOLD = 2

MAP_LANG_STOP_WORDS = {
    "en": EN_STOP_WORDS,
    "fr": FR_STOP_WORDS,
    "es": ES_STOP_WORDS,
    "de": DE_STOP_WORDS
}


def guess_language_ext(text, map_lang_stop_words=None):
    """
    Computes the number of stopwords of each language in the sentence.

    Parameters
    ----------
    text: :class:`str`
        Text to analyze.
    map_lang_stop_words: :class:`dict`, optional
        Common words for different languages.

    Returns
    -------
    :class:`dict`
        Number of words from each considered language.

    Examples
    --------

    >>> for k, v in LANG_EXAMPLES.items():
    ...     print(f"{k}: {v}")
    ...     print(dict(guess_language_ext(v)))
    en: My taylor is rich.
    {'en': 2, 'fr': 0, 'es': 0, 'de': 0}
    fr: La vie est belle.
    {'en': 0, 'fr': 2, 'es': 1, 'de': 0}
    es: Hasta la vista aqui.
    {'en': 0, 'fr': 1, 'es': 3, 'de': 0}
    de: Der Erlkönig tut mir leid.
    {'en': 0, 'fr': 0, 'es': 0, 'de': 2}
    """
    if map_lang_stop_words is None:
        map_lang_stop_words = MAP_LANG_STOP_WORDS
    map_lang_num_stop_words = defaultdict(lambda: 0)
    vocab = set(words(text))
    for (lang, stop_words) in map_lang_stop_words.items():
        map_lang_num_stop_words[lang] += len(vocab & set(stop_words))

    return map_lang_num_stop_words


def guess_language(text, map_lang_stop_words=None) -> str:
    """
    Recognises the language of the text by looking at common words.

    Parameters
    ----------
    text: :class:`str`
        Text to analyze.
    map_lang_stop_words: :class:`dict`, optional
        Common words for different languages.

    Returns
    -------
    :class:`str`
        Two-letters code for the language.

    Examples
    --------
    >>> for k, v in LANG_EXAMPLES.items():
    ...     print(f"{v} ({k})")
    ...     print(f"Guessed language: {guess_language(v)}")
    My taylor is rich. (en)
    Guessed language: en
    La vie est belle. (fr)
    Guessed language: fr
    Hasta la vista aqui. (es)
    Guessed language: es
    Der Erlkönig tut mir leid. (de)
    Guessed language: de
    """
    if map_lang_stop_words is None:
        map_lang_stop_words = MAP_LANG_STOP_WORDS
    map_lang_num_stop_words = guess_language_ext(text, map_lang_stop_words)
    best_score = 0
    best_lang = None
    for (lang, n) in map_lang_num_stop_words.items():
        if n > best_score:
            best_score = n
            best_lang = lang
    return best_lang
