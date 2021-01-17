# -*- coding: utf-8 -*

from nltk.tokenize import word_tokenize
import re

def ord(k):
	return int(k.replace('_',''))

# Obtendo abreviaturas e pronomes de tratamento contendo pontos e espacos
list_1 = open('lexicos/abreviaturas_com_pontos_e_espacos_ord.txt', 'r').readlines()
list_1 = [word.replace('\n','') for word in list_1]
# list_1 = [word.decode('utf-8') for word in list_1]
dict_abreviaturas_com_pontos_e_espacos_expressoes = dict()
dict_abreviaturas_com_pontos_e_espacos_numeros = dict()
dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram = dict()

id_ = 1
list_iter = []
for word in list_1:
	word = word
	dict_abreviaturas_com_pontos_e_espacos_expressoes[word] = str(str(id_) + '_')
	dict_abreviaturas_com_pontos_e_espacos_numeros[str(str(id_) + '_')] = word
	dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[str(str(id_) + '_')] = []
	list_iter.append(str(str(id_) + '_'))
	id_ += 1

# clíticos dos verbos conjugados em mesóclises no futuro do pretérito e do presente
list_vf = open('lexicos/verbos_irregulares_cliticizados.txt', 'r').readlines()
list_vf = [exp.replace('\n', '') for exp in list_vf]
# list_vf = [exp.decode('utf-8') for exp in list_vf]

# Tratando contrações de pron+artigo
list_abv = open('lexicos/contraidos_pronprep_prondet.txt', 'r').readlines()
list_abv = [word.replace('\n', '') for word in list_abv]
# list_abv = [word.decode('utf-8') for word in list_abv]


# Obtendo os pronomes
list_p = open('lexicos/pron_encontrados_cliticos.txt', 'r').readlines()
list_p = [pron.replace('\n', '') for pron in list_p]
# list_p = [pron.decode('utf-8') for pron in list_p]

# Obtendo os pronomes contraídos
list_pc = open('lexicos/pron_cliticos_contraidos.txt', 'r').readlines()
list_pc = [pron.replace('\n', '') for pron in list_pc]
# list_pc = [pron.decode('utf-8') for pron in list_pc]

dict_cliticos_contraidos_expressoes = dict()

for pron in list_pc:
	lpron = pron.split(',');
	dict_cliticos_contraidos_expressoes[lpron[0]] = lpron[1]


# name = ""
# name = str(input('Digite o nome do arquivo .txt de entrada (ex: input.txt): '))
# print("Arquivo de entrada dado -> ", name)
# frases = open(name, 'r').readlines()
frases = open("input.txt", 'r').readlines()
for i in range(0, len(frases)):
	frases[i] = frases[i].replace('\n', '')
	# frases[i] = frases[i].decode('utf-8')

	
# name = name.replace('.txt', '')
# arq = open(name+'_tokenizado.txt', 'w')
arq = open('input_tokenizado.txt', 'w')


