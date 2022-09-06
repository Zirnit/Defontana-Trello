import PedidosDefontana as PD
import TarjetasTrello as TT
import FechasRelativas as FR
import time
from datetime import datetime

lista_pedidos_Cerrados = ["EFX (EN_DESPACHO_FACTURADO)", "EEX (EN_DESPACHO_EN_FACTURACION)", 
"DEX (DESPACHADO_EN_FACTURACION)", "DFX (DESPACHADO_FACTURADO)", "M (CERRADO_MANUAL)"]
lista_pedidos_Semilistos = ["EFX (EN_DESPACHO_FACTURADO)", "EEX (EN_DESPACHO_EN_FACTURACION)",
"DEX (DESPACHADO_EN_FACTURACION)"]

# Consultar pedidos en defontana
def obtenerPedidos():
    pedidosDefontana = PD.lista_pedidos()
    return pedidosDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello()
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, pedidos, tarjetas):
    try:
        nombre, detalle, fecha, local = PD.detalle_pedido(numero) # A veces, no sé por qué, el pedido retorna None. Por eso la excepción
    except:
        print(numero, "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() > FR.hace2Semanas and pedidos[numero] == "P (PENDIENTE)":
            TT.post_trello(nombre, detalle, fecha)
        if numero in tarjetas:
            estado = pedidos[numero]
            if estado == "P (PENDIENTE)":
                estado = "false"
                if local == "MONS.":
                    TT.mod_trello(tarjetas[numero], estado, TT.monsalve_idList)
                elif local == "PLAYA":
                    TT.mod_trello(tarjetas[numero], estado, TT.playa_idList)
                else:
                    TT.mod_trello(tarjetas[numero], estado, TT.pendientes_idList)
            elif datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() < FR.ayer and estado in lista_pedidos_Cerrados:
                elimina_Trello(numero, tarjetas)
            # elif estado in lista_pedidos_Semilistos:
            #     estado = "false"
            #     TT.mod_trello(tarjetas[numero], estado, TT.facturando_idList)
            elif estado in lista_pedidos_Cerrados:
                estado = "false"
                TT.mod_trello(tarjetas[numero], estado, TT.listo_idList)
            else:
                print(numero, pedidos[numero])

# Elimina tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.listo_idList)

# Elimina tarjetas Trello que no estén en el listado de pedidos pendientes
def elimina_Trello2(pedidos, tarjetas):
    for numero in tarjetas:
        if numero not in pedidos:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código
def principal():
    pedidos = obtenerPedidos()
    tarjetas = obtenerTarjetas()
    for item in pedidos:
        cargar_trello(item, pedidos, tarjetas)
    elimina_Trello2(pedidos, tarjetas)

# Bucle que mantiene el programa actualizándose   
while True:
    principal()
    print("Actualización: ", datetime.now())
    time.sleep(300) # Tiempo de actualización: 5 minutos
