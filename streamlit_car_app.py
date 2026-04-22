import streamlit as st
import streamlit.components.v1 as com
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import time
import requests
import os

DATA_DIR = os.path.dirname(os.path.abspath('__file__'))



#----------------------------------------------------- All Dictionary ----------------------------------------------------------------
#----------------------------------------------------------Tab 1 ----------------------------------------------------------------
# translations dictionary
translations = {
    "project_title": {
        "en": "<div style='text-align: center;'><h1>Car Accident Analysis in Germany</h1><h3><br>An exploratory analysis of car accidents and weather impacts in Germany (2021–2023)</h3></div>",
        "de": "<div style='text-align: center;'><h1>Analyse von Autounfällen in Deutschland</h1><h3><br>Eine explorative Analyse von Verkehrsunfällen und Wettereinflüssen in Deutschland (2021–2023)</h3></div>"
    },
    "summary_heading": {
        "en": "## 📈Project Summary",
        "de": "## 📈Projektzusammenfassung"
    },
"summary_body": {
        "en":
            """This project analyzes car accidents in Germany (2021–2023) to identify key causes, patterns, and weather-related risks.
               We uncover high-risk areas, times, and conditions, and propose recommendations to improve road safety, aligned with Germany’s Vision Zero initiative.
            """,
        "de":
            """Dieses Projekt analysiert Verkehrsunfälle in Deutschland (2021–2023), um zentrale Ursachen, Muster und wetterbedingte Risiken zu identifizieren.
               Wir decken Hochrisikogebiete, -zeiten und -bedingungen auf und schlagen Empfehlungen zur Verbesserung der Verkehrssicherheit vor – im Einklang mit der Vision-Zero-Initiative Deutschlands.
            """
    },
    "introduction_heading": {
        "en": "## Introduction and Objectives",
        "de": "## Einführung und Ziele"
    },
"intro_text_1": {
"en": """### Objectives
- Identify major causes and contributing factors of car accidents
- Explore spatial and temporal trends (when and where accidents occur)
- Assess the role of weather in accident severity
- Provide recommendations to support safer roads in Germany""",
"de": """### Ziele
- Zentrale Ursachen und beitragende Faktoren von Verkehrsunfällen identifizieren  
- Räumliche und zeitliche Muster untersuchen (wann und wo Unfälle auftreten)  
- Die Rolle des Wetters bei der Unfallschwere bewerten  
- Empfehlungen zur Unterstützung sichererer Straßen in Deutschland geben"""
    },
    "introduction_heading_2": {
        "en": "## Data Sources:",
        "de": "## Datenquellen:"
    },
    "intro_text_2": {
        "en": """
    - Accident data: from Statistische Ämter des Bundes und der Länder (Germany’s official statistics)
      Visit [STATISTISCHE ÄMTER](https://unfallatlas.statistikportal.de/) for more information.
    - Weather data: from Open-Meteo API (hourly & daily, 2021–2023)""",
        "de": """
    - Unfalldaten: von den Statistischen Ämtern des Bundes und der Länder (offizielle Statistik Deutschlands)
      Besuchen Sie uns [STATISTISCHE ÄMTER](https://unfallatlas.statistikportal.de/) für weitere Informationen.
    - Wetterdaten: von der Open-Meteo-API (stündlich & täglich, 2021–2023)"""
    },
    "project_matters" : {
        "en": "## Why this project matters?",
        "de": "## Warum dieses Projekt wichtig ist?"
    },
    "answer"  : {
        "en": """##### *Even if the end of the world is at hand, if you have an opportunity to do something good, no matter how small, you should still do it.*
I believe that data analysis can be one of those “small but meaningful” actions.
This project may not change the world, but if it can contribute even a little to reducing accidents and saving lives, then it already matters.""",
        "de" :"""##### *Selbst wenn das Ende der Welt bevorsteht, wenn du die Möglichkeit hast, etwas Gutes zu tun, egal wie klein, solltest du es trotzdem tun.*
Ich glaube, dass Datenanalyse eine dieser „kleinen, aber bedeutungsvollen“ Handlungen sein kann.
Dieses Projekt wird die Welt vielleicht nicht verändern, aber wenn es auch nur ein wenig dazu beiträgt, Unfälle zu verringern und Leben zu retten, dann ist es bereits von Bedeutung."""
    },
#-----------------------------------------------------------------Tab 2 ----------------------------------------------------------------
"tab2_title": {
    "en": "## 🛠️ Our Data Journey",
    "de": "## 🛠️ Unsere Datenreise"
},
"tab2_subtitle": {
    "en": "### From raw numbers to meaningful insights — the challenges we solved",
    "de": "### Von rohen Zahlen zu bedeutungsvollen Erkenntnissen — die Herausforderungen, die wir gelöst haben"
},
"challenge_title": {
    "en": "## ⚔️ 6 Real Challenges We Faced",
    "de": "## ⚔️ 6 echte Herausforderungen, denen wir begegnet sind"
},
"c1_title": {"en": "🔤 Challenge 1 — German Column Names", "de": "🔤 Herausforderung 1 — Deutsche Spaltennamen"},
"c1_problem": {"en": "❌ **Problem:** All column names were in German — ULAND, UKREIS, USTUNDE, UWOCHENTAG...", "de": "❌ **Problem:** Alle Spaltennamen waren auf Deutsch — ULAND, UKREIS, USTUNDE, UWOCHENTAG..."},
"c1_solution": {"en": "💡 **Solution:** Researched every column in official German statistics documentation and translated all names to English for international readability.", "de": "💡 **Lösung:** Jede Spalte in der offiziellen deutschen Statistikdokumentation recherchiert und alle Namen ins Englische übersetzt."},
"c1_result": {"en": "✅ **Result:** Clean, readable column names — state, district, hour, day, category", "de": "✅ **Ergebnis:** Saubere, lesbare Spaltennamen — state, district, hour, day, category"},

"c2_title": {"en": "🔢 Challenge 2 — Mystery Codes Instead of Names", "de": "🔢 Herausforderung 2 — Mysteriöse Codes statt Namen"},
"c2_problem": {"en": "❌ **Problem:** Everything was numbers — states, districts, municipalities, accident types. Example: ULAND=1, UKREIS=54, UGEMEINDE=165", "de": "❌ **Problem:** Alles waren Zahlen — Bundesländer, Bezirke, Gemeinden, Unfalltypen. Beispiel: ULAND=1, UKREIS=54, UGEMEINDE=165"},
"c2_solution": {"en": "💡 **Solution:** Researched Germany's official Amtlicher Gemeindeschlüssel (AGS) system — an 8-digit code structure. Built a custom lookup table mapping every code to real state, district and city names.", "de": "💡 **Lösung:** Deutsches Amtliches Gemeindeschlüssel (AGS) System recherchiert — eine 8-stellige Codestruktur. Eine eigene Lookup-Tabelle erstellt, die jeden Code echten Bundes-, Bezirks- und Stadtnamen zuordnet."},
"c2_result": {"en": "✅ **Result:** Every accident now has real location names — nordrhein-westfalen, berlin, münchen", "de": "✅ **Ergebnis:** Jeder Unfall hat jetzt echte Ortsnamen — nordrhein-westfalen, berlin, münchen"},

"c3_title": {"en": "📅 Challenge 3 — Missing Exact Dates", "de": "📅 Herausforderung 3 — Fehlende genaue Datumsangaben"},
"c3_problem": {"en": "❌ **Problem:** Accident dataset had no exact day — only year, month and weekday (e.g. 2021, June, Monday). Impossible to match with hourly weather without exact date.", "de": "❌ **Problem:** Der Unfalldatensatz hatte kein genaues Datum — nur Jahr, Monat und Wochentag (z.B. 2021, Juni, Montag). Ohne genaues Datum unmöglich, mit stündlichen Wetterdaten abzugleichen."},
"c3_solution": {"en": "💡 **Solution:** Built a date estimation algorithm — find the first occurrence of the given weekday in that month and combine with accident hour to create a full timestamp.", "de": "💡 **Lösung:** Datumsschätzungsalgorithmus entwickelt — erstes Vorkommen des angegebenen Wochentags im Monat finden und mit der Unfallstunde kombinieren, um einen vollständigen Zeitstempel zu erstellen."},
"c3_result": {"en": "✅ **Result:** 782,642 accidents now have estimated full datetime — ready for weather matching", "de": "✅ **Ergebnis:** 782.642 Unfälle haben jetzt geschätzte vollständige Datums-/Zeitangaben — bereit für den Wetterabgleich"},

"c4_title": {"en": "💾 Challenge 4 — Weather Data Too Big (3 Days!)", "de": "💾 Herausforderung 4 — Wetterdaten zu groß (3 Tage!)"},
"c4_problem": {"en": "❌ **Problem:** Hourly weather data for Germany 2021-2023 = 2.6GB total. Took 3 days to download. Loading everything at once crashes any computer.", "de": "❌ **Problem:** Stündliche Wetterdaten für Deutschland 2021-2023 = insgesamt 2,6 GB. Download dauerte 3 Tage. Alles auf einmal zu laden, bringt jeden Computer zum Absturz."},
"c4_solution": {"en": "💡 **Solution:** Smart design decision — combine daily weather (small, ~136MB) for statistical analysis. Keep hourly files separate per year (~900MB each) and load only when needed for the animated map.", "de": "💡 **Lösung:** Intelligente Designentscheidung — tägliche Wetterdaten (klein, ~136MB) für statistische Analysen zusammenführen. Stündliche Dateien getrennt pro Jahr (~900MB) halten und nur bei Bedarf für die animierte Karte laden."},
"c4_result": {"en": "✅ **Result:** No crashes, fast analysis, smart memory management", "de": "✅ **Ergebnis:** Keine Abstürze, schnelle Analyse, intelligentes Speichermanagement"},

"c5_title": {"en": "🕐 Challenge 5 — Wrong Timezone (UTC vs Berlin)", "de": "🕐 Herausforderung 5 — Falsche Zeitzone (UTC vs. Berlin)"},
"c5_problem": {"en": "❌ **Problem:** Open-Meteo weather data stored in UTC. Germany uses UTC+1 (UTC+2 in summer). Without correction, every accident matched to wrong weather hour — 1-2 hours off!", "de": "❌ **Problem:** Open-Meteo Wetterdaten in UTC gespeichert. Deutschland verwendet UTC+1 (UTC+2 im Sommer). Ohne Korrektur wurde jeder Unfall der falschen Wetterstunde zugeordnet — 1-2 Stunden daneben!"},
"c5_solution": {"en": "💡 **Solution:** Implemented precise timezone conversion using Europe/Berlin timezone — correctly handles both winter (UTC+1) and summer (UTC+2) time automatically.", "de": "💡 **Lösung:** Präzise Zeitzonenkonvertierung mit Europe/Berlin-Zeitzone implementiert — verarbeitet automatisch sowohl Winter- (UTC+1) als auch Sommerzeit (UTC+2)."},
"c5_result": {"en": "✅ **Result:** Every accident matched to correct weather hour — accurate analysis", "de": "✅ **Ergebnis:** Jeder Unfall der richtigen Wetterstunde zugeordnet — genaue Analyse"},

"c6_title": {"en": "📍 Challenge 6 — Matching 782,642 Accidents to Weather", "de": "📍 Herausforderung 6 — 782.642 Unfälle mit Wetter abgleichen"},
"c6_problem": {"en": "❌ **Problem:** How to match nearly 800,000 accidents to exact weather at that location and time? Pandas merge would crash with 2.6GB of weather data.", "de": "❌ **Problem:** Wie fast 800.000 Unfälle dem genauen Wetter an diesem Ort und zu dieser Zeit zuordnen? Pandas-Merge würde mit 2,6 GB Wetterdaten abstürzen."},
"c6_solution": {"en": "💡 **Solution:** Used DuckDB — an in-process SQL engine that handles large CSV files without loading into RAM. SQL join on date + hour + rounded coordinates (2 decimal places).", "de": "💡 **Lösung:** DuckDB verwendet — eine In-Process-SQL-Engine, die große CSV-Dateien verarbeitet, ohne sie in den RAM zu laden. SQL-Join auf Datum + Stunde + gerundete Koordinaten (2 Dezimalstellen)."},
"c6_result": {"en": "✅ **Result:** 99.7% match rate — 888,414 out of 891,257 accidents have exact weather data", "de": "✅ **Ergebnis:** 99,7% Trefferquote — 888.414 von 891.257 Unfällen haben genaue Wetterdaten"},

"tab2_final": {
    "en": """### 🎯 The Result of All This Work

After solving all 6 challenges, we ended up with a unique dataset:
- **782,642 accidents** with clean, readable data
- **Every accident** linked to exact weather conditions
- **99.7% weather match** — rain, temperature, wind at moment of accident
- **Real location names** — not just codes
- **Full timestamps** — ready for hour-by-hour analysis

This foundation made everything else possible — the maps, the patterns, and the Gemma 4 insights.""",
    "de": """### 🎯 Das Ergebnis all dieser Arbeit

Nach der Lösung aller 6 Herausforderungen haben wir einen einzigartigen Datensatz:
- **782.642 Unfälle** mit sauberen, lesbaren Daten
- **Jeder Unfall** mit genauen Wetterbedingungen verknüpft
- **99,7% Wetterabgleich** — Regen, Temperatur, Wind zum Unfallzeitpunkt
- **Echte Ortsnamen** — nicht nur Codes
- **Vollständige Zeitstempel** — bereit für stündliche Analyse

Diese Grundlage machte alles andere möglich — die Karten, die Muster und die Gemma 4 Erkenntnisse."""
},
    # -------------------------------------------Tab 3 ----------------------------------------------------------------------------
"tab3_title": {
    "en": "## 📊 Exploratory Data Analysis",
    "de": "## 📊 Explorative Datenanalyse"
},
"tab3_subtitle": {
    "en": "### Interactive charts revealing patterns in 782,642 German accidents",
    "de": "### Interaktive Diagramme zeigen Muster in 782.642 deutschen Unfällen"
},
"chart1_title": {
    "en": "### 🕐 24-Hour Accident Cycle by State",
    "de": "### 🕐 24-Stunden-Unfallzyklus nach Bundesland"
},
"chart1_desc": {
    "en": "Press play to see how accidents change hour by hour across all German states. Notice the rush hour peaks and the dangerous late night hours.",
    "de": "Drücke Play, um zu sehen, wie sich Unfälle stündlich in allen Bundesländern verändern. Beachte die Stoßzeiten-Spitzen und die gefährlichen späten Nachtstunden."
},
"chart2_title": {
    "en": "### 🗺️ Accidents by Year / State / Category",
    "de": "### 🗺️ Unfälle nach Jahr / Bundesland / Kategorie"
},
"chart2_desc": {
    "en": "Click any block to drill down into states and accident categories. The size shows total accidents — the color shows intensity.",
    "de": "Klicke auf einen Block, um in Bundesländer und Unfallkategorien einzutauchen. Die Größe zeigt Gesamtunfälle — die Farbe zeigt die Intensität."
},
"chart3_title": {
    "en": "### 📅 Total Accidents by Day and State",
    "de": "### 📅 Gesamtunfälle nach Tag und Bundesland"
},
"chart3_desc": {
    "en": "Friday dominates in total accidents. But remember — Sunday has the highest FATAL rate. Hover over any bar to see exact numbers.",
    "de": "Freitag dominiert bei den Gesamtunfällen. Aber denke daran — Sonntag hat die höchste TODESRATE. Fahre über einen Balken für genaue Zahlen."
},
    # ------------------------------------------------------------Tab 4 -----------------------------------------------------------
"tab4_title": {
    "en": "## 🗺️ Weather & Accidents Map",
    "de": "## 🗺️ Wetter & Unfallkarte"
},
"tab4_subtitle": {
    "en": "### Every dot is a real accident — hover to see exact weather conditions at that moment",
    "de": "### Jeder Punkt ist ein echter Unfall — fahre darüber, um die genauen Wetterbedingungen zu sehen"
},
"tab4_desc": {
    "en": """
- 🔴 **Red** = Fatal accident (killed)
- 🟠 **Orange** = Seriously injured  
- 🟡 **Yellow** = Slightly injured
- 📍 Sample of 50,000 accidents shown for performance
- 🌤️ Hover over any point to see: weather, temperature, rain, wind
""",
    "de": """
- 🔴 **Rot** = Tödlicher Unfall
- 🟠 **Orange** = Schwer verletzt
- 🟡 **Gelb** = Leicht verletzt
- 📍 50.000 Unfälle als Stichprobe für Performance
- 🌤️ Fahre über einen Punkt: Wetter, Temperatur, Regen, Wind
"""
},
"tab4_insight": {
    "en": "### 💡 What to look for",
    "de": "### 💡 Worauf du achten solltest"
},
"tab4_insight_body": {
    "en": """
- **Zoom into NRW** (west) — highest accident density
- **Zoom into East Germany** — fewer accidents but more red dots (fatal)
- **Hover over red dots** — notice the weather conditions when people died
- **Compare urban vs rural** — different accident patterns
""",
    "de": """
- **Zoom in NRW** (Westen) — höchste Unfalldichte
- **Zoom in Ostdeutschland** — weniger Unfälle aber mehr rote Punkte
- **Fahre über rote Punkte** — beachte Wetterbedingungen bei tödlichen Unfällen
- **Vergleiche Stadt vs Land** — unterschiedliche Unfallmuster
"""
},
    # ---------------------------------------------Tab 5 ---------------------------------------------------------------------------
"tab5_title": {
    "en": "## 🤖 Key Findings & Gemma 4 Analysis",
    "de": "## 🤖 Wichtigste Erkenntnisse & Gemma 4 Analyse"
},
"tab5_subtitle": {
    "en": "### AI-powered insights from 782,642 accidents — running 100% offline via Ollama",
    "de": "### KI-gestützte Erkenntnisse aus 782.642 Unfällen — läuft 100% offline via Ollama"
},
"findings_title": {
    "en": "## 🔍 Key Discoveries",
    "de": "## 🔍 Wichtigste Entdeckungen"
},
"finding1_title": {
    "en": "🗓️ Discovery 1 — Sunday is More Deadly Than Friday",
    "de": "🗓️ Entdeckung 1 — Sonntag ist tödlicher als Freitag"
},
"finding1_body": {
    "en": """Everyone assumes Friday is the most dangerous day.
Our data proves otherwise:
- **Friday:** 146,410 accidents — highest volume
- **Sunday:** 81,594 accidents — but **1.27% fatal rate**
- Sunday drivers are **55% more likely to die** than Friday drivers

**Gemma 4 explanation:** Sunday driving shifts from routine commuting 
to leisure and post-weekend impaired driving.""",
    "de": """Alle nehmen an, Freitag sei der gefährlichste Tag.
Unsere Daten beweisen das Gegenteil:
- **Freitag:** 146.410 Unfälle — höchstes Volumen
- **Sonntag:** 81.594 Unfälle — aber **1,27% Todesrate**
- Sonntagsfahrer sterben mit **55% höherer Wahrscheinlichkeit**

**Gemma 4 Erklärung:** Sonntagsfahrten wechseln von Routine-Pendeln 
zu Freizeit und Fahren unter Alkoholeinfluss."""
},
"finding2_title": {
    "en": "🗺️ Discovery 2 — Two Different Germanys",
    "de": "🗺️ Entdeckung 2 — Zwei verschiedene Deutschlands"
},
"finding2_body": {
    "en": """- **West Germany** (NRW, Bayern): Most accidents → urban density problem
- **East Germany** (Sachsen-Anhalt **1.61%**, Brandenburg **1.24%**): Highest fatal rates → rural infrastructure problem

**Gemma 4 explanation:** West = density and complexity driven risk. 
East = rural roads, higher speeds, less controlled environment.""",
    "de": """- **Westdeutschland** (NRW, Bayern): Meiste Unfälle → urbanes Dichteproblem
- **Ostdeutschland** (Sachsen-Anhalt **1,61%**, Brandenburg **1,24%**): Höchste Todesraten → ländliches Infrastrukturproblem

**Gemma 4 Erklärung:** West = dichte- und komplexitätsbedingt. 
Ost = Landstraßen, höhere Geschwindigkeiten."""
},
"finding3_title": {
    "en": "🌤️ Discovery 3 — Good Weather Kills More",
    "de": "🌤️ Entdeckung 3 — Gutes Wetter tötet mehr"
},
"finding3_body": {
    "en": """Most fatal accidents happen in **mild, dry conditions**:
- Average rain when fatal: **0.11mm** (almost dry!)
- Average temperature: **12.4°C** (comfortable)
- Wind speed: minimal effect on severity

**Gemma 4 explanation:** Drivers speed more in good weather, 
reducing reaction time when accidents occur.""",
    "de": """Die meisten tödlichen Unfälle passieren bei **milden, trockenen Bedingungen**:
- Durchschnittlicher Regen bei tödlichen Unfällen: **0,11mm**
- Durchschnittstemperatur: **12,4°C**
- Windgeschwindigkeit: minimaler Einfluss

**Gemma 4 Erklärung:** Fahrer fahren bei gutem Wetter schneller, 
was die Reaktionszeit verringert."""
},
"finding4_title": {
    "en": "⏰ Discovery 4 — Monday 15:00 — The Hidden Danger",
    "de": "⏰ Entdeckung 4 — Montag 15:00 — Die versteckte Gefahr"
},
"finding4_body": {
    "en": """The single most deadly hour is **Monday at 15:00** (112 deaths).

**Gemma 4 explanation:** The 'Sunday Scaries' effect — stress and 
anxiety from returning to work combined with rush-hour pressure 
creates a deadly window every Monday afternoon.""",
    "de": """Die einzeln tödlichste Stunde ist **Montag um 15:00 Uhr** (112 Tode).

**Gemma 4 Erklärung:** Der 'Sonntagsangst'-Effekt — Stress durch 
Rückkehr zur Arbeit kombiniert mit Stoßzeitdruck schafft jeden 
Montagnachmittag ein tödliches Zeitfenster."""
},
"gemma_chat_title": {
    "en": "## 🤖 Ask Gemma 4",
    "de": "## 🤖 Frage Gemma 4"
},
"gemma_chat_desc": {
    "en": "Ask Gemma 4 anything about German road safety. Running 100% locally via Ollama — no internet required.",
    "de": "Frage Gemma 4 alles über die Verkehrssicherheit in Deutschland. Läuft 100% lokal via Ollama — kein Internet erforderlich."
},
"gemma_placeholder": {
    "en": "e.g. Why is Sunday more dangerous than Friday?",
    "de": "z.B. Warum ist Sonntag gefährlicher als Freitag?"
},
"gemma_btn": {
    "en": "Ask Gemma 4 🤖",
    "de": "Gemma 4 fragen 🤖"
},
"gemma_thinking": {
    "en": "🤖 Gemma 4 is thinking... (may take 3-5 minutes on CPU)",
    "de": "🤖 Gemma 4 denkt nach... (kann 3-5 Minuten auf CPU dauern)"
},
"gemma_context": {
    "en": "Gemma 4 answers based on our analysis of 782,642 German accidents (2021-2023) with weather data.",
    "de": "Gemma 4 antwortet basierend auf unserer Analyse von 782.642 deutschen Unfällen (2021-2023) mit Wetterdaten."
},
    # -----------------------------------------Tab 6-------------------------------------------------------------------------------
"tab6_title": {
    "en": "## 🎯 Conclusion & Next Steps",
    "de": "## 🎯 Fazit & Nächste Schritte"
},
"tab6_story": {
    "en": """## 💙 Why This Project Exists

In 2010, my father was involved in a serious road accident.
His car was completely destroyed. We almost lost him that day.

That moment never left me.

Road accidents are not random — they have patterns, causes,
and most importantly, **they can be prevented.**

This project is my contribution to making roads safer —
not just in Germany, but everywhere.""",
    "de": """## 💙 Warum dieses Projekt existiert

Im Jahr 2010 war mein Vater in einen schweren Verkehrsunfall verwickelt.
Sein Auto wurde völlig zerstört. Wir hätten ihn fast verloren.

Dieser Moment hat mich nie losgelassen.

Verkehrsunfälle sind nicht zufällig — sie haben Muster, Ursachen
und vor allem **können sie verhindert werden.**

Dieses Projekt ist mein Beitrag zu sichereren Straßen —
nicht nur in Deutschland, sondern überall."""
},
"tab6_summary_title": {
    "en": "## 📊 What We Discovered",
    "de": "## 📊 Was wir entdeckt haben"
},
"tab6_summary": {
    "en": """
| Discovery | Finding | Impact |
|-----------|---------|--------|
| 🗓️ Most dangerous day | Sunday (1.27% fatal) not Friday | Target drunk driving interventions |
| 🗺️ Location pattern | East Germany most deadly (rural) | Different strategies needed |
| 🌤️ Weather paradox | Good weather = more deaths | Speed enforcement in dry conditions |
| ⏰ Hidden danger | Monday 15:00 = 112 deaths | Fatigue awareness campaigns |
| 🤖 AI power | Gemma 4 explains WHY | Local, private, offline analysis |
""",
    "de": """
| Entdeckung | Ergebnis | Auswirkung |
|------------|---------|------------|
| 🗓️ Gefährlichster Tag | Sonntag (1,27%) nicht Freitag | Alkohol-Interventionen gezielt einsetzen |
| 🗺️ Standortmuster | Ostdeutschland am tödlichsten | Verschiedene Strategien nötig |
| 🌤️ Wetter-Paradox | Gutes Wetter = mehr Tode | Geschwindigkeitskontrolle bei trockenem Wetter |
| ⏰ Versteckte Gefahr | Montag 15:00 = 112 Tode | Müdigkeitskampagnen |
| 🤖 KI-Kraft | Gemma 4 erklärt WARUM | Lokale, private, offline Analyse |
"""
},
"tab6_vision": {
    "en": """## 🌍 Vision Zero & Beyond

Germany's Vision Zero initiative aims for **zero road fatalities**.
VisionZero AI directly supports this by:

- Identifying **Sunday drunk driving** as priority intervention
- Proving **East vs West Germany** need different strategies  
- Revealing **Monday 15:00** as a predictable danger window
- Making expert-level analysis available **offline, in any language**

### 🇪🇬 My Next Goal
As someone from Egypt — a country where road safety matters deeply —
my next step is applying VisionZero AI to **Egyptian road data**
to help save lives in my own country.""",
    "de": """## 🌍 Vision Zero & Darüber hinaus

Deutschlands Vision-Zero-Initiative zielt auf **null Verkehrstote**.
VisionZero AI unterstützt dies direkt durch:

- Identifizierung von **Sonntagstrunkenfahrten** als Priorität
- Beweis, dass **Ost- und Westdeutschland** verschiedene Strategien brauchen
- Aufdeckung von **Montag 15:00** als vorhersehbares Gefahrenfenster
- Expertenanalyse **offline, in jeder Sprache** verfügbar machen

### 🇪🇬 Mein nächstes Ziel
Als jemand aus Ägypten — einem Land, wo Verkehrssicherheit wichtig ist —
ist mein nächster Schritt, VisionZero AI auf **ägyptische Unfalldaten**
anzuwenden, um Leben in meinem eigenen Land zu retten."""
},
"tab6_tech": {
    "en": """## 🛠️ Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| 🤖 AI Model | Gemma 4 (e4b) via Ollama | Local, private, offline |
| 📊 Data Analysis | Python + Pandas | Industry standard |
| ⚡ SQL Engine | DuckDB | Handles 2.6GB without crashing |
| 🗺️ Maps | Plotly + OpenStreetMap | Interactive, no API key needed |
| 🌐 Web App | Streamlit | Fast prototyping, bilingual |
| 📡 Weather | Open-Meteo API | Free, accurate, historical |
| 🔢 Data Source | Destatis (Official German Stats) | Most reliable accident data |""",
    "de": """## 🛠️ Technologie-Stack

| Komponente | Technologie | Warum |
|------------|------------|-------|
| 🤖 KI-Modell | Gemma 4 (e4b) via Ollama | Lokal, privat, offline |
| 📊 Datenanalyse | Python + Pandas | Industriestandard |
| ⚡ SQL-Engine | DuckDB | Verarbeitet 2,6 GB ohne Absturz |
| 🗺️ Karten | Plotly + OpenStreetMap | Interaktiv, kein API-Schlüssel |
| 🌐 Web-App | Streamlit | Schnelles Prototyping, zweisprachig |
| 📡 Wetter | Open-Meteo API | Kostenlos, genau, historisch |
| 🔢 Datenquelle | Destatis (Offizielle Deutsche Statistik) | Zuverlässigste Unfalldaten |"""
},
"tab6_thanks": {
    "en": """---
## 🙏 Thank You

Thank you for exploring VisionZero AI.

Every red dot on that map is a real person.
Every pattern we found could save a life.

*Built with ❤️ by Lamiaa Bahgat — Cairo, Egypt*

🔗 **GitHub:** [VisionZero AI Repository](https://github.com/LamiaaBahgat/germany-accident-analysis)
""",
    "de": """---
## 🙏 Danke

Danke, dass du VisionZero AI erkundet hast.

Jeder rote Punkt auf dieser Karte ist ein echter Mensch.
Jedes Muster, das wir gefunden haben, könnte ein Leben retten.

*Gebaut mit ❤️ von Lamiaa Bahgat — Kairo, Ägypten*

🔗 **GitHub:** [VisionZero AI Repository](https://github.com/LamiaaBahgat/germany-accident-analysis)
"""
},

    # ------------------------------------------------------------------------------------------------------------------------------
    "tab_1" : {
         "en" : "🏠 Home",
         "de" : "🏠 Startseite"
    },
    "tab_2" : {
         "en" : "🛠️ Our Data Journey",
         "de" : "🛠️ Unsere Datenreise"
    },
    "tab_3" : {
         "en" : "📊 Analysis",
         "de" : "📊 Analyse"
    },
    "tab_4" : {
         "en" : "🗺️ Live Map",
         "de" : "🗺️ Live Karte"
    },
    "tab_5" : {
         "en" : "🤖 AI Insights",
         "de" : "🤖 KI Erkenntnisse"
    },
    "tab_6" : {
         "en" : "🎯 Conclusion",
         "de" : "🎯 Fazit"
    },
# ============================================
# Tab 1 — New translations
# ============================================
"hero_title": {
    "en": "<div style='text-align: center; padding: 40px 0;'><h1>🇩🇪 VisionZero AI</h1><h3 style='color: #888;'>Uncovering Hidden Patterns in German Road Accidents</h3></div>",
    "de": "<div style='text-align: center; padding: 40px 0;'><h1>🇩🇪 VisionZero AI</h1><h3 style='color: #888;'>Verborgene Muster in deutschen Verkehrsunfällen aufdecken</h3></div>"
},
"surprising_question": {
    "en": "### ❓ Which day do you think is most dangerous to drive in Germany?",
    "de": "### ❓ An welchem Tag ist das Fahren in Deutschland am gefährlichsten?"
},
"btn_monday": {
    "en": "Monday",
    "de": "Montag"
},
"btn_friday": {
    "en": "Friday",
    "de": "Freitag"
},
"btn_sunday": {
    "en": "Sunday",
    "de": "Sonntag"
},
"wrong_answer": {
    "en": "❌ Wrong! Most people think this — but the data tells a different story...",
    "de": "❌ Falsch! Die meisten Menschen denken das — aber die Daten erzählen eine andere Geschichte..."
},
"correct_answer": {
    "en": "✅ Correct! Sunday has the highest fatal rate (1.27%) — 55% more deadly than Friday!",
    "de": "✅ Richtig! Sonntag hat die höchste Todesrate (1,27%) — 55% tödlicher als Freitag!"
},
"surprising_reveal": {
    "en": """<div style='background: linear-gradient(135deg, #1a1a2e, #16213e);
                border-left: 4px solid #da1e28;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;'>
        <h2 style='color: #da1e28;'>⚠️ The Surprising Truth</h2>
        <h3 style='color: white;'>Friday has the MOST accidents — but Sunday KILLS more</h3>
        <p style='color: #ccc; font-size: 16px;'>
        Sunday drivers are 55% more likely to die than Friday drivers.<br>
        Suspected cause: post-weekend impaired driving + leisure risk behavior.
        </p>
    </div>""",
    "de": """<div style='background: linear-gradient(135deg, #1a1a2e, #16213e);
                border-left: 4px solid #da1e28;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;'>
        <h2 style='color: #da1e28;'>⚠️ Die überraschende Wahrheit</h2>
        <h3 style='color: white;'>Freitag hat die MEISTEN Unfälle — aber Sonntag tötet mehr</h3>
        <p style='color: #ccc; font-size: 16px;'>
        Sonntagsfahrer sterben mit 55% höherer Wahrscheinlichkeit als Freitagsfahrer.<br>
        Vermutete Ursache: Fahren unter Alkoholeinfluss nach dem Wochenende.
        </p>
    </div>"""
},
"stats_title": {
    "en": "### 📊 Project at a Glance",
    "de": "### 📊 Projektübersicht"
},
"stat_accidents": {
    "en": "🚗 Accidents Analyzed",
    "de": "🚗 Analysierte Unfälle"
},
"stat_weather": {
    "en": "🌤️ Weather Matched",
    "de": "🌤️ Wetter abgeglichen"
},
"stat_fatal": {
    "en": "💀 Fatal Accidents",
    "de": "💀 Tödliche Unfälle"
},
"stat_model": {
    "en": "🤖 AI Model",
    "de": "🤖 KI-Modell"
},
"stat_weather_delta": {
    "en": "Hourly precision",
    "de": "Stündliche Genauigkeit"
},
"stat_fatal_delta": {
    "en": "Sunday: highest risk",
    "de": "Sonntag: höchstes Risiko"
},
"nav_hint": {
    "en": "👆 Use the tabs above to explore: EDA charts, interactive map, weather analysis, and Gemma 4 insights!",
    "de": "👆 Nutze die Tabs oben, um zu erkunden: EDA-Diagramme, interaktive Karte, Wetteranalyse und Gemma 4 Erkenntnisse!"
},

}

