#!/usr/bin/env python
# coding: utf-8

# In[50]:


import pandas as pd
import matplotlib.pyplot as plt
 
# Charger les données à partir du fichier CSV
file_path = "D:\\Ecole ESIC\\ETL\\projet velib\\VelibOpenSource\\velib_data.csv"
data = pd.read_csv(file_path, sep=",")  # Specify the separator as ';'
 

 
# Calculer la part des stations en fonctionnement
if 'Station en fonctionnement' in data.columns:
    stations_en_fonctionnement = data[data['Station en fonctionnement'] == 'OUI']
    part_stations_en_fonctionnement = len(stations_en_fonctionnement) / len(data)
 
    # Créer un diagramme camembert
    labels = 'En fonctionnement', 'Hors fonctionnement'
    sizes = [part_stations_en_fonctionnement, 1 - part_stations_en_fonctionnement]
    colors = ['lightblue', 'lightgreen']
 
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Part des stations en fonctionnement sur l\'ensemble des communes du Syndicat Autolib\' Vélib\' Métropole')
    plt.show()
else:
    print("La colonne 'Station en fonctionnement' n'existe pas dans le DataFrame.")


# In[46]:


# Filtrer les données pour Paris uniquement
df_paris =data[data['Nom communes équipées'] == 'Paris']
 
# Trier les données par le nombre de bornettes libres
df_paris_sorted = df_paris.sort_values(by='Nombre bornettes libres', ascending=False)
 
# Sélectionner les 10 premières stations (à titre d'exemple, vous pouvez ajuster selon vos besoins)
df_top_stations = df_paris_sorted.head(10)
 
# Créer un graphique à barres
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
 
bar1 = ax.bar(df_top_stations['Nom station'], df_top_stations['Nombre bornettes libres'], bar_width, label='Bornettes Libres', color='lightblue')

bar2 = ax.bar(df_top_stations['Nom station'], df_top_stations['Nombre bornettes libres'], bar_width, label='Vélos Disponibles', color='lightgreen', bottom=df_top_stations['Nombre bornettes libres'])
plt.xticks(rotation=90)


# In[47]:


# Group by and calculate averages
moyenne_bornettes = data['Nombre bornettes libres'].mean()
moyenne_velos_mecaniques = data['Vélos mécaniques disponibles'].mean()
moyenne_velos_electriques = data['Vélos électriques disponibles'].mean()
 
 
# Plotting
plt.bar(['Bornettes libres', 'Vélos mécaniques', 'Vélos électriques'], [moyenne_bornettes, moyenne_velos_mecaniques, moyenne_velos_electriques], color=['grey', 'green', 'blue'])
plt.xlabel('Catégorie')
plt.ylabel('Moyenne')
plt.title('Moyenne de Bornettes et Vélos Disponibles')
plt.show()


# In[48]:


import numpy as np
capacite_par_commune = data.groupby('Nom communes équipées')['Vélos électriques disponibles'].sum()
 
# Créer une échelle logarithmique pour l'axe des y
capacite_log = np.log10(capacite_par_commune)
 
# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.bar(capacite_log.index, capacite_par_commune, color='blue', alpha=0.7)
plt.yscale('log')  # Définir l'échelle logarithmique sur l'axe des y
plt.xlabel('Commune')
plt.ylabel('Capacité d\'accueil (logarithmique)')
plt.title('Capacité d\'accueil des stations par commune (échelle logarithmique)')
plt.xticks(rotation=90)
plt.show()


# In[16]:


# Group the data by commune and calculate the sum of available bikes in each commune
grouped_data = data.groupby('Nom communes équipées')['Vélos électriques disponibles'].sum()
 
# Create a new DataFrame with the calculated values
result_df = pd.DataFrame({
    'Commune': grouped_data.index,
    'Total Bikes': grouped_data.values
})
 
# Sort the DataFrame by the total number of bikes in descending order
result_df = result_df.sort_values(by='Total Bikes', ascending=False)
 
