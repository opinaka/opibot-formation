# app.py
import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Visualisation CSV avec Altair", layout="wide")
st.title("📈 Visualisation CSV avec Altair et Streamlit")

st.markdown(
    "Sélectionnez un fichier CSV et la colonne à visualiser pour générer le graphique interactif."
)

data_folder = "data/"
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

if not csv_files:
    st.error("❌ Aucun fichier CSV trouvé dans 'data/'")
else:
    selected_file = st.selectbox("Sélectionnez un fichier CSV", csv_files)
    symbol = selected_file.replace(".csv", "")
    st.subheader(f"📊 Visualisation : {symbol}")

    path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(path, parse_dates=["Date"])

    st.write("Dernières données :")
    st.dataframe(df.tail(10))

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if "Date" in numeric_cols:
        numeric_cols.remove("Date")

    if not numeric_cols:
        st.warning("⚠️ Aucune colonne numérique à visualiser.")
    else:
        selected_col = st.selectbox("Sélectionnez la colonne à visualiser", numeric_cols)

        st.subheader(f"📈 Graphique {selected_col} - {symbol}")

        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x='Date:T',
                y=alt.Y(selected_col, title=selected_col),
                tooltip=['Date:T', f'{selected_col}:Q']
            )
            .properties(
                height=400,
                title=f"{symbol} - {selected_col} sur la période"
            )
            .interactive()
        )

        # Streamlit gère la largeur automatiquement
        st.altair_chart(chart)

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
