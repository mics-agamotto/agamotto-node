from agamotto.example_emails import EXAMPLE_EMAILS

from PSI.client_offline import client_prepare
from PSI.client_online import hash_and_fhe_encrypt_with_sk, oprf_process_result, hash_and_fhe_encrypt, process_psi_answer
from PSI.server_offline import server_prepare, server_oprf
from PSI.server_online import perform_oprf_online, perform_psi_online
from PSI.username_gen import preprocess_email, decode_ascii_str
import tenseal as ts
import proto.seal_pb2 as pb
import base64
from PSI.cuckoo_hash import Cuckoo
from PSI.auxiliary_functions import windowing
import json
from PSI.parameters import sigma_max, output_bits, plain_modulus, poly_modulus_degree, number_of_hashes, bin_capacity, alpha, ell, hash_seeds
from math import log2

def main2():
    # both
    preprocessed_emails = list(map(preprocess_email, EXAMPLE_EMAILS))

    # client
    client_encoded = client_prepare(0xdeadbeef123123, preprocessed_emails[:5])

    # server 
    client_encoded_prfed = perform_oprf_online(0xbeefdead321321, client_encoded)

    # client
    oprf_result = oprf_process_result(0xdeadbeef123123, client_encoded_prfed)

    # client
    ctx, query, priv_ctx, win = hash_and_fhe_encrypt(oprf_result)

    # server
    server_encoded_prfed = server_oprf(0xbeefdead321321, preprocessed_emails)

    # server
    poly_coeffs = server_prepare(server_encoded_prfed)

    # server
    answer = perform_psi_online(poly_coeffs, ctx, query)

    # client
    intersection = process_psi_answer(priv_ctx, win, EXAMPLE_EMAILS[:5], oprf_result, answer)
    print(intersection)


def main():
    # main2()
    # return

    # hash_and_fhe_encrypt([1, 2, 3, 4, 5])

    # with open("pk.bin", "rb") as f:
    #     data = f.read()

    # pctx = pb.TenSEALContextProto()
    # pctx.public_context.public_key = data
    # pctx.encryption_parameters = base64.b64decode(CTX)
    # ctx = ts.context_from(pctx.SerializeToString())

    # with open("ct.bin", "rb") as f:
    #     data = f.read()
    
    # vp = pb.BFVVectorProto()
    # vp.sizes.append(5)
    # vp.ciphertexts.append(data)

    # vec = ts.bfv_vector_from(ctx, vp.SerializeToString())
    # vec = vec * 2
    
    # vpp = pb.BFVVectorProto()
    # vpp.ParseFromString(vec.serialize())

    # with open("result", "wb") as f:
    #     encoded = base64.b64encode(vpp.ciphertexts[0])
    #     f.write(encoded)
    # return

    # private_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=2**13, plain_modulus=536690689)
    # public_context = ts.context_from(private_context.serialize())
    # public_context.make_context_public()

    # pctx = pb.TenSEALContextProto()
    # pctx.ParseFromString(private_context.serialize(save_public_key=True, save_secret_key=True))
    # print(pctx.private_context.secret_key)

    # vv=ts.bfv_vector(ts.context_from(pctx.SerializeToString()), [1,2,3,4,5]).decrypt()
    # return
    # vp.ParseFromString(vv.serialize())
    
    # with open("foo.bin", "rb") as f:
    #     data = f.read()

    #     foo = pb.BFVVectorProto()
    #     foo.sizes.append(5)
    #     foo.ciphertexts.append(data)

    #     print(ts.bfv_vector_from(private_context, vp.SerializeToString()))

    # preprocessed_emails = list(map(preprocess_email, EXAMPLE_EMAILS))
    # client_encoded = client_prepare(0xdeadbeef123123, preprocessed_emails[:5])
    # client_encoded_prfed = perform_oprf_online(0xbeefdead321321, client_encoded)
    # oprf_result = oprf_process_result(0xdeadbeef123123, client_encoded_prfed)
    # ctx, query, priv_ctx, win = hash_and_fhe_encrypt(oprf_result)

    # server_encoded_prfed = server_oprf(0xbeefdead321321, preprocessed_emails)
    # poly_coeffs = server_prepare(server_encoded_prfed)

    with open("query.json", "r") as f:
        data = json.load(f)
    
    print(data.keys())
    pctx = pb.TenSEALContextProto()
    pctx.encryption_parameters = base64.b64decode(data["parms"])
    pctx.public_context.public_key = base64.b64decode(data["pk"])
    # pctx.private_context.secret_key = base64.b64decode(data["sk"])

    base = 2 ** ell
    minibin_capacity = int(bin_capacity / alpha)
    logB_ell = int(log2(minibin_capacity) / ell) + 1 # <= 2 ** HE.depth
    enc_query_serialized = [[None for j in range(logB_ell)] for i in range(1, base)]
    for k in data.keys():
        if "ct" not in k:
            continue
        
        tokens = k.split("_")
        i = int(tokens[1])
        j = int(tokens[2])
        vp = pb.BFVVectorProto()
        vp.sizes.append(poly_modulus_degree)
        vp.ciphertexts.append(base64.b64decode(data[k]))
        enc_query_serialized[i][j] = vp.SerializeToString()

    # sk = ts.context_from(pctx.SerializeToString())
    # ctx, query, priv_ctx, win = hash_and_fhe_encrypt_with_sk(sk, [1,2,3,4,5])
    poly_coeffs = server_prepare([
        123454321,
        222222,
        3,
        4,
        5,
        6,
        3213,
        515314,
        44231,
        10
    ])
    answer = perform_psi_online(poly_coeffs, pctx.SerializeToString(), enc_query_serialized)

    answer_cpp = []
    for ans in answer:
        vp = pb.BFVVectorProto()
        vp.ParseFromString(ans)
        answer_cpp.append(base64.b64encode(vp.ciphertexts[0]).decode())

    obj = {
        "ciphertexts": answer_cpp
    }
    with open("response.json", "w") as f:
        json.dump(obj, f)

    # answer = perform_psi_online(poly_coeffs, ctx, query)
    # intersection = process_psi_answer(sk, [], [], [], answer)

    # print(list(map(decode_ascii_str, intersection)))


if __name__ == "__main__":
    main()
