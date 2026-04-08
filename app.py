import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
# Ein geheimer Schlüssel ist für 'session' notwendig (einfach ein langer String)
app.secret_key = 'superdupersecretpassword'

# Wir erlauben GET (Seite laden) POST (Formular abschicken)
@app.route('/', methods=['GET', 'POST'])

def home():

    # 1. Wenn das Spiel startet (oder nur geladen wird) und keine Zahl da ist
    if 'geheimzahl' not in session:
        session['geheimzahl'] = random.randint(1, 100)
        session['versuche'] = 0
        session['meldung'] = "Ich habe mir eine Zahl zwischen 1 und 100 ausgedacht."



    # ... 

    if request.method == 'POST':
        try:
            # Eingabe
            tipp = int(request.form.get('nutzer_eingabe'))
            session['versuche'] += 1
            
            # beim ersten Versuch wird die Liste 'geratene_zahlen' erstellt
            if 'geratene_zahlen' not in session:
                session['geratene_zahlen'] = []

            # Wir nehmen einen Umweg über eine lokale Variable 'liste',
            # damit Flask die Änderung sicher bemerkt.
            liste = session['geratene_zahlen']
            liste.append(tipp)
            session['geratene_zahlen'] = liste
            # ----------------------------------------------------------------------------------------

            # hier kommt die Logik aus dem Konsolentool rein:
            if tipp < session['geheimzahl']:
                session['meldung'] = f"Versuch {session['versuche']}: Zu niedrig! ❄️"
            elif tipp > session['geheimzahl']:
                session['meldung'] = f"Versuch {session['versuche']}: Zu hoch! 🔥"
            else:
                session['meldung'] = f"Glückwunsch! Erraten in {session['versuche']} Versuchen! ⚡"
                
                # Spiel zurücksetzen
                session.pop('geheimzahl')
                session.pop('geratene_zahlen')
                session.pop('versuche')

        except (TypeError, ValueError):
            session['meldung'] = "Bitte gib eine gültige Zahl ein!"

    return render_template('index.html', ausgabe=session['meldung'])

if __name__ == '__main__':
    app.run(debug=True)