from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl.backend import backend
import os

def collision_average(is_weak_collision, num_trials):
    total_trials = 0

    for _ in range(num_trials):
        unique_hashes = set()
        count = 0

        while True:
            str1 = os.urandom(3)
            digest = hashes.Hash(hashes.SHA256(), backend)
            digest.update(str1)
            hash1 = digest.finalize()

            if hash1[:3] in unique_hashes:
                break

            unique_hashes.add(hash1[:3])
            count += 1

        total_trials += count

    avg = total_trials / num_trials

    if is_weak_collision:
        print("Average trials for weak collision:", avg)
    else:
        print("Average trials for strong collision:", avg)

def main():
    # Weak Collision
    collision_average(True, 5)

    # Strong Collision
    collision_average(False, 100)

if __name__ == "__main__":
    main()
