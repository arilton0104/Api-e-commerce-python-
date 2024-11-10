# Importa o Flask, que é um micro-framework para criar APIs em Python
from flask import Flask, request, jsonify

# Importa o Redis para manipular o banco de dados Redis e o RedisError para lidar com erros de conexão
from redis import Redis, RedisError

# Importa a biblioteca json para manipulação de dados JSON (converter objetos Python para JSON e vice-versa)
import json

# Cria a aplicação Flask
app = Flask(__name__)

# Cria uma conexão com o Redis que está rodando no host local na porta padrão (6379) e banco de dados 0
redis_client = Redis(host='localhost', port=6379, db=0)

# Define uma rota para adicionar um item ao carrinho
@app.route('/api/cart/<user_id>/add', methods=['POST'])
def adicionar_ao_carrinho(user_id):
    try:
        # Obtém os dados do produto enviados na requisição, no formato JSON
        produto = request.json

        # Validação básica: verifica se os dados obrigatórios estão presentes
        if 'id' not in produto or 'nome' not in produto or 'preco' not in produto:
            # Se algum campo está ausente, retorna uma resposta de erro com código 400 (Bad Request)
            return jsonify({"erro": "Dados do produto inválidos"}), 400

        # Converte o user_id para string, garantindo que seja compatível com o Redis
        user_id = str(user_id)

        # Tenta buscar o carrinho do usuário no Redis; se não existe, cria um carrinho vazio (usando `or "{}"`)
        carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")

        # Converte o ID do produto para string para padronizar o formato de armazenamento
        produto_id = str(produto['id'])

        # Verifica se o produto já existe no carrinho
        if produto_id in carrinho:
            # Se já existe, incrementa a quantidade do produto no carrinho (ou adiciona 1 caso quantidade não seja especificada)
            carrinho[produto_id]['quantidade'] += produto.get('quantidade', 1)
        else:
            # Se não existe, adiciona o produto com os dados e define a quantidade como 1 (ou a quantidade especificada)
            carrinho[produto_id] = {
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': produto.get('quantidade', 1)
            }

        # Salva o carrinho atualizado no Redis, definindo um tempo de expiração de 3600 segundos (1 hora)
        redis_client.setex(f"cart:{user_id}", 3600, json.dumps(carrinho))

        # Retorna uma resposta com o status de sucesso e o carrinho atualizado
        return jsonify({"status": "sucesso", "carrinho": carrinho})
    
    # Se ocorrer um erro de conexão com o Redis, captura o erro e retorna uma mensagem de erro com código 500 (Internal Server Error)
    except RedisError:
        return jsonify({"erro": "Erro ao conectar com o Redis"}), 500

# Define uma rota para remover um item específico do carrinho
@app.route('/api/cart/<user_id>/remove/<product_id>', methods=['DELETE'])
def remover_do_carrinho(user_id, product_id):
    try:
        # Converte o user_id para string para manter o padrão de armazenamento no Redis
        user_id = str(user_id)

        # Busca o carrinho do usuário no Redis; se não existe, cria um carrinho vazio
        carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")

        # Verifica se o produto a ser removido está no carrinho
        if str(product_id) in carrinho:
            # Remove o produto do dicionário carrinho
            del carrinho[str(product_id)]
            # Salva o carrinho atualizado no Redis com expiração de 3600 segundos (1 hora)
            redis_client.setex(f"cart:{user_id}", 3600, json.dumps(carrinho))

        # Retorna uma resposta com o status de sucesso e o carrinho atualizado (mesmo se o produto não estava no carrinho)
        return jsonify({"status": "sucesso", "carrinho": carrinho})
    
    # Trata erros de conexão com o Redis e retorna uma mensagem de erro com código 500
    except RedisError:
        return jsonify({"erro": "Erro ao conectar com o Redis"}), 500

# Define uma rota para obter todos os itens do carrinho de um usuário específico
@app.route('/api/cart/<user_id>', methods=['GET'])
def obter_carrinho(user_id):
    try:
        # Converte o user_id para string, garantindo compatibilidade com o Redis
        user_id = str(user_id)

        # Busca o carrinho do usuário no Redis; se não existe, retorna um carrinho vazio
        carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")

        # Retorna o conteúdo do carrinho como resposta em JSON
        return jsonify({"carrinho": carrinho})
    
    # Trata erros de conexão com o Redis e retorna uma mensagem de erro com código 500
    except RedisError:
        return jsonify({"erro": "Erro ao conectar com o Redis"}), 500

# Executa a aplicação Flask apenas se este arquivo for executado diretamente
if __name__ == '__main__':
    # Coloca o servidor Flask para rodar em modo de debug (útil para desenvolvimento)
    app.run(debug=True)


