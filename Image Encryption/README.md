Image Encryption (and decryption)

By: Aidan Sharpe

Encrypt the pixel data of an image using a Caesar-Cypher-like algorithm for RGB values in an image

How it works:

Map each of the color channels to a different scrambling of numbers from 0-255
The mappings are saved with each number corresponding to the index of a word in the word list from words.py

The following then occurs 3 times:
- Each pixel in the image is mapped to a new color based on the R, G, & B color maps.
- The image is rotated 90 degrees

Decryption does the same thing backwards, using the words in words.txt as a key to rebuild the R, G, & B color maps

Example files:
Input: a.jpg
Encrypted output: b.jpg
Decrypted output: c.jpg