from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sacredapi',
}

# Função para conectar ao MySQL
def conectar_mysql():
    return mysql.connector.connect(**db_config)

# Endpoint para obter todos os livros da Bíblia
@app.route('/livros', methods=['GET'])
def obter_livros():
    try:
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT id, nome FROM livros')
        livros = [{'id': row[0], 'nome': row[1]} for row in cursor.fetchall()]

        return jsonify({'livros': livros})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para obter os capítulos de um livro específico
@app.route('/livros/<int:livro_id>/capitulos', methods=['GET'])
def obter_capitulos(livro_id):
    try:
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT id, numero FROM capitulos WHERE livro_id = %s', (livro_id,))
        capitulos = [{'id': row[0], 'numero': row[1]} for row in cursor.fetchall()]

        return jsonify({'capitulos': capitulos})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para obter os versículos de um capítulo específico
@app.route('/livros/<int:livro_id>/capitulos/<int:capitulo_id>/versiculos', methods=['GET'])
def obter_versiculos(livro_id, capitulo_id):
    try:
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT numero, texto FROM versiculos WHERE livro_id = %s AND capitulo_id = %s', (livro_id, capitulo_id))
        versiculos = [{'numero': row[0], 'texto': row[1]} for row in cursor.fetchall()]

        return jsonify({'versiculos': versiculos})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()


# Endpoint para criar um novo post
@app.route('/posts', methods=['POST'])
def criar_post():
    try:
        data = request.get_json()
        livro_id = data['livro_id']
        capitulo_id = data['capitulo_id']
        versiculo_id = data['versiculo_id']
        titulo = data['titulo']
        conteudo = data['conteudo']
        
        # Realize a autenticação e autorização aqui (por exemplo, verifique se o usuário está logado)

        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO posts (livro_id, capitulo_id, versiculo_id, titulo, conteudo) VALUES (%s, %s, %s, %s, %s)',
                       (livro_id, capitulo_id, versiculo_id, titulo, conteudo))

        connection.commit()

        return jsonify({'mensagem': 'Post criado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para obter todos os posts de um livro, capítulo ou versículo específico
@app.route('/posts/<int:livro_id>/<int:capitulo_id>/<int:versiculo_id>', methods=['GET'])
def obter_posts(livro_id, capitulo_id, versiculo_id):
    try:
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT id, titulo, conteudo FROM posts WHERE livro_id = %s AND capitulo_id = %s AND versiculo_id = %s',
                       (livro_id, capitulo_id, versiculo_id))
        posts = [{'id': row[0], 'titulo': row[1], 'conteudo': row[2]} for row in cursor.fetchall()]

        return jsonify({'posts': posts})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para atualizar um post existente
@app.route('/posts/<int:post_id>', methods=['PUT'])
def atualizar_post(post_id):
    try:
        data = request.get_json()
        novo_titulo = data['novo_titulo']
        novo_conteudo = data['novo_conteudo']
        
        # Realize a autenticação e autorização aqui (por exemplo, verifique se o usuário é o autor do post)

        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('UPDATE posts SET titulo = %s, conteudo = %s WHERE id = %s',
                       (novo_titulo, novo_conteudo, post_id))

        connection.commit()

        return jsonify({'mensagem': 'Post atualizado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para excluir um post existente
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def excluir_post(post_id):
    try:
        # Realize a autenticação e autorização aqui (por exemplo, verifique se o usuário é o autor do post)

        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))

        connection.commit()

        return jsonify({'mensagem': 'Post excluído com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()


# Endpoint para adicionar um novo livro
@app.route('/livros', methods=['POST'])
def adicionar_livro():
    try:
        data = request.get_json()
        nome = data['nome']
        testamento = data['testamento']
        
        # Verificar se o livro já existe no banco de dados
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM livros WHERE nome = %s', (nome,))
        livro_existente = cursor.fetchone()

        if livro_existente:
            return jsonify({'erro': 'Livro com o mesmo nome já existe'}), 400

        cursor.execute('INSERT INTO livros (nome, testamento) VALUES (%s, %s)',
                       (nome, testamento))

        connection.commit()

        return jsonify({'mensagem': 'Livro adicionado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para adicionar um novo capítulo a um livro específico
@app.route('/livros/<int:livro_id>/capitulos', methods=['POST'])
def adicionar_capitulo(livro_id):
    try:
        data = request.get_json()
        numero = data['numero']
        
        # Verificar se o capítulo já existe para o mesmo livro
        connection = conectar_mysql()
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM capitulos WHERE livro_id = %s AND numero = %s', (livro_id, numero))
        capitulo_existente = cursor.fetchone()

        if capitulo_existente:
            return jsonify({'erro': 'Capítulo já existe para o mesmo livro'}), 400

        # Defina explicitamente o número do capítulo na inserção
        cursor.execute('INSERT INTO capitulos (livro_id, numero) VALUES (%s, %s)',
                       (livro_id, numero))

        connection.commit()

        return jsonify({'mensagem': 'Capítulo adicionado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

# Endpoint para adicionar um novo versículo a um capítulo específico
@app.route('/livros/<int:livro_id>/capitulos/<int:capitulo_numero>/versiculos', methods=['POST'])
def adicionar_versiculo(livro_id, capitulo_numero):
    try:
        data = request.get_json()
        numero = data['numero']
        texto = data['texto']
        
        connection = conectar_mysql()
        cursor = connection.cursor()

        # Verifique se o capítulo e o livro existem no banco de dados com base no número do capítulo
        cursor.execute('SELECT id FROM capitulos WHERE livro_id = %s AND numero = %s', (livro_id, capitulo_numero))
        capitulo_existente = cursor.fetchone()

        if not capitulo_existente:
            return jsonify({'erro': 'O capítulo ou livro não existe no banco de dados'}), 400

        # Verifique se os tipos de dados dos parâmetros estão corretos
        if not isinstance(numero, int) or not isinstance(texto, str):
            return jsonify({'erro': 'Tipo de dados inválido para número ou texto'}), 400

        # Agora você pode usar o ID do capítulo encontrado com base no número fornecido
        cursor.execute('INSERT INTO versiculos (livro_id, capitulo_id, numero, texto) VALUES (%s, %s, %s, %s)',
                       (livro_id, capitulo_existente[0], numero, texto))

        connection.commit()

        return jsonify({'mensagem': 'Versículo adicionado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)})

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
