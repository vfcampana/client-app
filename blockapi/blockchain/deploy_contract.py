"""
Script para fazer deploy do contrato inteligente
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def deploy_contract():
    """
    Faz o deploy do contrato inteligente
    """
    print("🚀 DEPLOY DO CONTRATO INTELIGENTE")
    print("=" * 50)
    
    try:
        # Verificar variáveis de ambiente
        private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
        endpoint = os.getenv('ETHEREUM_ENDPOINT')
        
        if not private_key or not endpoint:
            print("❌ ERRO: Variáveis de ambiente não configuradas!")
            return False
        
        print("✅ Variáveis de ambiente encontradas")
        print(f"🌐 Rede: {endpoint}")
        
        # Verificar se já existe arquivo de configuração
        config_path = "scm_config/scm_config.json"
        if os.path.exists(config_path):
            resposta = input("⚠️  Arquivo de configuração já existe. Sobrescrever? (s/N): ").lower()
            if resposta not in ['s', 'sim', 'y', 'yes']:
                print("❌ Deploy cancelado pelo usuário")
                return False
            
            # Remover arquivo existente
            os.remove(config_path)
            print("🗑️  Arquivo de configuração anterior removido")
        
        print("📄 Importando SCManager admin_tools...")
        from scmanager import admin_tools as adm
        
        print("🔄 Iniciando deploy do contrato...")
        print("⚠️  ATENÇÃO: Isso consumirá ETH para taxas de transação!")
        print("💰 Custo estimado: ~0.01-0.05 ETH")
        
        input("   Pressione ENTER para continuar ou Ctrl+C para cancelar...")
        
        # Fazer deploy
        adm.create_config_file()
        
        print("✅ Deploy realizado com sucesso!")
        print(f"📁 Arquivo de configuração criado: {config_path}")
        
        # Verificar se arquivo foi criado
        if os.path.exists(config_path):
            print("✅ Arquivo de configuração verificado")
            
            # Ler e mostrar informações básicas
            try:
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                contract_info = config.get('contract', {})
                if 'address' in contract_info:
                    print(f"📋 Endereço do contrato: {contract_info['address']}")
                
            except Exception as e:
                print(f"⚠️  Erro ao ler configuração: {e}")
            
            return True
        else:
            print("❌ Arquivo de configuração não foi criado")
            return False
            
    except KeyboardInterrupt:
        print("\n❌ Deploy cancelado pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro durante deploy: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    Função principal
    """
    if deploy_contract():
        print("\n🎉 Deploy concluído com sucesso!")
        print("Agora você pode usar o sistema blockchain.")
        print("\nPróximos passos:")
        print("1. Execute: python blockapi\\blockchain\\setup.py")
        print("2. Teste as funcionalidades blockchain")
    else:
        print("\n❌ Deploy falhou!")
        print("Verifique os erros acima e tente novamente.")

if __name__ == "__main__":
    main()
