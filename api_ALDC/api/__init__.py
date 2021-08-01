from flask_restful import Api
from app import app
from .Compression import Compression
from .Decompression import Decompression

restServer = Api(app)

restServer.add_resource(Compression,"/api/compress")
restServer.add_resource(Decompression,"/api/decompress")