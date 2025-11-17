import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------
# Config Streamlit
# ------------------------------
st.set_page_config(page_title="Visualisation CSV avec Matplotlib", layout="wide")
st.title("📈 Visualisation CSV avec Matplotlib et Streamlit")

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
    # Sélection d'un fichier (1 seul)
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
        # Graphique Matplotlib
        # ------------------------------
        st.subheader(f"📈 Graphique {selected_col} - {symbol}")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Date"], df[selected_col], label=f"{symbol} - {selected_col}", color="blue")
        ax.set_xlabel("Date")
        ax.set_ylabel(selected_col)
        ax.set_title(f"{symbol} - {selected_col} sur la période")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

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
