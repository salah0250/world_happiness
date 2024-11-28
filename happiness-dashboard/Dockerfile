# Utilisez une image de base Anaconda
FROM continuumio/anaconda3

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Créer l'environnement Conda à partir du fichier environment.yml
RUN conda env create -f environment.yml

# Activer l'environnement Conda
# Cela permet de s'assurer que l'environnement est activé pour les prochaines commandes
RUN echo "conda activate happiness_dashboard" >> ~/.bashrc

# Exposez le port sur lequel l'application s'exécute
EXPOSE 8050

# Commande pour exécuter l'application
CMD ["bash", "-c", "source activate happiness_dashboard && python run.py"]
