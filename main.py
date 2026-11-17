# Name: Shiqian Zhang
import math
import queue
from collections import Counter


class TreeNode(object):
    # data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data

    def __lt__(self, other):
        return self.data < other.data

    def children(self):
        return self.left, self.right


def get_frequencies(fname):
    with open(fname, 'r') as f:
        return Counter(f.read())


def make_huffman_tree(f):
    p = queue.PriorityQueue()
    for c in f:
        p.put(TreeNode(data=(f[c], c)))
    if p.empty():
        return None
    while p.qsize() > 1:
        x = p.get()
        y = p.get()
        p.put(TreeNode(x, y, (x.data[0] + y.data[0], '')))
    return p.get()


def get_code(node, prefix='', code=None):
    # A fresh dictionary avoids mixing codes from different documents.
    if code is None:
        code = {}
    if node is None:
        return code
    if node.left is None and node.right is None:
        code[node.data[1]] = prefix
    else:
        get_code(node.left, prefix + '0', code)
        get_code(node.right, prefix + '1', code)
    return code


def fixed_length_cost(f):
    if not f:
        return 0
    bits_per_character = math.ceil(math.log2(len(f)))
    return sum(f.values()) * bits_per_character


def huffman_cost(C, f):
    return sum(f[c] * len(C[c]) for c in f)


def analyze_files():
    print('File\tFixed-length bits\tHuffman bits\tHuffman / Fixed')
    for fname in ['alice29.txt', 'asyoulik.txt', 'f1.txt',
                  'fields.c', 'grammar.lsp']:
        f = get_frequencies(fname)
        fixed = fixed_length_cost(f)
        codes = get_code(make_huffman_tree(f))
        huffman = huffman_cost(codes, f)
        ratio = f'{huffman / fixed:.6f}' if fixed else 'N/A'
        print(f'{fname}\t{fixed}\t{huffman}\t{ratio}')


# Problem 3: edit distance

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'),
              ('relevant', 'elephant')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'),
              ('relev-ant', '-elephant')]


def MED(S, T):
    if S == '':
        return len(T)
    if T == '':
        return len(S)
    if S[0] == T[0]:
        return MED(S[1:], T[1:])
    return 1 + min(MED(S, T[1:]),       # insertion
                   MED(S[1:], T),       # deletion
                   MED(S[1:], T[1:]))   # substitution


def _distance_table(S, T):
    # dp[i][j] is the distance between S[:i] and T[:j].
    m, n = len(S), len(T)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(dp[i - 1][j] + 1,
                           dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + (S[i - 1] != T[j - 1]))
    return dp


def fast_MED(S, T):
    return _distance_table(S, T)[len(S)][len(T)]


def fast_align_MED(S, T):
    dp = _distance_table(S, T)
    i, j = len(S), len(T)
    aligned_S, aligned_T = [], []
    while i > 0 or j > 0:
        # Tie order: deletion, insertion, then diagonal.
        # Different optimal paths can otherwise produce different alignments.
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            aligned_S.append(S[i - 1])
            aligned_T.append('-')
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            aligned_S.append('-')
            aligned_T.append(T[j - 1])
            j -= 1
        else:
            aligned_S.append(S[i - 1])
            aligned_T.append(T[j - 1])
            i -= 1
            j -= 1
    return ''.join(reversed(aligned_S)), ''.join(reversed(aligned_T))
