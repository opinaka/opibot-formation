import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ------------------------------
# Config Streamlit
# ------------------------------
st.set_page_config(page_title="Visualisation CSV avec Plotly", layout="wide")
st.title("📈 Visualisation CSV avec Plotly & Streamlit")

st.markdown(
    "Sélectionnez un fichier CSV et la colonne à visualiser pour générer le graphique interactif."
)

# ------------------------------
# Dossier des fichiers CSV
# ------------------------------
data_folder = "data/"
if not os.path.isdir(data_folder):
    st.error(f"❌ Dossier `{data_folder}` introuvable.")
    st.stop()

csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

if not csv_files:
    st.error("❌ Aucun fichier CSV trouvé dans `data/`")
    st.stop()

# ------------------------------
# Sélecteur de thème pour le graphique
# ------------------------------
st.sidebar.header("🎨 Options d'affichage")

theme_choice = st.sidebar.selectbox(
    "Thème du graphique",
    options=["Clair", "Sombre"],
    index=0
)

if theme_choice == "Clair":
    plotly_template = "plotly_white"
    hover_bg = "rgba(0, 0, 0, 0.85)"  # fond foncé
    hover_font_color = "white"
else:
    plotly_template = "plotly_dark"
    hover_bg = "rgba(255, 255, 255, 0.9)"  # fond clair
    hover_font_color = "black"

# ------------------------------
# Sélection du fichier
# ------------------------------
selected_file = st.selectbox(
    "📄 Fichier CSV",
    options=csv_files,
    index=0,
    key="file_select"
)

symbol = selected_file.replace(".csv", "")
st.subheader(f"📊 Visualisation : {symbol}")

# ------------------------------
# Lecture du CSV
# ------------------------------
path = os.path.join(data_folder, selected_file)

try:
    df = pd.read_csv(path)
except Exception as e:
    st.error(f"Erreur lors de la lecture du fichier : {e}")
    st.stop()

# Vérification / conversion Date
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)

# Afficher un aperçu
st.write("🧾 Dernières lignes :")
st.dataframe(df.tail(10), width="stretch")

# ------------------------------
# Sélection de la colonne numérique
# ------------------------------
numeric_cols = df.select_dtypes(include=["float64", "int64", "float32", "int32"]).columns.tolist()

# On ignore Date si elle apparaît comme numérique par erreur
if "Date" in numeric_cols:
    numeric_cols.remove("Date")

if not numeric_cols:
    st.warning("⚠️ Aucune colonne numérique à visualiser.")
    st.stop()

selected_col = st.selectbox(
    "📌 Colonne à visualiser",
    options=numeric_cols,
    index=0,
    key="column_select"
)

# ------------------------------
# Nettoyage / préparation des données
# ------------------------------
df[selected_col] = pd.to_numeric(df[selected_col], errors="coerce")
df_clean = df.dropna(subset=[selected_col])

if df_clean.empty:
    st.error(f"❌ Après nettoyage, aucune donnée valide pour la colonne `{selected_col}`.")
    st.stop()

# Si Date existe, on l’utilise pour l’axe X, sinon index
if "Date" in df_clean.columns and df_clean["Date"].notna().any():
    x_col = "Date"
else:
    df_clean = df_clean.reset_index().rename(columns={"index": "Index"})
    x_col = "Index"

# ------------------------------
# Graphique Plotly
# ------------------------------
st.subheader(f"📈 Graphique : {selected_col} - {symbol}")

fig = px.line(
    df_clean,
    x=x_col,
    y=selected_col,
    title=f"{symbol} - {selected_col} sur la période",
    labels={x_col: "Date" if x_col == "Date" else "Index", selected_col: selected_col},
    template=plotly_template,
)

fig.update_traces(mode="lines+markers")
fig.update_layout(
    xaxis_title="Date" if x_col == "Date" else "Index",
    yaxis_title=selected_col,
    hoverlabel=dict(
        bgcolor=hover_bg,
        font_size=14,
        font_color=hover_font_color,
    ),
    hovermode="x unified",
)

st.plotly_chart(fig, width="stretch")

# ------------------------------
# Statistiques simples
# ------------------------------
st.subheader(f"📊 Statistiques - {selected_col}")
col1, col2, col3, col4 = st.columns(4)

last_value = df_clean[selected_col].iloc[-1]
min_value = df_clean[selected_col].min()
max_value = df_clean[selected_col].max()
mean_value = df_clean[selected_col].mean()

with col1:
    st.metric("Dernière valeur", f"{last_value:.4f}")
with col2:
    st.metric("Minimum", f"{min_value:.4f}")
with col3:
    st.metric("Maximum", f"{max_value:.4f}")
with col4:
    st.metric("Moyenne", f"{mean_value:.4f}")
