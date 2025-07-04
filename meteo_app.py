import streamlit as st
import requests

# --- Fonction conseil vestimentaire ---
def conseil_vetements_detaille(temp, condition):
    condition = condition.lower()

    if temp < 0:
        haut = "🧥 Une doudoune chaude et un pull"
    elif temp < 6:
        haut = "🧥 Un manteau chaud et un pull"
    elif temp < 11:
        haut = "🧥 Une veste et un pull"
    elif temp < 16:
        haut = "🧥 Un pull léger ou une veste"
    elif temp < 21:
        haut = "👕 Un t-shirt avec une veste légère"
    elif temp < 26:
        haut = "👕 Un t-shirt"
    elif temp < 31:
        haut = "👕 Un t-shirt léger ou un débardeur"
    else:
        haut = "🩱 Un débardeur ou un t-shirt très léger"

    bas = "👖 Un pantalon" if temp < 21 else "🩳 Un short ou un pantalon léger"

    remarques = []
    if "pluie" in condition:
        remarques.append("🌧️ Prends un imperméable ou un parapluie.")
    if "neige" in condition:
        remarques.append("❄️ Porte des bottes et couvre-toi bien.")
    if "vent" in condition or "rafales" in condition:
        remarques.append("💨 Ajoute une couche coupe-vent.")
    if temp > 30:
        remarques.append("🥵 Bois beaucoup d'eau et porte une casquette.")

    return haut, bas, remarques

# --- Apparence générale ---
st.set_page_config(page_title="Météo & Habits", page_icon="🌦️")

st.markdown("""
    <style>
        .stApp {
            background-color: #f7fbff;
            padding: 10px;
            font-size: 18px;
            color: #222;
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        .alert {
            background-color: #ffe6e6;
            color: #990000;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("<h1>🌦️ Météo & Conseil Habits</h1>", unsafe_allow_html=True)

# --- Ville ---
ville = st.text_input("🏙️ Entre une ville :", "Strasbourg")

# --- API ---
API_KEY = "97e41cf22ddd4ba1950164407250407"  # 🔁 Mets ta vraie clé ici
URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={ville}&lang=fr&days=7"

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    current = data["current"]
    forecast_days = data["forecast"]["forecastday"]

    temp = current["temp_c"]
    condition = current["condition"]["text"]
    icon_url = "https:" + current["condition"]["icon"]

    haut, bas, remarques = conseil_vetements_detaille(temp, condition)

    # --- Météo actuelle ---
    st.markdown("## ☁️ Météo actuelle")
    col1, col2 = st.columns([1, 4])
    col1.image(icon_url, width=80)
    col2.write(f"🌡️ **{temp}°C** — {condition}")

    # --- Conseil vestimentaire ---
    st.markdown("## 👕 Conseil vestimentaire")
    st.write(haut)
    st.write(bas)

    for r in remarques:
        st.markdown(f"""
        <div style='background-color: #d0e8ff; padding: 10px; border-radius: 10px; margin: 5px 0; color: #222;'>
            {r}
        </div>
        """, unsafe_allow_html=True)

    # --- Prévisions ---
    st.markdown("## 📅 Prévisions à venir")
    for day in forecast_days[1:]:
        date = day["date"]
        day_temp = day["day"]["maxtemp_c"]
        day_condition = day["day"]["condition"]["text"]
        icon_day = "https:" + day["day"]["condition"]["icon"]

        with st.expander(f"📆 {date}"):
            st.image(icon_day, width=50)
            st.write(f"🌤️ Condition : **{day_condition}**")
            st.write(f"🌡️ Température max : **{day_temp}°C**")

else:
    st.markdown("""
    <div class='alert'>
        ❌ Ville introuvable. Vérifie l'orthographe.
    </div>
    """, unsafe_allow_html=True)

