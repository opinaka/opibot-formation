# app.py
import gradio as gr
import pandas as pd
import os
import plotly.express as px

# ------------------------------
# Dossier CSV
# ------------------------------
data_folder = "data/"
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
if not csv_files:
    raise FileNotFoundError("Aucun fichier CSV trouvé dans 'data/'")

# Colonnes numériques à visualiser
numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

# Thèmes disponibles pour Plotly
themes = ["plotly_white", "plotly_dark"]


# ------------------------------
# Fonction principale
# ------------------------------
def plot_csv(selected_file, selected_col, selected_theme):
    path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(path)

    # Nettoyage des données
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    df[selected_col] = pd.to_numeric(df[selected_col], errors="coerce")
    df = df.dropna(subset=[selected_col])

    if df.empty:
        return None, "Aucune donnée valide pour cette colonne."

    # Graphique Plotly
    fig = px.line(
        df,
        x="Date",
        y=selected_col,
        title=f"{selected_file} - {selected_col} sur la période",
        labels={"Date": "Date", selected_col: selected_col},
        template=selected_theme,
    )
    fig.update_traces(mode="lines+markers")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=selected_col,
        hoverlabel=dict(
            bgcolor="white" if selected_theme != "plotly_dark" else "black",
            font_size=14,
        ),
        hovermode="x unified",
    )

    # Statistiques simples
    stats_text = (
        f"Dernière valeur : {df[selected_col].iloc[-1]:.2f}\n"
        f"Minimum : {df[selected_col].min():.2f}\n"
        f"Maximum : {df[selected_col].max():.2f}\n"
        f"Moyenne : {df[selected_col].mean():.2f}"
    )

    return fig, stats_text


# ------------------------------
# Interface Gradio (style Blocks)
# ------------------------------
with gr.Blocks(title="📈 Visualisation CSV avec Plotly + Gradio") as demo:
    gr.Markdown("## 📈 Visualisation CSV avec Plotly + Gradio")
    gr.Markdown(
        "Sélectionnez un fichier CSV, une colonne **numérique** et un thème pour générer un graphique interactif."
    )

    with gr.Row():
        file_dd = gr.Dropdown(
            label="Sélection du fichier CSV",
            choices=csv_files,
            value=csv_files[0],
        )
        col_dd = gr.Dropdown(
            label="Sélection de la colonne",
            choices=numeric_cols,
            value="Close",
        )
        theme_dd = gr.Dropdown(
            label="Thème du graphique",
            choices=themes,
            value="plotly_white",
        )

    with gr.Row():
        plot_out = gr.Plot(label="Graphique interactif")
        stats_out = gr.Textbox(label="Statistiques", lines=5)

    btn = gr.Button("Générer le graphique")

    btn.click(
        fn=plot_csv,
        inputs=[file_dd, col_dd, theme_dd],
        outputs=[plot_out, stats_out],
    )

# ------------------------------
# Lancement
# ------------------------------
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8050)
