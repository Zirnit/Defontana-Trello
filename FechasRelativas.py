import datetime

# Fechas relativas a hoy
hoy = datetime.date.today()
ayer = hoy - datetime.timedelta(days=1)
anteayer = hoy - datetime.timedelta(days=2)
hace1Semana = hoy - datetime.timedelta(days=7)
hace2Semanas = hoy - datetime.timedelta(days=14)
en1Semana = hoy + datetime.timedelta(days=7)
