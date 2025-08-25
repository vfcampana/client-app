"""
Script para mostrar informações do contrato blockchain
"""
import os
import sys
import json
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def show_contract_info():
    """
    Mostra informações do contrato inteligente
    """
    print("📋 INFORMAÇÕES DO CONTRATO BLOCKCHAIN")
    print("=" * 50)
    
    try:
        from blockchain.blockchain_manager import blockchain_manager
        
        # Obter informações do contrato
        contract_info = blockchain_manager.get_contract_info()
        status = blockchain_manager.get_blockchain_status()
        
        if contract_info.get('success'):
            print("✅ Contrato encontrado!")
            print(f"📍 Endereço do contrato: {contract_info.get('contract_address')}")
            print(f"👤 Endereço da carteira: {contract_info.get('wallet_address')}")
            print(f"🏗️  Deployer: {contract_info.get('deployer_address')}")
            print(f"🌐 Rede: {contract_info.get('network_endpoint')}")
            print(f"📁 Arquivo de config: {contract_info.get('config_file')}")
            
            if blockchain_manager.is_connected():
                print(f"💰 Saldo: {status.get('account_balance')} ETH")
                print(f"👥 Usuários registrados: {status.get('total_users')}")
                print(f"🧱 Blocos registrados: {status.get('total_blocks')}")
                
                # Link para visualizar no Etherscan
                contract_address = contract_info.get('contract_address')
                if contract_address:
                    print(f"🔗 Ver no Etherscan: https://sepolia.etherscan.io/address/{contract_address}")
            else:
                print("⚠️  Blockchain offline")
        else:
            print("❌ Contrato não encontrado!")
            print(f"Erro: {contract_info.get('message')}")
            
            # Verificar se arquivo de configuração existe
            config_path = "scm_config/scm_config.json"
            if os.path.exists(config_path):
                print(f"📁 Arquivo de config existe: {config_path}")
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    print("📄 Conteúdo do arquivo:")
                    print(json.dumps(config, indent=2))
                except Exception as e:
                    print(f"Erro ao ler arquivo: {e}")
            else:
                print("❌ Arquivo de configuração não encontrado")
                print("Execute: python blockapi\\blockchain\\deploy_contract.py")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Função principal
    """
    show_contract_info()

if __name__ == "__main__":
    main()
