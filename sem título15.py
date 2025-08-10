import time

class Postagem:
    def __init__(self, autor, texto):
        self.autor = autor
        self.texto = texto
        self.curtidas = 0
        self.comentarios = [] #Lista de comentários em cada postagem 
        self.timestamp = time.time()

    def curtir(self):
        self.curtidas += 1

    def comentar(self, comentario):
        self.comentarios.append(comentario)

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.seguindo = set() #Conjunto (Set)-Lista de pessoas que um usuário segue- não vai seguir a mesma pessoa 2 vezes 
        self.postagens = [] # Lista de postagens de cada usuário

    def seguir(self, outro_usuario):
        self.seguindo.add(outro_usuario)

    def criar_postagem(self, texto):
        p = Postagem(self.nome, texto)
        self.postagens.append(p)
        return p

usuarios = {} #Hash table- Permite busca rápida de usuários por nome.
pilha_acoes = [] #Pilha- Histórico de ações para desfazer (curtir, comentar, postar)

def cadastrar_usuario(nome): #Hash table- Permite busca rápida de usuários por nome.
    if nome in usuarios:
        print("Usuário já existe.")
    else:
        usuarios[nome] = Usuario(nome)
        print(f"Usuário '{nome}' cadastrado com sucesso.")

def seguir_usuario(seguidor, seguido):
    if seguidor in usuarios and seguido in usuarios:
        usuarios[seguidor].seguir(usuarios[seguido])
        print(f"{seguidor} agora segue {seguido}.")
    else:
        print("Um dos usuários não existe.")

def postar(nome, texto):
    if nome in usuarios:
        post = usuarios[nome].criar_postagem(texto)
        print("Postagem criada com sucesso.")
        pilha_acoes.append(("postar", post, usuarios[nome]))
    else:
        print("Usuário não encontrado.")

def curtir_postagem(nome, autor):
    if nome in usuarios and autor in usuarios:
        posts = usuarios[autor].postagens
        if posts:
            for i, p in enumerate(posts):
                print(f"[{i}] {p.texto} | Curtidas: {p.curtidas}")
            idx = int(input("Escolha o número da postagem para curtir: "))
            post = posts[idx]
            post.curtir()
            pilha_acoes.append(("curtir", post))
        else:
            print("Esse usuário ainda não postou nada.")
    else:
        print("Usuário(s) não encontrado(s).")

def comentar_postagem(nome, autor):
    if nome in usuarios and autor in usuarios:
        posts = usuarios[autor].postagens
        if posts:
            for i, p in enumerate(posts):
                print(f"[{i}] {p.texto} | Comentários: {len(p.comentarios)}")
            idx = int(input("Escolha o número da postagem para comentar: "))
            comentario = input("Digite seu comentário: ")
            post = posts[idx]
            post.comentar(comentario)
            pilha_acoes.append(("comentar", post, comentario))
        else:
            print("Esse usuário ainda não postou nada.")
    else:
        print("Usuário(s) não encontrado(s).")

def ver_comentarios(nome, autor):
    if nome in usuarios and autor in usuarios:
        posts = usuarios[autor].postagens
        if posts:
            for i, p in enumerate(posts):
                print(f"[{i}] {p.texto} | Comentários: {len(p.comentarios)}")
            idx = int(input("Escolha o número da postagem para ver os comentários: "))
            post = posts[idx]
            print(f"Comentários da postagem '{post.texto}':")
            for c in post.comentarios:
                print(f"- {c}")
        else:
            print("Esse usuário ainda não postou nada.")
    else:
        print("Usuário(s) não encontrado(s).")

def desfazer_ultima_acao(): #Pilha- Histórico de ações para desfazer (curtir, comentar, postar)
    if pilha_acoes:
        acao = pilha_acoes.pop()
        if acao[0] == "curtir":
            acao[1].curtidas -= 1
        elif acao[0] == "comentar":
            acao[1].comentarios.remove(acao[2])
        elif acao[0] == "postar":
            acao[2].postagens.remove(acao[1])
        print("Ação desfeita.")
    else:
        print("Nenhuma ação para desfazer.")

def gerar_feed(nome):
    if nome in usuarios:
        feed = []
        user = usuarios[nome]
        for seguido in user.seguindo:
            feed.extend(seguido.postagens)
        feed.sort(key=lambda p: (p.curtidas * 2 + len(p.comentarios), -p.timestamp), reverse=True) #Árvore Binária (simulada na ordenação do feed)-prioridade
        for p in feed:
            print(f"{p.autor}: {p.texto} | Curtidas: {p.curtidas} | Comentários: {len(p.comentarios)}")
    else:
        print("Usuário não encontrado.")

while True:
    print("\n1. Cadastrar usuário")
    print("2. Seguir usuário")
    print("3. Postar")
    print("4. Curtir postagem")
    print("5. Comentar postagem")
    print("6. Ver comentários de uma postagem")
    print("7. Gerar feed")
    print("8. Desfazer ação")
    print("0. Sair")
    op = input("Escolha uma opção: ")

    if op == "1":
        nome = input("Nome do usuário: ")
        cadastrar_usuario(nome)
    elif op == "2":
        seguidor = input("Seu nome: ")
        seguido = input("Nome da pessoa a seguir: ")
        seguir_usuario(seguidor, seguido)
    elif op == "3":
        nome = input("Seu nome: ")
        texto = input("Texto da postagem: ")
        postar(nome, texto)
    elif op == "4":
        nome = input("Seu nome: ")
        autor = input("Nome do autor da postagem: ")
        curtir_postagem(nome, autor)
    elif op == "5":
        nome = input("Seu nome: ")
        autor = input("Nome do autor da postagem: ")
        comentar_postagem(nome, autor)
    elif op == "6":
        nome = input("Seu nome: ")
        autor = input("Nome do autor da postagem: ")
        ver_comentarios(nome, autor)
    elif op == "7":
        nome = input("Seu nome: ")
        gerar_feed(nome)
    elif op == "8":
        desfazer_ultima_acao()
    elif op == "0":
        break
    else:
        print("Opção inválida.")