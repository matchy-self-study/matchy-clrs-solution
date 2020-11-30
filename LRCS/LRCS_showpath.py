import argparse, sys, re

HAS_NUMPY = True

try:
    import numpy as np
except ImportError:
    HAS_NUMPY = False

import matplotlib.pyplot as plt

###############################################################################

match = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

def check_valid_input(string: str) -> bool:
    '''
    Checks whether the input string only contains ATCG
    '''
    search = re.compile(r'[^ACGT]').search
    return not bool(search(string))

def rev(s: str) -> str:
    '''
    Returns the reverse string of input string
    '''
    return s[::-1]

def rev_comp(s: str) -> str:
    '''
    Returns the reverse complementary string of input string according to Watson
    -Crick base pairing law
    '''
    return ''.join([match[c] for c in rev(s)])


def LCS_midpoint(str1: str, str2: str):
    '''
    Computes the longest common subsequence of strings str1 and str2
    '''
    fw_path_x = []
    fw_path_y = []
    n = len(str1)
    dp = np.zeros((n+1, n+1), dtype=np.int32)

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
        fw_path_y.append(i)
        fw_path_x.append(j)
        if curr == dp[i, j-1]: # "left"
            j = j-1
            fw_path_y.append(i)
            fw_path_x.append(j)
        elif curr == dp[i-1, j]: # "up"
            i = i-1
            fw_path_y.append(i)
            fw_path_x.append(j)
        elif curr - 1 == dp[i-1, j-1]: # "up-left", matched
            cand.append(str1[i-1])
            i = i-1; j = j-1
            fw_path_y.append(i)
            fw_path_x.append(j)

    half = ''.join(cand[::-1])

    rev_path_x = [n - x for x in fw_path_y]
    rev_path_y = [n - y for y in fw_path_x]
    fw_path_x = fw_path_x[::-1]
    fw_path_y = fw_path_y[::-1]
    return half + rev_comp(half), fw_path_x + rev_path_x, fw_path_y + rev_path_y

def LCS(str1: str, str2: str, has_numpy=True) -> (str, list, list):
    '''
    Returns one of the longest common subsequence of the two input strings
    '''
    fw_path_x = []
    fw_path_y = []
    rev_path_x = []
    rev_path_y = []
    n = len(str1)
    if has_numpy:
        dp = np.zeros((n+1, n+1), dtype=int)
    else:
        dp = [[0]*(n+1) for i in range(n+1)]

    for i in range(1, n+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i][j-1], dp[i-1][j])

    cand_former = []
    cand_latter = []
    i = n; j = n; k = 0; l = 0
    while (i > n - j):
        curr = dp[i][j]
        if curr == dp[i][j-1]: # "left"
            try:
                assert dp[k+1][l] == dp[k][l] # "down"
            except:
                sys.exit( 'The path is not valid! ' \
                         f'up: {dp[k][l]}, down: {dp[k+1][l]}')
            k = k+1
            j = j-1
            rev_path_x.append(l)
            rev_path_y.append(k)
            fw_path_y.append(i)
            fw_path_x.append(j)
        elif curr == dp[i-1][j]: # "up"
            try:
                assert dp[k][l+1] == dp[k][l] # "right"
            except:
                sys.exit( 'The path is not valid!' \
                         f'left: {dp[k][l]}, right: {dp[k][l+1]}')
            l = l+1
            i = i-1
            rev_path_x.append(l)
            rev_path_y.append(k)
            fw_path_y.append(i)
            fw_path_x.append(j)
        elif curr - 1 == dp[i-1][j-1]: # "up-left", matched
            cand_former.append(str1[k]) # "down-right"
            cand_latter.append(str1[i-1])
            k = k+1; l = l+1
            i = i-1; j = j-1
            rev_path_x.append(l)
            rev_path_y.append(k)
            fw_path_y.append(i)
            fw_path_x.append(j)
    former = ''.join(cand_former)
    latter = ''.join(cand_latter[::-1])
    return former + latter, fw_path_x + rev_path_x[::-1], fw_path_y + rev_path_y[::-1]

################################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=(
        'Print the longest reverse complement sequence of the sequence in the' 'input file'
        ), allow_abbrev=True)
    parser.add_argument('infile', metavar='INPUT', nargs='?',
                        type=str,
                        help='a DNA string or a file containing only one DNA '
                        'string. A DNA string only consists of A, C, G, T '
                        '(case insensitive)')
    parser.add_argument('-o', '--output', metavar='OUTPUT', nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='the file to write the output')

    args = parser.parse_args()

    if args.infile == None:
        parser.print_help()
        sys.exit(0)

    if check_valid_input(args.infile.upper()):
        s = args.infile.upper().strip()
    else:
        try:
            f = open(args.infile, 'r')
        except:
            print('Input is neither a DNA string nor a file!\n')
            parser.print_help()
            sys.exit(1)
        else:
            s = f.read().strip()
            if not check_valid_input(s):
                print('The string stored in the input file is not valid!')
                print('There should only be one DNA string')
                sys.exit(1)
            f.close()

    revcomp_s = rev_comp(s)

    longest_revcomp_subseq, x1, y1 = LCS(s, revcomp_s, has_numpy=HAS_NUMPY)
    longest_revcomp_subseq2, x2, y2 = LCS_midpoint(s, revcomp_s)

    # n = len(longest_revcomp_subseq)
    # first_half = longest_revcomp_subseq[:n//2]
    # second_half = longest_revcomp_subseq[n//2:]

    # try:
    #     assert first_half == rev_comp(second_half)
    # except AssertionError:
    #     sys.exit(f'Not reverse compliment!\n {first_half}\n{second_half}\n')
    n = len(s)
    fig, ax = plt.subplots()
    # ax.plot(x2, y2)
    ax.plot(x1, y1, color='orange')
    ax.legend(['LRCS2'])
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.show()

    outfile = args.output
    outfile.write(longest_revcomp_subseq + '\n')
    outfile.write(longest_revcomp_subseq2 + '\n')
    outfile.close()
