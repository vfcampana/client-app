"""
Módulo para gerenciar transações blockchain usando SCManager
"""
import os
import sys
import logging
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Adicionar o path do SCManager
scmanager_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'SCManager-master', 'SCManager-master', 'src')
if scmanager_path not in sys.path:
    sys.path.insert(0, scmanager_path)

from scmanager import SCManager
from scmanager import admin_tools as adm
from models.usuario import Usuario
from models.bloco import Bloco
from sqlalchemy.orm import Session

# Carrega o .env da raiz do projeto (dois níveis acima - sai de blockchain/ e blockapi/)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlockchainManager:
    """
    Classe para gerenciar interações com blockchain através do SCManager
    """
    
    def __init__(self):
        """
        Inicializa o BlockchainManager
        """
        self.scm: Optional[SCManager] = None
        self._initialize_blockchain()
    
    def _initialize_blockchain(self):
        """
        Inicializa a conexão com blockchain
        """
        try:
            # Verificar variáveis de ambiente primeiro
            private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
            endpoint = os.getenv('ETHEREUM_ENDPOINT')
            
            if not private_key or not endpoint:
                logger.error("Variáveis de ambiente ETHEREUM_PRIVATE_KEY ou ETHEREUM_ENDPOINT não encontradas")
                self.scm = None
                return
            
            logger.info(f"Conectando à rede: {endpoint}")
            logger.info(f"Endereço da carteira: {self._get_wallet_address_from_private_key(private_key)}")
                
            # Verificar se arquivo de configuração existe
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scm_config", "scm_config.json")
            if not os.path.exists(config_path):
                logger.info("Arquivo de configuração não encontrado. Criando novo contrato...")
                try:
                    self._deploy_contract()
                except Exception as deploy_error:
                    logger.error(f"Erro no deploy do contrato: {deploy_error}")
                    logger.error(f"Tipo do erro: {type(deploy_error).__name__}")
                    import traceback
                    traceback.print_exc()
                    logger.info("Modo offline ativado - blockchain não disponível")
                    self.scm = None
                    return
            
            # Inicializar SCManager
            logger.info("Inicializando SCManager...")
            self.scm = SCManager()
            logger.info("BlockchainManager inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar blockchain: {e}")
            logger.error(f"Tipo do erro: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            logger.info("Modo offline ativado - blockchain não disponível")
            self.scm = None
    
    def _get_wallet_address_from_private_key(self, private_key: str) -> str:
        """
        Obtém o endereço da carteira a partir da chave privada
        """
        try:
            from eth_account import Account
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            logger.error(f"Erro ao obter endereço da carteira: {e}")
            return "Endereço inválido"
    
    def _deploy_contract(self):
        """
        Faz deploy do contrato inteligente
        """
        try:
            # Mudar para o diretório raiz do projeto antes de criar o config
            original_cwd = os.getcwd()
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            os.chdir(project_root)
            
            # Criar arquivo de configuração e fazer deploy
            adm.create_config_file()
            logger.info("Contrato inteligente implantado com sucesso")
            
            # Voltar ao diretório original
            os.chdir(original_cwd)
        except Exception as e:
            logger.error(f"Erro ao fazer deploy do contrato: {e}")
            # Garantir que volta ao diretório original mesmo em caso de erro
            try:
                os.chdir(original_cwd)
            except:
                pass
            raise
    
    def is_connected(self) -> bool:
        """
        Verifica se a conexão com blockchain está ativa
        """
        return self.scm is not None
    
    def get_account_balance(self) -> float:
        """
        Obtém o saldo da conta
        """
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        try:
            return self.scm.get_account_balance()
        except Exception as e:
            logger.error(f"Erro ao obter saldo da conta: {e}")
            raise
    
    def is_user_registered_on_blockchain(self, usuario: Usuario) -> bool:
        """
        Verifica se um usuário já está registrado na blockchain
        """
        if not self.is_connected():
            return False
        
        try:
            # Buscar usuários existentes na blockchain
            users_list = self.scm.get_user_uids_list()
            
            # Verificar se existe usuário com mesmo email ou documento
            for user_uid in users_list:
                user_data = self.scm.get_user_data(user_uid)
                if (user_data.get('email') == usuario.email or 
                    user_data.get('cnpj') == usuario.documento):
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar usuário na blockchain: {e}")
            return False
    
    def register_user_on_blockchain(self, usuario: Usuario) -> Dict[str, Any]:
        """
        Registra um usuário na blockchain
        """
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        try:
            # Verificar se usuário já está registrado
            if self.is_user_registered_on_blockchain(usuario):
                return {
                    'success': True,
                    'message': 'Usuário já está registrado na blockchain',
                    'already_registered': True
                }
            
            # Preparar dados do usuário
            user_names = [usuario.nome]
            user_cnpjs = [usuario.documento]
            user_emails = [usuario.email]
            
            # Registrar na blockchain
            result = self.scm.add_new_users(
                user_name_list=user_names,
                user_cnpj_list=user_cnpjs,
                user_email_address_list=user_emails
            )
            
            logger.info(f"Usuário {usuario.nome} registrado na blockchain com sucesso")
            
            # Verificar se result é uma tupla ou dict
            if isinstance(result, tuple):
                actual_result = result[0] if result else {}
            else:
                actual_result = result or {}
            
            return {
                'success': True,
                'message': 'Usuário registrado na blockchain com sucesso',
                'transaction_hash': actual_result.get('transaction_hash') if isinstance(actual_result, dict) else None,
                'user_uid': actual_result.get('user_uids', [None])[0] if isinstance(actual_result, dict) and actual_result.get('user_uids') else None,
                'already_registered': False
            }
            
        except Exception as e:
            logger.error(f"Erro ao registrar usuário na blockchain: {e}")
            return {
                'success': False,
                'message': f'Erro ao registrar usuário: {str(e)}',
                'already_registered': False
            }
    
    def register_block_on_blockchain(self, bloco: Bloco, proprietario: Usuario) -> Dict[str, Any]:
        """
        Registra um bloco ornamental na blockchain
        """
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        try:
            # Primeiro, garantir que o proprietário está registrado
            user_result = self.register_user_on_blockchain(proprietario)
            if not user_result['success'] and not user_result.get('already_registered'):
                return {
                    'success': False,
                    'message': 'Falha ao registrar proprietário na blockchain'
                }
            
            # Obter UID do usuário na blockchain
            user_uid = self._get_user_uid_by_email(proprietario.email)
            if not user_uid:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado na blockchain'
                }
            
            # Preparar dados do bloco
            block_names = [bloco.nome]
            block_materials = [bloco.material or "Não especificado"]
            block_colors = [bloco.cor or "Não especificado"]
            block_dimensions = [f"{bloco.largura or 0}x{bloco.altura or 0}x{bloco.profundidade or 0}"]
            block_weights = [float(bloco.peso) if bloco.peso else 0.0]
            block_owner_uids = [user_uid]
            
            # Preparar dados do bloco no formato correto para o SCManager
            mining_data_list = [{
                'company': proprietario.nome,
                'mining_date': datetime.now().strftime('%Y-%m-%d'),
                'mining_site': 'local não especificado'
            }]
            
            code_list = [f"BLK-{bloco.id}"]
            
            properties_list = [{
                'material': bloco.material or 'Não especificado',
                'dimensions': f"{bloco.largura or 0}x{bloco.altura or 0}x{bloco.profundidade or 0} mm",
                'weight': f"{bloco.peso or 0} kg"
            }]
            
            hash_list = [f"hash-{bloco.id}-{datetime.now().timestamp()}"]
            owners_uid_list = [user_uid]
            
            # Registrar bloco na blockchain
            result_tuple = self.scm.add_new_ornamental_blocks(
                mining_data_list=mining_data_list,
                code_list=code_list,
                properties_list=properties_list,
                hash_list=hash_list,
                owners_uid_list=owners_uid_list
            )
            
            new_blocks_data, transactions = result_tuple
            result = {
                'ornamental_blocks': new_blocks_data,
                'transactions': transactions,
                'transaction_hash': transactions[0].get('transaction_hash') if transactions else None
            }
            
            logger.info(f"Bloco {bloco.nome} registrado na blockchain com sucesso")
            
            # Extrair o UID do bloco criado
            block_uid = new_blocks_data[0]['uid'] if new_blocks_data else None
            
            return {
                'success': True,
                'message': 'Bloco registrado na blockchain com sucesso',
                'transaction_hash': result.get('transaction_hash'),
                'block_uid': block_uid
            }
            
        except Exception as e:
            logger.error(f"Erro ao registrar bloco na blockchain: {e}")
            return {
                'success': False,
                'message': f'Erro ao registrar bloco: {str(e)}'
            }
    
    def transfer_block_ownership(self, bloco: Bloco, vendedor: Usuario, comprador: Usuario) -> Dict[str, Any]:
        """
        Transfere a propriedade de um bloco entre usuários na blockchain
        """
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        try:
            # Garantir que ambos os usuários estejam registrados
            vendedor_result = self.register_user_on_blockchain(vendedor)
            comprador_result = self.register_user_on_blockchain(comprador)
            
            if not vendedor_result['success'] and not vendedor_result.get('already_registered'):
                return {
                    'success': False,
                    'message': 'Falha ao registrar vendedor na blockchain'
                }
            
            if not comprador_result['success'] and not comprador_result.get('already_registered'):
                return {
                    'success': False,
                    'message': 'Falha ao registrar comprador na blockchain'
                }
            
            # Obter UIDs dos usuários
            vendedor_uid = self._get_user_uid_by_email(vendedor.email)
            comprador_uid = self._get_user_uid_by_email(comprador.email)
            
            if not vendedor_uid or not comprador_uid:
                return {
                    'success': False,
                    'message': 'Usuários não encontrados na blockchain'
                }
            
            # Buscar UID do bloco na blockchain
            block_uid = self._get_block_uid_by_name(bloco.nome)
            if not block_uid:
                # Se o bloco não existe, registrá-lo primeiro
                block_result = self.register_block_on_blockchain(bloco, vendedor)
                if not block_result['success']:
                    return block_result
                block_uid = block_result['block_uid']
            
            # Transferir propriedade usando a função correta do SCManager
            invoice_number = f"INV-{datetime.now().timestamp()}"
            
            result_tuple = self.scm.transfer_ornamental_blocks(
                ornamental_block_uid_list=[block_uid],
                new_owner_uid_list=[comprador_uid],
                invoice_number_list=[invoice_number]
            )
            
            # O resultado é uma tupla (transferred_blocks_data_list, transactions_list)
            transferred_blocks_data, transactions = result_tuple
            result = {
                'transferred_blocks': transferred_blocks_data,
                'transactions': transactions,
                'transaction_hash': transactions[0].get('transaction_hash') if transactions else None
            }
            
            logger.info(f"Propriedade do bloco {bloco.nome} transferida de {vendedor.nome} para {comprador.nome}")
            
            return {
                'success': True,
                'message': 'Propriedade transferida com sucesso',
                'transaction_hash': result.get('transaction_hash'),
                'block_uid': block_uid,
                'vendedor_uid': vendedor_uid,
                'comprador_uid': comprador_uid
            }
            
        except Exception as e:
            logger.error(f"Erro ao transferir propriedade: {e}")
            return {
                'success': False,
                'message': f'Erro ao transferir propriedade: {str(e)}'
            }
    
    def _get_user_uid_by_email(self, email: str) -> Optional[str]:
        """
        Busca UID de usuário por email
        """
        try:
            users_list = self.scm.get_user_uids_list()
            
            for user_uid in users_list:
                try:
                    user_data = self.scm.get_user_data(user_uid)
                    
                    # Verificar diferentes formatos de retorno
                    user_email = None
                    if isinstance(user_data, dict):
                        user_email = user_data.get('email') or user_data.get('email_address')
                    elif isinstance(user_data, tuple) and len(user_data) > 6:
                        user_email = user_data[6]
                    
                    if user_email == email:
                        return user_uid
                        
                except Exception as user_error:
                    logger.error(f"Erro ao verificar usuário {user_uid}: {user_error}")
                    continue
                    
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email: {e}")
            return None
    
    def _get_block_uid_by_name(self, nome: str) -> Optional[str]:
        """
        Busca UID de bloco por nome
        """
        try:
            blocks_list = self.scm.get_ornamental_block_uids_list()
            
            for block_uid in blocks_list:
                try:
                    block_data = self.scm.get_ornamental_block_data(block_uid)
                    
                    # O nome pode estar em diferentes campos dependendo da implementação
                    block_name = None
                    if isinstance(block_data, dict):
                        block_name = block_data.get('name') or block_data.get('code') or block_data.get('mining_data')
                    elif isinstance(block_data, tuple) and len(block_data) > 5:
                        block_name = block_data[5]  # code field
                    
                    # Verificar se o nome/código contém o título do bloco
                    if block_name and (nome in str(block_name) or f"BLK-{nome}" in str(block_name)):
                        return block_uid
                        
                except Exception as block_error:
                    logger.error(f"Erro ao verificar bloco {block_uid}: {block_error}")
                    continue
                    
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar bloco por nome: {e}")
            return None
    
    def get_blockchain_status(self) -> Dict[str, Any]:
        """
        Obtém status geral da blockchain
        """
        if not self.is_connected():
            return {
                'connected': False,
                'message': 'Blockchain não conectado',
                'contract_address': self.get_contract_address(),
                'network': os.getenv('ETHEREUM_ENDPOINT')
            }
        
        try:
            balance = self.scm.get_account_balance()
            users_count = len(self.scm.get_user_uids_list())
            blocks_count = len(self.scm.get_ornamental_block_uids_list())
            last_update = self.scm.get_last_updated_timestamp()
            contract_info = self.get_contract_info()
            
            return {
                'connected': True,
                'account_balance': balance,
                'total_users': users_count,
                'total_blocks': blocks_count,
                'last_update': last_update,
                'contract_address': contract_info.get('contract_address'),
                'deployer': contract_info.get('deployer'),
                'network': contract_info.get('network'),
                'wallet_address': self._get_wallet_address_from_private_key(os.getenv('ETHEREUM_PRIVATE_KEY', '')),
                'message': 'Blockchain conectado e funcionando'
            }
        except Exception as e:
            logger.error(f"Erro ao obter status da blockchain: {e}")
            return {
                'connected': False,
                'message': f'Erro ao obter status: {str(e)}',
                'contract_address': self.get_contract_address(),
                'network': os.getenv('ETHEREUM_ENDPOINT')
            }
    
    def get_contract_address(self) -> Optional[str]:
        """
        Obtém o endereço do contrato inteligente
        """
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scm_config", "scm_config.json")
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                contract_info = config.get('contract', {})
                return contract_info.get('address')
            
            return None
        except Exception as e:
            logger.error(f"Erro ao obter endereço do contrato: {e}")
            return None
    
    def get_contract_info(self) -> Dict[str, Any]:
        """
        Obtém informações do contrato inteligente
        """
        try:
            import json
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scm_config", "scm_config.json")
            
            if not os.path.exists(config_path):
                return {
                    'success': False,
                    'message': 'Arquivo de configuração não encontrado',
                    'contract_address': None,
                    'deployer_address': None
                }
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            contract_info = config.get('contract', {})
            
            return {
                'success': True,
                'contract_address': contract_info.get('address', 'N/A'),
                'deployer_address': config.get('deployer', 'N/A'),
                'network_endpoint': os.getenv('ETHEREUM_ENDPOINT', 'N/A'),
                'wallet_address': self._get_wallet_address_from_private_key(os.getenv('ETHEREUM_PRIVATE_KEY', '')),
                'config_file': config_path
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do contrato: {e}")
            return {
                'success': False,
                'message': f'Erro ao ler configuração: {str(e)}',
                'contract_address': None,
                'deployer_address': None
            }

    def processar_venda(self, vendedor_id: int, comprador_id: int, bloco_id: int, valor: float) -> Dict[str, Any]:
        """
        Processa a venda de um bloco ornamental na blockchain
        """
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        try:
            from models.database import Session as SessionDB
            from models.usuario import Usuario
            from models.bloco import Bloco
            
            session = SessionDB()
            
            try:
                # Buscar dados dos usuários e bloco
                vendedor = session.query(Usuario).filter_by(id=vendedor_id).first()
                comprador = session.query(Usuario).filter_by(id=comprador_id).first()
                bloco = session.query(Bloco).filter_by(id=bloco_id).first()
                
                if not vendedor or not comprador or not bloco:
                    return {
                        'success': False,
                        'error': 'Dados não encontrados no banco de dados'
                    }
                
                # Registrar usuários na blockchain se necessário
                vendedor_result = self.register_user_on_blockchain(vendedor)
                comprador_result = self.register_user_on_blockchain(comprador)
                
                if not vendedor_result['success'] and not vendedor_result.get('already_registered'):
                    return {
                        'success': False,
                        'error': f'Falha ao registrar vendedor na blockchain: {vendedor_result.get("message")}'
                    }
                
                if not comprador_result['success'] and not comprador_result.get('already_registered'):
                    return {
                        'success': False,
                        'error': f'Falha ao registrar comprador na blockchain: {comprador_result.get("message")}'
                    }
                
                # Obter UIDs dos usuários na blockchain
                vendedor_uid = self._get_user_uid_by_email(vendedor.email)
                comprador_uid = self._get_user_uid_by_email(comprador.email)
                
                if not vendedor_uid or not comprador_uid:
                    return {
                        'success': False,
                        'error': 'UIDs dos usuários não encontrados na blockchain'
                    }
                
                # Verificar se o bloco já está registrado na blockchain
                block_uid = self._get_block_uid_by_name(bloco.titulo)
                
                if not block_uid:
                    # Registrar bloco na blockchain primeiro
                    block_result = self.register_block_on_blockchain(bloco, vendedor)
                    if not block_result['success']:
                        return {
                            'success': False,
                            'error': f'Falha ao registrar bloco na blockchain: {block_result.get("message")}'
                        }
                    block_uid = block_result['block_uid']
                
                # Transferir propriedade na blockchain
                invoice_number = f"INV-{bloco_id}-{vendedor_id}-{comprador_id}-{int(datetime.now().timestamp())}"
                
                result_tuple = self.scm.transfer_ornamental_blocks(
                    ornamental_block_uid_list=[block_uid],
                    new_owner_uid_list=[comprador_uid],
                    invoice_number_list=[invoice_number]
                )
                
                transferred_blocks_data, transactions = result_tuple
                
                return {
                    'success': True,
                    'message': 'Venda processada com sucesso na blockchain',
                    'transaction_hash': transactions[0].get('transaction_hash') if transactions else None,
                    'block_uid': block_uid,
                    'vendedor_uid': vendedor_uid,
                    'comprador_uid': comprador_uid,
                    'invoice_number': invoice_number,
                    'valor': valor
                }
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao processar venda na blockchain: {e}")
            return {
                'success': False,
                'error': f'Erro na transação blockchain: {str(e)}'
            }

# Instância global do gerenciador
blockchain_manager = BlockchainManager()
