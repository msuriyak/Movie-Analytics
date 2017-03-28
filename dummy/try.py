import re

with open('critics_films') as f:
    lines = f.readlines()

# lines1 = []

# for i in range(len(lines)):
#     if len(re.findall(r'\d+', lines[i])) != 0:
#         lines1.append(lines[i][0:5] + '\n')
#         lines1.append(lines[i][5:])
#     else:
#         lines1.append(lines[i])


# thefile = open('test.txt', 'w')
# for item in lines1:
#   thefile.write("%s\n" % item)



lines1 = []

for i in range(len(lines)):
    if len(re.findall(r'\d+', lines[i])) != 0:
        a = re.findall(r'\d+', lines[i])
        lines1.append(lines[i])
    else:
        lines1.append(str(a[0]) + ',' + lines[i])

thefile = open('test.csv', 'w')
for item in lines1:
  thefile.write("%s" % item)

