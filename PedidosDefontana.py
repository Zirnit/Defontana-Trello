import requests
import FechasRelativas as FR
import HeadersKeys as HK

# Para obtener la lista de pedidos y su status en un dict
def lista_pedidos():
    listaPedidosAPI = "https://api.defontana.com/api/Order/List"
    listaPedidosAPIQS = {"FromDate":FR.hace2Semanas,"ToDate":FR.en1Semana,"ItemsPerPage":"1000","PageNumber":"0","fromNumber":"0"}
    listaPedidosJson = requests.request("GET", listaPedidosAPI, headers=HK.headersDefontana, params=listaPedidosAPIQS).json()
    listaStatusPedidosDefon = {}
    for i in listaPedidosJson["items"]:
        listaStatusPedidosDefon[str(i["number"])] = i["status"]
    return listaStatusPedidosDefon

# Para obtener del pedido solicitado: ("número de pedido - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_pedido(numero):
    obtenerPedidoAPI = "https://api.defontana.com/api/Order/Get"
    obtenerPedidoAPIQS = {"number":numero}
    pedidoJson = requests.request("GET", obtenerPedidoAPI, headers=HK.headersDefontana, params=obtenerPedidoAPIQS)
    try:
        nombreCliente = pedidoJson.json()["orderData"]["client"]["name"] # A veces, no sé por qué, retorna None. Por eso la excepción 
    except:
        return None
    else:
        fechaVenc = pedidoJson.json()["orderData"]["creationDate"]
        localPedido = pedidoJson.json()["orderData"]["shopID"]
        detallePedido = ["Código \t", "Cant. \t", "Descripción\n"]
        for item in pedidoJson.json()["orderData"]["details"]:
            detallePedido.append(item["code"])
            detallePedido.append(" \t")
            detallePedido.append(str(item["count"]))
            detallePedido.append(" \t")
            detallePedido.append(item["name"])
            detallePedido.append("\n")
        detallePedido.append("\n"+pedidoJson.json()["orderData"]["comment"])
        detallePedido = "".join(detallePedido)
        nombrePedidoTrello = str(numero)+" - "+nombreCliente
        return nombrePedidoTrello, detallePedido, fechaVenc, localPedido
