gap = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': 'gap',
    'shuffle': True,
    'instances': 1,
    'gap_length': 20,
}}

task = """ description

[gap(1.0P)]Answer A, Answer B, Answer C[/gap]

This is a numeric gap and follows the syntax: <value>(,<min>,<max>)
[numeric(1.0P)]5, 0, 10[/numeric]

[select]
[ ] Answer A
[2] Answer B
[4] Answer C
[/select]

"""

feedback = """ feedback """
'''

order = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': 'order',
    'instances': 1,
    'points': {}, # total number of points
}}

task = """ decription """

order = """ Answer A -- Answer B -- Answer C """

feedback = """ feedback """
'''

choice = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': '{}',
    'instances': 1,
    'shuffle': True,
    'points': {}, # points per correct question
}}

task = """ decription """

choices = """
    [ ] Answer A
    [ ] Answer B
    [X] Answer C
"""

feedback = """ feedback """
'''

free = r'''meta = {{
    'author': '{}',
    'title': '{}',
    'type': 'free',
    'instances': 1,
    'points': {},
}}

task = """ decription """

feedback = """ feedback """
'''

javaScript = r'''meta = {{
    'author': '{author}',
    'title': '{title}',
    'type': 'javaScript',
    'instances': 1,
}}

# Hier ein einfaches Beispiel zur Vorverarbeitung von Eingaben um irrelevante Schreibunterschiede zu ignorieren

task = """ In die folgende Eingabezeile, kann man 'Korrekt' oder 'Okay' für Punkte schreiben. Dabei wird nicht auf Groß- und Kleinschreibung geachtet, auch Sonderzeichen werden ignoriert:
[textField(dasEingabefeld)]30,20[/textField]
In dieses Textfeld kann man 30 Zeichen schreiben, aber nur 20 werden garantiert ohne Scrollen im Eingabefeld angezeigt.
"""

correctAnswers = """
Answer korrekt : 100.0P
Answer okay : 50.0P
"""

# Um die Voraussetzungen zu erfüllen, sind die korrekten Antworten Sonderzeichenlos und vollkommen klein geschrieben.
# Nun kann man mit allen Eingaben gleich umgehen.

javaScriptCode = """
function newEval(){ // Erstellung eines neuen Evaluators
  var userInput = HGInput("dasEingabefeld").HGGetter(); // Wert des Eingabefelds lesen
  userInput = userInput.replace(/\\W/g, ""); // nicht-alphanumerische Symbole entfernen (bis auf _), man beachte das escaping des Backslashs, da wir am Ende einen Backslashs haben wollen, aber dies schon ein Python-String ist (alternativ kann auch ein raw string benutzt werden)
  userInput = userInput.replace("_", ""); // nun auch "_" entfernen
  userInput = userInput.toLowerCase(); // zum Schluss noch alles auf Kleinschreibung setzen
  HGOutput("answer").HGSetter(userInput); // die abgewandelte Antwort wird als tatsächliche Antwort gesetzt und diese wird so auch von ILIAS bewertet
}

HGRegisterEvaluator(newEval); // Registration des Evaluators
"""

feedback = """ feedback """
'''

config_sample = """[META]
author = {}
output = {}

[UPLAODER]
user = root
pass = homer
host = http://localhost:8000/ilias/
rtoken = c13456ec3d71dc657e19fb826750f676
"""


