# app.py
import dash
from dash import dcc, html
import pandas as pd
import os
import plotly.express as px

# ------------------------------
# Création de l'application Dash
# ------------------------------
app = dash.Dash(__name__)
server = app.server  # pour déploiement éventuel

# ------------------------------
# Dossier CSV
# ------------------------------
data_folder = "data/"
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

if not csv_files:
    raise FileNotFoundError("Aucun fichier CSV trouvé dans 'data/'")

# Colonnes numériques à visualiser
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

# Thèmes disponibles pour Plotly
themes = ['plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'plotly']

# ------------------------------
# Layout Dash
# ------------------------------
app.layout = html.Div([
    html.H1("📈 Visualisation CSV avec Plotly Dash"),
    
    html.Label("Sélection du fichier CSV :"),
    dcc.Dropdown(
        id='file-dropdown',
        options=[{'label': f, 'value': f} for f in csv_files],
        value=csv_files[0]
    ),
    
    html.Label("Sélection de la colonne :"),
    dcc.Dropdown(
        id='col-dropdown',
        options=[{'label': col, 'value': col} for col in numeric_cols],
        value='Close'
    ),

    html.Label("Thème du graphique :"),
    dcc.Dropdown(
        id='theme-dropdown',
        options=[{'label': theme, 'value': theme} for theme in themes],
        value='plotly_white'
    ),
    
    dcc.Graph(id='graph'),
    
    html.Div(id='stats')
])

# ------------------------------
# Callbacks
# ------------------------------
@app.callback(
    [dash.dependencies.Output('graph', 'figure'),
     dash.dependencies.Output('stats', 'children')],
    [dash.dependencies.Input('file-dropdown', 'value'),
     dash.dependencies.Input('col-dropdown', 'value'),
     dash.dependencies.Input('theme-dropdown', 'value')]
)
def update_graph(selected_file, selected_col, selected_theme):
    path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(path)
    
    # Conversion Date et nettoyage
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date').reset_index(drop=True)
    df[selected_col] = pd.to_numeric(df[selected_col], errors='coerce')
    df = df.dropna(subset=[selected_col])
    
    # Graphique Plotly avec template choisi
    fig = px.line(
        df,
        x='Date',
        y=selected_col,
        title=f"{selected_file} - {selected_col} sur la période",
        labels={'Date': 'Date', selected_col: selected_col},
        template=selected_theme
    )
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=selected_col,
        hoverlabel=dict(bgcolor='white' if selected_theme != 'plotly_dark' else 'black', font_size=14),
        hovermode='x unified'
    )
    
    # Statistiques simples
    stats = html.Div([
        html.H4("📊 Statistiques"),
        html.P(f"Dernière valeur : {df[selected_col].iloc[-1]:.2f}"),
        html.P(f"Minimum : {df[selected_col].min():.2f}"),
        html.P(f"Maximum : {df[selected_col].max():.2f}"),
        html.P(f"Moyenne : {df[selected_col].mean():.2f}")
    ])
    
    return fig, stats

# ------------------------------
# Lancement du serveur
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8050, host="0.0.0.0")
