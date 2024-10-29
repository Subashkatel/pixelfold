"""
convert to csv file
"""
if __name__ == "__main__":
    INPUT_FILE = 'chroot.7big.ps2.txt'
    OUTPUT_FILE = f'{INPUT_FILE[0:-4]}.csv'
    time = 0
    with open(INPUT_FILE, 'r') as raw, open(OUTPUT_FILE, 'w') as csv:
        csv.write(f'{",".join(raw.readline().split())}\n')
        for line in raw:
            fields = line.split()
            if len(fields) == 0:
                time += 1
                continue
            if fields[0] == "%CPU":
                continue
            fields[3] = str(time*5)
            csv.write(f"{','.join(fields[0:5])},{' '.join(fields[5:])}\n")
