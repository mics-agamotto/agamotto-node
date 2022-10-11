from .server import app
from .state import PSIServerState


def main():
    app.add_task(PSIServerState.preprocess([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    app.run(host="0.0.0.0", port=8000, workers=1, dev=True)


if __name__ == "__main__":
    main()
