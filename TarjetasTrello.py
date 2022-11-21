import requests
import HeadersKeys as HK

# Lista idList de Trello board "Pedidos"
pendientes_idList = "61ce1d50882ab9559d105e44" #Pendientes Santiago
playa_idList = "62f67cff9ba3ce0c4ffd4be2" # Pendientes playa
monsalve_idList = "62f67d119efeba8106426433" # Pendientes Monsalve
listo_idList = "61ce1d50882ab9559d105e46"
sodexo_idList = "63728d27fb591a00e0656147"

# Lista labelList de Trello board "Pedidos"
etiqueta_Playa = "62eaecd5dfd104854cc9ff3d"
etiqueta_Monsalve = "62f691943b8e600bfc3bad29"
etiqueta_Sodexo = "63728b8b472fe7012578ce78"

# Create Trello card
def post_trello(nombre, detalle, fechaC, fechaV, idLabels="false", idList=pendientes_idList):
    trelloCard = "https://api.trello.com/1/cards" # Dirección API
    TrelloQS = {
    "key":HK.tKey,
    "token":HK.tToken,
    "idList":idList, # Lista del pedido en Trello
    "name":nombre, # Nombre de la tarjeta
    "desc":detalle, # Descripción de la tarjeta
    "pos":"top", # Posición en la cual se crea la tarjeta (top, bottom, or a positive float)
    "start": fechaC, # Fecha de creación de la tarjeta
    "due": fechaV, # Fecha de "caducidad" de la tarjeta
    "idLabels": idLabels} # Etiqueta de la tarjeta
    requests.request("POST", trelloCard, headers=HK.trelloHeaders, params=TrelloQS)

# Para obtener las ID de las tarjetas de Trello
def lista_tarjetas_trello():
    tarjetasTrelloURL = "https://api.trello.com/1/boards/61ce1d50882ab9559d105e43/cards" # filter Valid Values: all, closed, none, open, visible.
    IDtarjetasTrello = {}
    requestTarjetasTrello = requests.request(
    "GET",
    tarjetasTrelloURL,
    headers=HK.trelloHeaders,
    params=HK.trelloQuery
    ).json()
    for i in requestTarjetasTrello:
        espacio = i["name"].index(" ")
        IDtarjetasTrello[i["name"][:espacio]] = i["id"]
    return IDtarjetasTrello

# Modificar tarjeta Trello
def mod_trello(cardID, closed, idList):
    trelloCard = f"https://api.trello.com/1/cards/{cardID}" # Dirección API
    querystring = {"key":HK.tKey,
    "token":HK.tToken,
    "closed": closed,
    "idList": idList,}
    requests.put(trelloCard, headers=HK.trelloHeaders, params=querystring)
