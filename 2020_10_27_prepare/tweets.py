lines = open("tweets.txt").readlines()
s = 0
g = 0
for line in lines:
    line_lower = line.lower().strip().split(" ")
    if "#gopdebates" in line_lower or "#gopdebate" in line_lower:
        if line_lower[0] == 'rt':
            pass
        else:
            g += 1
            print(s)
    s += 1
print("Number of matched tweets: %s"%(g))