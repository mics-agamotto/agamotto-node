from PSI.server import server_perform_preprocess


class PSIServerState:
    server_preprocessed = None

    @staticmethod
    async def preprocess(server_set):
        print("Preprocessing server set and generating polynomials...")
        PSIServerState.server_preprocessed = server_perform_preprocess(server_set)
        print("Preprocessing complete.")
        return PSIServerState.server_preprocessed
