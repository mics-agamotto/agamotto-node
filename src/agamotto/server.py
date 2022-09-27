from sanic import Sanic
from sanic.response import text

app = Sanic("agamotto-node")

@app.route("/")
async def home(request):
    return text("Hello, Agamotto!")
