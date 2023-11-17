import os
import face_recognition
from shutil import move

# Diretórios de origem, banco de imagens e destino
diretorio_origem = "C:\\Users\\Yukari\\Pictures\\from"
diretorio_banco_imagens = "C:\\Users\\Yukari\\Pictures\\test img"
diretorio_destino = "C:\\Users\\Yukari\\Pictures\\to"

# Lista para armazenar os caminhos das imagens no banco de imagens
imagens_banco = []

# Iterar sobre as imagens no banco de imagens e armazenar os caminhos
for nome_arquivo_banco in os.listdir(diretorio_banco_imagens):
    caminho_arquivo_banco = os.path.join(
        diretorio_banco_imagens, nome_arquivo_banco)

    # Verificar se é uma imagem
    if nome_arquivo_banco.lower().endswith(('.png', '.jpg', '.jpeg')):
        imagens_banco.append(caminho_arquivo_banco)

# Iterar sobre as imagens na pasta de origem
for nome_arquivo_desconhecido in os.listdir(diretorio_origem):
    caminho_arquivo_desconhecido = os.path.join(
        diretorio_origem, nome_arquivo_desconhecido)

    # Verificar se é uma imagem
    if nome_arquivo_desconhecido.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Carregar imagem desconhecida
        imagem_desconhecida = face_recognition.load_image_file(
            caminho_arquivo_desconhecido)
        codificacao_desconhecida = face_recognition.face_encodings(
            imagem_desconhecida)

        if len(codificacao_desconhecida) > 0:
            # Iterar sobre as imagens no banco de imagens
            for caminho_arquivo_banco in imagens_banco:
                # Carregar imagem do banco
                imagem_banco = face_recognition.load_image_file(
                    caminho_arquivo_banco)
                codificacao_banco = face_recognition.face_encodings(
                    imagem_banco)

                # Comparar rostos
                for codificacao_banco_individual in codificacao_banco:
                    for codificacao_desconhecida_individual in codificacao_desconhecida:
                        resultado_comparacao = face_recognition.compare_faces(
                            [codificacao_banco_individual], codificacao_desconhecida_individual)

                        if any(resultado_comparacao):
                            # Mover imagem desconhecida para o diretório de destino
                            novo_caminho = os.path.join(
                                diretorio_destino, nome_arquivo_desconhecido)
                            move(caminho_arquivo_desconhecido, novo_caminho)
                            print(
                                f"Rosto conhecido encontrado. Imagem movida para {novo_caminho}")
                            break  # Se encontrar uma correspondência, não precisa verificar mais para esta imagem desconhecida
                    if any(resultado_comparacao):
                        break
                if any(resultado_comparacao):
                    break
        else:
            print(f"Nenhum rosto detectado em {nome_arquivo_desconhecido}")
