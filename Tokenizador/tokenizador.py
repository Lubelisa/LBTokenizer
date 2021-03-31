# -*- coding: utf-8 -*

from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
import unidecode
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

for word in list_1:
	word = word
	dict_abreviaturas_com_pontos_e_espacos_expressoes[word] = str('__' + str(id_) + '__')
	dict_abreviaturas_com_pontos_e_espacos_numeros[str('__' + str(id_) + '__')] = word
	dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[str('__' + str(id_) + '__')] = []
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
list_p = ['me', 'te', 'se', 'lhe', 'o', 'a', 'nos', 'vos', 'lhes', 'os', 'as']
list_t = ['ei', 'ás', 'á', 'emos', 'eis', 'ão', 'ia', 'ias', 'ia', 'íamos', 'íeis', 'iam']

# Obtendo os pronomes contraídos
list_pc = open('lexicos/pron_cliticos_contraidos.txt', 'r').readlines()
list_pc = [pron.replace('\n', '') for pron in list_pc]
# list_pc = [pron.decode('utf-8') for pron in list_pc]

dict_cliticos_contraidos_expressoes = dict()

for pron in list_pc:
	lpron = pron.split(',');
	dict_cliticos_contraidos_expressoes[lpron[0]] = lpron[1]


# Recebendo e abrindo o arquivo a ser tokenizado
name = ""
name = str(input('Digite o nome do arquivo .txt de entrada (ex: input.txt): '))
print("Arquivo de entrada dado -> ", name)
frases = open(name, 'r', encoding='utf-8').readlines()

for i in range(0, len(frases)):
	frases[i] = frases[i].replace('\n', '')

# Abrindo o novo arquivo que vai receber o texto tokenizado	
name = name.replace('.txt', '')
arq = open(name+'_tokenizado.txt', 'w')

