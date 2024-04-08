import requests

url = "http://localhost:8000/"
ep = "orders"

url_o = f"{url}/{ep}"
productos = ["camiseta","pantalon","zapatos"]
productos1 = ["Licuadora","Refrigerador","Lavadora"]
orden_nueva ={        
    "client": "Juan Perez",
    "status": "pendiente",
    "payment": "Tarjeta de credito",
    "shipping": 10.0,
    "products": productos,    
    "order_type": "fisica"   
}
orden_nueva1 ={        
    "client": "Maria Ridruguez",
    "status": "pendiente",
    "payment": "Paypal",
    "shipping": "",
    "products": "",
    "code": "ABC123",
    "expiration": "2022-12-31",
    "order_type": "digital"   
}
orden_nueva2 ={        
    "client": "Ana Guitierrez",
    "status": "pendiente",
    "payment": "Tarjeta de debito",    
    "shipping": 10.0,
    "products": productos1,
    "order_type": "fisica"   
}


# post
r = requests.request(method="POST", url=url_o, json=orden_nueva)
print(r.text)
print()

# post
r = requests.request(method="POST", url=url_o, json=orden_nueva1)
print(r.text)
print()

# get
r = requests.request(method="GET", url=url_o)
print(r.text)
print()

# get ? status= pendiente
status="pendiente"
ruta=f"{url_o}?status={status}"
r = requests.request(method="GET", url=ruta)
print(r.text)
print()

# put
orden_modificada ={  

    "status": "en proceso",
    
}
id=1
ruta_put = f"{url_o}/{id}"
r = requests.request(method="PUT", url=ruta_put, json=orden_modificada)
print(r.text)
print()

# delete
id=1
ruta_del = f"{url_o}/{id}"
r = requests.request(method="DELETE", url=ruta_del)
print(r.text)
print()

# post
r = requests.request(method="POST", url=url_o, json=orden_nueva2)
print(r.text)
print()

# get
r = requests.request(method="GET", url=url_o)
print(r.text)
print()





