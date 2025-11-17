import streamlit as st
import pandas as pd
import os
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

# ------------------------------
# Config Streamlit
# ------------------------------
st.set_page_config(page_title="Visualisation CSV avec Bokeh", layout="wide")
st.title("📈 Visualisation CSV avec Bokeh et Streamlit")

st.markdown(
    "Sélectionnez un fichier CSV et la colonne à visualiser pour générer le graphique interactif."
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
        # Graphique Bokeh
        # ------------------------------
        st.subheader(f"📈 Graphique interactif {selected_col} - {symbol}")

        source = ColumnDataSource(df)

        p = figure(
            title=f"{symbol} - {selected_col} sur la période",
            x_axis_label="Date",
            y_axis_label=selected_col,
            x_axis_type="datetime",
            width=900,     # correction Bokeh 3.x
            height=400,    # correction Bokeh 3.x
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )

        # Tracé de la ligne
        p.line(x="Date", y=selected_col, source=source, line_width=2, color="blue", legend_label=selected_col)

        # Hover interactif
        hover = HoverTool(
            tooltips=[("Date", "@Date{%F}"), (selected_col, f"@{selected_col}")],
            formatters={"@Date": "datetime"},
            mode="vline"
        )
        p.add_tools(hover)
        p.legend.location = "top_left"

        st.bokeh_chart(p, use_container_width=True)

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
