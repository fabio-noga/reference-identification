import os

current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = current_dir
while not os.path.isfile(os.path.join(ROOT_FOLDER, '../README.md')):
    ROOT_FOLDER = os.path.dirname(ROOT_FOLDER)

# Train the tagger on the tagged sentences in the corpus
MAC_MORPHO_FILE = "mac_morpho_custom.txt"

# https://duvidas.dicio.com.br/abreviaturas-lista-de-abreviacoes/
ABBREV = ['exs', 'exas', 'trf', 'dr', 'dra', 'prof', 'r', 'al', 'als',
          "proc", "procs", "n", "ac", "fls", "art", "arts", "ep", "cfr", "cf", "ob", "obs", "cit", "dl",
          "doc", "docs", "ed", "rel", "j", "v.g", "Lx",
          "ver", "vol", "segs",
          "p", "ps", "p", 'pp', "págs", "pags", "pag", "pág",  # Paginas
          "loc", "op", "ap", "ss", "vs", "cons", "acs",
          'inc', 'e.g', 'i.e', 'etc', 'sgs', 'vg', 'Lx', 'J',

          # "º ", "ª ", "º", "ª", "º",
          # "I", "V", "X", "D", "L", "C", "M",
          "1", "2", "3", "4", "5", "6", "7", "8", "9"]

PATTERNS = [
    r" in ",
    r" by ",
    r" pag\. ",
    r" pág\. ",
    r" pags\. ",
    r" págs\. ",
    r" p\. ",
    r" pp\. ",
    r" pps\. ",
    r" cfr\. ",
    r" citando ",
    r"afirma que",
    r"a expressão é de",
    r"como .+ sublinha",
    r"como dá conta",
    r"como ensina",
    r"como nos dá conta",
    r"como sublinha",
    r"como sugerido por",
    r"como sustenta",
    r"conforme alerta",
    r"conforme discorre",
    r"conforme explicam",
    r"conforme explica",
    r"do mesmo modo,",
    r"em sentido próximo .+ se pronuncia",
    r" escreve ",
    r"explica o autor:",
    r"na doutrina",
    r"na síntese de",
    r"nas palavras de",
    r"neste sentido",
    # r"neste sentido, afirma",
    r"no mesmo sentido aponta",
    # r"no mesmo sentido aponta também o prof.",
    # r"No mesmo sentido, refere .+ in artigo publicado",
    # r"Para ...",
    # r"Por todos, cfr.",
    # r"Refere, a este propósito, ... in...",
    r"seguindo .+ a obra de",
    r"segundo",
    r"sobre .+ vide",
    # r"sobre este ponto, .+ vide ainda",
    # r"neste sentido, vide",
    # r"em sentido oposto, vide",
    r"sobre o tema pode ver-se ainda",
    r" vide ",
    # r"vide, por todos,",
    r"como acentua a ",
    r"como acentua o ",
    r"por Acórdão do ",
    r"por Acórdão da ",
    r"mencionado acórdão do",
    r"mencionado acórdão da",
    r" cfr. ",

]