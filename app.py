from flask import Flask, request, jsonify
import psycopg2
import time

# Tenta conectar até o banco estar pronto
def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="meu-banco",
                database="mensagensdb",
                user="usuario",
                password="senha123"
            )
            return conn
        except:
            print("Aguardando banco iniciar...")
            time.sleep(2)

app = Flask(__name__)
conn = connect_db()
cur = conn.cursor()

# Cria tabela caso não exista
cur.execute("""
CREATE TABLE IF NOT EXISTS mensagens (
    id SERIAL PRIMARY KEY,
    texto TEXT
);
""")
conn.commit()

@app.route('/mensagem', methods=['POST'])
def add_msg():
    data = request.json
    texto = data.get('texto')

    if not texto:
        return jsonify({"erro": "Campo 'texto' obrigatório"}), 400

    cur.execute("INSERT INTO mensagens (texto) VALUES (%s) RETURNING id;", (texto,))
    conn.commit()

    return jsonify({"status": "mensagem salva", "texto": texto}), 201

@app.route('/mensagens', methods=['GET'])
def get_msgs():
    cur.execute("SELECT * FROM mensagens;")
    rows = cur.fetchall()

    mensagens = [{"id": r[0], "texto": r[1]} for r in rows]

    return jsonify(mensagens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
