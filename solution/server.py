from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

ordenes = {}


class OrdenComercio:    
    def __init__(self, client, status, payment, shipping, products, code, expiration, order_type):        
        self.client = client
        self.status = status
        self.payment = payment
        self.shipping = shipping
        self.products = products
        self.code = code
        self.expiration = expiration
        self.order_type = order_type

class Fisica(OrdenComercio):
    def __init__(self, client, status, payment, shipping, products, code, expiration, order_type ):
        super().__init__(client, status, payment, shipping, products, code, expiration, "Fisica")

class Digital(OrdenComercio):
    def __init__(self, client, status, payment, shipping, products, code, expiration, order_type ):
        super().__init__(client, status, payment, shipping, products, code, expiration, "Digital")

class ComercioFactory:
    @staticmethod
    def create_orden( client, status, payment, shipping, products, code, expiration, order_type):
        if order_type == "fisica":
            return Fisica(client, status, payment, shipping, products, code, expiration, order_type)
        elif order_type == "digital":
            return Digital(client, status, payment, shipping, products, code, expiration, order_type)

        else:
            raise ValueError("no valido")
        

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class ComercioService:
    def __init__(self):
        self.factory = ComercioFactory()
    
    def add_orden(self, data):
        client = data.get("client", None)
        status = data.get("status", None)
        payment = data.get("payment", None)
        shipping = data.get("shipping", None)
        products = data.get("products", None)
        code = data.get("code", None)
        expiration = data.get("expiration", None)
        order_type = data.get("order_type", None)       

        orden_com = self.factory.create_orden(
            client, status, payment, shipping, products, code, expiration, order_type
        )
        ordenes[len(ordenes) + 1] = orden_com
        return orden_com
    
    def list_ordenes(self):
        return {index: orden.__dict__ for index, orden in ordenes.items()}

    def search_orden_for_status(self,status):
        ordenes_encontrados = []
        for orden in ordenes.values():
            if orden.status == status:
                ordenes_encontrados.append(animal)
        return ordenes_encontrados

    def delete_orden(self, orden_id):
        if orden_id in ordenes:
            del ordenes[orden_id]
            return {"message": "orden eliminado"}
        else:
            return None

            
        


class ComercioRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.comercio_service = ComercioService()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.comercio_service.add_orden(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "ruta no encontrada"}
            )

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/orders":
            if "status" in query_params:
                estado = query_params["status"][0]
                ordenes_filtrados = self.comercio_service.search_orden_for_status(estado)
                if ordenes_filtrados:
                    orden_serializable = [orden.__dict__ for orden in ordenes_filtrados]
                    HTTPDataHandler.handle_response(self, 200, orden_serializable)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "No se encontraron pendientes "})
            
            else:
                response_data = self.comercio_service.list_ordenes()
                orden_serializable = {index: orden for index, orden in response_data.items()}
                HTTPDataHandler.handle_response(self, 200, orden_serializable)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "ruta no encontrada"})
    
    def do_PUT(self):
       if self.path.startswith("/orders/"):
           id = int(self.path.split("/")[-1])
           data = HTTPDataHandler.handle_reader(self)
           response_data = self.comercio_service.update_orden(id, data)
           if response_data:
               HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
           else:
               HTTPDataHandler.handle_response(
                   self, 404, {"message": "orden no encontrado"}
               )
       else:
           HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no encontrada"}
           )
        
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ComercioRequestHandler)
        print("Iniciado")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando")
        httpd.socket.close()


if __name__ == "__main__":
    main()

