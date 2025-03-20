from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl.backend import backend
import os

def main():
    # Weak Collision
    weak_collision_avg = 0
    for trial in range(5):
        str1 = "abf"
        digest = hashes.Hash(hashes.SHA256(), backend)
        digest.update(str1.encode("utf-8"))
        hash1 = digest.finalize()

        total_trials = 0
        while True:
            randstr = os.urandom(3)
            randdigest = hashes.Hash(hashes.SHA256(), backend)
            randdigest.update(randstr)
            hash2 = randdigest.finalize()
            total_trials += 1

            if hash1[:3] == hash2[:3]:
                break

        weak_collision_avg += total_trials

    print("Average trials for weak collision:", weak_collision_avg / 5)

    # Strong Collision
    strong_collision_avg = 0
    for i in range(100):
        total_trials = 0
        unique_hashes = set()

        while True:
            str1 = os.urandom(3)
            digest = hashes.Hash(hashes.SHA256(), backend)
            digest.update(str1)
            hash1 = digest.finalize()
            total_trials += 1

            if hash1[:3] in unique_hashes:
                break

            unique_hashes.add(hash1[:3])

        strong_collision_avg += total_trials

    print("Average trials for strong collision:", strong_collision_avg / 100)

if __name__ == "__main__":
    main()
