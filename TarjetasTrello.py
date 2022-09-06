import requests
import HeadersKeys as HK

# Lista idList de Trello
Lista1 = "{id}" # id de lista 1
Lista2 = "{id}" # id de lista 2
Lista3 = "{id}" # id de lista 3
Lista4 = "{id}" # id de lista 4


# Create Trello card
def post_trello(nombre, detalle, fecha):
    trelloCard = "https://api.trello.com/1/cards" # Dirección API
    TrelloQS = {"key":"key","token":"token",
    "idList":"idlist", # Lista del pedido en Trello
    "name":nombre, # Nombre de la tarjeta
    "desc":detalle, # Descripción de la tarjeta
    "pos":"top", # Posición en la cual se crea la tarjeta (top, bottom, or a positive float)
    "due": fecha} # Fecha de "caducidad" de la tarjeta
    requests.request("POST", trelloCard, headers=HK.trelloHeaders, params=TrelloQS)

# Para obtener las ID de las tarjetas de Trello
def lista_tarjetas_trello():
    tarjetasTrelloURL = "https://api.trello.com/1/boards/{boardID}/cards" # filter Valid Values: all, closed, none, open, visible.
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
    querystring = {"key":"key",
    "token":"token",
    "closed": closed,
    "idList": idList}
    requests.put(trelloCard, headers=HK.trelloHeaders, params=querystring)
