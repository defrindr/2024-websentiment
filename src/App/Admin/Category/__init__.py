from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('category', __name__, template_folder="/Category")
registerRoute = Routes(Module)

registerRoute.get("/", controller.index)
registerRoute.get("/create", controller.create)
registerRoute.post("/store", controller.store)
registerRoute.get("/edit/<id>", controller.edit)
registerRoute.post("/update/<id>", controller.update)
registerRoute.post("/destroy/<id>", controller.destroy)
