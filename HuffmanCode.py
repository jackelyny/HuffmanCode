import sys
import heapq
import math


class Node:
    def __init__(self, letter, frequency):
        self.parent = None
        self.left = None
        self.right = None
        self.letter = letter
        self.frequency = frequency


def traversal(huffman_tree, path, words):

    if huffman_tree.left is not None:
        path.append('0')
        words = traversal(huffman_tree.left, path, words)
        path.pop()

    if len(huffman_tree.letter) == 1:
        words.append((huffman_tree.letter, ''.join(path)))

    if huffman_tree.right is not None:
        path.append('1')
        words = traversal(huffman_tree.right, path, words)
        path.pop()

    return words


input = open(sys.argv[1], 'r')
characters_list = list(input.read())

count = {}
frequency = {}
h = []
heapq.heapify(h)
total = len(characters_list)
for i in characters_list:
    if i in count:
        count[i] = count[i] + 1
    else:
        count[i] = 1
for key, value in count.items():
    frequency[key] = (value / total)
    heapq.heappush(h, (frequency[key], key, (Node(key, frequency[key]))))

while len(h) > 1:
    n = Node(None, 0)
    a = heapq.heappop(h)
    b = heapq.heappop(h)
    n.left = a[2]
    n.right = b[2]
    n.frequency = n.left.frequency + n.right.frequency
    n.letter = n.left.letter + n.right.letter
    heapq.heappush(h, (n.frequency, n.letter, n))
path = []
words = []
huffman_tree = heapq.heappop(h)
traversal(huffman_tree[2], path, words)
words.sort()

avg_length = 0.0
print('Char    Frequency Count  Codeword')
for pair in words:
    string = "{letter:5s} {freq:.6f}% ({count:3d})    {code:<10}"
    print(string.format(letter=pair[0], freq=frequency[pair[0]], count=count[pair[0]], code=pair[1]))
    avg_length += len(pair[1]) * frequency[pair[0]]
print("Average Codeword Length: %.4f" % avg_length)
print("Original Size (ASCII): %d bits" % (len(characters_list) * 8))

block_size = math.ceil(math.log(len(count), 2))
original_block = len(characters_list) * block_size
original_codeword = block_size * len(characters_list)
actual_encoding = round(avg_length * len(characters_list))
ACL_ratio = 100 * (block_size - avg_length) / block_size
file_ratio = 100 * actual_encoding / (len(characters_list) * 8)


print("Original Size (Block Length): {length} bits".format(length=original_block))
print("Actual Encoding Size: %d bits" % actual_encoding)
print("ACL Compression Ratio: %.3f%%" % ACL_ratio)
print("File Compression Ration: %.3f%%" % file_ratio)
input.close()