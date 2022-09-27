# from random import sample
from parameters import server_size, client_size, intersection_size
import random, string

#set elements can be integers < order of the generator of the elliptic curve (192 bits integers if P192 is used); 'sample' works only for a maximum of 63 bits integers.

# disjoint_union = sample(range(2 ** 63 - 1), server_size + client_size)

disjoint_union = []
sample = string.ascii_letters + string.digits
for i in range(server_size + client_size):
    user_len = random.randint(5, 20)
    user = ''.join(random.choice(sample) for j in range(user_len))
    user_encoded = int(bytes(user, "ascii").hex(), 16)
    disjoint_union.append(user_encoded)


intersection = disjoint_union[:intersection_size]
server_set = intersection + disjoint_union[intersection_size: server_size]
client_set = intersection + disjoint_union[server_size: server_size - intersection_size + client_size]

f = open('server_set', 'w')
for item in server_set:
	f.write(str(item) + '\n')
f.close()

g = open('client_set', 'w')
for item in client_set:
	g.write(str(item) + '\n')
g.close()		

h = open('intersection', 'w')
for item in intersection:
	h.write(str(item) + '\n')
h.close()
