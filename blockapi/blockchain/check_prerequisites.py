"""
Script para verificar pré-requisitos da blockchain
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_environment_variables():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("🔍 Verificando variáveis de ambiente...")
    
    private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
    endpoint = os.getenv('ETHEREUM_ENDPOINT')
    
    if not private_key:
        print("❌ ETHEREUM_PRIVATE_KEY não encontrada no .env")
        return False
    
    if not endpoint:
        print("❌ ETHEREUM_ENDPOINT não encontrada no .env")
        return False
    
    if not private_key.startswith('0x'):
        print("❌ ETHEREUM_PRIVATE_KEY deve começar com '0x'")
        return False
    
    if len(private_key) != 66:  # 0x + 64 caracteres hex
        print("❌ ETHEREUM_PRIVATE_KEY deve ter 66 caracteres (incluindo 0x)")
        return False
    
    if 'sepolia' in endpoint.lower():
        print("✅ Usando rede Sepolia (testnet) - Recomendado para testes")
    elif 'mainnet' in endpoint.lower():
        print("⚠️ Usando rede Mainnet - Cuidado! Requer ETH real")
    else:
        print(f"ℹ️ Usando endpoint personalizado: {endpoint}")
    
    print("✅ Variáveis de ambiente configuradas corretamente")
    return True

def check_wallet_balance():
    """Verifica saldo da carteira"""
    print("\n💰 Verificando saldo da carteira...")
    
    try:
        from web3 import Web3
        from eth_account import Account
        
        private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
        endpoint = os.getenv('ETHEREUM_ENDPOINT')
        
        # Conectar à blockchain
        w3 = Web3(Web3.HTTPProvider(endpoint))
        
        if not w3.is_connected():
            print("❌ Não foi possível conectar à blockchain")
            return False
        
        # Obter endereço da carteira
        account = Account.from_key(private_key)
        address = account.address
        
        print(f"📍 Endereço da carteira: {address}")
        
        # Verificar saldo
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        print(f"💳 Saldo atual: {balance_eth} ETH")
        
        if balance_eth == 0:
            print("⚠️ Saldo zero! Você precisa de ETH para pagar taxas de transação")
            if 'sepolia' in endpoint.lower():
                print("💡 Para Sepolia testnet, você pode obter ETH gratuito em:")
                print("   - https://sepoliafaucet.com/")
                print("   - https://www.alchemy.com/faucets/ethereum-sepolia")
                print("   - https://faucet.chainstack.com/ethereum-testnet-faucet")
            return False
        elif balance_eth < 0.01:
            print("⚠️ Saldo baixo! Recomendamos pelo menos 0.01 ETH para testes")
        else:
            print("✅ Saldo suficiente para transações")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install web3 eth-account")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar saldo: {e}")
        return False

def check_scmanager():
    """Verifica se SCManager está instalado"""
    print("\n🔧 Verificando SCManager...")
    
    try:
        import scmanager
        print("✅ SCManager instalado")
        
        # Verificar se admin_tools está disponível
        from scmanager import admin_tools
        print("✅ admin_tools disponível")
        
        return True
        
    except ImportError as e:
        print(f"❌ SCManager não encontrado: {e}")
        print("Execute: pip install -e \"c:\\Users\\Enzo\\Downloads\\SCManager-master\\SCManager-master\"")
        return False

def check_dependencies():
    """Verifica dependências Python"""
    print("\n📦 Verificando dependências...")
    
    required_packages = [
        'web3',
        'eth_account', 
        'eth_typing',
        'sqlalchemy',
        'flask',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ Todas as dependências instaladas")
    return True

def test_blockchain_connection():
    """Testa conexão básica com blockchain"""
    print("\n🌐 Testando conexão com blockchain...")
    
    try:
        from web3 import Web3
        
        endpoint = os.getenv('ETHEREUM_ENDPOINT')
        w3 = Web3(Web3.HTTPProvider(endpoint))
        
        if not w3.is_connected():
            print("❌ Não foi possível conectar à blockchain")
            print("Verifique seu endpoint e conexão com internet")
            return False
        
        # Verificar número do bloco atual
        latest_block = w3.eth.block_number
        print(f"✅ Conectado! Último bloco: {latest_block}")
        
        # Verificar chain ID
        chain_id = w3.eth.chain_id
        print(f"🔗 Chain ID: {chain_id}")
        
        if chain_id == 11155111:
            print("✅ Rede Sepolia (testnet)")
        elif chain_id == 1:
            print("⚠️ Rede Mainnet (produção)")
        else:
            print(f"ℹ️ Rede personalizada (ID: {chain_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    """Função principal de verificação"""
    print("🔍 VERIFICAÇÃO DE PRÉ-REQUISITOS BLOCKCHAIN")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    checks = [
        ("Variáveis de ambiente", check_environment_variables),
        ("Dependências Python", check_dependencies), 
        ("SCManager", check_scmanager),
        ("Conexão blockchain", test_blockchain_connection),
        ("Saldo da carteira", check_wallet_balance)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        print("-" * 30)
        
        if check_func():
            passed += 1
        else:
            print(f"⚠️ Falha em: {name}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("🎉 Todos os pré-requisitos atendidos!")
        print("Você pode prosseguir com o setup da blockchain.")
    else:
        print("❌ Alguns pré-requisitos não foram atendidos.")
        print("Corrija os problemas acima antes de continuar.")
    
    return passed == total

if __name__ == "__main__":
    main()
