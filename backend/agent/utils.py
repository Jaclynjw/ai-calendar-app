from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.sql_database import SQLDatabase 

# LLMs
langchain_chat_kwargs = {
    "temperature": 0,
    "max_tokens": 4000,
    "verbose": True,
}
chat_openai_model_kwargs = {
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": -1,
}

# # Database constants
# RAPPEL_CONSO_COLUMNS = [
#     "reference_fiche",
#     "risques_pour_le_consommateur",
#     "recommandations_sante",
#     "date_debut_commercialisation",
#     "date_fin_commercialisation",
#     "informations_complementaires",
#     "categorie_de_produit",
#     "sous_categorie_de_produit",
#     "nom_de_la_marque_du_produit",
#     "noms_des_modeles_ou_references",
#     "identification_des_produits",
#     "conditionnements",
#     "temperature_de_conservation",
#     "zone_geographique_de_vente",
#     "distributeurs",
#     "motif_du_rappel",
#     "numero_de_contact",
#     "modalites_de_compensation",
#     "liens_vers_les_images",
#     "lien_vers_la_liste_des_produits",
#     "lien_vers_la_liste_des_distributeurs",
#     "lien_vers_affichette_pdf",
#     "lien_vers_la_fiche_rappel",
#     "date_de_publication",
#     "date_de_fin_de_la_procedure_de_rappel",
# ]

# Set up LLM
def get_chat_openai(model_name):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(
        model_name=model_name,
        api_key=api_key,
        model_kwargs=chat_openai_model_kwargs,
        **langchain_chat_kwargs
    )
    return llm

# Set up langchain database connection
def get_db():
    load_dotenv()
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    mydatabase = os.getenv("DB_NAME")
    pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
    db = SQLDatabase.from_uri(pg_uri)
    return db