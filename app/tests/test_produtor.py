import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_get_produtor_encontrado(client):
    with patch('resources.produtor.produtorModel.validaCpfCnpj', return_value=True), \
         patch('resources.produtor.produtorModel.findProdutor') as mock_find:

        mock_produtor = MagicMock()
        mock_produtor.json.return_value = {
            "id_Produtor": 1,
            "cpf_cnpj14": "12345678901",
            "nome_Produtor": "João",
            "tipo_Produtor": "PF",
            "criado_em": "2023-01-01",
            "atualizado_em": "2023-01-01"
        }
        mock_find.return_value = mock_produtor

        response = client.get('/produtores', json={
            "cpf_cnpj14": "12345678901",
            "tipo_Produtor": "PF"
        })
        assert response.status_code == 200
        assert response.json["message"]["nome_Produtor"] == "João"

def test_get_produtor_nao_encontrado(client):
    with patch('resources.produtor.produtorModel.validaCpfCnpj', return_value=True), \
         patch('resources.produtor.produtorModel.findProdutor', return_value=None):

        response = client.get('/produtores', json={
            "cpf_cnpj14": "00000000000",
            "tipo_Produtor": "PF"
        })
        assert response.status_code == 400
        assert response.json["message"] == "Produtores Não Encontrado"

def test_post_produtor_sucesso(client):
    with patch('resources.produtor.produtorModel.validaCpfCnpj', return_value=True), \
         patch('resources.produtor.produtorModel.findProdutor', return_value=None), \
         patch('resources.produtor.produtorModel.saveProdutor'), \
         patch('resources.produtor.produtorModel.__init__', return_value=None), \
         patch('resources.produtor.produtorModel.json', return_value={"nome_Produtor": "Novo Produtor"}):

        response = client.post('/produtores', json={
            "cpf_cnpj14": "12345678901",
            "nome_Produtor": "Novo Produtor",
            "tipo_Produtor": "PF"
        })
        assert response.status_code == 201
        assert response.json["message"]["nome_Produtor"] == "Novo Produtor"

def test_put_produtor_sucesso(client):
    mock_produtor = MagicMock()
    mock_produtor.json.return_value = {"nome_Produtor": "Atualizado"}

    with patch('resources.produtor.produtorModel.validaCpfCnpj', return_value=True), \
         patch('resources.produtor.produtorModel.findProdutor', return_value=mock_produtor), \
         patch.object(mock_produtor, 'updateProdutor'):

        response = client.put('/produtores', json={
            "cpf_cnpj14": "12345678901",
            "nome_Produtor": "Atualizado",
            "tipo_Produtor": "PF"
        })
        assert response.status_code == 201
        assert response.json["message"]["nome_Produtor"] == "Atualizado"

def test_delete_produtor_sucesso(client):
    mock_produtor = MagicMock()
    mock_produtor.nome_Produtor = "Para Deletar"

    with patch('resources.produtor.produtorModel.validaCpfCnpj', return_value=True), \
         patch('resources.produtor.produtorModel.findProdutor', return_value=mock_produtor), \
         patch.object(mock_produtor, 'deleteProdutor'):

        response = client.delete('/produtores', json={
            "cpf_cnpj14": "12345678901",
            "tipo_Produtor": "PF"
        })
        assert response.status_code == 204
