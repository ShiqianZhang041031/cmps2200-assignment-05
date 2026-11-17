# CMPS 2200 Assignment 5
## Answers

**Name:** Shiqian Zhang

## 1: Fixed-Length vs. Variable-Length Codes

### 1d

The following results come from running `analyze_files()` on the five supplied files. Costs count encoded character bits only, excluding the codebook and file metadata. Files are read in Python text mode, as in the starter code.

| File | Fixed-length cost (bits) | Huffman cost (bits) | Huffman / Fixed |
|---|---:|---:|---:|
| alice29.txt | 1,039,367 | 676,374 | 0.650756 |
| asyoulik.txt | 876,253 | 606,448 | 0.692092 |
| f1.txt | 1,340 | 826 | 0.616418 |
| fields.c | 78,050 | 56,206 | 0.720128 |
| grammar.lsp | 26,047 | 17,356 | 0.666334 |

Huffman coding uses fewer bits for every tested file, taking about 62% to 72% of the fixed-length cost. It assigns shorter codes to more frequent characters, reducing the frequency-weighted total cost. The exact ratio varies because documents have different alphabet sizes and character-frequency distributions. The smallest ratio here is for f1.txt, while the largest is for fields.c. The trend does not mean that a larger document must have a better compression ratio.

### 1e

Let m = |Sigma| be the number of distinct characters, let n be the document length, and suppose every character appears n/m times.

If m is a power of two, every Huffman code has length log2(m), so the total cost is n log2(m) bits, exactly the same as fixed-length encoding.

For arbitrary m >= 2, let k = floor(log2(m)). An optimal Huffman tree for equal frequencies has 2^(k+1) - m leaves at depth k and 2m - 2^(k+1) leaves at depth k+1. Thus the average cost per character is

L = k + 2 - 2^(k+1)/m,

and the document cost is nL bits. This average lies between log2(m) and ceil(log2(m)). For example, when m = 3, the code lengths are 1, 2, 2, giving an average of 5/3 bits per character rather than 2.

The cost is consistent for equal-frequency documents with the same length and alphabet size, regardless of their actual symbols or order. It is not one constant across all documents: changing n or m changes the total cost. Different tie choices can change which character receives which code without changing the optimal cost.

For m = 1, the implementation uses an empty codeword and counts zero payload bits, assuming the document length is known separately. This matches the fixed-length formula. A practical file format must also store decoding information.

## 2: Making Change

### 2a

Assume N is a nonnegative integer and there is an unlimited supply of coins with values 1, 2, ..., 2^k. Maintain a remainder R, initially N. Process denominations from largest to smallest. For each value d, take q = floor(R/d) coins, record that count, and replace R by R mod d. Stop when the remainder is zero.

Equivalently, repeatedly take the largest available coin no greater than the remainder. Using division computes all repeated choices of the same denomination at once.

For N > 0, denominations greater than N can be skipped, so start at exponent j = min(k, floor(log2(N))). For N = 0, return no coins.

### 2b

**Greedy-choice property.** Let d be the largest available denomination no greater than the current positive remainder R. In a minimum-coin solution, there cannot be two coins of any value 2^i < d: replacing that pair with one coin of value 2^(i+1) preserves the amount and reduces the number of coins.

Consequently, all coins smaller than d together contribute at most

1 + 2 + ... + d/2 = d - 1.

Write R = qd + r, where 0 <= r < d. A solution cannot contain more than q coins of value d. If it contains fewer than q, its smaller coins must contribute at least d + r, which exceeds d - 1. Therefore every optimal solution must contain exactly q coins of value d. This is exactly the greedy choice. For d = 1, only unit coins remain, so the choice is immediate.

**Optimal substructure.** After choosing those q coins, the remaining amount is r. The coins used for r must form an optimal solution for r. Otherwise, replacing them with a solution using fewer coins would also improve the solution for R, contradicting optimality.

The greedy choice is therefore safe, and the remainder is a smaller instance with the same structure. Inducting on the remainder, with base case R = 0, proves the greedy algorithm is optimal.

### 2c

For the division-based algorithm in 2a, each visited denomination requires constant work under the unit-cost arithmetic model. For N > 0, at most min(k, floor(log2(N))) + 1 denominations are visited. Therefore the worst-case work and span are both

O(1 + min(k, floor(log2(N)))).

The span equals the work for this sequential implementation because each remainder depends on the previous step. If the algorithm scans all denominations without first skipping those larger than N, both bounds are O(k + 1). If all powers up to N are available, the usual bound is O(log N) for N >= 2. N = 0 takes constant time.

These bounds represent the answer as counts per denomination. Explicitly outputting c individual coins adds O(c) work and, for a sequential output loop, O(c) span. This matters when the largest denomination is fixed and N is much larger than it.

## 3: Edit Distance

### 3a

Let D(i,j) be the minimum edit cost of transforming the first i characters of S into the first j characters of T.

Base cases:

- D(0,j) = j, because j insertions are necessary.
- D(i,0) = i, because i deletions are necessary.

For i,j > 0,

D(i,j) = min(D(i-1,j) + 1,
             D(i,j-1) + 1,
             D(i-1,j-1) + delta),

where delta = 0 if S[i-1] = T[j-1], and delta = 1 otherwise.

The three choices are deletion, insertion, and matching/substitution. Any optimal alignment ends in one of these choices. The preceding alignment must itself be optimal for the corresponding shorter prefixes. Otherwise, replacing it with a cheaper one would lower the total cost, a contradiction. Taking the minimum over all three choices therefore gives the optimum.

The recursive MED implementation uses the equivalent recurrence on suffixes. When the first characters differ, it considers insertion, deletion, and substitution, each with unit cost.

### Implementation notes for 3b and 3c

fast_MED fills the table bottom-up. fast_align_MED traces optimal predecessors from its bottom-right entry, adding a hyphen for an insertion or deletion. It reverses the collected characters to produce the final alignment. For ties, it checks deletion, then insertion, then a diagonal step, which produces the supplied expected alignments.

Both implementations use O((|S|+1)(|T|+1)) table space and sequential work. The traceback adds O(|S|+|T|) work.

