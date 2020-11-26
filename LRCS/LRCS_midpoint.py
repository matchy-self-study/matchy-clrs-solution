import argparse, sys
import numpy as np

match = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

def rev(s):
    return s[::-1]

def rev_comp(s):
    return ''.join([match[c] for c in rev(s)])

def LCS(str1, str2):
    '''
    Computes the longest common subsequence of strings str1 and str2
    '''
    n = len(str1)
    dp = np.zeros((n+1, n+1), dtype=int)

    for i in range(1, n+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i, j] = 1 + dp[i-1, j-1]
            else:
                dp[i, j] = max(dp[i, j-1], dp[i-1, j])

    max_j = np.argmax(np.flipud(dp[1:,1:]).diagonal()) + 1

    cand = []
    i = n - max_j; j = max_j
    while (i != 0 and j != 0):
        curr = dp[i, j]
        if curr == dp[i, j-1]: # "left"
            j = j-1
        elif curr == dp[i-1, j]: # "up"
            i = i-1
        elif curr - 1 == dp[i-1, j-1]: # "up-left", matched
            cand.append(str1[i-1])
            i = i-1; j = j-1
    half = ''.join(cand[::-1])
    return half + rev_comp(half)


parser = argparse.ArgumentParser(description=(
    'Print the longest reverse complement sequence of the sequence in the input'
    ' file'
    ), allow_abbrev=True)
parser.add_argument('infile', metavar='FILE', nargs='?',
                    type=str,
                    help='The file containing the input sequence or a string')
parser.add_argument('-o', '--output', metavar='OUTPUT', nargs='?',
                    type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='The file to write the output.')

args = parser.parse_args()

if args.infile == None:
    parser.print_help()
    sys.exit(0)

try:
    f = open(args.infile, 'r')
    s = f.read().strip()
    f.close()
except:
    s = args.infile.strip()

revcomp_s = rev_comp(s)

longest_revcomp_subseq = LCS(s, revcomp_s)

n = len(longest_revcomp_subseq)
print(n)
first_half = longest_revcomp_subseq[:n//2]
second_half = longest_revcomp_subseq[n//2:]

try:
    assert first_half == rev_comp(second_half)
except AssertionError:
    sys.exit(f"Not reverse compliment!\n {first_half}\n{second_half}\n\n")

outfile = args.output
outfile.write(longest_revcomp_subseq + '\n')
outfile.close()
