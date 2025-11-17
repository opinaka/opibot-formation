import streamlit as st
import pandas as pd
import os

# ------------------------------
# Config Streamlit
# ------------------------------
st.set_page_config(page_title="Visualisation CSV avec Pandas", layout="wide")
st.title("📈 Visualisation CSV avec Pandas et Streamlit")

st.markdown(
    "Sélectionnez un fichier CSV et la colonne à visualiser pour générer le graphique."
)

# ------------------------------
# Dossier des fichiers CSV
# ------------------------------
data_folder = "data/"
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

if not csv_files:
    st.error("❌ Aucun fichier CSV trouvé dans 'data/'")
else:
    # Sélection d'un fichier
    selected_file = st.selectbox("Sélectionnez un fichier CSV", csv_files)

    # Nom du symbole / label
    symbol = selected_file.replace(".csv", "")
    st.subheader(f"📊 Visualisation : {symbol}")

    # Lecture du CSV
    path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(path, parse_dates=["Date"])

    # Afficher un aperçu
    st.write("Dernières données :")
    st.dataframe(df.tail(10))

    # ------------------------------
    # Sélection de la colonne
    # ------------------------------
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if "Date" in numeric_cols:
        numeric_cols.remove("Date")

    if not numeric_cols:
        st.warning("⚠️ Aucune colonne numérique à visualiser.")
    else:
        selected_col = st.selectbox("Sélectionnez la colonne à visualiser", numeric_cols)

        # ------------------------------
        # Graphique Pandas (streamlit line_chart)
        # ------------------------------
        st.subheader(f"📈 Graphique {selected_col} - {symbol}")
        # On crée un DataFrame pour la colonne sélectionnée avec l'index Date
        chart_data = df.set_index("Date")[[selected_col]]
        st.line_chart(chart_data)

        # ------------------------------
        # Statistiques simples
        # ------------------------------
        st.subheader(f"📊 Statistiques - {selected_col}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Dernière valeur", f"{df[selected_col].iloc[-1]:.2f}")
        with col2:
            st.metric("Minimum", f"{df[selected_col].min():.2f}")
        with col3:
            st.metric("Maximum", f"{df[selected_col].max():.2f}")
        with col4:
            st.metric("Moyenne", f"{df[selected_col].mean():.2f}")
