import streamlit as st
import streamlit.components.v1 as com
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import time
import requests
import os


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

    # ------------------------------------------------------------------------------------------------------------------------------
    "tab_1" : {
         "en" : "Project Overview",
         "de" : "Projektübersicht"
    },
    "tab_2" : {
         "en" : "Data Sources & Cleaning",
         "de" : "Datenquellen & Aufbereitung"
    },
    "tab_3" : {
         "en" : "Exploratory Data Analysis",
         "de" : "Explorative Datenanalyse"
    },
    "tab_4" : {
         "en" : "Weather & Accidents Map",
         "de" : "Wetter & Unfallkarte"
    },
    "tab_5" : {
         "en" : "Key Questions & Findings",
         "de" : "Zentrale Fragestellungen & Ergebnisse"
    },
    "tab_6" : {
         "en" : "Conclusion & Next Steps",
         "de" : "Fazit & nächste Schritte"
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








