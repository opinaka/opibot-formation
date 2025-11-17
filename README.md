
## **🚀 Test des solutions de visualisation Python**

### **📋 Objectif**

Cette séance vous permet de **tester et comparer** facilement les différentes combinaisons de frameworks et bibliothèques de visualisation Python :

- **Frameworks** : Dash, Gradio, Streamlit
- **Bibliothèques de visualisation** : Plotly, Matplotlib, Seaborn, Altair, Bokeh, Pandas

Chaque combinaison est dans un conteneur Docker séparé pour faciliter les tests.

---

### **⚙️ Installation et lancement**

#### **1. Cloner le projet**

```bash
git clone https://github.com/opinaka/opibot-formation.git
cd opibot-formation
```

#### **2. Lancer tous les exemples**

```bash
docker compose up --build
```

Cette commande va :

- ✅ Construire tous les conteneurs Docker
- ✅ Lancer toutes les applications en parallèle
- ✅ Les rendre accessibles sur différents ports

#### **3. Accéder aux applications**

Une fois lancé, ouvrez votre navigateur sur :

|Framework|Bibliothèque|URL|Port|
|---|---|---|---|
|**Dash**|Plotly|http://localhost:8050|8050|
|**Gradio**|Matplotlib|http://localhost:7860|7860|
|**Gradio**|Plotly|http://localhost:7861|7861|
|**Streamlit**|Altair|http://localhost:8501|8501|
|**Streamlit**|Bokeh|http://localhost:8502|8502|
|**Streamlit**|Matplotlib|http://localhost:8503|8503|
|**Streamlit**|Pandas|http://localhost:8504|8504|
|**Streamlit**|Plotly|http://localhost:8505|8505|
|**Streamlit**|Seaborn|http://localhost:8506|8506|

#### **4. Arrêter les applications**

```bash
docker compose down
```

Cette commande arrête et supprime tous les conteneurs.


---

### **📁 Structure du projet**

```
opibot-formation/
├── dash-plotly/           # Dash + Plotly
├── gradio-matplotlib/     # Gradio + Matplotlib
├── gradio-plotly/         # Gradio + Plotly
├── streamlit-altair/      # Streamlit + Altair
├── streamlit-bokeh/       # Streamlit + Bokeh
├── streamlit-matplotlib/  # Streamlit + Matplotlib
├── streamlit-pandas/      # Streamlit + Pandas
├── streamlit-plotly/      # Streamlit + Plotly
├── streamlit-seaborn/     # Streamlit + Seaborn
└── docker-compose.yml     # Configuration Docker
```

Chaque dossier contient :

- `app.py` ou `main.py` : Le code de l'application
- `Dockerfile` : Configuration du conteneur
- `requirements.txt` : Dépendances Python

---

### **📊 Grille d'évaluation suggérée**

Pour chaque combinaison, notez de 1 à 5 :

|Critère|Dash-Plotly|Streamlit-Plotly|Gradio-Plotly|...|
|---|---|---|---|---|
|**Facilité d'utilisation**|?|?|?|?|
|**Qualité visuelle**|?|?|?|?|
|**Interactivité**|?|?|?|?|
|**Vitesse de chargement**|?|?|?|?|
|**Intuitivité interface**|?|?|?|?|

---