# language selector
language = st.selectbox("Language / Sprache", ["English", "Deutsch"])
lang_code = "en" if language == "English" else "de"

# tabs
tab1, tab2, tab3, tab4, tab5, tab6  = st.tabs ([translations["tab_1"][lang_code],translations["tab_2"][lang_code],translations["tab_3"][lang_code],translations["tab_4"][lang_code], translations["tab_5"][lang_code],translations["tab_6"][lang_code]])

# ---------------------------------------------------------------Tab1-----------------------------------------------

# Show translated content
with tab1:
    # Hero title
    st.markdown(translations["hero_title"][lang_code], unsafe_allow_html=True)
    st.markdown("---")

    # Surprising question
    st.markdown(translations["surprising_question"][lang_code])

    col1, col2, col3 = st.columns(3)
    with col1:
        monday_btn = st.button(
            translations["btn_monday"][lang_code],
            use_container_width=True
        )
    with col2:
        friday_btn = st.button(
            translations["btn_friday"][lang_code],
            use_container_width=True
        )
    with col3:
        sunday_btn = st.button(
            translations["btn_sunday"][lang_code],
            use_container_width=True
        )

    # Button responses
    if monday_btn or friday_btn:
        st.error(translations["wrong_answer"][lang_code])

    if sunday_btn:
        st.success(translations["correct_answer"][lang_code])

    # Surprising reveal — always shown
    st.markdown("---")
    st.markdown(translations["surprising_reveal"][lang_code], unsafe_allow_html=True)

    # Stats
    st.markdown("---")
    st.markdown(translations["stats_title"][lang_code])

    # Provides a 'shiny' glow effect and precise alignment under the metric value.
    def shiny_pill(text, top_margin="-20px", color="#79df7d", bg_color="rgba(76, 175, 80, 0.15)"):
        st.markdown(
            f"""
            <div style="
                position: relative;
                top: {top_margin};
                display: inline-block;
                background-color: {bg_color}; 
                color: {color}; 
                padding: 2px 12px; 
                border-radius: 15px; 
                font-size: 0.8rem; 
                font-weight: 600;
                margin-left: 5px;
                border: 1px solid {color}4D; 
                box-shadow: 0px 0px 12px {bg_color};
                z-index: 999;
                white-space: nowrap; 
                width: max-content;   
                ">
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
            st.metric(
                label=translations["stat_accidents"][lang_code],
                value="782,642")
            shiny_pill("2021-2023")

    with col2:
            st.metric(
                label=translations["stat_weather"][lang_code],
                value="99.7%")
            shiny_pill(translations["stat_weather_delta"][lang_code])

    with col3:
            st.metric(
                label=translations["stat_fatal"][lang_code],
                value="7,952")
            shiny_pill(translations["stat_fatal_delta"][lang_code])

    with col4:
            st.metric(
                label=translations["stat_model"][lang_code],
                value="Gemma 4")
            shiny_pill("100% Offline")

    # Project summary
    st.markdown("---")
    st.markdown(translations["summary_heading"][lang_code])
    st.markdown(translations["summary_body"][lang_code])
    st.markdown(translations["introduction_heading"][lang_code])
    st.markdown(translations["intro_text_1"][lang_code])
    st.markdown(translations["introduction_heading_2"][lang_code])
    st.markdown(translations["intro_text_2"][lang_code])
    st.markdown(translations["project_matters"][lang_code])
    st.markdown(translations["answer"][lang_code])

    # Navigation hint
    st.markdown("---")
    st.info(translations["nav_hint"][lang_code])

# ---------------------------------------------------------------Tab2-----------------------------------------------

with tab2:
    st.markdown(translations["tab2_title"][lang_code])
    st.markdown(translations["tab2_subtitle"][lang_code])
    st.markdown("---")

    st.markdown(translations["challenge_title"][lang_code])

    # Challenge 1
    with st.expander(translations["c1_title"][lang_code], expanded=False):
        st.markdown(translations["c1_problem"][lang_code])
        st.markdown(translations["c1_solution"][lang_code])
        st.markdown(translations["c1_result"][lang_code])

    # Challenge 2
    with st.expander(translations["c2_title"][lang_code], expanded=False):
        st.markdown(translations["c2_problem"][lang_code])
        st.markdown(translations["c2_solution"][lang_code])
        st.markdown(translations["c2_result"][lang_code])
        # Show the AGS code structure
        st.markdown("""
        8-digit AGS code: 11 0 00 000
    └─ Digits 1-2: Federal State (11 = Berlin)
    └─ Digit 3: Administrative District (0 = None)
    └─ Digits 4-5: District/County (00 = No division)
    └─ Digits 6-8: Municipality (000 = City itself)""")

    # Challenge 3
    with st.expander(translations["c3_title"][lang_code], expanded=False):
        st.markdown(translations["c3_problem"][lang_code])
        st.markdown(translations["c3_solution"][lang_code])
        st.markdown(translations["c3_result"][lang_code])

    # Challenge 4
    with st.expander(translations["c4_title"][lang_code], expanded=False):
        st.markdown(translations["c4_problem"][lang_code])
        st.markdown(translations["c4_solution"][lang_code])
        st.markdown(translations["c4_result"][lang_code])
        # Show file sizes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("2021 Hourly", "806 MB")
        with col2:
            st.metric("2022 Hourly", "836 MB")
        with col3:
            st.metric("2023 Hourly", "909 MB")

    # Challenge 5
    with st.expander(translations["c5_title"][lang_code], expanded=False):
        st.markdown(translations["c5_problem"][lang_code])
        st.markdown(translations["c5_solution"][lang_code])
        st.markdown(translations["c5_result"][lang_code])
        # Show timezone example
        st.markdown("""
        Before conversion:  2021-07-01 22:00:00+00:00 (UTC)
        After conversion:   2021-07-02 00:00:00+02:00 (Berlin)
        Difference: 2 hours in summer! """)

# Challenge 6
    with st.expander(translations["c6_title"][lang_code], expanded=False):
        st.markdown(translations["c6_problem"][lang_code])
        st.markdown(translations["c6_solution"][lang_code])
        st.markdown(translations["c6_result"][lang_code])
        # Show match rate
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accidents", "891,257")
        with col2:
            st.metric("Weather Matched", "888,414")
        with col3:
            st.metric("Match Rate", "99.7%")

    # Final result
    st.markdown("---")
    st.markdown(translations["tab2_final"][lang_code])

# ---------------------------------------------------------------------------------------------------------------
# Load merged data used in Tab 3 and Tab 4
    @st.cache_data
    def load_merged():
        return pd.read_csv(
             "https://huggingface.co/datasets/LamiaaBahgat/visionzero-data/resolve/main/merged_accidents_weather.csv",
            low_memory=False
        )

    df_merged = load_merged()
    df_merged['category'] = df_merged['category'].str.strip()
# ------------------------------------------------------Tab 3 ---------------------------------------------------
with tab3:
    st.markdown(translations["tab3_title"][lang_code])
    st.markdown(translations["tab3_subtitle"][lang_code])
    st.markdown("---")


    # ============================================
    # Chart 1 — Animated 24-hour cycle
    # ============================================
    st.markdown(translations["chart1_title"][lang_code])
    st.markdown(translations["chart1_desc"][lang_code])

    df_time = df_merged.groupby(['hour', 'state', 'category']).size().reset_index(name='counts')

    fig1 = px.bar(
        df_time,
        x='state',
        y='counts',
        color='category',
        animation_frame='hour',
        color_discrete_map={
            'killed': '#da1e28',
            'seriously injury': '#ff832b',
            'slightly injury': '#f1c21b'
        },
        title='Accidents by State: 24-Hour Cycle | Unfälle nach Bundesland im 24-Stunden-Verlauf',
        labels={'counts': 'counts', 'state': 'state'},
        category_orders={'state': df_merged.groupby('state').size().sort_values(ascending=False).index.tolist()}
    )
    fig1.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    # ============================================
    # Chart 2 — Icicle chart
    # ============================================
    st.markdown(translations["chart2_title"][lang_code])
    st.markdown(translations["chart2_desc"][lang_code])

    import plotly.graph_objects as go

    df_counts = df_merged.groupby(
        ['year', 'state', 'category']
    ).size().reset_index(name='accident_count')

    levels = ['category', 'state', 'year']
    value_column = 'accident_count'

    def build_hierarchical_dataframe(df, levels, value_column):
        df_list = []
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
            dfg = df.groupby(levels[i:])[value_column].sum().reset_index()
            dfg['unique_id'] = dfg[levels[i:]].astype(str).agg(' | '.join, axis=1)
            df_tree['id'] = dfg['unique_id']
            df_tree['value'] = dfg[value_column]
            df_tree['color'] = dfg[value_column]
            if i < len(levels) - 1:
                dfg['parent_id'] = dfg[levels[i+1:]].astype(str).agg(' | '.join, axis=1)
                df_tree['parent'] = dfg['parent_id']
            else:
                df_tree['parent'] = 'Germany'
            df_list.append(df_tree)

        total = pd.Series(dict(
            id='Germany',
            parent='',
            value=df[value_column].sum(),
            color=df[value_column].sum()
        ), name=0)
        df_list.append(total)
        return pd.concat(df_list, ignore_index=True)

    df_all_trees = build_hierarchical_dataframe(df_counts, levels, value_column)

    custom_colorscale = [
        [0.0, '#f1c21b'],
        [0.5, '#ff832b'],
        [1.0, '#da1e28'],
    ]

    fig2 = go.Figure()
    fig2.add_trace(go.Icicle(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale=custom_colorscale,
            showscale=True,
            colorbar=dict(title='Accidents')
        ),
        hovertemplate='<b>%{label}</b><br>Accidents: %{value:,}<extra></extra>',
        maxdepth=2,
        tiling=dict(orientation='v', pad=2),
        textfont=dict(size=10),
        pathbar=dict(visible=True)
    ))

    fig2.update_layout(
        title='🇩🇪 Accidents by Year / State / Category',
        margin=dict(t=80, l=25, r=25, b=25),
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ============================================
    # Chart 3 — Accidents by Day and State
    # ============================================
    st.markdown(translations["chart3_title"][lang_code])
    st.markdown(translations["chart3_desc"][lang_code])

    df_day = df_merged.groupby(['day', 'state']).size().reset_index(name='total')

    day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    fig3 = px.bar(
        df_day,
        x='total',
        y='day',
        color='state',
        orientation='h',
        title='Total Accidents by Day and State | Gesamtunfälle nach Tag und Bundesland',
        category_orders={'day': day_order},
        height=500
    )
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ------------------------------------------------Tab 4----------------------------------------------------------------
    with tab4:
        st.markdown(translations["tab4_title"][lang_code])
        st.markdown(translations["tab4_subtitle"][lang_code])
        st.markdown(translations["tab4_desc"][lang_code])
        st.markdown("---")


        # ============================================
        # Generate map with weather hover
        # ============================================
        @st.cache_data
        def generate_map():
        

            # Sample for performance
            df_map = df_merged.sample(n=50000, random_state=42).copy()

            # Round weather values
            df_map['temperature_2m'] = df_map['temperature_2m'].round(1)
            df_map['wind_speed_10m'] = df_map['wind_speed_10m'].round(1)

            # Weather code descriptions
            weather_code_map = {
                0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy',
                3: 'Overcast', 45: 'Fog', 48: 'Icy fog',
                51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Heavy drizzle',
                61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
                71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
                80: 'Slight showers', 81: 'Moderate showers', 82: 'Heavy showers',
                95: 'Thunderstorm', 96: 'Thunderstorm with hail'
            }
            df_map['weather_description'] = df_map['weather_code_hourly'].map(
                weather_code_map).fillna('Unknown')

            fig = px.scatter_map(
                df_map,
                lat='lat_round',
                lon='lon_round',
                color='category',
                color_discrete_map={
                    'killed': '#da1e28',
                    'seriously injury': '#FF6B6B',
                    'slightly injury': '#f1c21b'
                },
                hover_data={
                    'state': True,
                    'district': True,
                    'join_date': True,
                    'join_hour': True,
                    'weather_description': True,
                    'rain': True,
                    'temperature_2m': True,
                    'wind_speed_10m': True,
                    'cloud_cover': True,
                    'lat_round': False,
                    'lon_round': False,
                    'weather_code_hourly': False,
                    'latitude': False,
                    'longitude': False,
                },
                labels={
                    'weather_description': '🌤️ Weather',
                    'rain': '🌧️ Rain (mm)',
                    'temperature_2m': '🌡️ Temp (°C)',
                    'wind_speed_10m': '💨 Wind (km/h)',
                    'cloud_cover': '☁️ Cloud Cover (%)',
                    'join_date': '📅 Date',
                    'join_hour': '⏰ Hour',
                    'state': '📍 State',
                    'district': '🏘️ District',
                    'category': '⚠️ Severity'
                },
                zoom=5,
                center=dict(lat=51.1657, lon=10.4515),
                map_style='open-street-map',
                opacity=0.6,
                title='🇩🇪 Accident Locations with Weather Conditions 2021-2023'
            )
            fig.update_layout(
                height=700,
                margin=dict(t=80, l=0, r=0, b=0)
            )
            return fig


        # Show loading message
        with st.spinner('🗺️ Loading map with 50,000 accident points...'):
            fig_map = generate_map()

        st.plotly_chart(fig_map, use_container_width=True)

        # Insights
        st.markdown("---")
        st.markdown(translations["tab4_insight"][lang_code])
        st.markdown(translations["tab4_insight_body"][lang_code])

    # ------------------------------------- Tab 5-------------------------------------------------------------------------------
    with tab5:
        st.markdown(translations["tab5_title"][lang_code])
        st.markdown(translations["tab5_subtitle"][lang_code])
        st.markdown("---")

        # ============================================
        # Key Findings
        # ============================================
        st.markdown(translations["findings_title"][lang_code])

        # Finding 1 — Sunday
        with st.expander(translations["finding1_title"][lang_code], expanded=True):
            st.markdown(translations["finding1_body"][lang_code])

            # Show day comparison chart
            day_stats = pd.DataFrame({
                'day': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'total': [133928, 141413, 140003, 142473, 146410, 105436, 81594],
                'fatal_pct': [0.87, 0.78, 0.78, 0.84, 0.82, 1.10, 1.27]
            })

            col1, col2 = st.columns(2)
            with col1:
                fig_day1 = px.bar(
                    day_stats,
                    x='day', y='total',
                    title='Total Accidents by Day',
                    color='total',
                    color_continuous_scale=['#f1c21b', '#da1e28']
                )
                fig_day1.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_day1, use_container_width=True)

            with col2:
                fig_day2 = px.bar(
                    day_stats,
                    x='day', y='fatal_pct',
                    title='Fatal Rate % by Day',
                    color='fatal_pct',
                    color_continuous_scale=['#f1c21b', '#da1e28']
                )
                fig_day2.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_day2, use_container_width=True)

        # Finding 2 — Two Germanys
        with st.expander(translations["finding2_title"][lang_code], expanded=False):
            st.markdown(translations["finding2_body"][lang_code])

            state_stats = df_merged.groupby('state').agg(
                total=('category', 'count'),
                fatal=('category', lambda x: (x == 'killed').sum())
            ).reset_index()
            state_stats['fatal_pct'] = (state_stats['fatal'] / state_stats['total'] * 100).round(2)

            fig_state = px.bar(
                state_stats.sort_values('fatal_pct', ascending=True),
                x='fatal_pct',
                y='state',
                orientation='h',
                title='Fatal Rate % by State',
                color='fatal_pct',
                color_continuous_scale=['#f1c21b', '#ff832b', '#da1e28']
            )
            fig_state.update_layout(height=500)
            st.plotly_chart(fig_state, use_container_width=True)

        # Finding 3 — Good weather
        with st.expander(translations["finding3_title"][lang_code], expanded=False):
            st.markdown(translations["finding3_body"][lang_code])

            weather_stats = df_merged.groupby('category').agg(
                avg_rain=('rain', 'mean'),
                avg_temp=('temperature_2m', 'mean'),
                avg_wind=('wind_speed_10m', 'mean')
            ).round(2).reset_index()

            fig_weather = px.bar(
                weather_stats,
                x='category',
                y='avg_rain',
                title='Average Rain by Accident Severity',
                color='category',
                color_discrete_map={
                    'killed': '#da1e28',
                    'seriously injury': '#FF6B6B',
                    'slightly injury': '#f1c21b'
                }
            )
            fig_weather.update_layout(height=300)
            st.plotly_chart(fig_weather, use_container_width=True)

        # Finding 4 — Monday 15:00
        with st.expander(translations["finding4_title"][lang_code], expanded=False):
            st.markdown(translations["finding4_body"][lang_code])

            time_stats = df_merged.groupby(['day', 'hour'])['category'].apply(
                lambda x: (x == 'killed').sum()
            ).reset_index(name='fatal_count')

            fig_time = px.density_heatmap(
                time_stats,
                x='hour',
                y='day',
                z='fatal_count',
                title='Fatal Accidents by Day and Hour',
                color_continuous_scale=['#f1c21b', '#ff832b', '#da1e28'],
                category_orders={'day': ['monday', 'tuesday', 'wednesday',
                                         'thursday', 'friday', 'saturday', 'sunday']}
            )
            fig_time.update_layout(height=400)
            st.plotly_chart(fig_time, use_container_width=True)

        # ============================================
        # Gemma 4 Chat Interface
        # ============================================
        

            st.info(
            "🤖 Gemma 4 runs locally via Ollama. Below are pre-generated insights:"
            if lang_code == "en" else
            "🤖 Gemma 4 läuft lokal via Ollama. Unten sind vorberechnete Erkenntnisse:"
        )

        responses = {
            "🌤️ Weather Analysis / Wetteranalyse": "gemma_responses/gemma_weather.txt",
            "📍 Location Analysis / Standortanalyse": "gemma_responses/gemma_location.txt",
            "⏰ Time Patterns / Zeitmuster": "gemma_responses/gemma_time.txt",
            "💡 Recommendations / Empfehlungen": "gemma_responses/gemma_recommendations.txt"
        }

        for title, filepath in responses.items():
            with st.expander(title):
                try:
                    with open(os.path.join(DATA_DIR, filepath), 'r') as f:
                        st.markdown(f.read())
                except:
                    st.info("Response not available.")

    # -------------------------------------------Tab 6-----------------------------------------------------------------------
    with tab6:
        # Personal story
        st.markdown(translations["tab6_story"][lang_code])
        st.markdown("---")

        # Summary table
        st.markdown(translations["tab6_summary_title"][lang_code])
        st.markdown(translations["tab6_summary"][lang_code])
        st.markdown("---")

        # Vision Zero
        st.markdown(translations["tab6_vision"][lang_code])
        st.markdown("---")

        # Tech stack
        st.markdown(translations["tab6_tech"][lang_code])

        # Thank you
        st.markdown(translations["tab6_thanks"][lang_code])








