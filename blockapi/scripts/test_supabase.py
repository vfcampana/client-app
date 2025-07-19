#!/usr/bin/env python3
"""
Script de teste para verificar a configuração do Supabase
Execute este script para testar se a conexão com o Supabase está funcionando
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.supabase_config import get_supabase_client
from models.imagem_supabase import ImagemSupabase

def teste_conexao_supabase():
    """Testa a conexão com o Supabase"""
    print("🔍 Testando conexão com Supabase...")
    
    try:
        supabase = get_supabase_client()
        
        # Teste simples de conectividade
        response = supabase.table("imagens_blocos").select("count").execute()
        print("✅ Conexão com Supabase estabelecida com sucesso!")
        
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com Supabase: {e}")
        return False

def teste_servico_imagem():
    """Testa o serviço de imagens"""
    print("\n🔍 Testando serviço de imagens...")
    
    try:
        imagem_service = ImagemSupabase()
        
        # Teste de listagem (mesmo que retorne vazio)
        imagens = imagem_service.listar_imagens_bloco(1)
        print(f"✅ Serviço de imagens funcionando! Encontradas {len(imagens)} imagens para bloco ID 1")
        
        return True
    except Exception as e:
        print(f"❌ Erro no serviço de imagens: {e}")
        return False

def verificar_estrutura_tabela():
    """Verifica se a tabela existe e tem a estrutura esperada"""
    print("\n🔍 Verificando estrutura da tabela...")
    
    try:
        supabase = get_supabase_client()
        
        # Tentar fazer uma consulta simples para verificar se a tabela existe
        response = supabase.table("imagens_blocos").select("*").limit(1).execute()
        print("✅ Tabela 'imagens_blocos' existe e é acessível!")
        
        return True
    except Exception as e:
        print(f"❌ Problema com a tabela: {e}")
        print("\n💡 Execute o script SQL em blockapi/sql/setup_supabase.sql no Supabase Dashboard")
        return False

def main():
    """Função principal para executar todos os testes"""
    print("🚀 Iniciando testes de configuração do Supabase...\n")
    
    # Lista de testes
    testes = [
        ("Conexão com Supabase", teste_conexao_supabase),
        ("Estrutura da tabela", verificar_estrutura_tabela),
        ("Serviço de imagens", teste_servico_imagem)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        resultado = funcao_teste()
        resultados.append((nome_teste, resultado))
    
    # Resumo dos resultados
    print("\n📊 RESUMO DOS TESTES:")
    print("=" * 50)
    
    todos_passaram = True
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if not resultado:
            todos_passaram = False
    
    print("=" * 50)
    
    if todos_passaram:
        print("🎉 Todos os testes passaram! Supabase está configurado corretamente.")
        print("\n📝 Próximos passos:")
        print("1. Execute o backend: python app.py")
        print("2. Teste as rotas de upload de imagem")
        print("3. Integre com o frontend React")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração do Supabase.")
        print("\n🔧 Passos para resolver:")
        print("1. Verifique se as variáveis SUPABASE_URL e SUPABASE_KEY estão corretas no .env")
        print("2. Execute o script SQL em blockapi/sql/setup_supabase.sql")
        print("3. Crie o bucket 'imagens-blocos' no Supabase Storage")
        print("4. Execute este teste novamente")

if __name__ == "__main__":
    main()