for i in range(0, len(frases)):

	# Tratando abreviaturas e pronomes de tratamento contendo pontos e espacos (antes de tokenizar) ###############################

	for word in list_1:
		text = frases[i].lower()
		id_word = text.find(word)
		Flag = False
		while id_word != -1:
			if word in text and (id_word == 0):
				dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[dict_abreviaturas_com_pontos_e_espacos_expressoes[word]].append(frases[i][id_word:(id_word+len(word))])
				frases[i] = dict_abreviaturas_com_pontos_e_espacos_expressoes[word] + frases[i][(id_word+len(word)):len(frases[i])]
				text = frases[i].lower()
				Flag = True
			else:
				for pnt in [' ',',','!','?',';',':']:
					if word in text and (id_word != 0 and text[id_word-1] == pnt):
						dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[str(dict_abreviaturas_com_pontos_e_espacos_expressoes[word])].append(frases[i][id_word:(id_word+len(word))])
						frases[i] = frases[i][0:id_word] + dict_abreviaturas_com_pontos_e_espacos_expressoes[word] + frases[i][(id_word+len(word)):len(frases[i])]
						text = frases[i].lower()
						# print(text)
						Flag = True
			id_word = text.find(word)
			if Flag == False:
				id_word = -1

	# Tokenizando o texto usando a função word_tokenize ###########################################################################

	palavras_frase = word_tokenize(frases[i], language='portuguese')

	# Procurando por siglas #######################################################################################################

	dict_siglas = dict()
	id_ = 1

	for i in range(len(palavras_frase)):
		if len(re.findall('[A-Z\.]', palavras_frase[i])) == len(palavras_frase[i]) and len(palavras_frase[i]) > 1:
			dict_siglas['_'+str(id_)+'_'] = palavras_frase[i]
			palavras_frase[i] = '_'+str(id_)+'_'
			id_+=1

	# Verificando quais palavras da sentença iniciam com letra máiúscula e quais não

	palavras_frase_maiusculas = ['L'] * len(palavras_frase)
	
	for i in range(len(palavras_frase)):
		# print(palavras_frase[i])
		# print(palavras_frase[i][0].isupper())
		if palavras_frase[i][0].isupper() == True:
			palavras_frase_maiusculas[i] = 'U'
		else:
			palavras_frase_maiusculas[i] = 'L'


	# Criando outra versão da sentença em lowercase apa realizar o processamento ##################################################

	palavras_tokenize = [palavras_frase[i].lower() for i in range(len(palavras_frase))]

	# Tratando os clíticos dos verbos conjugados em mesóclises no futuro do pretérito e do presente (antes de tokenizar) ##########
	for i in range(len(palavras_tokenize)):
		for exp in list_vf:
			exp = exp.split(',')
			if palavras_tokenize[i] == exp[0]:
				palavras_tokenize[i] = exp[1]

	# Tratando contracoes de pronomes+artigos #####################################################################################

	for id_ in range(0,len(palavras_tokenize)):
		for word in list_abv:
			word = word.split(',')
			if palavras_tokenize[id_] == word[0]:
				palavras_tokenize[id_] = word[1]
		
	# Tratando clíticos (depois de tokenizar) #####################################################################################

	for id_ in range(0,len(palavras_tokenize)):
		# Caso seja enclise
		if palavras_tokenize[id_].count('-') == 1:
			posHifen = palavras_tokenize[id_].find('-')
			pron = palavras_tokenize[id_][posHifen+1:len(palavras_tokenize[id_])]
			if pron in list_p:
				if pron in list_pc:
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-'+pron, ' '+dict_cliticos_contraidos_expressoes[pron])
				else:
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-',' ')

		# Caso seja mesóclise
		if palavras_tokenize[id_].count('-') == 2:
			# Encontrando os hifens e o possível pronome
			primHifen = palavras_tokenize[id_].find('-')
			segHifen = palavras_tokenize[id_].find('-', primHifen+1,len(palavras_tokenize[id_]))
			pron = palavras_tokenize[id_][primHifen+1:segHifen]

			# Tratando se for mesóclise
			if pron in list_p:
				if palavras_tokenize[id_][primHifen-1] != 'r':
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-'+pron+'-', 'r')
				else:
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-'+pron+'-', '')

				if pron in dict_cliticos_contraidos_expressoes.keys():
					palavras_tokenize[id_] += ' '+dict_cliticos_contraidos_expressoes[pron]
				else:
					palavras_tokenize[id_] += ' '+pron


	# Recolocando os pronomes de tratamento (depois de tokenizar e tratar os casos) #################################################

	for key_ in dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram.keys():
		for i in range(len(palavras_tokenize)):
			if palavras_tokenize[i] == key_:
				palavras_tokenize[i] = dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[key_][0]
				dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[key_].pop(0)

	for i in range(0, len(palavras_frase_maiusculas)):
		if palavras_frase_maiusculas[i] == 'U':
			palavras_tokenize[i] = palavras_tokenize[i][0].upper() + palavras_tokenize[i][1:len(palavras_tokenize[i])]

	text = ' '.join(palavras_tokenize)

	for key_ in dict_siglas.keys():
		if key_ in text:
			text = text.replace(key_, dict_siglas[key_])

	# text = text.encode('utf-8')
	arq.write(text+'\n')

arq.close()
