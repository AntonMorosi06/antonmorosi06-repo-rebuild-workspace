from __future__ import annotations

from dataclasses import dataclass, field
import random

from .text_utils import normalize_text


@dataclass
class Intent:
    name: str
    keywords: list[str]
    responses: list[str]
    weight: int = 1
    examples: list[str] = field(default_factory=list)


def default_intents() -> list[Intent]:
    return [
        Intent(
            name="greeting",
            keywords=["ciao", "buongiorno", "buonasera", "salve", "hey", "ehi"],
            responses=[
                "Ciao, sono qui. Dimmi pure cosa vuoi fare.",
                "Ciao Anton, pronto. Possiamo ragionare sul progetto, sullo studio o su una demo.",
                "Eccomi. Scrivimi o parlami e provo a risponderti in modo semplice.",
            ],
            examples=["ciao", "buongiorno"],
        ),
        Intent(
            name="identity",
            keywords=["chi sei", "cosa sei", "presentati", "come ti chiami"],
            responses=[
                "Sono un piccolo chatbot italiano ricostruito come progetto educativo. Non sono un modello generativo completo: rispondo tramite regole, intenti e frasi preparate.",
                "Sono una baseline di assistente vocale italiano. Posso funzionare in modalità testo e, se le librerie audio sono installate, anche in modalità voce.",
            ],
            examples=["chi sei?", "presentati"],
        ),
        Intent(
            name="microbot",
            keywords=["microbot", "micro bot", "robot", "sciame", "swarm", "telemetria", "esp32", "drone"],
            responses=[
                "MicroBot può essere spiegato come un ecosistema modulare: simulazione, firmware, dashboard, telemetria, prototipi fisici e documentazione tecnica devono restare separati ma coerenti.",
                "Per MicroBot conviene distinguere sempre ciò che è simulato, ciò che è preparato, ciò che è testato offline e ciò che è validato su hardware reale.",
                "Un assistente vocale come questo potrebbe diventare una piccola interfaccia di comando per dashboard, telemetria o demo, ma solo dopo avere definito bene sicurezza e limiti operativi.",
            ],
            examples=["parlami di microbot", "come collego il chatbot al drone?"],
        ),
        Intent(
            name="study",
            keywords=["studio", "esame", "universita", "fondamenti", "algoritmica", "algebra", "laboratorio", "ripasso"],
            responses=[
                "Per studiare bene conviene fare tre passaggi: prima teoria sintetica, poi esercizi guidati, poi simulazione senza guardare. Dopo si corregge con calma.",
                "Se devi preparare un esame, la cosa migliore è alternare definizioni formali, esercizi piccoli e prove complete a tempo.",
                "Non serve fare tutto perfetto al primo giro. Serve costruire continuità: un blocco al giorno, correzione chiara e ripetizione degli errori tipici.",
            ],
            examples=["aiutami a studiare", "devo fare fondamenti"],
        ),
        Intent(
            name="motivation",
            keywords=["sono perso", "non riesco", "paura", "ansia", "fallire", "solo", "bloccato"],
            responses=[
                "Capisco. Però il fatto che tu stia ordinando repo, studio e progetti non è niente: è lavoro vero. Va spezzato in passi più piccoli, non giudicato tutto insieme.",
                "Quando ti senti bloccato, riduci il problema: un file, un commit, un esercizio, una pagina. Il movimento torna da lì.",
                "Non devi dimostrare tutto oggi. Devi solo non buttare via il filo. Anche un piccolo avanzamento fatto bene conta.",
            ],
            examples=["mi sento perso", "ho paura di non farcela"],
        ),
        Intent(
            name="help",
            keywords=["aiuto", "help", "comandi", "cosa posso dire", "istruzioni"],
            responses=[
                "Puoi chiedermi cose come: parlami di MicroBot, aiutami a studiare, motivami, spiegami il progetto, oppure puoi scrivere esci per chiudere.",
                "Comandi utili: /help mostra aiuto, /save salva il transcript, esci chiude la conversazione.",
            ],
            examples=["/help", "che comandi ci sono?"],
        ),
        Intent(
            name="privacy",
            keywords=["privacy", "microfono", "registri", "audio", "dati", "salvi"],
            responses=[
                "La modalità testo non usa il microfono. La modalità voce dipende dalle librerie installate e dal backend di riconoscimento. Per test sicuri evita dati personali.",
                "Il transcript viene salvato solo quando il programma lo scrive nella cartella transcripts. Per una demo pubblica conviene usare frasi neutre e non private.",
            ],
            examples=["usi il microfono?", "salvi i dati?"],
        ),
        Intent(
            name="thanks",
            keywords=["grazie", "ti ringrazio", "perfetto", "grande", "ottimo"],
            responses=[
                "Figurati, andiamo avanti con calma e precisione.",
                "Di nulla. Passo dopo passo viene fuori una cosa ordinata.",
                "Perfetto, continuiamo così.",
            ],
            examples=["grazie", "ottimo"],
        ),
        Intent(
            name="goodbye",
            keywords=["ciao", "a dopo", "arrivederci", "esci", "chiudi", "quit", "exit"],
            responses=[
                "Va bene, chiudo la conversazione. A dopo.",
                "Ok, ci sentiamo dopo.",
            ],
            examples=["esci", "a dopo"],
        ),
    ]


def score_intent(message: str, intent: Intent) -> int:
    normalized = normalize_text(message)
    if not normalized:
        return 0

    score = 0
    for keyword in intent.keywords:
        normalized_keyword = normalize_text(keyword)
        if normalized_keyword and normalized_keyword in normalized:
            score += intent.weight + len(normalized_keyword.split())

    return score


def classify_intent(message: str, intents: list[Intent] | None = None) -> Intent | None:
    intents = intents or default_intents()
    scored = [(score_intent(message, intent), intent) for intent in intents]
    scored.sort(key=lambda item: item[0], reverse=True)

    if not scored or scored[0][0] <= 0:
        return None

    return scored[0][1]


def response_for_intent(intent: Intent | None) -> str:
    if intent is None:
        return random.choice(
            [
                "Non sono sicuro di avere capito. Puoi riformularlo in modo più semplice?",
                "Questa cosa non è ancora nel mio set di regole. Posso però rispondere su studio, MicroBot, privacy, motivazione o uso del chatbot.",
                "Non ho trovato un intento preciso. Per ora sono un chatbot rule-based, quindi funziono meglio con frasi dirette.",
            ]
        )

    return random.choice(intent.responses)
