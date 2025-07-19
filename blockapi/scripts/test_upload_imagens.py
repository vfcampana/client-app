#!/usr/bin/env python3
"""
Script para testar o upload de múltiplas imagens
"""

import sys
import os
import requests
from io import BytesIO
from PIL import Image

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.imagem_supabase import ImagemSupabase

def criar_imagem_teste(nome_arquivo, cor=(255, 0, 0)):
    """Criar uma imagem de teste simples"""
    img = Image.new('RGB', (300, 200), color=cor)
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer

def teste_upload_multiplas_imagens():
    """Testa o upload de múltiplas imagens"""
    print("🔍 Testando upload de múltiplas imagens...")
    
    try:
        imagem_service = ImagemSupabase()
        bloco_id_teste = 1  # ID de teste
        
        # Criar algumas imagens de teste
        cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Vermelho, Verde, Azul
        nomes = ["teste_vermelha.jpg", "teste_verde.jpg", "teste_azul.jpg"]
        
        resultados = []
        
        for i, (cor, nome) in enumerate(zip(cores, nomes)):
            print(f"  📤 Enviando {nome}...")
            
            # Simular arquivo de upload
            class FakeFile:
                def __init__(self, nome, buffer):
                    self.filename = nome
                    self.content_type = 'image/jpeg'
                    self._buffer = buffer
                
                def read(self):
                    return self._buffer.getvalue()
                
                def seek(self, pos):
                    self._buffer.seek(pos)
            
            buffer = criar_imagem_teste(nome, cor)
            fake_file = FakeFile(nome, buffer)
            
            try:
                resultado = imagem_service.fazer_upload_imagem(fake_file, bloco_id_teste)
                resultados.append(resultado)
                print(f"    ✅ {nome} enviada com sucesso!")
                print(f"    🔗 URL: {resultado.get('url_publica', 'N/A')}")
            except Exception as e:
                print(f"    ❌ Erro ao enviar {nome}: {e}")
                return False
        
        print(f"\n✅ {len(resultados)} imagens enviadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de upload: {e}")
        return False

def teste_listar_imagens():
    """Testa a listagem de imagens"""
    print("\n🔍 Testando listagem de imagens...")
    
    try:
        imagem_service = ImagemSupabase()
        bloco_id_teste = 1
        
        imagens = imagem_service.listar_imagens_bloco(bloco_id_teste)
        
        print(f"✅ Encontradas {len(imagens)} imagens para o bloco {bloco_id_teste}")
        
        for i, imagem in enumerate(imagens, 1):
            print(f"  {i}. {imagem['nome_arquivo']} - {imagem['url_imagem']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao listar imagens: {e}")
        return False

def teste_deletar_imagem():
    """Testa a deleção de imagens"""
    print("\n🔍 Testando deleção de imagem...")
    
    try:
        imagem_service = ImagemSupabase()
        bloco_id_teste = 1
        
        # Listar imagens primeiro
        imagens = imagem_service.listar_imagens_bloco(bloco_id_teste)
        
        if not imagens:
            print("  ⚠️  Nenhuma imagem para deletar")
            return True
        
        # Deletar a primeira imagem
        imagem_para_deletar = imagens[0]
        print(f"  🗑️  Deletando: {imagem_para_deletar['nome_arquivo']}")
        
        resultado = imagem_service.deletar_imagem(imagem_para_deletar['id'])
        
        if resultado:
            print("  ✅ Imagem deletada com sucesso!")
            return True
        else:
            print("  ❌ Falha ao deletar imagem")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao deletar imagem: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Testando funcionalidades de upload de imagens...\n")
    
    testes = [
        ("Upload de múltiplas imagens", teste_upload_multiplas_imagens),
        ("Listagem de imagens", teste_listar_imagens),
        ("Deleção de imagem", teste_deletar_imagem),
        ("Listagem após deleção", teste_listar_imagens)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print("=" * 50)
        resultado = funcao_teste()
        resultados.append((nome_teste, resultado))
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print("=" * 50)
    
    todos_passaram = True
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if not resultado:
            todos_passaram = False
    
    print("=" * 50)
    
    if todos_passaram:
        print("🎉 Todos os testes passaram! Sistema de imagens funcionando!")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração.")

if __name__ == "__main__":
    main()
