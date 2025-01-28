# 1 - Bibliotecas
import pytest
import requests
import json

from utils.utils import ler_csv

# (Opcional) 2 - Classe

# 2.1 Atributos/Propriedades
pet_id = 173218101
pet_name = "Snoopy"
pet_category_id = 1
pet_category_name = "dog"
pet_tag_id = 9
pet_tag_name = "vaccined"
pet_status1 = "available"
pet_status2 = "sold"

url = "https://petstore.swagger.io/v2/pet"
headers = { "Content-Type": "application/json" }
# headers = { "Content-Type: text/xml" } # se fosse SOAP

# 2.2 Funções e Metódos de Apoio

def validar_pet(response, status):

    response_body = response.json() # formata a resposta como json

    assert response.status_code == 200
    assert response_body["id"] == pet_id
    assert response_body["name"] == pet_name
    assert response_body["category"]["id"] == pet_category_id
    assert response_body["category"]["name"] == pet_category_name
    assert response_body["tags"][0]["id"] == pet_tag_id
    assert response_body["tags"][0]["name"] == pet_tag_name
    assert response_body["status"] == status


# 2.3 Funções de Teste
@pytest.mark.order(1)
def test_post_pet():
    # Arrange / Configura
    pet=open("./fixtures/json/pet1.json") # abre o arquivo
    data=json.loads(pet.read())       # carrega na memória como json

    # Act / Execute
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data), # json body da mensagem a ser enviada
        timeout=5
    )
    
    validar_pet(response, pet_status1)
    
@pytest.mark.order(2)
def test_get_pet():
    # Arrange / Configura
    # Os dados de entrada e saída (resultados esperados)
    # estão no atributos deste arquivo

    # Act / Executa
    response = requests.get(
        # url=url + "/" + pet_id, # clássica concatenação
        url=f'{url}/{pet_id}',    # forma mais atual - Python >= 3.6
        headers=headers,
        timeout=5
    )

    # Assert / Valida (Afirmação)
    validar_pet(response, pet_status1)

@pytest.mark.order(3)
def test_put_pet():
    # Arrange / Configura
    pet = open("./fixtures/json/pet2.json")
    data = json.loads(pet.read())

    # Act / Execute
    response = requests.put(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    # Assert / Valida (Afirmação)
    validar_pet(response, pet_status2)

@pytest.mark.order(4)
def test_delete_pet():
    # Arrange / Configure
    # Dados de entrada e saída vem dos atributos deste arquivo

    # Act / Executa
    response = requests.delete(
        url=f'{url}/{pet_id}',
        headers=headers,
        timeout=5
    )

    # Arrange / Valida
    response_body = response.json()

    assert response.status_code == 200      # valida a comunicação
    assert response_body["code"] == 200     # valida o funcionamento
    assert response_body["type"] == "unknown"
    assert response_body["message"] == str(pet_id)

# Post Parametrizado - Leitura da Massa
@pytest.mark.order(5)
@pytest.mark.parametrize("id,category_id,category_name,name,tags,status",
        ler_csv("./fixtures/csv/pets.csv"))
def test_post_pet_dinamico(id,category_id,category_name,name,tags,status):
    pet = {}
    pet["id"] = int(id)
    pet["category"] = {}
    pet["category"]["id"] = int(category_id)
    pet["category"]["name"] = category_name
    pet["name"] = name
    pet["photoUrls"] = []
    pet["tags"] = []

    tags = tags.split(";")
    for tag in tags:
        tag = tag.split("-")
        tag_formatada = {}
        tag_formatada["id"] = int(tag[0])
        tag_formatada["name"] = tag[1]
        pet["tags"].append(tag_formatada)

    pet["status"] = status

    # Act / Execute
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(obj=pet, indent=4), # json body da mensagem a ser enviada
        timeout=5
    )

    # Assert / Valida (Afirmação)
    response_body = response.json() # formata a resposta como json
    # validar_pet(response)
    assert response.status_code == 200
    assert response_body["id"] == int(id)
    assert response_body["name"] == name
    assert response_body["category"]["id"] == int(category_id)
    assert response_body["category"]["name"] == category_name
    assert response_body["status"] == status