"""
Esse código é um microserviço em Python usando o framework Flask para criar uma API de carrinho de compras. Abaixo, 
explicarei o funcionamento de cada parte e o que poderia ser feito para torná-lo mais robusto.

### Estrutura e Funcionamento do Microserviço

1. **Dependências Importadas**
   ```python
   from flask import Flask, request, jsonify
   from redis import Redis
   import json
   ```

   - `Flask` é o framework usado para criar a API.
   - `Redis` é um banco de dados de chave-valor em memória usado para armazenar o carrinho de compras de cada usuário.
   - `json` é utilizado para converter dados entre objetos Python e strings JSON, necessárias para 
    manipulação de dados no Redis.

2. **Configuração Inicial**
   ```python
   app = Flask(__name__)
   redis_client = Redis(host='localhost', port=6379, db=0)
   ```

   - `app` é a instância da aplicação Flask.
   - `redis_client` é a conexão com o Redis, configurado para se conectar ao Redis rodando na máquina local, 
   na porta 6379, usando o banco de dados 0.

3. **Função `adicionar_ao_carrinho`**
   ```python
   @app.route('/api/cart/<user_id>/add', methods=['POST'])
   def adicionar_ao_carrinho():
       user_id = str(user_id)
       produto = request.json
   ```
   
   - Esta rota permite adicionar um produto ao carrinho de um usuário.
   - `user_id` representa o identificador único do usuário, e `produto` é um JSON enviado na requisição com 
   informações do produto.
   
   **Passo a Passo do que a Função Faz:**
   - **Recuperar ou Criar o Carrinho**: Usa `redis_client.get(f"cart:{user_id}")` para buscar o carrinho do usuário. 
   Caso não exista, cria um novo dicionário `{}`.
   - **Adicionar ou Atualizar Produto**: 
     - Converte o `produto['id']` em string, checando se já está no carrinho.
     - Se o produto já existe, incrementa a quantidade. Caso contrário, adiciona o produto ao dicionário com quantidade 1.
   - **Salvar Carrinho**: O carrinho atualizado é salvo no Redis.

   **Exemplo de JSON do Produto para Envio:**
   ```json
   {
       "id": "123",
       "nome": "Camiseta",
       "preco": 29.90
   }
   ```

4. **Função `remover_do_carrinho`**
   ```python
   @app.route('/api/cart/<user_id>/remove/<product_id>', methods=['DELETE'])
   def remover_do_carrinho(user_id, product_id):
       user_id = str(user_id)
       carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
   ```

   - Esta rota permite remover um produto específico do carrinho de um usuário.
   - `user_id` identifica o usuário, e `product_id` é o identificador do produto a ser removido.

   **Passo a Passo:**
   - **Verificar e Remover Produto**: 
     - Se `product_id` está no carrinho, remove o item.
   - **Salvar Carrinho**: O carrinho atualizado é salvo no Redis novamente.

5. **Função `obter_carrinho`**
   ```python
   @app.route('/api/cart/<user_id>', methods=['GET'])
   def obter_carrinho(user_id):
       carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
       return jsonify({"carrinho": carrinho})
   ```

   - Esta rota permite visualizar todos os itens no carrinho de um usuário específico.
   - `user_id` é o identificador do usuário cujo carrinho será retornado.

   **Passo a Passo:**
   - Busca o carrinho no Redis e retorna como JSON.

---

### O Que Está Faltando para Tornar o Microserviço Mais Robusto

1. **Validação de Entrada**
   - Validar os dados antes de processá-los, como verificar se o JSON do produto tem `id`, `nome` e `preco`, e se `preco` 
   é numérico.
   - Exemplo:
     ```python
     if 'id' not in produto or 'nome' not in produto or 'preco' not in produto:
         return jsonify({"erro": "Dados do produto inválidos"}), 400
     ```

2. **Controle de Quantidade de Produto no Carrinho**
   - Permitir ao cliente definir a quantidade de um produto em vez de apenas incrementar a quantidade. 
   Isso tornaria o microserviço mais flexível.

3. **Persistência com Expiração de Carrinho**
   - Configurar o Redis para expirar os dados do carrinho automaticamente, caso o usuário fique inativo por muito tempo:
     ```python
     redis_client.setex(f"cart:{user_id}", 3600, json.dumps(carrinho))  # Expira em 1 hora
     ```

4. **Tratamento de Erros de Conexão e Resiliência**
   - Adicionar tratamento de exceções para falhas na conexão com o Redis:
     ```python
     try:
         carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")
     except RedisError as e:
         return jsonify({"erro": "Erro ao conectar com o Redis"}), 500
     ```

5. **Autenticação e Autorização**
   - Implementar uma forma de autenticação para garantir que apenas usuários 
   autorizados possam acessar seus próprios carrinhos.

6. **Testes Unitários e de Integração**
   - Adicionar testes unitários e de integração para garantir que cada endpoint 
   funcione conforme esperado.

7. **Documentação**
   - Documentar o código e criar um arquivo README que explica como configurar e executar o microserviço.

---

### Exemplo Completo com Melhorias

Abaixo, incluo as melhorias no código original:

```python
from flask import Flask, request, jsonify
from redis import Redis, RedisError
import json

app = Flask(__name__)
redis_client = Redis(host='localhost', port=6379, db=0)

@app.route('/api/cart/<user_id>/add', methods=['POST'])
def adicionar_ao_carrinho(user_id):
    try:
        produto = request.json
        if 'id' not in produto or 'nome' not in produto or 'preco' not in produto:
            return jsonify({"erro": "Dados do produto inválidos"}), 400

        user_id = str(user_id)
        carrinho = json.loads(redis_client.get(f"cart:{user_id}") or "{}")

        produto_id = str(produto['id'])
        if produto_id in carrinho:
            carrinho[produto_id]['quantidade'] += produto.get('quantidade', 1)
        else:
            carrinho[produto_id] = {
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': produto.get('quantidade', 1)
            }

        redis_client.setex(f"cart:{user_id}", 3600, json.dumps(carrinho))
        return jsonify({"status": "sucesso", "carrinho": carrinho})
    
    except RedisError:
        return jsonify({"erro": "Erro ao conectar com o Redis"}), 500
```

Essas melhorias tornam o microserviço mais robusto, seguro e escalável.
"""
