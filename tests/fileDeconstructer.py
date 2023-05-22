
def apelidos():
    with open("./../assets/apelidos", "r", encoding='utf-8') as outfile:
        lines = outfile.readlines()
        names = []
        for line in lines:
            if line[0] != ',':
                continue
            name = line.split(",")[1]
            names.append(name)

    with open("./../assets/apelidos.txt", "w", encoding='utf-8') as outfile:
        lines = [str(item) + '\n' for item in names]
        outfile.writelines(lines)
    print(names)
    print(len(names))

def proprios():
    with open("../assets/proprios", "r", encoding='utf-8') as outfile:
        lines = outfile.readlines()
        names = []
        for line in lines:
            if line == "\n" or "NOME" in line:
                continue
            names.append(line.capitalize())
    names = list(set(names))
    names.sort()
    with open("./../assets/proprios.txt", "w", encoding='utf-8') as outfile:
        outfile.writelines(names)
    print(names)
    print(len(names))