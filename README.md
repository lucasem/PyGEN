# PyGEN
Very simple solver for puzzle 66 written in python.

Code based on https://bitcointalk.org/index.php?topic=5432068.0

Can easily be modified for other puzzles.

# How it works
1. It generates a batch of sequential private keys with random starting points in the puzzle 66 keyspace;

2. It generates their corresponding P2PKH(Compressed) addresses using https://github.com/iceland2k14/secp256k1;

3. Then, it searches in the addresses for '13zb1hQbWV';

4. Finally, if it finds a match, it saves the results in a file named 'found.txt'.

# Tests
#Test using 12 cpu threads:

1 million keys checked in 3.1 seconds.

10 million keys checked in 22.5 seconds.

Not as fast as other programs, but has the advantage of running on almost any device.

# Why
Python is easy, and I'm a noob.
