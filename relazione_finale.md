# RELAZIONE FINALE - PROGETTO ANALISI SENTIMENT AUTO REVIEWS

## 1. Descrizione delle Fasi Svolte

### a. Analisi Esplorativa dei Dati (EDA)
- Raccolta e validazione di 205 recensioni auto tramite scraping ([notebooks/scraping.ipynb](notebooks/scraping.ipynb)).
- Analisi distribuzione brand, correlazione prezzo-rating, identificazione pattern di sentiment ([analisi_EDA.ipynb](analisi_EDA.ipynb)).

### b. Progettazione Architettura
- Definizione schema database relazionale normalizzato ([db/database.py](db/database.py)).
- Scelta di SQLite per semplicità e portabilità ([db/auto_reviews.db](db/auto_reviews.db)).
- Gestione configurazioni tramite environment variables ([.env.vars](.env.vars)).

### c. UX/UI e Sviluppo Dashboard
- Progettazione dashboard interattiva con Streamlit ([app.py](app.py)).
- Layout multi-tab, filtri avanzati, visualizzazioni comparative e KPI business-oriented.
- Color coding e iconografie per immediatezza e chiarezza.

### d. Sviluppo e Testing
- Pipeline di scraping, preprocessing e sentiment analysis ([pre_processing.ipynb](pre_processing.ipynb)).
- Testing funzionale su tutte le componenti: scraping, AI, dashboard, database.
- Validazione automatica delle risposte AI e gestione errori.

---

## 2. Motivazione delle Scelte Tecniche

- **Database**: SQLite scelto per zero-config, embedded e performance su dataset medio-piccoli.
- **Connettori**: Gestione centralizzata delle connessioni per robustezza e manutenibilità.
- **Metodo di pubblicazione**: Deploy locale tramite Streamlit per rapidità e semplicità demo.
- **AI locale**: Ollama per privacy, controllo e costi ridotti rispetto a servizi cloud.
- **Prompt engineering**: Strutturazione dei prompt per massimizzare coerenza e accuratezza delle risposte AI.
- **Visualizzazione**: Plotly per grafici interattivi e Pandas per manipolazione dati.

---

## 3. Difficoltà Incontrate e Soluzioni Adottate

- **Parsing incoerente delle risposte AI**  
  → Implementato sistema di retry con prompt modificati e cleaning automatico delle risposte.
- **Errori di sintassi JSON**  
  → Funzione di pulizia con regex e fallback su valori di default.
- **Gestione dati mancanti**  
  → Validazione automatica e fallback per evitare interruzioni della pipeline.
- **Rate limiting durante scraping**  
  → Delay automatici e gestione delle eccezioni di rete.
- **Testing**  
  → Test funzionali su ogni fase, validazione manuale e automatica dei risultati.

---

## 4. Processo Operativo e Decisionale

Ogni scelta è stata guidata da:
- Semplicità e rapidità di sviluppo (time-to-market).
- Robustezza e riproducibilità della pipeline.
- Scalabilità futura (integrazione nuove fonti e modelli AI).
- Focus su valore business e immediatezza degli insight.

---

## 5. Risultati e Prospettive Future

- **Risultati**: Dashboard pronta all’uso, pipeline riproducibile, insight strategici per i brand europei.
- **Limiti**: Dataset UK-only, AI single model, assenza dati temporali.
- **Roadmap**: Espansione fonti dati, modelli ML avanzati, pipeline real-time, analisi multi-mercato.

---