#Um programa Python para renovar os livros da Biblioteca
import requests

# 1 Passo: fazer login
url = 'https://biblioteca.ifsc.edu.br/asp/login.asp?iIdioma=0&iBanner=0&content=mensagens'

login = False

while not login:
    matricula = input('Digite sua matricula: ')
    senha = input('Digite sua senha: ')

    payload = {
        "codigo": matricula,
        "senha": senha,
        "sub_login": "sim"
    }

    session = requests.Session()


    response = session.post(url, data=payload)

    # Imprimindo o status da resposta e o conteúdo
    print(f"Status Code: {response.status_code}")
    if "rio ou senha inv" in response.text:
        print("Algo deu errado, tente novamente!!\n")
    else:
        login = True
with open('arquivo.html', 'w') as file:
    file.write(response.text)


# 2 Passo: Salvar os cookies
cookies = response.cookies
cookie = cookies.get_dict()['ASPSESSIONIDQSSDACRA']


headers = {
    "Cookie": f"ASPSESSIONIDQSSDACRA={cookie}; TESTE=TESTECOOKIES; fileDownload=true"
}

# 3 Passo: encontrar o código dos livros
print('\n\nObtendo o(s) código(s) do(s) livro(s)...')
url = 'https://biblioteca.ifsc.edu.br/index.asp?modo_busca=rapida&content=circulacoes&iFiltroBib=0&iBanner=0&iEscondeMenu=0&iSomenteLegislacao=0&iIdioma=0'

response = requests.get(url, headers=headers)
texto = response.text
print(f"Status Code: {response.status_code}")

codigos = []

fragmento = "input type='checkbox' name='ck"

# Encontrar a posição do fragmento de texto
posicao = texto.find(fragmento)
while posicao != -1 and len(codigos) < 10:
    # Se o fragmento for encontrado, encontrar as palavras seguintes
    inicio_value = texto[posicao:].find("value='")
    fim_value = texto[posicao+inicio_value:].find("'>")
    codigo_value = texto[posicao+inicio_value+7:posicao+inicio_value+fim_value]
    codigos.append(codigo_value)
    posicao += texto[posicao+inicio_value+fim_value:].find(fragmento)
print(f"O(s) código(s): {codigos}")

# 4 Passo: renovar os livros
print("\n\nRequisitando renovação de livros...")

url = 'https://biblioteca.ifsc.edu.br/index.asp?content=circulacoes&acao=renovacao&num_circulacao='
for i,codigo in enumerate(codigos):
    if i < (len(codigos) - 1):  
        url = url+codigo+','
    else:
        url = url+codigo+'&iBanner=0&iIdioma=0&iFiltroBib=0'


response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")

if "mais de uma vez no mesmo dia" in response.text:
    print("1 ou mais itens já haviam sido renovados")
else:
    print("Livros renovados!")
