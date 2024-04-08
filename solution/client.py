import requests

url = "http://localhost:8000/"
ep = "orders"

url_o = f"{url}/{ep}"

orden_nueva ={        
    "client": "alex",
    "status": "alex",
    "payment": "alex",
    "shipping": "alex",
    "products": "alex",
    "code": "alex",
    "expiration": "alex",
    "order_type": "fisica"   
}

# post
r = requests.request(method="POST", url=url_o, json=orden_nueva)
print(r.text)

# get
r = requests.request(method="GET", url=url_o)
print(r.text)

# get ? status= pendiente
status="pendiente"
ruta=f"{url_o}?status={status}"
r = requests.request(method="GET", url=ruta)
print(r.text)

# delete
id=1
ruta_del = f"{url_o}/{id}"
r = requests.request(method="DELETE", url=ruta_del)
print(r.text)




