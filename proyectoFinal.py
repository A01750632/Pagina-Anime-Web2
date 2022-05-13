import json
import random
import requests
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = "Esto no debería ir aqui."

@app.route("/")
def index():
   session["imagenFondo"] = {'url':'/static/images/shinobu.gif'}
   return redirect("/generarImagen")

@app.route("/generarImagen")
def generaImagen():
   session["listaCategorias"] = ["kick","happy","wink","poke","dance","cringe","waifu","neko","shinobu",
   "megumin","bully","cuddle","cry","hug","awoo","pat","smug","bonk","yeet","blush","smile",
   "wave","highfive","nom","bite","glomp","slap","kill"]
   session["categoria"]=random.choice(session["listaCategorias"])
   response = requests.get("https://api.waifu.pics/sfw/"+session["categoria"])
   if(response.status_code == 200):
      session["imagen"] = response.json()
      return redirect("/imagen")
   return render_template("notFound.html")
   
   
@app.route("/imagen")
def imagen():
      return render_template("inicio.html", imagen = session["imagen"],imagenFondo = session["imagenFondo"])

@app.route("/cambiarFondo")
def fondo():
   session["categoria2"]=random.choice(session["listaCategorias"])
   response = requests.get("https://api.waifu.pics/sfw/"+session["categoria2"])
   if(response.status_code == 200):
      session["imagenFondo"] = response.json()
      return render_template("inicio.html", imagen = session["imagen"], imagenFondo = session["imagenFondo"])

@app.route("/datos",methods=["POST"])
def nombre():
   name = request.form.get("name", "dragon_ball")
   nameInTitle = name.lower().capitalize()
   name = name.lower().replace(" ","_")
   response = requests.get("https://anime-facts-rest-api.herokuapp.com/api/v1/"+name)
   if (response.status_code == 200):
      response = response.json()
      return render_template("Anime.html", datosAnime = response, name = nameInTitle, imagenFondo = session["imagenFondo"])
   return render_template("notFound.html")


@app.route("/elegirAnime")
def Anime():
  return render_template("nombreAnime.html", imagen = session["imagen"], imagenFondo = session["imagenFondo"] )

@app.route("/Frase")
def Frase():
   response = requests.get("https://animechan.vercel.app/api/random")
   if(response.status_code == 200):
      response = response.json()
      return render_template("Frase.html", frase = response, imagenFondo = session["imagenFondo"] )
   return render_template("notFound.html")

@app.route("/PersonajeRandom")
def Personaje():
   response = requests.get("https://api.jikan.moe/v4/random/characters")
   if(response.status_code == 200):
      response = response.json()
      return render_template("personaje.html", personaje = response, imagenFondo = session["imagenFondo"] )
   return render_template("notFound.html")

@app.route("/recomendacion")
def recomendacion():
   response = requests.get("https://api.jikan.moe/v4/random/anime")
   if(response.status_code == 200):
      response = response.json()
      return render_template("recomendacion.html", anime = response, imagenFondo = session["imagenFondo"] )
   return render_template("notFound.html")

@app.route("/seasonAnimes")
def season():
   response = requests.get("https://api.jikan.moe/v4/seasons/upcoming")
   if(response.status_code == 200):
      response = response.json()
      for i in response["data"]:
         if i["trailer"]["embed_url"]:
            url = i["trailer"]["embed_url"]
            url = url.replace("utoplay=1", "utoplay=0")
      return render_template("seasonAnime.html", seasonAnimes = response, imagenFondo = session["imagenFondo"] )
   return render_template("notFound.html")

@app.route("/promos")
def promos():
   response = requests.get("https://api.jikan.moe/v4/watch/promos/popular")
   if(response.status_code == 200):
      response = response.json()
      for i in response["data"]:
         if i["trailer"]["embed_url"]:
            url = i["trailer"]["embed_url"]
            url = url.replace("utoplay=1", "utoplay=0")
      return render_template("promos.html", seasonAnimes = response, imagenFondo = session["imagenFondo"] )
   return render_template("notFound.html")
   



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)