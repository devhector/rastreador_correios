# Autor: Hector Fernandes

import requests as r
import sys as s
from datetime import datetime

emojis = {
	'trânsito': '🚚',
	'entregue': '✅',
	'Correios': '🛬',
	'aduaneira': '🚨',
	'exportação': '🛫',
	'erro': '❌',
	'postado': '📦',
	'saiu': '🚀',
	'confirmado' : '💸',
	'pagamento': '💰',
	'indo' : '➡️'
}

def get_status(codigo):
	response = r.get('https://proxyapp.correios.com.br/v1/sro-rastro/' + codigo)
	if response.status_code == 200:
		obj = response.json()['objetos'][0]
		if 'mensagem' in obj:
			if "SRO-019: Objeto inválido" in obj['mensagem']:
				return None
		return obj
	else:
		return None
		
def create_status_string(item):
	unidade = item['unidade']
	if 'nome' in unidade:
		local = unidade['nome']
	else:
		local = unidade['endereco']['cidade'] + '-' + unidade['endereco']['uf']
	if 'unidadeDestino' in item:
		unidadeDestino = item['unidadeDestino']
		if 'nome' in unidadeDestino:
			dest = unidadeDestino['nome']
		else:
			dest = unidadeDestino['endereco']['cidade'] + '-' + unidadeDestino['endereco']['uf']
		return (f'{local} {emojis["indo"]}  {dest}')
	else:
		return (local)

def create_event_string(item):
	date = item['dtHrCriado']
	hour = date[11:16]
	date = date[8:10] + '/' + date[5:7] + '/' + date[0:4]
	desc = item['descricao']
	string = date + ' - ' + hour + ' - ' + desc
	for emoji in emojis:
		if emoji in desc:
			string = emojis[emoji] + ' ' + string
	status_string = create_status_string(item)
	string = string + " | " + status_string
	return string

def print_status(status):
	events = status['eventos']
	for item in events:
		print(create_event_string(item))


def convert_date(date):
	date = date[8:10] + '/' + date[5:7] + '/' + date[0:4] + ' ' + date[11:16]
	date = datetime.strptime(date, '%d/%m/%Y %H:%M')
	return date

def print_all(status):
	last_date = convert_date(status['eventos'][0]['dtHrCriado'])
	status_date = datetime.now() - last_date
	status_date = status_date.days

	if status_date < 2 and status_date != 0:
		status_date = f'Última atualização há {status_date} dia'
		print(f'\n{emojis["postado"]} Cód: {status["codObjeto"]} - {status_date}')
	else:
		status_date = f'Última atualização há {status_date} dias'
		print(f'\n{emojis["postado"]} Cód: {status["codObjeto"]} - {status_date}')

	print_status(status)

def main():

	if len(s.argv) < 2:
		print('Uso: rastreador "<codigo>" ...')
		return

	for i in range(1, len(s.argv)):
		code = s.argv[i]
		status = get_status(code)

		if status is None:
			print(f'\n{emojis["erro"]} Código {code} inválido')
		else:
			print_all(status)

main()
