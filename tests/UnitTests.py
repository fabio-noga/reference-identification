import pytest

import TextExtraction


def setUp(self):
    none = []

def tearDown(self):
    none = []

@pytest.mark.parametrize("data, expected_result", [
    ({'autor': ['João Calvão da Silva', "Joao Alfredo da Costa Godofredo"], 'pag': ['78','79', '80'], 'obra': " Sinal De Contrato Promessa ", 'outro': ['Almedina'], 'ano': '2007', 'edicao': '12ª Edição', "vol": ['II', 'III', 'IV'], "notes": ["4", "5"]},
     "Silva, João Calvão da; Godofredo, Joao Alfredo da Costa (2007). \" Sinal De Contrato Promessa \", 12ª Edição, págs. 78, 79 e 80, vols. II, III e IV, notes 4 e 5"),
    ({'autor': ['Fernando de Gravato Morais'], 'pag': ['278', '279'], 'obra': "Contratos-promessa Em Geral.contratos-promessa Em Especial", 'outro': ['Almedina', 'Abril De 2009']},
     "Morais, Fernando de Gravato. \"Contratos-promessa Em Geral.contratos-promessa Em Especial\", págs. 278 e 279"),
])
def test_IeeeCreation(data, expected_result):
    assert TextExtraction.getQuoteJsonAsIEEE(data) == expected_result

@pytest.mark.parametrize("data, expected_result", [
    ("relação ao contrato de depósito bancário ou ao de abertura de crédito em conta corrente, acessoriedade revelada não apenas pela função do próprio contrato, mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais (Maria Raquel Guimarães, ob. cit., pags. 107/112).",
     [{'autor': ['Maria Raquel Guimarães'], 'pag': ['107', '112'], 'obra': "Ob Cit."}]),
    ("Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 ).",
     [{'autor': ['Maria Raquel Guimarães'], 'pag': ['55', '58', '63', '64'], 'obra': "As Transferências Electrónicas De Fundos E Os Cartões De Débito", 'outro': ['Almedina'], 'ano': '1999'}]),
    ("se o cliente decidir contratar, terá de se sujeitar às cláusulas previamente determinadas por outrem, no exercício de um law making power de que este, de facto, desfruta, limitando-se aquele, pois, a aderir a um modelo prefixado\" (cfr. António Pinto Monteiro, Cláusula Penal e Indemnização, pag. 748;Meneses Cordeiro, Direito das Obrigações, pags. 96 e sgs;Vaz Serra, Obrigações, Ideias Preliminares, pags. 162 e sgs;Antunes Varela, Das Obrigações em Geral;Almeida Costa, Direito das Obrigações, pags. 196 e sgs;Mota Pinto, Contratos de Adesão, Revista de Direito e de Estudos Sociais, pags. 119 e sgs.).",
     [{'autor': ['Antunes Varela'], 'pag': ['196', '+']}]),
    ("mesmo Autor em BMJ n. 83, pag. 69 e segs. António Covas (\"Cláusulas Limitativas e de Exclusão da Responsabilidade \", pag. 85 nota 164 e \"Clausula Penal e Indemnização, pag. 31, nota 77).",
     [{'autor': ['António Covas'], 'pag': ['85'], 'obra': "Cláusulas Limitativas E De Exclusão Da Responsabilidade", "note": "77"}])
])
def test_QuoteExtraction(data, expected_result):
    assert TextExtraction.extractQuoteDataFromPhrase(data) == expected_result


# "mesmo Autor em BMJ n. 83, pag. 69 e segs. António Pinto Monteiro (\"Cláusulas Limitativas e de Exclusão da Responsabilidade \", pag. 85 nota 164 e \"Clausula Penal e Indemnização, pag. 31, nota 77)."

#Weird
# "Fernando Andrade Ires de Lima/João de Matos Antunes Varela, Código Civil Anotado , Vol. III, Coimbra, Coimbra Editora, 1987, pp.378 e ss. Mais recentemente, a propósito da legitimidade do alienante, demandado numa ação de preferência, para recorrer de acórdão que julgou procedente a ação, conforme o acórdão do Supremo Tribunal de Justiça de 19 de junho de 2019 (Abrantes Geraldes), proc. n.º 1274/15.8T8FAR.E1.S1"
#
# "O phishing (do inglês fishing «pesca») pressupõe uma fraude electrónica caracterizada por tentativas de adquirir dados pessoais, através do envio de e-mails com uma pretensa proveniência da entidade bancária do receptor, por exemplo, a pedir determinados elementos confidenciais (número de conta, número de contrato, número de cartão de contribuinte ou qualquer outra informação pessoal), por forma a que este ao abri-los e ao fornecer as informações solicitadas e/ou ao clicar em links para outras páginas ou imagens, ou ao descarregar eventuais arquivos ali contidos, poderá estar a proporcionar o furto de informações bancárias e a sua utilização subsequente, cfr Pedro Verdelho, in Phishing e outras formas de defraudação nas redes de comunicação, in Direito da Sociedade De Informação, Volume VIII, 407/419: Maria Raquel Guimarães, in Cadernos de Direito Privado, nº41, Janeiro/Março de 2013;"
#
# "Tal como a posse relevante para usucapião (a par de outros requisitos, deve ser pública), também a oposição exercida pelo detentor precário tem de ser ostensiva em relação àquele em nome de quem possuía, sendo que, como observa Orlando de Carvalho, in \"Introdução à Posse\", RLJ, Ano 123°, nº3792 (1990-1991), a respeito da posse pública, esta não deixa de ser pública quando não é propriamente conhecida de toda a gente, é-o acima de tudo, quando é conhecida do interessado directo ou indirecto - \"trata-se de uma relação mais com o próprio interessado do que com o público em geral\"».",

#João Calvão da Silva in \"Sinal de Contrato Promessa\" , Almedina, 2007, 12ª edição, a páginas 79 a 80
# "(Neste sentido, vide João Calvão da Silva in \"Sinal de Contrato Promessa\" , Almedina, 2007, 12ª edição, a páginas 79 a 80, onde refere: \"A admitir-se a validade da cláusula pela qual o promitente comprador renuncia antecipadamente ao direito de arguir a nulidade estaria aberta a porta para com a maior das facilidades os promitentes vendedores incluirem nas promessas uma cláusula do estilo em que as partes declarariam prescindir das formalidades impostas pelo artigo 410º, nº 3, renunciando à invocação da respectiva omissão, e assim sabotar o sentido e fim de uma norma de protecção da parte mais fraca, o consumidor.",

# "Perfilhando o mesmo entendimento, vide o acórdão do Supremo Tribunal de Justiça de 5 de Julho de 2007 (relator Oliveira Rocha), proferido no processo nº 07B2027, publicado in www.dgsi.pt. Em sentido oposto, vide Fernando Gravato de Morais, in \"Contratos-Promessa em Geral.Contratos-Promessa em Especial\" , Almedina, Abril de 2009, a páginas 278 a 279, quando refere: \"Quanto ao facto de os promitentes prescindirem do reconhecimento presencial das assinaturas, renunciando assim à invocação da nulidade do contrato promessa, cremos que nada obsta a que tal aconteça.",

# TODO: change from JSON to list