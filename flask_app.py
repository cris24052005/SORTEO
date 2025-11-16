import os
import random
import threading
import redis
from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------
# Conexión a KV Store (Redis)
# -------------------------------
REDIS_URL = os.getenv("RENDER_KV_URL")
db = redis.from_url(REDIS_URL, decode_responses=True)

# Premios y probabilidades
PREMIOS = [
    "Pizza personal",
    "Pizza mediana",
    "Pizza grande",
    "Vaso de jugo",
    "Vaso de chicha",
    "Gelatina",
    "Postre",
    "Empanada",
    "Papa Rellena",
    "Tamal",
    "Cena",
    "Tajada de queque",
    "Gaseosa 500ml",
    "Gaseosa 1L"
]
PROBABILIDADES = [7,6,6,7,8,8,7,7,7,7,7,8,8,7]  # Total = 100

file_lock = threading.Lock()

# -------------------------------
# Funciones usando KV
# -------------------------------

def es_codigo_valido(codigo):
    return db.sismember("codigos_validos", codigo)

def es_codigo_usado(codigo):
    return db.sismember("codigos_usados", codigo)

def marcar_codigo_como_usado(codigo):
    db.sadd("codigos_usados", codigo)

# -------------------------------
# Inicializar códigos válidos
# (solo la primera vez)
# -------------------------------
def inicializar_codigos():
    if db.scard("codigos_validos") == 0:
        codigos = [
        "YF71R","XU54Q","RK99W","CE48F","ZV57X","AU53J","DP61B","VL39X","SO78Y","PF83W",
        "GJ91F","WN65V","BH41Y","JX27M","QM52K","ZB62U","OT36L","LY13V","FG74P","KI43D",
        "UF51H","CB28E","NR85T","ID63G","HV92Z","EA97C","MK26X","TP45L","RW18J","BU76A",
        "LX37D","QY82Z","WN15G","VJ49P","CZ73B","FS68K","OI94Y","PE56T","DB21M","GH77R",
        "UK33F","JB86W","AZ91L","YX48V","RG59U","TM12E","IQ67C","PV35Z","HK81S","NW24J",
        "FB72D","UO66G","LM93K","ES47Q","ZT58A","QC14B","BY63F","XJ82T","RM49V","KD75W",
        "AG31H","LP96S","VF57N","HQ18M","ZU42Y","IW69E","NB33C","TK84J","CP51G","FY29R",
        "OX76D","BJ65K","DS97U","GQ43V","MZ12P","UL88W","VE61A","YR39Z","SI74B","KH55T",
        "PN28M","JG92F","WC73R","AV46H","EF16S","RL67D","UX34G","BO89Y","IZ52K","DY25W",
        "TQ91B","FN83J","SW47M","CP14Z","VB68F","LK92P","JR56T","HE37D","YM75R","OG29W",
        "UI41G","ZT83B","AX59S","KV62Y","NC18M","BP45J","EQ77H","FX31L","RD96K","UJ24V",
        "ZI66E","QB81T","PO53F","NY38D","MK72A","GW49S","LH13Z","DS64R","VF87J","CB22U",
        "XP51W","AJ95E","HM28G","TQ46K","IY79B","RZ35V","OU61L","SK82M","BW93T","FN47Y",
        "JG18D","PC36S","XE71R","QV59A","UL24B","ZM85G","KI67W","RT92F","YB53E","NW16J",
        "AH39L","FX74V","DP28M","SO61R","GJ45T","VB97K","CE33Y","QU86B","LY52Z","IT19S",
        "RK48J","BH65D","WM27G","EA94L","ZF76P","OV31E","UX58V","JB43W","HG82M","DN91F",
        "TS69R","YC25A","KJ77B","FR34S","QM56Z","PL12T","WE88G","BI93K","UV41Y","MZ62V",
        "NP79H","SC85D","TL37J","GK54E","FD16W","AY29R","JX81L","CB48Z","OH63T","VW92A",
        "ZU75S","EQ31B","IK24M","PR57G","HY86V","NF13J","GW98K","DB69Y","TM25E","LX42W",
        "RZ73D","SF51R","UO94P","KJ36B","YT87Z","FG19H","PM64S","AC22V","VK78T","WZ45E",
        "BN33L","EH59G","QR81F","JB72K","XS46D","DY97C","OM14J","UV28A","PC65W","FL39R",
        "GK83S","BZ51E","TW67V","IQ96H","NH24G","VP12T","RE58Z","AS73D","UX47J","YW61B",
        "ZI95K","DF49N","QB36R","LJ15S","HK82G","MT28V","CN74Y","PS91E","FG33T","OR57A",
        "BX42W","EJ69L","KU85Z","RV16M","ZA78D","IW24P","GY93B","QF52R","TP66S","HN41J",
        "VK87E","LS35G","MJ12H","DB94K","YX58W","EO79V","NP36Z","CW23A","UF61D","ZQ88R",
        "BT45Y","SV97T","GR19E","KH52F","JL26B","WY73J","WC48M","PX31G","EM64L","RN59S",
        "AB85V","FZ76D","IU91K","OC27H","VE32R","TQ54P","BJ4CM","IY68E","QH19X","DS73T",
        "MK46Z","NB55S","XJ82W","LG29V","PF71Y","UK37R","ZR64B","VW95G","ERQ23","CJD45",
        "ROSD3","DF49N","SDP1D","DFL40","DFC34","GLDS2","3DS4S","FLD40","DFKS1","SAW23",
        "43DF3","DF34D","ÑLK34","MKF4Ñ","DFV90","23FG0","HL0FB","FGÑFÑ","ZMC40","VMX20",
        "SLD-1","SD-45","MCX-6"
        ]
        db.sadd("codigos_validos", *codigos)


inicializar_codigos()

# -------------------------------
# Rutas
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sortear', methods=['POST'])
def sortear():
    codigo_usuario = request.form['codigo'].strip().upper()

    if not es_codigo_valido(codigo_usuario):
        return render_template('index.html', error="❌ El código ingresado no es válido.")

    if es_codigo_usado(codigo_usuario):
        return render_template('index.html', error="⚠️ Este código ya fue utilizado.")

    # sortear premio
    premio_ganado = random.choices(PREMIOS, weights=PROBABILIDADES, k=1)[0]

    # guardar en KV
    marcar_codigo_como_usado(codigo_usuario)

    return render_template('resultado.html', premio_final=premio_ganado)

# -------------------------------
# Ejecutar localmente
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
