# %%
import pandas as pd
import numpy as np
from fastapi import FastAPI

# %%
app =FastAPI()

# %% [markdown]
# cargar datos

# %%
def load_datos():
    df=pd.read_csv('Data/co-emissions-per-capita new.csv')
    df['Annual CO₂ emissions (per capita)']=df[('Annual CO₂ emissions (per capita)')].str.replace('.','')
    df['Annual CO₂ emissions (per capita)']=df[('Annual CO₂ emissions (per capita)')].astype('int')
    df['Annual CO₂ emissions (per capita)']=round(df[('Annual CO₂ emissions (per capita)')]/1000000,2)
    return df
df = load_datos()

# %% [markdown]
# Definicio de rutas

# %% [markdown]
# Ruta raíz (/): Devuelve un mensaje de bienvenida

# %%
@app.get("/")
def index():
    return{"message":"Bienvenido"}

# %%
index()

# %% [markdown]
# Ruta para obtener todos los datos (/data): Devuelve todos los datos 
# del DataFrame en formato JSON.

# %%
@app.get('/data')
def data():
    pais=list(df['Entity'].unique())
    dic={}
    for i in pais:
        data=df[df['Entity']==i].sort_values(ascending=False, by='Year')
        dic2={}
        for j in range(len(data)):
            dic2[int(data['Year'].iloc[j])]= float(data['Annual CO₂ emissions (per capita)'].iloc[j])
            dic[data['Entity'].iloc[0]]=dic2
        return dic

# %%
data()

# %% [markdown]
# Ruta para obtener datos por país (/data/country/{country}): 
# Devuelve los datos de un país específico.

# %%
@app.get('/data/country/{country}')
def country(country: str):
    if country not in df['Entity'].values:
        return{'Error':f"{country} not found"}
    data= df[df['Entity']== country].sort_values(ascending=False, by='Year')
    dic={}
    for i in range(len(data)):
        dic[int(data['Year'].iloc[i])]=float(data['Annual CO₂ emissions (per capita)'].iloc[i])
    return {country:dic}

# %%
country('Mexic')

# %% [markdown]
# Ruta para obtener datos por año (/data/year/{year}): Devuelve los 
# datos de un año específico.

# %%
@app.get('/data/year/{year}')
def year(year: int):
    if year not in df['Year'].values:
        return{'Error':f"{year} not found"}
    data= df[df['Year']== year].sort_values(ascending=False, by='Entity')
    dic={}
    for i in range(len(data)):
        dic[ data['Entity'].iloc[i] ]=float(data['Annual CO₂ emissions (per capita)'].iloc[i])
    return {year:dic}

# %%
year(1990)


