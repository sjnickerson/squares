# squares.org solver
# Simon Nickerson, 2024-05-18

import sys

def read_relevant_words(word_file, grid):
  file = open(word_file, "r")
  lines = file.readlines()
  file.close()
  grid_letters = set(grid)
  return [w.upper().strip()
          for w in lines
          if len(w.strip()) >= 4
            # If list distinguishes proper nouns, filter these out
            and not (w[0].isupper() and not w.isupper())
            and set(w.upper().strip()).issubset(grid_letters)]

def compute_trie(word_list):
  trie = {}
  for w in word_list:
    t = trie;
    for c in w:
      if not (c in t):
        t[c] = {}
      t = t[c]
    t[""] = '!'
  return trie

#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
  
NEIGHBOURS = [
  [1, 4, 5],                    # 0
  [0, 2, 4, 5, 6],              # 1
  [1, 3, 5, 6, 7],              # 2
  [2, 6, 7],                    # 3
  [0, 1, 5, 8, 9],              # 4
  [0, 1, 2, 4, 6, 8, 9, 10],    # 5
  [1, 2, 3, 5, 7, 9, 10, 11],   # 6
  [2, 3, 6, 10, 11],            # 7
  [4, 5, 9, 12, 13],            # 8
  [4, 5, 6, 8, 10, 12, 13, 14], # 9
  [5, 6, 7, 9, 11, 13, 14, 15], # 10
  [6, 7, 10, 14, 15],           # 11
  [8, 9, 13],                   # 12
  [8, 9, 10, 12, 14],           # 13
  [9, 10, 11, 13, 15],          # 14
  [10, 11, 14]                  # 15
]


def solve_from_prefix(grid, path_prefix, word_prefix, trie):
  found_words = []
  if "" in trie:
    found_words.append(word_prefix)
  for neighbour in NEIGHBOURS[path_prefix[-1]]:
    if neighbour in path_prefix:
      continue
    next_letter = grid[neighbour]
    if next_letter in trie:
      found_words.extend(solve_from_prefix(grid, path_prefix + [neighbour], word_prefix + next_letter, trie[next_letter]))
  return found_words


def solve(grid, trie):
  found_words = []
  for start in range(16):
    start_letter = grid[start]
    if start_letter in trie:
      found_words.extend(solve_from_prefix(grid, [start], str(start_letter), trie[start_letter]))
  return found_words


def solve_from_wordlist(grid, word_list_file_name):
  words = read_relevant_words(word_list_file_name, grid);
  trie = compute_trie(words)
  return set(solve(grid, trie))


def parse_grid():
  if len(sys.argv) != 2:
    sys.exit("Single argument must be the grid as a string of length 16 with optional separators, e.g. MTHU-ZURE-ZNKN-ALIC")
  grid_str = ''.join(filter(str.isalpha, sys.argv[1])) 
  if len(grid_str) != 16:
    sys.exit("Single argument must be the grid as a string of length 16 with optional separators, e.g. MTHU-ZURE-ZNKN-ALIC")
  return list(grid_str.upper())

def output_grid(grid):
  for i in range(4):
    print('   '.join(grid[(i*4):(i*4+4)]))
    print()
  print()
  
def output_words(header, word_list):
  print(header)
  counter = 0
  for w in word_list:
    counter += 1
    print("%-16s" % w, end="")
    if counter % 4 == 0:
      print()
  if counter % 4 != 0:
    print()
  print()

def main():
  grid = parse_grid()
  output_grid(grid)
  easy = sorted(solve_from_wordlist(grid, "words2.txt"))
  medium = sorted(solve_from_wordlist(grid, "words3.txt").difference(easy))
  obscure = sorted(solve_from_wordlist(grid, "words.txt").difference(medium).difference(easy))

  output_words("Easy solutions", easy)
  output_words("Moderate solutions", medium)
  output_words("Obscure solutions", obscure)


main()