for i in range(0, len(frases)):
	
	# Tratando abreviaturas e pronomes de tratamento contendo pontos e espacos (antes de tokenizar) ###############################

	list_iter = []

	for word in list_1:
		text = frases[i].lower()
		id_word = text.find(word)
		Flag = False
		while id_word != -1:
			Flag = False
			if word in text and (id_word == 0):
				dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[dict_abreviaturas_com_pontos_e_espacos_expressoes[word]].append(frases[i][id_word:(id_word+len(word))])
				list_iter.append(dict_abreviaturas_com_pontos_e_espacos_expressoes[word])
				frases[i] = dict_abreviaturas_com_pontos_e_espacos_expressoes[word] + frases[i][(id_word+len(word)):len(frases[i])]
				text = frases[i].lower()
				Flag = True
			else:
				for pnt in [' ',',','!','?',';',':']:
					if word in text and (id_word != 0 and text[id_word-1] == pnt):
						# print('Entrou!!!')
						dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[str(dict_abreviaturas_com_pontos_e_espacos_expressoes[word])].append(frases[i][id_word:(id_word+len(word))])
						list_iter.append(dict_abreviaturas_com_pontos_e_espacos_expressoes[word])
						frases[i] = frases[i][0:id_word] + dict_abreviaturas_com_pontos_e_espacos_expressoes[word] + frases[i][(id_word+len(word)):len(frases[i])]
						text = frases[i].lower()
						# print(text)
						Flag = True
			id_word = text.find(word)
			if Flag == False:
				id_word = -1

	# Separando aspas simples ########################################################################################################

	frases[i] = frases[i].replace('\'', ' \' ')
	frases[i] = frases[i].replace('  ', ' ')

	# Procurando por acronimos #######################################################################################################

	dict_siglas = dict()
	list_siglas = []
	id_ = 1

	list_siglas = re.findall('(?:(?<=\.|\s)[A-Z]\.)+', frases[i])

	for j in range(len(list_siglas)):
		frases[i] = frases[i].replace(list_siglas[j], '_+'+str(id_)+'+_')
		dict_siglas['_+'+str(id_)+'+_'] = list_siglas[j]
		id_+=1

	# Tokenizando o texto usando a função word_tokenize ###########################################################################

	palavras_frase = word_tokenize(frases[i], language='portuguese')
	for j in range(len(palavras_frase)):
		palavras_frase[j] = palavras_frase[j].replace('\'\'', '"')
		palavras_frase[j] = palavras_frase[j].replace('``', '"')

	# Procurando por siglas #######################################################################################################

	for j in range(len(palavras_frase)):
		poss_sigla = re.findall('[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0123456789][A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0123456789]+', palavras_frase[j])
		# print(len(poss_sigla) > 0)
		# print(poss_sigla[0] == len(palavras_frase[j]))
		# print(poss_sigla)
		if len(poss_sigla) > 0 and (poss_sigla[0] == palavras_frase[j]):
			# print(id_)
			palavras_frase[j] = '_+'+str(id_)+'+_'
			dict_siglas['_+'+str(id_)+'+_'] = poss_sigla[0]
			id_+=1

	# Verificando quais palavras da sentença iniciam com letra máiúscula e quais não

	palavras_frase_maiusculas = ['L'] * len(palavras_frase)
	
	for j in range(len(palavras_frase)):
		# print(palavras_frase[i])
		# print(palavras_frase[i][0].isupper())
		if palavras_frase[j][0].isupper() == True:
			palavras_frase_maiusculas[j] = 'U'
		else:
			palavras_frase_maiusculas[j] = 'L'


	# Criando outra versão da sentença em lowercase apa realizar o processamento ##################################################

	palavras_tokenize = [palavras_frase[j].lower() for j in range(len(palavras_frase))]

	# Tratando os clíticos dos verbos conjugados em mesóclises no futuro do pretérito e do presente (antes de tokenizar) ##########
	for j in range(len(palavras_tokenize)):
		for exp in list_vf:
			exp = exp.split(',')
			if palavras_tokenize[j] == exp[0]:
				palavras_tokenize[j] = exp[1]

	# Tratando contracoes de pronomes+artigos #####################################################################################

	for id_ in range(0,len(palavras_tokenize)):
		for word in list_abv:
			word = word.split(',')
			if palavras_tokenize[id_] == word[0]:
				# print('oi')
				# print(word[1])
				palavras_tokenize[id_] = word[1]
				# print(palavras_tokenize[id_])
		
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

			else:
				palavras_tokenize[id_] = palavras_frase[id_]

		# Caso seja mesóclise
		elif palavras_tokenize[id_].count('-') == 2:
			# Encontrando os hifens e o possível pronome
			primHifen = palavras_tokenize[id_].find('-')
			segHifen = palavras_tokenize[id_].find('-', primHifen+1,len(palavras_tokenize[id_]))
			pron = palavras_tokenize[id_][primHifen+1:segHifen]
			term = palavras_tokenize[id_][segHifen+1:len(palavras_tokenize[id_])]

			# Tratando se for mesóclise
			if pron in list_p and term in list_t:
				if palavras_tokenize[id_][primHifen-1] != 'r':
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-'+pron+'-', 'r')
				else:
					palavras_tokenize[id_] = palavras_tokenize[id_].replace('-'+pron+'-', '')

				if pron in dict_cliticos_contraidos_expressoes.keys():
					palavras_tokenize[id_] += ' '+dict_cliticos_contraidos_expressoes[pron]
				else:
					palavras_tokenize[id_] += ' '+pron


	# Recolocando os pronomes de tratamento (depois de tokenizar e tratar os casos) #################################################

	for key_ in list_iter:
		for id_ in range(len(palavras_tokenize)):
			id_key = palavras_tokenize[id_].find(key_)
			while id_key != -1:
				palavras_tokenize[id_] = palavras_tokenize[id_][0:id_key]+dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[key_][0]+palavras_tokenize[id_][id_key+len(key_):len(palavras_tokenize[id_])]
				dict_abreviaturas_com_pontos_e_espacos_numeros_expressoescomoeram[key_].pop(0)
				id_key = palavras_tokenize[id_].find(key_)

	for j in range(0, len(palavras_frase_maiusculas)):
		if palavras_frase_maiusculas[j] == 'U':
			palavras_tokenize[j] = palavras_tokenize[j][0].upper() + palavras_tokenize[j][1:len(palavras_tokenize[j])]

	text = ' '.join(palavras_tokenize)

	for key_ in dict_siglas.keys():
		if key_ in text:
			text = text.replace(key_, dict_siglas[key_])

	text = text.replace('R $', 'R$')

	# text = text.encode('utf-8')
	arq.write(text+'\n')

arq.close()
