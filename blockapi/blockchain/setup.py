"""
Script para configuração inicial da blockchain
"""
import os
import sys
import logging
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from blockchain.blockchain_manager import blockchain_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_blockchain():
    """
    Configura a blockchain para primeira utilização
    """
    print("🔗 Configurando Blockchain...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
    endpoint = os.getenv('ETHEREUM_ENDPOINT')
    
    if not private_key or not endpoint:
        print("❌ ERRO: Variáveis de ambiente não configuradas!")
        print("Certifique-se de que as seguintes variáveis estão no arquivo .env:")
        print("- ETHEREUM_PRIVATE_KEY")
        print("- ETHEREUM_ENDPOINT")
        return False
    
    print("✅ Variáveis de ambiente encontradas")
    
    # Verificar se está usando mainnet
    if "mainnet" in endpoint.lower():
        print("⚠️  AVISO: Você está usando a MAINNET do Ethereum!")
        print("   Isso requer ETH real para transações.")
        print("   Para testes, considere usar uma testnet como Sepolia ou Goerli.")
        resposta = input("   Deseja continuar mesmo assim? (s/N): ").lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            print("❌ Configuração cancelada pelo usuário")
            return False
    
    # Tentar conectar com blockchain
    try:
        print("🔄 Tentando conectar com blockchain...")
        
        # Importar web3 para testar conexão básica
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(endpoint))
        
        if not w3.is_connected():
            print("❌ Não foi possível conectar ao endpoint")
            print("   Verifique se o endpoint está correto e funcionando")
            return False
        
        print("✅ Conexão com endpoint estabelecida")
        
        # Verificar chave privada
        from eth_account import Account
        try:
            account = Account.from_key(private_key)
            print(f"✅ Carteira carregada: {account.address}")
            
            # Verificar saldo
            balance_wei = w3.eth.get_balance(account.address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            print(f"💰 Saldo da carteira: {balance_eth} ETH")
            
            if balance_eth == 0:
                print("⚠️  AVISO: Carteira sem saldo ETH!")
                print("   Você precisará de ETH para pagar taxas de transação.")
                if "mainnet" in endpoint.lower():
                    print("   Na mainnet, isso significa ETH real.")
                
        except Exception as key_error:
            print(f"❌ Erro na chave privada: {key_error}")
            return False
        
        # Tentar inicializar blockchain_manager
        if blockchain_manager.is_connected():
            print("✅ Blockchain conectada com sucesso!")
            
            # Mostrar status
            status = blockchain_manager.get_blockchain_status()
            print(f"👥 Total de usuários: {status.get('total_users', 0)}")
            print(f"🧱 Total de blocos: {status.get('total_blocks', 0)}")
            print(f"🕒 Última atualização: {status.get('last_update', 'N/A')}")
            
            # Mostrar informações do contrato
            contract_info = blockchain_manager.get_contract_info()
            if contract_info.get('success'):
                print(f"📋 Endereço do contrato: {contract_info.get('contract_address', 'N/A')}")
                print(f"👤 Endereço da carteira: {contract_info.get('wallet_address', 'N/A')}")
                print(f"🌐 Rede: {contract_info.get('network_endpoint', 'N/A')}")
            
            return True
        else:
            print("⚠️  Blockchain manager não conectado, mas endpoint básico funciona")
            print("   Isso pode indicar que o contrato ainda não foi implantado")
            print("   O sistema funcionará em modo offline até o primeiro deploy")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao configurar blockchain: {e}")
        print("   Sistema funcionará em modo offline")
        return False

def test_blockchain_operations():
    """
    Testa operações básicas da blockchain
    """
    print("\n🧪 Testando operações da blockchain...")
    print("=" * 50)
    
    try:
        # Criar usuário de teste
        from models.usuario import Usuario
        
        usuario_teste = Usuario()
        usuario_teste.nome = "Usuário Teste Blockchain"
        usuario_teste.documento = "12345678901"
        usuario_teste.email = "teste_blockchain@exemplo.com"
        
        print("👤 Testando registro de usuário...")
        result = blockchain_manager.register_user_on_blockchain(usuario_teste)
        
        if result['success']:
            print("✅ Usuário de teste registrado com sucesso!")
            if result.get('transaction_hash'):
                print(f"📋 Hash da transação: {result['transaction_hash']}")
        else:
            print(f"❌ Falha ao registrar usuário: {result['message']}")
        
        # Verificar se usuário foi registrado
        print("🔍 Verificando registro do usuário...")
        is_registered = blockchain_manager.is_user_registered_on_blockchain(usuario_teste)
        if is_registered:
            print("✅ Usuário encontrado na blockchain!")
        else:
            print("⚠️ Usuário não encontrado na blockchain")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

def main():
    """
    Função principal de configuração
    """
    print("🚀 CONFIGURAÇÃO INICIAL DA BLOCKCHAIN")
    print("=" * 50)
    
    # Configurar blockchain
    if not setup_blockchain():
        print("\n❌ Falha na configuração da blockchain")
        return
    
    # Perguntar se deseja executar testes
    resposta = input("\n🧪 Deseja executar testes da blockchain? (s/N): ").lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        test_blockchain_operations()
    
    print("\n✅ Configuração concluída!")
    print("Agora você pode usar as funcionalidades blockchain na sua aplicação.")

if __name__ == "__main__":
    main()
