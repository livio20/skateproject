import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import contextily
import geopandas as gpd
import io
import pandas as pd



from flask import Flask, render_template, request, Response , redirect , url_for
app = Flask(__name__)

dati = pd.read_csv("database.csv")
park1 = pd.read_csv('skatepark_milano_list.csv')
milano = gpd.read_file('ds964_nil_wm-20220322T104009Z-001.zip')
PARKS1 = gpd.read_file('PARKS.geojson')
SHOPS1 = gpd.read_file('SHOPS.geojson')

@app.route("/", methods=["GET"])
def scelta():
    return render_template("choice.html")


@app.route('/selezione', methods=['GET'])
def selezione():

    scelta = request.args['Scelta']
    if scelta == 'utente':
        return render_template("utente.html")
    elif scelta == 'ospite':
        return render_template("home.html")


@app.route('/selezione1', methods=['GET'])
def selezione1():

    scelta = request.args['Scelta']
    if scelta == 'login':
        return render_template("login.html")
    elif scelta == 'new_account':
        return render_template("new_account.html")


##registrazione##
@app.route('/register', methods=['GET', 'POST'])
def register():
    

    global utente

    if request.method == 'GET':
        return render_template('register.html')
    else:
        psw = request.form.get("psw")
        cpas = request.form.get("psw-repeat")
        email = request.form.get("email")
        
        
        utente = [{"psw": psw,"email":email}]

       


        #controllo password
        if cpas!= psw:
            return 'le password non corrispondono'
        else:
            dati_append = dati.append(utente,ignore_index=True)
            dati_append.to_csv('database.csv',index=False)
            return render_template('login.html',  psw = psw ,utente = utente, email = email)





##login##

@app.route('/login', methods=['GET', 'POST'])
def login():

    #dichiarazione di df. legge il file json creato per preservare i dati degli utenti
        #login sistemato---
        # ciclo for di controllo alternativo
        if request.method == 'GET':
            return render_template('home.html')
        elif request.method == 'POST':
            pas = request.form.get("psw")
            email = request.form.get("email")
            print(psw, email)

        for _, r in dati.iterrows():
            if email == r['email'] and psw == r['psw']:  
                return '<h1>login effettuato </h1>'

        return '<h1>Errore</h1>'




@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/login1", methods=["GET"])
def home1():
    return render_template("home.html")


@app.route("/storia", methods=["GET"])
def storia():
    return render_template("storia.html")


@app.route("/tavole", methods=["GET"])
def tavole():
    return render_template("tavole.html")


@app.route("/truck", methods=["GET"])
def truck():
    return render_template("truck.html")


@app.route("/ruote", methods=["GET"])
def ruote():
    return render_template("ruote.html")


@app.route("/cuscinetti", methods=["GET"])
def cuscinetti():
    return render_template("cuscinetti.html")


@app.route("/hardware", methods=["GET"])
def hardware():
    return render_template("hardware.html")


@app.route("/grip_tape", methods=["GET"])
def grip():
    return render_template("grip_tape.html")


@app.route("/tool", methods=["GET"])
def tool():
    return render_template("tool.html")


@app.route("/wax", methods=["GET"])
def wax():
    return render_template("wax.html")


@app.route("/guida_tavole", methods=["GET"])
def guida_tavole():
    return render_template("guida_tavole.html")


@app.route("/guida_truck", methods=["GET"])
def guida_truck():
    return render_template("guida_truck.html")


@app.route("/guida_ruote", methods=["GET"])
def guida_ruote():
    return render_template("guida_route.html")


@app.route("/contatti", methods=["GET"])
def contatti():
    return render_template("contatti.html")

@app.route("/maps", methods=["GET"])
def maps():
    return render_template("maps.html")


#MAPPA MAPS#

@app.route('/mappa', methods=['GET'])
def mappa():

    fig, ax = plt.subplots(figsize = (12,8))

    PARKS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    SHOPS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='blue')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.2, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')






#mappe e ricerca skatepark#
@app.route("/skatepark", methods=["GET"])
def park():
    
    return render_template("skatepark.html",risultato=PARKS1.to_html())
   
@app.route('/mappapark', methods=['GET'])
def mappapark():

    fig, ax = plt.subplots(figsize = (12,8))

    PARKS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/ricercapark', methods=['GET'])
def ricercapark():
    global quartiere,park_quartiere
    nome_park=request.args["park3"]
    quartiere=milano[milano.NIL.str.contains(nome_park.upper())]
    park_quartiere=PARKS1[PARKS1.within(quartiere.geometry.squeeze())]
    
    return render_template("skatepark_risultato.html",risultatopark2=park_quartiere.to_html())

@app.route('/mappapark1', methods=['GET'])
def mappapark1():

    fig, ax = plt.subplots(figsize = (10,10))

    park_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


#mappe e ricerca skateshop#
@app.route("/skateshop", methods=["GET"])
def shop():
    return render_template("skateshop.html",risultatoshop=SHOPS1.to_html())   

@app.route('/mappashop', methods=['GET'])
def mappashop():

    fig, ax = plt.subplots(figsize = (12,8))

    SHOPS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/ricercashop', methods=['GET'])
def ricercashop():
    global quartiere,shop_quartiere
    nome_shop=request.args["shop3"]
    quartiere=milano[milano.NIL.str.contains(nome_shop.upper())]
    shop_quartiere=SHOPS1[SHOPS1.within(quartiere.geometry.squeeze())]
    
    return render_template("skateshop_risultato.html",risultatoshop2=shop_quartiere.to_html())

@app.route('/mappashop1', methods=['GET'])
def mappashop1():

    fig, ax = plt.subplots(figsize = (10,10))

    shop_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')






#fine#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
