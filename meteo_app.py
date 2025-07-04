
import streamlit as st
import requests

# --- Configuration ---
API_KEY = "97e41cf22ddd4ba1950164407250407"
VILLE = "Strasbourg"
URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={VILLE}&lang=fr"

# --- Fonction de conseil vestimentaire ---
def conseil_vetements_detaille(temp, condition):
    condition = condition.lower()
    
    if temp < 0:
        haut = "Une doudoune chaude et un pull"
    elif temp < 6:
        haut = "Un manteau chaud et un pull"
    elif temp < 11:
        haut = "Une veste et un pull"
    elif temp < 16:
        haut = "Un pull léger ou une veste"
    elif temp < 21:
        haut = "Un t-shirt avec une veste légère"
    elif temp < 26:
        haut = "Un t-shirt"
    elif temp < 31:
        haut = "Un t-shirt léger ou un débardeur"
    else:
        haut = "Un débardeur ou un t-shirt très léger"

    bas = "Un pantalon" if temp < 21 else "Un short ou un pantalon léger"

    remarques = []
    if "pluie" in condition:
        remarques.append("Prends un imperméable ou un parapluie.")
    if "neige" in condition:
        remarques.append("Porte des bottes et couvre-toi bien.")
    if "vent" in condition or "rafales" in condition:
        remarques.append("Ajoute une couche coupe-vent.")
    if temp > 30:
        remarques.append("Porte une casquette et bois beaucoup d'eau.")
    
    return haut, bas, remarques

# --- Interface utilisateur ---
st.title("🌦️ Météo & Conseil Habits - Strasbourg")

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]

    haut, bas, remarques = conseil_vetements_detaille(temp, condition)

    st.subheader("📍 Météo actuelle")
    st.write(f"🌡️ Température : **{temp}°C**")
    st.write(f"☁️ Condition météo : **{condition}**")

    st.subheader("🧥 Conseil vestimentaire")
    st.write(f"👕 Haut : {haut}")
    st.write(f"👖 Bas : {bas}")

    if remarques:
        st.markdown("💡 **Remarques supplémentaires :**")
        for remarque in remarques:
            st.info(remarque)
else:
    st.error("Erreur : impossible de récupérer la météo.")