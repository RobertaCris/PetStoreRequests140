# 1 - bibliotecas
import json              # leitor e escritor de arquivos json
import pytest            # engine (motor) / framework de teste de unidade
import requests          # framework de teste de API

# 2 - classe (opcional no Python, em muitos casos)

# 2.1 - atributos ou variaveis
# consulta e resultado esperado
pet_id = 314277501        # código do animal = 3 primeiros digitos CPF + 4 ultimos numero telefone + 01
pet_name =  "Baruk"       # nome do animal
pet_category_id = 1       # código da categoria do aninal
pet_category_name = "dog" # título da categoria
pet_tag_id = 1            # codigo do rótulo
pet_tag_name = "vacinado" # título do rotulo

# informações em comum
url = 'https://petstore.swagger.io/v2/pet'      # endereço
headers = { 'Content-Type': 'application/json' }  # formato dos dados trafegados

# 2.2 - funções / métodos

def test_post_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet1.json')          # abre o arquivo json
    data=json.loads(pet.read())                    # ler o conteúdo e carrega como json em uma variável data - loads para cerregar
    # dados de saída / resultado esperado estão nos atibutos acima das funções

    # executa    <--
    response = requests.post(        # executo o método post com as informações a seguir
        url=url,                     # endereço
        headers=headers,             # cabeçalho / informaçoes extras da mensagem
        data=json.dumps(data),       # a mensagem = json / dumps para carregar / extrai os dados 
        timeout=5                    # tempo limite da transmissão, em segundos
    )

    # valida
    response_body = response.json()  # criar uma variavel e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    # Configura
    # Dados de Entrada Saída / Resultado Esperado estão na seção de atributos antes das funções

    # Executa
    response = requests.get(
        url=f'{url}/{pet_id}',       # chama o endereço do get/consulta passando o código do animal
        headers=headers,             # cabeçalho / informaçoes extras da mensagem
        # não tem corpo da mensagem / body
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == "available"

def test_put_pet():
    # Configura
    # Dados de Entrada vem de um arquivo json
    pet=open('./fixtures/json/pet2.json')          # abre o arquivo json
    data=json.loads(pet.read())                    # ler o conteúdo e carrega como json em uma variável data - loads para cerregar
    # dados de saída / resultado esperado vem dos atributos descritos antes das funções

    # Executa
    response = requests.put(        # executo o método post com as informações a seguir
        url=url,                     # endereço
        headers=headers,             # cabeçalho / informaçoes extras da mensagem
        data=json.dumps(data),       # a mensagem = json / dumps para carregar / extrai os dados 
        timeout=5                    # tempo limite da transmissão, em segundos
    )

    # Valida
    response_body = response.json()  # criar uma variavel e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['status'] == 'sold'
    

def test_delete_pet():
    # Configura
    # Dados de Entrada e Saída virão  dos atributos

    # Executa
    response = requests.delete(
        url=f'{url}/{pet_id}',       # chama o endereço do get/consulta passando o código do animal
        headers=headers,             # cabeçalho / informaçoes extras da mensagem
    )

    # Valida
    response_body = response.json()
    assert response.status_code == 200 # da comunicação que foi e voltou / se o pedido chegou ou não
    assert response_body['code'] == 200 # se o pedido veio certo
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)