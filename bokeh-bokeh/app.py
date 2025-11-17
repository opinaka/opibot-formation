import os
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (
    ColumnDataSource,
    Select,
    Div,
    DataTable,
    TableColumn,
    NumberFormatter,
    HoverTool,
    Legend,
    LegendItem,
)
from bokeh.plotting import figure

DATA_FOLDER = "data"

# -----------------------------------------
# Lecture des CSV disponibles
# -----------------------------------------
csv_files = [
    f for f in os.listdir(DATA_FOLDER)
    if f.endswith(".csv")
]

if not csv_files:
    message = Div(
        text="<h2 style='color:red'>❌ Aucun fichier CSV trouvé dans 'data/'</h2>",
        width=800,
    )
    curdoc().add_root(column(message))
    curdoc().title = "Visualisation CSV avec Bokeh"
    raise SystemExit("No CSV files found in data/")

# -----------------------------------------
# Widgets
# -----------------------------------------
file_select = Select(
    title="Sélectionnez un fichier CSV :",
    value=csv_files[0],
    options=csv_files,
    width=300,
)

symbol_div = Div(text="", width=800)

column_select = Select(
    title="Sélectionnez la colonne à visualiser :",
    value="",
    options=[],
    width=300,
)

info_div = Div(
    text=(
        "<p>Sélectionnez un fichier CSV et la colonne à visualiser "
        "pour générer le graphique interactif.</p>"
    ),
    width=800,
)

# -----------------------------------------
# Sources Bokeh
# -----------------------------------------
source = ColumnDataSource(data=dict(Date=[], y=[]))
table_source = ColumnDataSource(data=dict())  # pour afficher les dernières lignes

# -----------------------------------------
# Figure Bokeh
# -----------------------------------------
p = figure(
    title="",
    x_axis_type="datetime",
    x_axis_label="Date",
    y_axis_label="",
    width=900,
    height=400,
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Renderer de la ligne (sans legend_label ici)
line = p.line(
    x="Date",
    y="y",
    source=source,
    line_width=2,
)

# Legend Bokeh 3.x : via Legend + LegendItem
legend_item = LegendItem(label="", renderers=[line])
legend = Legend(items=[legend_item])
p.add_layout(legend, "right")  # ou "top_left", "right", etc.

hover = HoverTool(
    tooltips=[("Date", "@Date{%F}"), ("Valeur", "@y")],
    formatters={"@Date": "datetime"},
    mode="vline",
)
p.add_tools(hover)

# -----------------------------------------
# Tableau des dernières données
# -----------------------------------------
data_table_columns = []
data_table = DataTable(
    source=table_source,
    columns=data_table_columns,
    width=900,
    height=200,
    index_position=None,
)

# Div pour les stats
stats_div = Div(text="", width=900)


# -----------------------------------------
# Fonctions utilitaires
# -----------------------------------------
def load_dataframe(file_name: str) -> pd.DataFrame:
    """Charge un DataFrame depuis le dossier data/."""
    path = os.path.join(DATA_FOLDER, file_name)
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


def update_column_select(df: pd.DataFrame):
    """Met à jour la liste des colonnes numériques pour le Select."""
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    if "Date" in numeric_cols:
        numeric_cols.remove("Date")
    if not numeric_cols:
        column_select.options = []
        column_select.value = ""
    else:
        column_select.options = numeric_cols
        column_select.value = numeric_cols[0]


def update_table(df: pd.DataFrame):
    """Met à jour le tableau des dernières lignes."""
    last_rows = df.tail(10).copy()
    # Conversion de Date en string pour affichage lisible
    if "Date" in last_rows.columns:
        last_rows["Date"] = last_rows["Date"].dt.strftime("%Y-%m-%d")

    table_source.data = last_rows.to_dict(orient="list")

    # Mise à jour des colonnes de la DataTable
    columns = []
    for col in last_rows.columns:
        if pd.api.types.is_numeric_dtype(last_rows[col]):
            formatter = NumberFormatter(format="0.00")
            columns.append(TableColumn(field=col, title=col, formatter=formatter))
        else:
            columns.append(TableColumn(field=col, title=col))

    data_table.columns = columns


def update_stats(df: pd.DataFrame, col: str):
    """Met à jour le bloc de statistiques."""
    if col not in df.columns or df[col].empty:
        stats_div.text = "<p>Pas de données pour les statistiques.</p>"
        return

    last_val = df[col].iloc[-1]
    min_val = df[col].min()
    max_val = df[col].max()
    mean_val = df[col].mean()

    stats_div.text = f"""
    <h3>📊 Statistiques - {col}</h3>
    <table border="1" cellspacing="0" cellpadding="5">
        <tr>
            <th>Dernière valeur</th>
            <th>Minimum</th>
            <th>Maximum</th>
            <th>Moyenne</th>
        </tr>
        <tr>
            <td>{last_val:.2f}</td>
            <td>{min_val:.2f}</td>
            <td>{max_val:.2f}</td>
            <td>{mean_val:.2f}</td>
        </tr>
    </table>
    """


def update_plot(df: pd.DataFrame, col: str, symbol: str):
    """Met à jour le graphique Bokeh."""
    if col not in df.columns:
        return

    # Mettre à jour la source
    new_data = {
        "Date": df["Date"],
        "y": df[col],
    }
    source.data = new_data

    # Met à jour les labels
    p.title.text = f"{symbol} - {col} sur la période"
    p.yaxis.axis_label = col

    # Mettre à jour le HoverTool
    hover.tooltips = [("Date", "@Date{%F}"), (col, "@y")]

    # 🔁 Mise à jour du texte de la légende (LegendItem en Bokeh 3.x)
    # label est une dict de forme {"value": "..."} ou {"field": "..."}
    legend_item.label = {"value": col}


def update_symbol_div(symbol: str):
    symbol_div.text = f"<h2>📊 Visualisation : {symbol}</h2>"


def on_file_change(attr, old, new):
    """Callback quand on change de fichier CSV."""
    df = load_dataframe(new)
    symbol = new.replace(".csv", "")

    update_symbol_div(symbol)
    update_column_select(df)
    update_table(df)

    # Si une colonne est disponible, on met le plot & stats à jour
    if column_select.value:
        update_plot(df, column_select.value, symbol)
        update_stats(df, column_select.value)


def on_column_change(attr, old, new):
    """Callback quand on change de colonne."""
    if not new:
        return

    file_name = file_select.value
    df = load_dataframe(file_name)
    symbol = file_name.replace(".csv", "")

    update_plot(df, new, symbol)
    update_stats(df, new)


# -----------------------------------------
# Initialisation avec le premier fichier
# -----------------------------------------
initial_df = load_dataframe(file_select.value)
initial_symbol = file_select.value.replace(".csv", "")

update_symbol_div(initial_symbol)
update_column_select(initial_df)
update_table(initial_df)

if column_select.value:
    update_plot(initial_df, column_select.value, initial_symbol)
    update_stats(initial_df, column_select.value)

# -----------------------------------------
# Callbacks
# -----------------------------------------
file_select.on_change("value", on_file_change)
column_select.on_change("value", on_column_change)

# -----------------------------------------
# Layout
# -----------------------------------------
layout = column(
    Div(text="<h1>📈 Visualisation CSV avec Bokeh</h1>"),
    info_div,
    row(file_select, column_select),
    symbol_div,
    p,
    Div(text="<h3>Dernières données :</h3>"),
    data_table,
    stats_div,
)

curdoc().add_root(layout)
curdoc().title = "Visualisation CSV avec Bokeh"
