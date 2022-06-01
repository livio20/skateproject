#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import contextily
import geopandas as gpd
import io
import pandas as pd
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------


from flask import Flask, render_template, request, Response , redirect , url_for
app = Flask(__name__)


#IMPORTAZIONE CSV
#------------------------------------------------------------------------------------------------------------------------------------------------------------
cuscinetti1 = pd.read_csv("static/csv/cuscinetti.csv")
grip1 = pd.read_csv("static/csv/grip.csv")
hardware1 = pd.read_csv("static/csv/hardware.csv")
ruote1 = pd.read_csv("static/csv/ruote.csv")
tavole1 = pd.read_csv("static/csv/tavole.csv")
tool1 = pd.read_csv("static/csv/tool.csv")
truck1 = pd.read_csv("static/csv/truck.csv")
wax1 = pd.read_csv("static/csv/wax.csv")
dati = pd.read_csv("database.csv")
park1 = pd.read_csv('skatepark_milano_list.csv')
milano = gpd.read_file('ds964_nil_wm-20220322T104009Z-001.zip')
PARKS1 = gpd.read_file('PARKS.geojson')
SHOPS1 = gpd.read_file('SHOPS.geojson')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#INIZIO
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def scelta():
    return render_template("choice.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#PAGINA SELEZIONE USER-OSPITE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args['Scelta']
    if scelta == 'utente':
        return render_template("utente.html")
    elif scelta == 'ospite':
        return render_template("home.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#PAGINA SELEZIONE NUOVO ACCOUNT-LOGIN
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/selezione1', methods=['GET'])
def selezione1():
    scelta = request.args['Scelta']
    if scelta == 'login':
        return render_template("login.html")
    elif scelta == 'new_account':
        return render_template("new_account.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#CODICE LOGIN
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
            psw = request.form.get("psw")
            email = request.form.get("email")
            dati = pd.read_csv("database.csv")
            for _, r in dati.iterrows():
                print(r['email'])
                if email == r['email'] and psw == r['psw']:
                    return render_template("home.html")   
            return render_template("error.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#CODICE REGISTRAZIONE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    global utente

    if request.method == 'GET':
        return render_template('register.html')
    else:
        psw = request.form.get("psw")
        cpas = request.form.get("psw-repeat")
        email = request.form.get("email")
        utente = [{"psw": psw, "email": email}]
                   
        if cpas!= psw:
            return 'le password non corrispondono'
        else:
            dati = pd.read_csv("database.csv")
            dati = dati.append(utente, ignore_index=True)
            dati.to_csv('database.csv')
            return render_template('home.html', psw = psw , email = email)
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE TERMINI
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/termini", methods=["GET"])
def termini():
    return render_template("termini.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE HOME
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE ACCOUNT(SCELTA ACCOUNT-LOGIN)
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/account", methods=["GET"])
def acc():
    return render_template("utente.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE STORIA
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/storia", methods=["GET"])
def storia():
    return render_template("storia.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE TAVOLE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/tavole", methods=["GET"])
def tavole():
    return render_template("tavole.html",risultato=tavole1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO TAVOLE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_tavole/<foto>", methods=["GET"])
def dettaglio_tavole(foto):
    tav=tavole1[tavole1['foto']==foto]
    return render_template("dettaglio_tavole.html",marca=list(tav.marca),prezzo=list(tav.prezzo),dimensione=list(tav.dimensione),foto=list(tav.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE TRUCK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/truck", methods=["GET"])
def truck():
    return render_template("truck.html",risultato=truck1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO TRUCK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_truck/<foto>", methods=["GET"])
def dettaglio_truck(foto):
    tru=truck1[truck1['foto']==foto]
    return render_template("dettaglio_truck.html",marca=list(tru.marca),prezzo=list(tru.prezzo),dimensione=list(tru.dimensione),foto=list(tru.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE RUOTE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/ruote", methods=["GET"])
def ruote():
    return render_template("ruote.html",risultato=ruote1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO RUOTE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_ruote/<foto>", methods=["GET"])
def dettaglio_ruote(foto):
    ruo=ruote1[ruote1['foto']==foto]
    return render_template("dettaglio_ruote.html",marca=list(ruo.marca),prezzo=list(ruo.prezzo),dimensione=list(ruo.dimensione),foto=list(ruo.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE CUSCINETTI
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/cuscinetti", methods=["GET"])
def cuscinetti():
    return render_template("cuscinetti.html",risultato=cuscinetti1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO CUSCINETTI
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_cuscinetti/<foto>", methods=["GET"])
def dettaglio_cuscinetti(foto):
    cus=cuscinetti1[cuscinetti1['foto']==foto]
    return render_template("dettaglio_cuscinetti.html",marca=list(cus.marca),prezzo=list(cus.prezzo),foto=list(cus.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE HARDWARE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/hardware", methods=["GET"])
def hardware():
    return render_template("hardware.html",risultato=hardware1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO HARDWARE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_hardware/<foto>", methods=["GET"])
def dettaglio_hardware(foto):
    har=hardware1[hardware1['foto']==foto]
    return render_template("dettaglio_hardware.html",marca=list(har.marca),prezzo=list(har.prezzo),dimensione=list(har.dimensione),foto=list(har.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE GRIP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/grip_tape", methods=["GET"])
def grip():
    return render_template("grip_tape.html",risultato=grip1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO GRIP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_grip/<foto>", methods=["GET"])
def dettaglio_grip(foto):
    gri=grip1[grip1['foto']==foto]
    return render_template("dettaglio_grip.html",marca=list(gri.marca),prezzo=list(gri.prezzo),foto=list(gri.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE TOOL
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/tool", methods=["GET"])
def tool():
    return render_template("tool.html",risultato=tool1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO TOOL
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_tool/<foto>", methods=["GET"])
def dettaglio_tool(foto):
    too=tool1[tool1['foto']==foto]
    return render_template("dettaglio_tool.html",marca=list(too.marca),prezzo=list(too.prezzo),foto=list(too.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE WAX
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/wax", methods=["GET"])
def wax():
    return render_template("wax.html",risultato=wax1['foto'].to_list())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#RUOTE DETTAGLIO WAX
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/dettaglio_wax/<foto>", methods=["GET"])
def dettaglio_wax(foto):
    waa=wax1[wax1['foto']==foto]
    return render_template("dettaglio_wax.html",marca=list(waa.marca),prezzo=list(waa.prezzo),foto=list(waa.foto))
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE GUIDA TAVOLE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/guida_tavole", methods=["GET"])
def guida_tavole():
    return render_template("guida_tavole.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE GUIDA TRUCK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/guida_truck", methods=["GET"])
def guida_truck():
    return render_template("guida_truck.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE GUIDA RUOTE 
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/guida_ruote", methods=["GET"])
def guida_ruote():
    return render_template("guida_route.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE CONTATTI
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/contatti", methods=["GET"])
def contatti():
    return render_template("contatti.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE MAPPA GENERALE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/maps", methods=["GET"])
def maps():
    return render_template("maps.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE VISUALIZZAZIONE MAPPA SKATEPARK-SKATESHOP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (11,7))
    PARKS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    SHOPS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='blue')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.2, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE SKATEPARK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/skatepark", methods=["GET"])
def park():
    return render_template("skatepark.html",risultato=PARKS1.to_html())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE VISUALIZZAZIONE MAPPA SKATEPARK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/mappapark', methods=['GET'])
def mappapark():
    fig, ax = plt.subplots(figsize = (11,7))
    PARKS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE RICERCA PER UNO SKATEPARK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/ricercapark', methods=['GET'])
def ricercapark():
    global quartiere,park_quartiere
    nome_park=request.args["park3"]
    quartiere=milano[milano.NIL.str.contains(nome_park.upper())]
    park_quartiere=PARKS1[PARKS1.within(quartiere.geometry.squeeze())]
    return render_template("skatepark_risultato.html",risultatopark2=park_quartiere.to_html())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE VISUALIZZAZIONE MAPPA RICERCA SKATEPARK
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/mappapark1', methods=['GET'])
def mappapark1():
    fig, ax = plt.subplots(figsize = (10,10))
    park_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE SKATESHOP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/skateshop", methods=["GET"])
def shop():
    return render_template("skateshop.html",risultatoshop=SHOPS1.to_html())   
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE VISUALIZZAZIONE MAPPA SKATESHOP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/mappashop', methods=['GET'])
def mappashop():
    fig, ax = plt.subplots(figsize = (11,7))
    SHOPS1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE RICERCA PER UNO SKATESHOP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/ricercashop', methods=['GET'])
def ricercashop():
    global quartiere,shop_quartiere
    nome_shop=request.args["shop3"]
    quartiere=milano[milano.NIL.str.contains(nome_shop.upper())]
    shop_quartiere=SHOPS1[SHOPS1.within(quartiere.geometry.squeeze())]
    return render_template("skateshop_risultato.html",risultatoshop2=shop_quartiere.to_html())
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE VISUALIZZAZIONE MAPPA RICERCA SKATESHOP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/mappashop1', methods=['GET'])
def mappashop1():
    fig, ax = plt.subplots(figsize = (10,10))
    shop_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, color='RED')
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE CARTA DI CREDITO
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/compra', methods=['GET'])
def compra():
    return render_template("compra.html")
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#ROUTE
#------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/paga', methods=['GET'])
def paga():
   return render_template("paga.html")   
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#fine#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
