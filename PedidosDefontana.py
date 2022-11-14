import requests
import FechasRelativas as FR
import HeadersKeys as HK

# Para obtener la lista de pedidos y su status en un dict
def lista_pedidos():
    listaPedidosAPI = "https://api.defontana.com/api/Order/List"
    listaPedidosAPIQS = {"FromDate":FR.hace2Semanas,"ToDate":FR.en1Semana,"ItemsPerPage":"1000","PageNumber":"0","fromNumber":"4400"}
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
        nombreCliente = pedidoJson.json()["orderData"]["client"]["name"]
    except:
        return None
    else:
        fechaCrea = pedidoJson.json()["orderData"]["creationDate"][0:19]
        fechaVenc = pedidoJson.json()["orderData"]["expirationDate"]
        localPedido = pedidoJson.json()["orderData"]["shopID"]
        detallePedido = ["Código \t", "Cant. \t", "Descripción\n"]
        comentario = pedidoJson.json()["orderData"]["comment"]
        if comentario == None:
            comentario = ""
        for item in pedidoJson.json()["orderData"]["details"]:
            detallePedido.append(item["code"])
            detallePedido.append(" \t")
            detallePedido.append(str(item["count"]))
            detallePedido.append(" \t")
            detallePedido.append(item["name"])
            detallePedido.append("\n")
        detallePedido.append("\n"+comentario)
        detallePedido = "".join(detallePedido)
        nombrePedidoTrello = str(numero)+" - "+nombreCliente
        return nombrePedidoTrello, detallePedido, fechaCrea, fechaVenc, localPedido
