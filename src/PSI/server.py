import base64
import math
import json

import proto.seal_pb2 as pb

from PSI.server_offline import server_prepare
from PSI.server_online import perform_psi_online
from PSI.parameters import poly_modulus_degree, bin_capacity, alpha, ell


def server_perform_preprocess(server_set):
    return server_prepare(server_set)


def server_perform_psi(server_preprocessed, request):
    print(request.keys())
    pctx = pb.TenSEALContextProto()
    pctx.encryption_parameters = base64.b64decode(request["parms"])
    pctx.public_context.public_key = base64.b64decode(request["pk"])

    base = 2**ell
    minibin_capacity = int(bin_capacity / alpha)
    logB_ell = int(math.log2(minibin_capacity) / ell) + 1  # <= 2 ** HE.depth
    enc_query_serialized = [[None for j in range(logB_ell)] for i in range(1, base)]
    for k in request.keys():
        if "ct" not in k:
            continue

        tokens = k.split("_")
        i = int(tokens[1])
        j = int(tokens[2])
        vp = pb.BFVVectorProto()
        vp.sizes.append(poly_modulus_degree)
        vp.ciphertexts.append(base64.b64decode(request[k]))
        enc_query_serialized[i][j] = vp.SerializeToString()

    answer = perform_psi_online(
        server_preprocessed, pctx.SerializeToString(), enc_query_serialized
    )
    answer_cpp = []
    for ans in answer:
        vp = pb.BFVVectorProto()
        vp.ParseFromString(ans)
        answer_cpp.append(base64.b64encode(vp.ciphertexts[0]).decode())

    resp = {"ciphertexts": answer_cpp}
    return resp
