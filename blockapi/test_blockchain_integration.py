"""
Script de teste para verificar integração blockchain com logs detalhados
"""
import sys
import os
sys.path.append('.')

from blockchain.blockchain_manager import blockchain_manager
from models.usuario import Usuario
from models.bloco import Bloco
from models.extensions import SessionLocal
import logging

# Configurar logging detalhado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_blockchain_integration():
    """Testa a integração blockchain com dados reais"""
    logger.info("=== INICIANDO TESTE DE INTEGRAÇÃO BLOCKCHAIN ===")
    
    # Verificar status do blockchain manager
    logger.info(f"Blockchain conectado: {blockchain_manager.is_connected()}")
    
    if not blockchain_manager.is_connected():
        logger.warning("⚠️  Blockchain não conectado - testando em modo offline")
        logger.info("Para testar com conexão real, configure ETHEREUM_PRIVATE_KEY e ETHEREUM_ENDPOINT no .env")
        return
    
    # Buscar dados reais do banco
    session = SessionLocal()
    try:
        # Buscar um usuário existente
        usuario = session.query(Usuario).first()
        if not usuario:
            logger.error("❌ Nenhum usuário encontrado no banco de dados")
            return
        
        logger.info(f"✓ Usuário encontrado: {usuario.nome} ({usuario.email})")
        
        # Buscar um bloco existente
        bloco = session.query(Bloco).first()
        if not bloco:
            logger.error("❌ Nenhum bloco encontrado no banco de dados")
            return
        
        logger.info(f"✓ Bloco encontrado: {bloco.titulo} (ID: {bloco.id})")
        
        # Testar verificação de usuário na blockchain
        logger.info("--- Testando verificação de usuário na blockchain ---")
        is_registered = blockchain_manager.is_user_registered_on_blockchain(usuario)
        logger.info(f"Usuário {usuario.nome} registrado na blockchain: {is_registered}")
        
        # Testar registro de usuário na blockchain
        logger.info("--- Testando registro de usuário na blockchain ---")
        result = blockchain_manager.register_user_on_blockchain(usuario)
        logger.info(f"Resultado do registro: {result}")
        
        # Testar verificação de bloco na blockchain
        logger.info("--- Testando verificação de bloco na blockchain ---")
        block_registered = blockchain_manager.is_block_registered_on_blockchain(bloco.id)
        logger.info(f"Bloco {bloco.titulo} registrado na blockchain: {block_registered}")
        
        # Testar registro de bloco na blockchain
        logger.info("--- Testando registro de bloco na blockchain ---")
        block_result = blockchain_manager.register_block_on_blockchain(bloco, usuario)
        logger.info(f"Resultado do registro do bloco: {block_result}")
        
        # Obter status geral da blockchain
        logger.info("--- Status geral da blockchain ---")
        status = blockchain_manager.get_blockchain_status()
        logger.info(f"Status da blockchain: {status}")
        
    except Exception as e:
        logger.error(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()
    
    logger.info("=== TESTE DE INTEGRAÇÃO BLOCKCHAIN FINALIZADO ===")

if __name__ == "__main__":
    test_blockchain_integration()