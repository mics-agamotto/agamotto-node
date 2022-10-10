from .example_emails import EXAMPLE_EMAILS
from .server import app


def main():
    app.run(host="0.0.0.0", port=8000, workers=1, dev=True)


if __name__ == "__main__":
    main()
