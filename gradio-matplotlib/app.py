import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# ------------------------------
# Dossier CSV
# ------------------------------
data_folder = "data/"
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
if not csv_files:
    raise FileNotFoundError("Aucun fichier CSV trouvé dans 'data/'")

# Colonnes numériques à visualiser
numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

# Thèmes pour Matplotlib
themes = ["light", "dark"]


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

    # ------------------------------
    # Graphique Matplotlib
    # ------------------------------
    plt_style = "dark_background" if selected_theme == "dark" else "default"
    plt.style.use(plt_style)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Date"], df[selected_col], marker="o",
            label=selected_col,
            color="cyan" if selected_theme == "dark" else "blue")

    ax.set_xlabel("Date")
    ax.set_ylabel(selected_col)
    ax.set_title(f"{selected_file} - {selected_col} sur la période")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Conversion de la figure en image (numpy array) pour Gradio
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())  # RGBA (H, W, 4)
    plt.close(fig)

    # ------------------------------
    # Statistiques simples
    # ------------------------------
    stats_text = (
        f"Dernière valeur : {df[selected_col].iloc[-1]:.2f}\n"
        f"Minimum : {df[selected_col].min():.2f}\n"
        f"Maximum : {df[selected_col].max():.2f}\n"
        f"Moyenne : {df[selected_col].mean():.2f}"
    )

    return img, stats_text


# ------------------------------
# Interface Gradio
# ------------------------------
with gr.Blocks(title="📈 Visualisation CSV avec Matplotlib + Gradio") as demo:
    gr.Markdown("## 📈 Visualisation CSV avec Matplotlib + Gradio")
    gr.Markdown("Sélectionnez un fichier CSV, une colonne et un thème pour générer le graphique.")

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
            value="light",
        )

    with gr.Row():
        img_out = gr.Image(label="Graphique")
        stats_out = gr.Textbox(label="Statistiques", lines=5)

    btn = gr.Button("Générer le graphique")

    btn.click(
        fn=plot_csv,
        inputs=[file_dd, col_dd, theme_dd],
        outputs=[img_out, stats_out],
    )

# ------------------------------
# Lancement
# ------------------------------
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8050)
