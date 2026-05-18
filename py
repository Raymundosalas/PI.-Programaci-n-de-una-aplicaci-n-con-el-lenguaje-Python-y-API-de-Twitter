# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# ==========================================
# CREDENCIALES DE TWITTER API
# ==========================================

consumer_key = "TU_CONSUMER_KEY"
consumer_secret = "TU_CONSUMER_SECRET"
access_token = "TU_ACCESS_TOKEN"
access_token_secret = "TU_ACCESS_TOKEN_SECRET"

# ==========================================
# AUTENTICACIÓN
# ==========================================

auth = tweepy.OAuthHandler(
    consumer_key,
    consumer_secret
)

auth.set_access_token(
    access_token,
    access_token_secret
)

api = tweepy.API(auth)

# ==========================================
# TEMA A ANALIZAR
# ==========================================

tema = input("Ingresa el tema o hashtag a analizar: ")

# ==========================================
# BUSCAR TWEETS
# ==========================================

tweets = tweepy.Cursor(
    api.search_tweets,
    q=tema,
    lang="es",
    tweet_mode="extended"
).items(100)

# ==========================================
# LISTAS
# ==========================================

usuarios = []
fechas = []
textos = []
sentimientos = []
polaridades = []

# ==========================================
# ANALIZAR TWEETS
# ==========================================

for tweet in tweets:

    try:

        texto = tweet.full_text

        # Análisis de sentimiento
        analisis = TextBlob(texto)

        polaridad = analisis.sentiment.polarity

        # Clasificación
        if polaridad > 0:
            sentimiento = "Positivo"

        elif polaridad < 0:
            sentimiento = "Negativo"

        else:
            sentimiento = "Neutral"

        # Guardar datos
        usuarios.append(tweet.user.screen_name)
        fechas.append(tweet.created_at)
        textos.append(texto)
        sentimientos.append(sentimiento)
        polaridades.append(polaridad)

    except:
        print("Error en un tweet")

# ==========================================
# CREAR DATAFRAME
# ==========================================

df = pd.DataFrame({
    "Usuario": usuarios,
    "Fecha": fechas,
    "Tweet": textos,
    "Sentimiento": sentimientos,
    "Polaridad": polaridades
})

# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print("\n")
print("===================================")
print("RESULTADOS DEL ANÁLISIS")
print("===================================")

print(df.head())

# ==========================================
# GUARDAR CSV
# ==========================================

df.to_csv("resultados_twitter.csv", index=False)

print("\nArchivo CSV guardado correctamente")

# ==========================================
# CONTEO DE SENTIMIENTOS
# ==========================================

conteo = df["Sentimiento"].value_counts()

print("\n")
print(conteo)

# ==========================================
# GRÁFICA DE BARRAS
# ==========================================

conteo.plot(
    kind="bar"
)

plt.title("Análisis de Sentimientos")
plt.xlabel("Tipo de Sentimiento")
plt.ylabel("Cantidad")

plt.show()
