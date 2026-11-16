from flask import Flask, redirect, render_template, request
import psycopg2

app = Flask(__name__)

def ligar_banco():
   banco=psycopg2.connect(
       host="localhost",
       dbname="BancoFarmacia",
       user="postgres",
       password="senai",
       port="5432")
   return banco

@app.route('/')
def tarefas():
    return render_template("index.html")
@app.route('/tarefas/remedio')
def tarefas_remedio():
   banco=ligar_banco()
   cursor=banco.cursor()
   cursor.execute("SELECT id_remedio, nome, laboratorio, estoque, preco FROM remedio ORDER BY id_remedio")
   remedio=cursor.fetchall()
   banco.close()
   return render_template("tarefas_remedio.html", remedios=remedio)

@app.route('/tarefas/remedio/enviar', methods=['POST'])
def enviar_tarefa_remedio():
   nome = request.form.get('nome')
   laboratorio = request.form.get('laboratorio')
   estoque = request.form.get('estoque')
   preco = request.form.get('preco')
   banco = ligar_banco()
   cursor = banco.cursor()
   cursor.execute(""" INSERT INTO  remedio (nome, laboratorio, estoque, preco) VALUES (%s, %s, %s, %s)""", (nome, laboratorio, estoque, preco))
   banco.commit()
   banco.close()
   return redirect('/tarefas/remedio')

@app.route('/tarefas/remedio/editar/<int:id>')
def editar_tarefa_remedio(id):
   banco = ligar_banco()
   cursor = banco.cursor()
   cursor.execute("SELECT id_remedio, nome, laboratorio, estoque, preco FROM remedio WHERE id_remedio = %s", (id,))
   remedio = cursor.fetchone()
   banco.close()

   if remedio is None:
       return redirect('/tarefas/remedio')
   return render_template("editar_remedio.html", remedio=remedio)

@app.route('/tarefas/remedio/atualizar/<int:id>', methods=['POST'])
def atualizar_tarefa_remedio(id):
   nome = request.form.get('nome')
   laboratorio = request.form.get('laboratorio')
   estoque = request.form.get('estoque')
   preco = request.form.get('preco')
   banco = ligar_banco()
   cursor = banco.cursor()
   cursor.execute("""UPDATE remedio SET nome = %s, laboratorio = %s, estoque = %s, preco = %s WHERE id_remedio = %s""", (nome, laboratorio, estoque, preco, id))
   banco.commit()
   banco.close()
   return redirect('/tarefas/remedio')

@app.route('/tarefas/remedio/excluir/<int:id>', methods=['POST'])
def excluir_tarefa_remedio(id):
   banco = ligar_banco()
   cursor = banco.cursor()
   cursor.execute("""DELETE FROM remedio WHERE id_remedio = %s""", (id,))
   banco.commit()
   banco.close()
   return redirect('/tarefas/remedio')







@app.route('/cliente')
def cliente():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, nome, telefone, idade, data_cadastro FROM cliente ORDER BY id")
    lista = cursor.fetchall()
    banco.close()
    return render_template("cliente.html", clientes=lista)


@app.route("/cliente/enviar", methods=["POST"])
def enviar_cliente():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    idade = request.form["idade"]
    data_cadastro = request.form["data_cadastro"]

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO cliente (nome, telefone, idade, data_cadastro)
                VALUES (%s,%s,%s,%s)""", (nome, telefone, idade, data_cadastro))
    banco.commit()
    banco.close()
    return redirect("/cliente")


@app.route("/cliente/editar/<int:id>")
def editar_cliente(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id, nome, telefone, idade, data_cadastro FROM cliente WHERE id = %s""", (id,))
    cliente = cursor.fetchone()
    banco.close()

    if cliente is None:
        return redirect("/cliente")
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/cliente/atualizar/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    idade = request.form.get("idade")
    data_cadastro = request.form.get("data_cadastro")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE cliente SET nome = %s, telefone = %s, idade = %s, data_cadastro = %s
                WHERE id = %s""", (nome, telefone, idade, data_cadastro, id))
    banco.commit()
    banco.close()
    return redirect("/cliente")


@app.route("/cliente/excluir/<int:id>", methods=["POST"])
def excluir_cliente(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""DELETE FROM cliente WHERE id = %s""", (id,))
    banco.commit()
    banco.close()
    return redirect("/cliente")



if __name__ == '__main__':
   app.run()