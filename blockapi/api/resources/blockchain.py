"""
Recursos da API para operações blockchain
"""
from flask import request, jsonify
from flask_restful import Resource
from models.extensions import verificar_jwt
from models.usuario import Usuario
from models.bloco import Bloco
from models.conversa import Conversa
from blockchain.blockchain_manager import blockchain_manager
from blockchain.chat_service import blockchain_chat_service
from sqlalchemy.orm import sessionmaker
from models.extensions import engine
import logging

logger = logging.getLogger(__name__)
Session = sessionmaker(bind=engine)

class BlockchainStatus(Resource):
    """
    Endpoint para verificar status da blockchain
    """
    
    def get(self):
        """
        GET /api/blockchain/status
        Retorna o status atual da blockchain
        """
        try:
            status = blockchain_manager.get_blockchain_status()
            return jsonify(status)
        except Exception as e:
            logger.error(f"Erro ao obter status da blockchain: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainUserRegister(Resource):
    """
    Endpoint para registrar usuário na blockchain
    """
    
    def post(self):
        """
        POST /api/blockchain/user/register
        Registra o usuário atual na blockchain
        """
        try:
            # Verificar autenticação
            auth_result = verificar_jwt()
            if auth_result.get('code', 401) != 200:
                return jsonify({
                    'success': False,
                    'message': auth_result.get('message', 'Token inválido')
                }), auth_result.get('code', 401)
            
            user_id = auth_result['message']
            session = Session()
            
            try:
                # Buscar usuário
                usuario = session.query(Usuario).filter_by(id=user_id).first()
                if not usuario:
                    return jsonify({
                        'success': False,
                        'message': 'Usuário não encontrado'
                    }), 404
                
                # Registrar na blockchain
                result = blockchain_manager.register_user_on_blockchain(usuario)
                
                return jsonify(result)
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao registrar usuário na blockchain: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainUserCheck(Resource):
    """
    Endpoint para verificar se usuário está registrado na blockchain
    """
    
    def get(self, user_id=None):
        """
        GET /api/blockchain/user/check[/<user_id>]
        Verifica se usuário está registrado na blockchain
        """
        try:
            # Se não especificado user_id, usar usuário atual
            if user_id is None:
                auth_result = verificar_jwt()
                if auth_result.get('code', 401) != 200:
                    return jsonify({
                        'success': False,
                        'message': auth_result.get('message', 'Token inválido')
                    }), auth_result.get('code', 401)
                user_id = auth_result['message']
            
            session = Session()
            
            try:
                usuario = session.query(Usuario).filter_by(id=user_id).first()
                if not usuario:
                    return jsonify({
                        'success': False,
                        'message': 'Usuário não encontrado'
                    }), 404
                
                is_registered = blockchain_manager.is_user_registered_on_blockchain(usuario)
                
                return jsonify({
                    'success': True,
                    'user_id': user_id,
                    'registered_on_blockchain': is_registered,
                    'blockchain_connected': blockchain_manager.is_connected()
                })
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao verificar usuário na blockchain: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainSaleProposal(Resource):
    """
    Endpoint para criar proposta de venda com blockchain
    """
    
    def post(self):
        """
        POST /api/blockchain/sale/proposal
        Cria uma proposta de venda
        Body: {
            "conversa_id": int,
            "bloco_id": int,
            "preco": float
        }
        """
        try:
            # Verificar autenticação
            auth_result = verificar_jwt()
            if auth_result.get('code', 401) != 200:
                return jsonify({
                    'success': False,
                    'message': auth_result.get('message', 'Token inválido')
                }), auth_result.get('code', 401)
            
            user_id = auth_result['message']
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados JSON necessários'
                }), 400
            
            conversa_id = data.get('conversa_id')
            bloco_id = data.get('bloco_id')
            preco = data.get('preco')
            
            if not all([conversa_id, bloco_id, preco]):
                return jsonify({
                    'success': False,
                    'message': 'Campos obrigatórios: conversa_id, bloco_id, preco'
                }), 400
            
            session = Session()
            
            try:
                # Verificar se usuário é participante da conversa
                conversa = session.query(Conversa).filter_by(id=conversa_id).first()
                if not conversa or user_id not in [conversa.usuario1_id, conversa.usuario2_id]:
                    return jsonify({
                        'success': False,
                        'message': 'Acesso negado à conversa'
                    }), 403
                
                # Criar proposta
                result = blockchain_chat_service.criar_mensagem_proposta_venda(
                    session=session,
                    conversa_id=conversa_id,
                    vendedor_id=user_id,
                    bloco_id=bloco_id,
                    preco=float(preco)
                )
                
                return jsonify(result)
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao criar proposta de venda: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainSaleAccept(Resource):
    """
    Endpoint para aceitar proposta de venda
    """
    
    def post(self):
        """
        POST /api/blockchain/sale/accept
        Aceita uma proposta de venda
        Body: {
            "conversa_id": int,
            "mensagem_proposta_id": int
        }
        """
        try:
            # Verificar autenticação
            auth_result = verificar_jwt()
            if auth_result.get('code', 401) != 200:
                return jsonify({
                    'success': False,
                    'message': auth_result.get('message', 'Token inválido')
                }), auth_result.get('code', 401)
            
            user_id = auth_result['message']
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados JSON necessários'
                }), 400
            
            conversa_id = data.get('conversa_id')
            mensagem_proposta_id = data.get('mensagem_proposta_id')
            
            if not all([conversa_id, mensagem_proposta_id]):
                return jsonify({
                    'success': False,
                    'message': 'Campos obrigatórios: conversa_id, mensagem_proposta_id'
                }), 400
            
            session = Session()
            
            try:
                # Verificar acesso à conversa
                conversa = session.query(Conversa).filter_by(id=conversa_id).first()
                if not conversa or user_id not in [conversa.usuario1_id, conversa.usuario2_id]:
                    return jsonify({
                        'success': False,
                        'message': 'Acesso negado à conversa'
                    }), 403
                
                # Processar aceitação
                result = blockchain_chat_service.processar_aceitacao_proposta(
                    session=session,
                    conversa_id=conversa_id,
                    comprador_id=user_id,
                    mensagem_proposta_id=mensagem_proposta_id
                )
                
                return jsonify(result)
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao aceitar proposta: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainTransferCheck(Resource):
    """
    Endpoint para verificar se usuários estão preparados para transação
    """
    
    def post(self):
        """
        POST /api/blockchain/transfer/check
        Verifica se vendedor e comprador estão preparados para transação
        Body: {
            "vendedor_id": int,
            "comprador_id": int
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados JSON necessários'
                }), 400
            
            vendedor_id = data.get('vendedor_id')
            comprador_id = data.get('comprador_id')
            
            if not all([vendedor_id, comprador_id]):
                return jsonify({
                    'success': False,
                    'message': 'Campos obrigatórios: vendedor_id, comprador_id'
                }), 400
            
            session = Session()
            
            try:
                vendedor = session.query(Usuario).filter_by(id=vendedor_id).first()
                comprador = session.query(Usuario).filter_by(id=comprador_id).first()
                
                if not vendedor or not comprador:
                    return jsonify({
                        'success': False,
                        'message': 'Usuários não encontrados'
                    }), 404
                
                result = blockchain_chat_service.verificar_usuarios_blockchain(vendedor, comprador)
                
                return jsonify(result)
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro ao verificar usuários: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

class BlockchainContractInfo(Resource):
    """
    Endpoint para obter informações do contrato
    """
    
    def get(self):
        """
        GET /api/blockchain/contract
        Retorna informações do contrato inteligente
        """
        try:
            contract_info = blockchain_manager.get_contract_info()
            status = blockchain_manager.get_blockchain_status()
            
            result = {
                **contract_info,
                'blockchain_connected': blockchain_manager.is_connected(),
                'wallet_address': status.get('wallet_address'),
                'account_balance': status.get('account_balance') if blockchain_manager.is_connected() else None
            }
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"Erro ao obter informações do contrato: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500
