
with open('gene.fna', 'r') as f:
    lines = f.read().split('\n')[1:]

s = ''

for line in lines:
    if line.startswith('>'):
        continue
    s += line.upper().replace('N', '').replace('X', '').replace('R', '').replace('Y', '').replace('S', '').replace('W', '').replace('K', '').replace('M', '').replace('B', '').replace('D', '').replace('H', '').replace('V', '')

with open('gene.txt', 'w') as f:
    f.write(s)
