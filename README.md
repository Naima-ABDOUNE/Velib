# Velib
Le projet Velib, utilisant l'ETL (Extract, Transform, Load) :  récupère, transforme et met à jour automatiquement les données de disponibilité des vélos Velib à Paris toutes les 4 minutes.

# Fonctionnalités

**Extraction des données Velib :** Les données sont extraites de l'API Velib, fournissant des informations détaillées sur la disponibilité des vélos dans différentes stations.

**Transformation des données :** Les données sont nettoyées et transformées pour assurer une qualité optimale, y compris la correction des formats, le nettoyage des valeurs alphanumériques, et la normalisation des noms de stations et de communes.

**Chargement dans un fichier CSV :** Les données traitées sont chargées dans un fichier CSV avec des colonnes renommées pour une facilité d'utilisation et des filtres appliqués pour garantir la qualité des données.

**Exécution périodique :** Le script est conçu pour s'exécuter périodiquement, récupérant les données toutes les 4 minutes et mettant à jour le fichier CSV.
