# from random import sample
from .parameters import server_size, client_size, intersection_size
import hashlib, random, string

# set elements can be integers < order of the generator of the elliptic curve (192 bits integers if P192 is used); 'sample' works only for a maximum of 63 bits integers.

# disjoint_union = sample(range(2 ** 63 - 1), server_size + client_size)


def encode_ascii_str(s: str) -> int:
    digest = hashlib.sha256(s.encode()).digest()
    # We pack the first 28 bits of sha256(s) as the int representation
    val = ((digest[0] * 256 + digest[1]) * 256 + digest[2]) * 16 + ((digest[3] >> 4) % 16)
    return val


def decode_ascii_str(s: int) -> str:
    digest = (
        hex((s >> 20) % 256)[2:]
        + hex((s >> 12) % 256)[2:]
        + hex((s >> 4) % 256)[2:]
        + hex(s % 16)[2:]
    )
    return digest


def preprocess_email(s: str) -> int:
    if "@" not in s:
        raise RuntimeError("Invalid email address")

    [username, domain] = s.split("@")
    return encode_ascii_str(username)


def generate_username_dataset():
    disjoint_union = []
    sample = string.ascii_letters + string.digits
    for i in range(server_size + client_size):
        user_len = random.randint(5, 20)
        user = "".join(random.choice(sample) for j in range(user_len))
        disjoint_union.append(encode_ascii_str(user))

    intersection = disjoint_union[:intersection_size]
    server_set = intersection + disjoint_union[intersection_size:server_size]
    client_set = (
        intersection
        + disjoint_union[server_size : server_size - intersection_size + client_size]
    )

    return server_set, client_set, intersection


if __name__ == "__main__":
    server_set, client_set, intersection = generate_username_dataset()
    f = open("server_set", "w")
    for item in server_set:
        f.write(str(item) + "\n")
    f.close()

    g = open("client_set", "w")
    for item in client_set:
        g.write(str(item) + "\n")
    g.close()

    h = open("intersection", "w")
    for item in intersection:
        h.write(str(item) + "\n")
    h.close()
