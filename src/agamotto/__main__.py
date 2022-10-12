from .server import app, preprocess


def main():
    app.run(host="0.0.0.0", port=8000, workers=1, dev=True)


def main_prod():
    app.run(host="0.0.0.0", port=443, ssl=dict(
    cert="/certs/server.crt",
    key="/certs/server.key",
))


if __name__ == "__main__":
    main()