# Plot the data in logarithmic scale
plt.figure(figsize=(10, 6))
plt.bar(result_df['Commune'], result_df['Total Bikes'], color='green')
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xlabel('Commune')
plt.ylabel('Total Bikes (log scale)')
plt.title('Total Bikes by Commune (logarithmic scale)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# In[21]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]
 
# Group by commune and calculate average values
average_values = filtered_data.groupby("Nom communes équipées").mean()
 
# Plotting the stacked histogram
fug, ex = plt.subplots(figsize=(12, 6))
 
# Bar width
bar_width = 0.8
 
# Bar positions
bar_positions = range(len(average_values))
 
# Plotting each bar, stacking them on top of each other
ex.bar(bar_positions, average_values["Nombre bornettes libres"], width=bar_width, label="Bornes libres", color="gray")
ex.bar(bar_positions, average_values["Vélos mécaniques disponibles"], bottom=average_values["Nombre bornettes libres"], width=bar_width, label="Vélos mécaniques", color="green")
ex.bar(bar_positions, average_values["Vélos électriques disponibles"], bottom=average_values["Nombre bornettes libres"] + average_values["Vélos mécaniques disponibles"], width=bar_width, label="Vélos électriques", color="blue")
 
# X-axis and Y-axis labels
ex.set_xticks(bar_positions)
ex.set_xticklabels(average_values.index, rotation=45, ha="right")
ex.set_xlabel("Communes")
ex.set_ylabel("Moyenne des vélos et bornes")
 
# Title and legend
ex.set_title("Disponibilité des bornettes, vélos mécaniques et électriques par commune")
ex.legend()
 
# Show the plot
plt.tight_layout()
plt.show()


# In[22]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]

# Group by commune and calculate average values
average_values = filtered_data.groupby("Nom communes équipées").mean()

# Plotting the stacked histogram
fig, ax = plt.subplots(figsize=(12, 6))

# Bar width
bar_width = 0.8

# Bar positions
bar_positions = range(len(average_values))

# Plotting each bar, stacking them on top of each other
ax.bar(bar_positions, average_values["Nombre bornettes libres"], width=bar_width, label="Bornes libres", color="gray")
ax.bar(bar_positions, average_values["Vélos mécaniques disponibles"], bottom=average_values["Nombre bornettes libres"], width=bar_width, label="Vélos mécaniques", color="green")
ax.bar(bar_positions, average_values["Vélos électriques disponibles"], bottom=average_values["Nombre bornettes libres"] + average_values["Vélos mécaniques disponibles"], width=bar_width, label="Vélos électriques", color="blue")

# X-axis and Y-axis labels
ax.set_xticks(bar_positions)
ax.set_xticklabels(average_values.index, rotation=45, ha="right")
ax.set_xlabel("Communes")
ax.set_ylabel("Moyenne des vélos et bornes")

# Title and legend
ax.set_title("Disponibilité des bornettes, vélos mécaniques et électriques par commune")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()


# In[25]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]
 
# Group by commune and calculate average values
average_value = filtered_data.groupby("Nom communes équipées").mean()
 
# Plotting the stacked histogram
fug, ex = plt.subplots(figsize=(12, 6))
 
# Bar width
bar_width = 0.8
 
# Bar positions
bar_positions = range(len(average_value))
 
# Plotting each bar, stacking them on top of each other
ex.bar(bar_positions, average_value["Nombre bornettes libres"], width=bar_width, label="Bornes libres", color="gray")
ex.bar(bar_positions, average_value["Vélos mécaniques disponibles"], bottom=average_value["Nombre bornettes libres"], width=bar_width, label="Vélos mécaniques", color="green")
ex.bar(bar_positions, average_value["Vélos électriques disponibles"], bottom=average_value["Nombre bornettes libres"] + average_values["Vélos mécaniques disponibles"], width=bar_width, label="Vélos électriques", color="blue")
 
# X-axis and Y-axis labels
ex.set_xticks(bar_positions)
ex.set_xticklabels(average_value.index, rotation=45, ha="right")
ex.set_xlabel("Communes")
ex.set_ylabel("Moyenne des vélos et bornes")
 
# Title and legend
ex.set_title("Disponibilité des bornettes, vélos mécaniques et électriques par commune")
ex.legend()
 
# Show the plot
plt.tight_layout()
plt.show()


# In[51]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]

# Group by commune and calculate average values
average_value = filtered_data.groupby("Nom communes équipées").mean()

# Plotting the stacked histogram
fig, ax = plt.subplots(figsize=(12, 6))

# Bar width
bar_width = 0.8

# Bar positions
bar_positions = range(len(average_value))

# Plotting each bar, stacking them on top of each other
ax.bar(bar_positions, average_value["Nombre bornettes libres"], width=bar_width, label="Bornes libres", color="gray")
ax.bar(bar_positions, average_value["Vélos mécaniques disponibles"], bottom=average_value["Nombre bornettes libres"], width=bar_width, label="Vélos mécaniques", color="green")
ax.bar(bar_positions, average_value["Vélos électriques disponibles"], bottom=average_value["Nombre bornettes libres"] + average_values["Vélos mécaniques disponibles"], width=bar_width, label="Vélos électriques", color="blue")

# X-axis and Y-axis labels
ax.set_xticks(bar_positions)
ax.set_xticklabels(average_value.index, rotation=45, ha="right")
ax.set_xlabel("Communes")
ax.set_ylabel("Moyenne des vélos et bornes")

# Title and legend
ax.set_title("Disponibilité des bornettes, vélos mécaniques et électriques par commune")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()


# In[34]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]

filtered_data['Nom station'] = pd.to_numeric(filtered_data['Nom station'])


# Group by commune and calculate average values
average_values = filtered_data.groupby("Nom communes équipées").mean()
 


# In[49]:


# Filter data for stations equipped with Vélib'
filtered_data = data[data["Nom communes équipées"].notnull()]
 
filtered_data['Nom station'] = pd.to_numeric(filtered_data['Nom station'], errors = 'coerce')

# Group by commune and calculate average values
average_values = filtered_data.groupby("Nom communes équipées").mean()
 
# Plotting the histogram
fig, ax = plt.subplots(figsize=(12, 6))
 
# Bar width
bar_width = 0.2
 
# Bar positions
bar_positions = range(len(average_values))
 
# Plotting each bar
ax.bar(bar_positions, average_values["Nombre bornettes libres"], width=bar_width, label="Bornes libres", color="gray")
ax.bar([pos + bar_width for pos in bar_positions], average_values["Vélos mécaniques disponibles"], width=bar_width, label="Vélos mécaniques", color="green")
ax.bar([pos + 2 * bar_width for pos in bar_positions], average_values["Vélos électriques disponibles"], width=bar_width, label="Vélos électriques", color="blue")
 
# X-axis and Y-axis labels
ax.set_xticks([pos + bar_width for pos in bar_positions])
ax.set_xticklabels(average_values.index, rotation=45, ha="right")
ax.set_xlabel("Communes")
ax.set_ylabel("Moyenne des vélos et bornes")
 
# Title and legend
ax.set_title("Disponibilité des bornettes, vélos mécaniques et électriques par commune")
ax.legend()
 
# Show the plot
plt.tight_layout()
plt.show()







