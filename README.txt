The logistic map is the well-known function x(t+1) = k*x(t)*(1 - x(t))

For x in (0,1) and k in (0, 4), it is clear by inspection that x remains within (0,1) for every iteration.

However, what is notable is that for sufficiently high k, repeated applications of the logistic map quickly develop chaotic behavior.

This module exploits the onset of chaos in the logistic map in order to generate a hash.

The algorithm maintains a representation of a number between 0 and 1 in base 256, with each position representated by a byte.

This number is twice is long as the hash length.

Chunks of input equal in size to the hash length are read into the most significant positions of the base-256 number.

The number is passed through the logistic map several times, and the output of the hash function is the contents of the least significant positions of the final number, since they contain the most randomness.

The size of the hash and the number of logistic map iterations can be set arbitrarily (there are very large limits in place merely to prevent infinitely-sized buffers and endless loops). However, k in the logistic map function is always 3.75, since that simplifies the process greatly (we can multiply by 960 and then divide by 256 by shifting, thereby keeping all computation in integers).

It is also possible to set an initial seed value for the least significant bits in the initial number. By chaining logistic map calls along chunks of an object and using seed values that are the output of the previous call, it is therefore also possible to essentially encode a set of bytes.
