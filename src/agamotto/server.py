import json
from sanic import Sanic, response
from sanic.response import text
from .state import PSIServerState
from PSI.server import server_perform_psi

app = Sanic("agamotto-node")

@app.route("/")
async def home(request):
    return text("Hello, Agamotto!")

@app.route('/sup')
async def sup(request):
    print(request)
    print("sup")
    return text("hi")

@app.post('/test')
async def test(request):
    res = json.loads(request.body)
    # print(res)
    print('blach')
    pre_processed_result = await PSIServerState.preprocess([1, 2, 3, 4, 5, 6, 7, 8, 9])
    #print(PSIServerState.server_preprocessed)
    performed_psi = server_perform_psi(pre_processed_result, res)
    # print(blah)
    # print(blah)
    return text(performed_psi)