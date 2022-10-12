from .server import app, preprocess


def main():
    app.run(host="0.0.0.0", port=8000, workers=1, dev=True)


if __name__ == "__main__":
    main()
