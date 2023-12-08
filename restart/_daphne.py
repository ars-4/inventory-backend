from daphne.server import Server
server = Server("StockBackend.asgi:application")
server.on('changed', lambda: server.reload)
server.run()

# from daphne.service.server import Server
# server = Server()
# server.on('changed', lambda: server.reload)
# server.run()