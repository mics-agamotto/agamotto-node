import json
from sanic import Sanic, response
from sanic.log import logger
from sanic.response import text, file
from .example_emails import EXAMPLE_EMAILS, EXAMPLE_PASSWORDS
from PSI.server import server_perform_preprocess, server_perform_psi
from PSI.username_gen import encode_ascii_str, preprocess_email

app = Sanic("agamotto-node")


async def preprocess(app):
    logger.info("Preprocessing server set and generating polynomials...")
    logger.info(f"Server set: {EXAMPLE_EMAILS} {EXAMPLE_PASSWORDS}")
    preprocessed_emails = list(map(preprocess_email, EXAMPLE_EMAILS))
    app.ctx.server_preprocessed = server_perform_preprocess(preprocessed_emails)
    preprocessed_passwords = list(map(encode_ascii_str, EXAMPLE_PASSWORDS))
    app.ctx.server_preprocessed_passwords = server_perform_preprocess(
        preprocessed_passwords
    )
    logger.info("Preprocessing complete.")


@app.route("/sup")
async def sup(request):
    print(request)
    print("sup")
    return text("hi")


@app.route("/snapshot")
async def snapshot(request):
    app.add_task(preprocess)
    return text("yes")


@app.post("/usernamePSI")
async def usernamePSI(request):
    res = json.loads(request.body)
    performed_psi = server_perform_psi(app.ctx.server_preprocessed, res)
    return text(performed_psi)


@app.post("/passwordPSI")
async def passwordPSI(request):
    res = json.loads(request.body)
    performed_psi = server_perform_psi(app.ctx.server_preprocessed_passwords, res)
    return text(performed_psi)
