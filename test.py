import hashlib
import matplotlib.pyplot as plt
import random
import string
import time
import math
from collections import Counter
from HWVL1 import HWVL as HWVL1
from HWVL2 import HWVL as HWVL2

def random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def string_to_bits(s: str) -> str:
    return ''.join(f"{ord(c):08b}" for c in s)

def bit_difference(h1: str, h2: str) -> int:
    b1 = string_to_bits(h1)
    b2 = string_to_bits(h2)
    max_len = max(len(b1), len(b2))
    b1 = b1.ljust(max_len, '0')
    b2 = b2.ljust(max_len, '0')
    return sum(c1 != c2 for c1, c2 in zip(b1, b2))

def time_hash_function(hash_func, data):
    start_time = time.time()
    hash_func(data)
    return time.time() - start_time

def bit_uniformity(hash_output: str):
    bits = string_to_bits(hash_output)
    ones = bits.count('1')
    zeros = bits.count('0')
    return ones / len(bits) * 100, zeros / len(bits) * 100

def collision_test(hash_func, trials=10000):
    hashes = set()
    for _ in range(trials):
        s = random_string()
        h = hash_func(s)
        if h in hashes:
            return True
        hashes.add(h)
    return False

def preimage_attack(hash_func, length=6, max_tries=100000):
    target_input = random_string(length)
    target_hash = hash_func(target_input)
    for _ in range(max_tries):
        guess = random_string(length)
        if hash_func(guess) == target_hash and guess != target_input:
            return True
    return False

def second_preimage_attack(hash_func, length=6, max_tries=100000):
    input1 = random_string(length)
    h1 = hash_func(input1)
    for _ in range(max_tries):
        input2 = random_string(length)
        if input1 != input2 and hash_func(input2) == h1:
            return True
    return False

def calculate_entropy(s):
    prob = [v / len(s) for v in Counter(s).values()]
    return -sum(p * math.log2(p) for p in prob)

def max_run_length(bits):
    max_run = 1
    current_run = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    return max_run

NUM_TESTS = 500

def wrap_std_hash(hash_func):
    return lambda s: hash_func(s.encode()).hexdigest()

hash_algorithms = {
    "HWVL1": HWVL1,
    "HWVL2": HWVL2,
    "MD5": wrap_std_hash(hashlib.md5),
    "SHA1": wrap_std_hash(hashlib.sha1),
    "SHA224": wrap_std_hash(hashlib.sha224),
    "SHA256": wrap_std_hash(hashlib.sha256),
    "SHA384": wrap_std_hash(hashlib.sha384),
    "SHA512": wrap_std_hash(hashlib.sha512),
    "BLAKE2b": wrap_std_hash(hashlib.blake2b),
    "BLAKE2s": wrap_std_hash(hashlib.blake2s),
    "SHA3_224": wrap_std_hash(hashlib.sha3_224),
    "SHA3_256": wrap_std_hash(hashlib.sha3_256),
    "SHA3_384": wrap_std_hash(hashlib.sha3_384),
    "SHA3_512": wrap_std_hash(hashlib.sha3_512),
}

avalanche_results = {k: [] for k in hash_algorithms}
time_results = {k: [] for k in hash_algorithms}
entropy_results = {k: [] for k in hash_algorithms}
run_lengths = {k: [] for k in hash_algorithms}

for _ in range(NUM_TESTS):
    text = random_string()
    mod_text = text[:-1] + chr((ord(text[-1]) + 1) % 94 + 33)

    for name, func in hash_algorithms.items():
        h1 = func(text)
        h2 = func(mod_text)
        diff = bit_difference(h1, h2)
        total = len(string_to_bits(h1))
        avalanche_results[name].append((diff / total) * 100)
        entropy_results[name].append(calculate_entropy(h1))
        run_lengths[name].append(max_run_length(string_to_bits(h1)))
        time_results[name].append(time_hash_function(func, text))

x = list(range(1, NUM_TESTS + 1))
plt.figure(figsize=(16, 10))
plt.subplot(2, 1, 1)
for algo in avalanche_results:
    plt.plot(x, avalanche_results[algo], label=f'{algo} Bit Diff %')
plt.title('Avalanche Effect')
plt.ylabel('% Bit Difference')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
for algo in time_results:
    plt.plot(x, time_results[algo], label=f'{algo} Time (s)')
plt.title('Hash Time')
plt.xlabel('Test')
plt.ylabel('Seconds')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

for algo in avalanche_results:
    print(f"{algo} - Avalanche: {sum(avalanche_results[algo])/NUM_TESTS:.2f}%, Entropy: {sum(entropy_results[algo])/NUM_TESTS:.2f}, Max Run: {sum(run_lengths[algo])/NUM_TESTS:.2f}, Time: {sum(time_results[algo])/NUM_TESTS:.6f}s")

print("\n--- Security Tests (10000 tries) ---")
for algo, func in hash_algorithms.items():
    try:
        print(f"Collision {algo}:", collision_test(func))
        print(f"Preimage {algo}:", preimage_attack(func))
        print(f"Second Preimage {algo}:", second_preimage_attack(func))
    except Exception as e:
        print(f"{algo} skipped due to error: {e}")
