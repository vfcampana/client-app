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

class BlockchainSale(Resource):
    """
    Endpoint para realizar venda completa com integração blockchain
    """
    
    def post(self):
        """
        POST /api/blockchain/vendas
        Realiza uma venda com integração blockchain automática
        
        Fluxo implementado:
        1. Verifica se vendedor está cadastrado na blockchain (cadastra se necessário)
        2. Verifica se comprador está cadastrado na blockchain (cadastra se necessário)  
        3. Verifica se bloco está cadastrado na blockchain (cadastra se necessário)
        4. Executa a transferência de propriedade na blockchain
        5. Atualiza propriedade no banco de dados
        
        Body: {
            "bloco_id": int,
            "comprador_id": int,
            "comprador_wallet_address": str,
            "valor": float,
            "observacoes": str (opcional)
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
            
            # Validar dados obrigatórios
            required_fields = ['bloco_id', 'comprador_id', 'comprador_wallet_address', 'valor']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'success': False,
                        'message': f'Campo obrigatório: {field}'
                    }), 400
            
            session = Session()
            
            try:
                # Buscar vendedor (usuário logado)
                vendedor = session.query(Usuario).filter_by(id=user_id).first()
                if not vendedor:
                    return jsonify({
                        'success': False,
                        'message': 'Vendedor não encontrado'
                    }), 404
                
                # Buscar comprador
                comprador = session.query(Usuario).filter_by(id=data['comprador_id']).first()
                if not comprador:
                    return jsonify({
                        'success': False,
                        'message': 'Comprador não encontrado'
                    }), 404
                
                # Buscar bloco
                bloco = session.query(Bloco).filter_by(id=data['bloco_id']).first()
                if not bloco:
                    return jsonify({
                        'success': False,
                        'message': 'Bloco não encontrado'
                    }), 404
                
                # Verificar se vendedor é o proprietário do bloco
                if bloco.usuario_id != user_id:
                    return jsonify({
                        'success': False,
                        'message': 'Usuário não é proprietário do bloco'
                    }), 403
                
                # Atualizar wallet address do comprador se fornecido
                comprador_wallet = data['comprador_wallet_address']
                if comprador.wallet_address != comprador_wallet:
                    comprador.wallet_address = comprador_wallet
                    session.commit()
                
                # Executar processo blockchain
                resultado_blockchain = self._processar_venda_blockchain(
                    session, vendedor, comprador, bloco, data.get('valor', 0)
                )
                
                if not resultado_blockchain['success']:
                    return jsonify(resultado_blockchain), 400
                
                # Atualizar propriedade do bloco no banco
                bloco.usuario_id = comprador.id
                session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Venda realizada com sucesso',
                    'data': {
                        'bloco_id': bloco.id,
                        'vendedor_id': vendedor.id,
                        'comprador_id': comprador.id,
                        'valor': data.get('valor', 0),
                        'blockchain_data': resultado_blockchain['data']
                    }
                })
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Erro na venda blockchain: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500
    
    def _processar_venda_blockchain(self, session, vendedor: Usuario, comprador: Usuario, bloco: Bloco, valor: float):
        """
        Processa a venda na blockchain seguindo o fluxo completo
        """
        try:
            resultado = {
                'success': True,
                'message': 'Venda processada com sucesso na blockchain',
                'data': {
                    'steps': [],
                    'blockchain_available': blockchain_manager.is_blockchain_available()
                }
            }
            
            # PASSO 1: Verificar/cadastrar vendedor na blockchain
            if not vendedor.wallet_address:
                return {
                    'success': False,
                    'message': 'Vendedor deve ter um endereço de carteira válido'
                }
            
            vendedor_registrado = blockchain_manager.is_user_registered_on_blockchain(vendedor)
            if not vendedor_registrado:
                logger.info(f"Cadastrando vendedor {vendedor.id} na blockchain...")
                registro_vendedor = blockchain_manager.register_user_on_blockchain(vendedor)
                resultado['data']['steps'].append({
                    'step': 'register_seller',
                    'success': registro_vendedor['success'],
                    'message': registro_vendedor['message']
                })
                
                if not registro_vendedor['success']:
                    resultado['success'] = False
                    resultado['message'] = f"Erro ao cadastrar vendedor: {registro_vendedor['message']}"
                    return resultado
            else:
                resultado['data']['steps'].append({
                    'step': 'verify_seller',
                    'success': True,
                    'message': 'Vendedor já cadastrado na blockchain'
                })
            
            # PASSO 2: Verificar/cadastrar comprador na blockchain
            if not comprador.wallet_address:
                return {
                    'success': False,
                    'message': 'Comprador deve ter um endereço de carteira válido'
                }
            
            comprador_registrado = blockchain_manager.is_user_registered_on_blockchain(comprador)
            if not comprador_registrado:
                logger.info(f"Cadastrando comprador {comprador.id} na blockchain...")
                registro_comprador = blockchain_manager.register_user_on_blockchain(comprador)
                resultado['data']['steps'].append({
                    'step': 'register_buyer',
                    'success': registro_comprador['success'],
                    'message': registro_comprador['message']
                })
                
                if not registro_comprador['success']:
                    resultado['success'] = False
                    resultado['message'] = f"Erro ao cadastrar comprador: {registro_comprador['message']}"
                    return resultado
            else:
                resultado['data']['steps'].append({
                    'step': 'verify_buyer',
                    'success': True,
                    'message': 'Comprador já cadastrado na blockchain'
                })
            
            # PASSO 3: Verificar/cadastrar bloco na blockchain
            bloco_registrado = blockchain_manager.is_block_registered_on_blockchain(bloco.id)
            if not bloco_registrado:
                logger.info(f"Cadastrando bloco {bloco.id} na blockchain...")
                registro_bloco = blockchain_manager.register_block_on_blockchain(bloco, vendedor)
                resultado['data']['steps'].append({
                    'step': 'register_block',
                    'success': registro_bloco['success'],
                    'message': registro_bloco['message']
                })
                
                if not registro_bloco['success']:
                    resultado['success'] = False
                    resultado['message'] = f"Erro ao cadastrar bloco: {registro_bloco['message']}"
                    return resultado
            else:
                resultado['data']['steps'].append({
                    'step': 'verify_block',
                    'success': True,
                    'message': 'Bloco já cadastrado na blockchain'
                })
            
            # PASSO 4: Transferir propriedade do bloco
            logger.info(f"Transferindo propriedade do bloco {bloco.id} de {vendedor.id} para {comprador.id}...")
            transferencia = blockchain_manager.transfer_block_ownership(bloco, vendedor, comprador)
            resultado['data']['steps'].append({
                'step': 'transfer_ownership',
                'success': transferencia['success'],
                'message': transferencia['message'],
                'data': transferencia.get('data')
            })
            
            if not transferencia['success']:
                resultado['success'] = False
                resultado['message'] = f"Erro na transferência: {transferencia['message']}"
                return resultado
            
            # PASSO 5: Finalizar processo
            resultado['data']['steps'].append({
                'step': 'finalize',
                'success': True,
                'message': 'Venda blockchain finalizada com sucesso',
                'transaction_details': {
                    'valor': valor,
                    'block_id': bloco.id,
                    'from_user': vendedor.id,
                    'to_user': comprador.id
                }
            })
            
            logger.info(f"Venda blockchain finalizada: bloco {bloco.id}, vendedor {vendedor.id}, comprador {comprador.id}")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro no processamento blockchain: {e}")
            return {
                'success': False,
                'message': f'Erro no processamento blockchain: {str(e)}'
            }
