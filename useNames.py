import csv

names = []
with open("assets/surnames.csv", 'r', newline='', encoding='utf-8') as csvfile: #4200-072 e 44 e 3060-123 ??
    lines = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in lines:
        name = ', '.join(row).split(',')[0]
        names.append(name)

names.sort()


def check_phrases(phrase, wordList):
    characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
    for char in characters_to_replace:
        phrase = phrase.replace(char, "")
    words = phrase.split(" ")

    for i, word in enumerate(words):
        if word in wordList:
            if i != len(words)-1 and words[i+1] in wordList:
                return True
    return False


# Example usage
phrases = [
    "Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 ).",
    "Subjacente ao levantamento de numerário de uma máquina automática de caixa e à operação de pagamento automático está um contrato, designado por \"contrato de utilização\" do cartão.",
]

for phrase in phrases:
    result = check_phrases(phrase.lower(), names)
    print(result)