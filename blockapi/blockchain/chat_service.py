"""
Serviço para integrar blockchain com sistema de chat/vendas
"""
import logging
from typing import Dict, Any, Optional
from blockchain.blockchain_manager import blockchain_manager
from models.usuario import Usuario
from models.bloco import Bloco
from models.conversa import Conversa
from models.mensagem import Mensagem
from sqlalchemy.orm import Session
from datetime import datetime

logger = logging.getLogger(__name__)

class BlockchainChatService:
    """
    Serviço para gerenciar transações blockchain durante vendas no chat
    """
    
    @staticmethod
    def processar_venda_bloco(
        session: Session,
        conversa_id: int,
        vendedor_id: int,
        comprador_id: int,
        bloco_id: int,
        preco: float
    ) -> Dict[str, Any]:
        """
        Processa a venda de um bloco incluindo registro na blockchain
        """
        try:
            # Buscar dados necessários
            vendedor = session.query(Usuario).filter_by(id=vendedor_id).first()
            comprador = session.query(Usuario).filter_by(id=comprador_id).first()
            bloco = session.query(Bloco).filter_by(id=bloco_id).first()
            conversa = session.query(Conversa).filter_by(id=conversa_id).first()
            
            if not all([vendedor, comprador, bloco, conversa]):
                return {
                    'success': False,
                    'message': 'Dados incompletos para processar venda'
                }
            
            # Verificar se blockchain está conectado
            if not blockchain_manager.is_connected():
                logger.warning("Blockchain não conectado, processando venda sem blockchain")
                return {
                    'success': True,
                    'message': 'Venda processada sem blockchain (offline)',
                    'blockchain_enabled': False
                }
            
            # Processar transação blockchain
            blockchain_result = blockchain_manager.transfer_block_ownership(
                bloco=bloco,
                vendedor=vendedor,
                comprador=comprador
            )
            
            if blockchain_result['success']:
                # Criar mensagem de confirmação da transação
                mensagem_blockchain = Mensagem(
                    conversa_id=conversa_id,
                    usuario_id=None,  # Mensagem do sistema
                    conteudo=f"🔗 TRANSAÇÃO BLOCKCHAIN CONFIRMADA\n"
                             f"Bloco: {bloco.nome}\n"
                             f"Vendedor: {vendedor.nome}\n"
                             f"Comprador: {comprador.nome}\n"
                             f"Preço: R$ {preco:.2f}\n"
                             f"Hash: {blockchain_result.get('transaction_hash', 'N/A')}",
                    tipo='sistema_blockchain',
                    enviada_em=datetime.utcnow()
                )
                session.add(mensagem_blockchain)
                
                # Atualizar conversa
                conversa.ultima_atividade = datetime.utcnow()
                session.commit()
                
                logger.info(f"Venda processada com blockchain: {bloco.nome} de {vendedor.nome} para {comprador.nome}")
                
                return {
                    'success': True,
                    'message': 'Venda processada e registrada na blockchain',
                    'blockchain_enabled': True,
                    'transaction_hash': blockchain_result.get('transaction_hash'),
                    'block_uid': blockchain_result.get('block_uid')
                }
            else:
                # Falha na blockchain, mas continuar com venda local
                mensagem_erro = Mensagem(
                    conversa_id=conversa_id,
                    usuario_id=None,
                    conteudo=f"⚠️ AVISO: Venda processada localmente\n"
                             f"Erro blockchain: {blockchain_result.get('message')}\n"
                             f"A venda foi registrada no sistema local.",
                    tipo='sistema_aviso',
                    enviada_em=datetime.utcnow()
                )
                session.add(mensagem_erro)
                conversa.ultima_atividade = datetime.utcnow()
                session.commit()
                
                return {
                    'success': True,
                    'message': 'Venda processada localmente (erro na blockchain)',
                    'blockchain_enabled': False,
                    'blockchain_error': blockchain_result.get('message')
                }
                
        except Exception as e:
            logger.error(f"Erro ao processar venda: {e}")
            session.rollback()
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
    
    @staticmethod
    def verificar_usuarios_blockchain(vendedor: Usuario, comprador: Usuario) -> Dict[str, Any]:
        """
        Verifica se os usuários estão registrados na blockchain
        """
        if not blockchain_manager.is_connected():
            return {
                'vendedor_registrado': False,
                'comprador_registrado': False,
                'blockchain_disponivel': False,
                'message': 'Blockchain não disponível'
            }
        
        try:
            vendedor_registrado = blockchain_manager.is_user_registered_on_blockchain(vendedor)
            comprador_registrado = blockchain_manager.is_user_registered_on_blockchain(comprador)
            
            return {
                'vendedor_registrado': vendedor_registrado,
                'comprador_registrado': comprador_registrado,
                'blockchain_disponivel': True,
                'message': 'Verificação concluída'
            }
        except Exception as e:
            logger.error(f"Erro ao verificar usuários na blockchain: {e}")
            return {
                'vendedor_registrado': False,
                'comprador_registrado': False,
                'blockchain_disponivel': False,
                'message': f'Erro na verificação: {str(e)}'
            }
    
    @staticmethod
    def preparar_usuarios_blockchain(vendedor: Usuario, comprador: Usuario) -> Dict[str, Any]:
        """
        Prepara (registra se necessário) usuários na blockchain
        """
        if not blockchain_manager.is_connected():
            return {
                'success': False,
                'message': 'Blockchain não disponível'
            }
        
        try:
            resultados = {
                'vendedor': {'success': True, 'already_registered': True},
                'comprador': {'success': True, 'already_registered': True}
            }
            
            # Verificar e registrar vendedor
            if not blockchain_manager.is_user_registered_on_blockchain(vendedor):
                vendedor_result = blockchain_manager.register_user_on_blockchain(vendedor)
                resultados['vendedor'] = vendedor_result
            
            # Verificar e registrar comprador
            if not blockchain_manager.is_user_registered_on_blockchain(comprador):
                comprador_result = blockchain_manager.register_user_on_blockchain(comprador)
                resultados['comprador'] = comprador_result
            
            # Verificar se ambos foram registrados com sucesso
            vendedor_ok = resultados['vendedor']['success']
            comprador_ok = resultados['comprador']['success']
            
            if vendedor_ok and comprador_ok:
                return {
                    'success': True,
                    'message': 'Usuários preparados para transação blockchain',
                    'detalhes': resultados
                }
            else:
                return {
                    'success': False,
                    'message': 'Falha ao preparar usuários para blockchain',
                    'detalhes': resultados
                }
                
        except Exception as e:
            logger.error(f"Erro ao preparar usuários: {e}")
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
    
    @staticmethod
    def criar_mensagem_proposta_venda(
        session: Session,
        conversa_id: int,
        vendedor_id: int,
        bloco_id: int,
        preco: float
    ) -> Dict[str, Any]:
        """
        Cria uma mensagem de proposta de venda com verificação blockchain
        """
        try:
            vendedor = session.query(Usuario).filter_by(id=vendedor_id).first()
            bloco = session.query(Bloco).filter_by(id=bloco_id).first()
            
            if not vendedor or not bloco:
                return {
                    'success': False,
                    'message': 'Dados incompletos'
                }
            
            # Verificar status blockchain
            blockchain_info = ""
            if blockchain_manager.is_connected():
                if blockchain_manager.is_user_registered_on_blockchain(vendedor):
                    blockchain_info = "🔗 Vendedor registrado na blockchain"
                else:
                    blockchain_info = "⚠️ Vendedor será registrado na blockchain durante a venda"
            else:
                blockchain_info = "📱 Venda será processada localmente (blockchain offline)"
            
            # Criar mensagem de proposta
            conteudo_proposta = (
                f"💰 PROPOSTA DE VENDA\n"
                f"Bloco: {bloco.nome}\n"
                f"Material: {bloco.material or 'Não especificado'}\n"
                f"Dimensões: {bloco.largura or 0}x{bloco.altura or 0}x{bloco.profundidade or 0}\n"
                f"Preço: R$ {preco:.2f}\n\n"
                f"{blockchain_info}\n\n"
                f"Para aceitar, responda 'ACEITO'"
            )
            
            mensagem = Mensagem(
                conversa_id=conversa_id,
                usuario_id=vendedor_id,
                conteudo=conteudo_proposta,
                tipo='proposta_venda',
                enviada_em=datetime.utcnow(),
                metadata_json={
                    'bloco_id': bloco_id,
                    'preco': preco,
                    'blockchain_disponivel': blockchain_manager.is_connected()
                }
            )
            
            session.add(mensagem)
            session.commit()
            
            return {
                'success': True,
                'message': 'Proposta de venda criada',
                'mensagem_id': mensagem.id
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar proposta: {e}")
            session.rollback()
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
    
    @staticmethod
    def processar_aceitacao_proposta(
        session: Session,
        conversa_id: int,
        comprador_id: int,
        mensagem_proposta_id: int
    ) -> Dict[str, Any]:
        """
        Processa a aceitação de uma proposta de venda
        """
        try:
            # Buscar mensagem de proposta
            proposta = session.query(Mensagem).filter_by(
                id=mensagem_proposta_id,
                conversa_id=conversa_id,
                tipo='proposta_venda'
            ).first()
            
            if not proposta or not proposta.metadata_json:
                return {
                    'success': False,
                    'message': 'Proposta não encontrada'
                }
            
            bloco_id = proposta.metadata_json.get('bloco_id')
            preco = proposta.metadata_json.get('preco')
            vendedor_id = proposta.usuario_id
            
            if not all([bloco_id, preco, vendedor_id]):
                return {
                    'success': False,
                    'message': 'Dados da proposta incompletos'
                }
            
            # Processar venda
            resultado_venda = BlockchainChatService.processar_venda_bloco(
                session=session,
                conversa_id=conversa_id,
                vendedor_id=vendedor_id,
                comprador_id=comprador_id,
                bloco_id=bloco_id,
                preco=preco
            )
            
            # Criar mensagem de confirmação
            if resultado_venda['success']:
                mensagem_confirmacao = Mensagem(
                    conversa_id=conversa_id,
                    usuario_id=comprador_id,
                    conteudo="✅ PROPOSTA ACEITA! Venda confirmada.",
                    tipo='aceitacao_proposta',
                    enviada_em=datetime.utcnow()
                )
                session.add(mensagem_confirmacao)
                session.commit()
            
            return resultado_venda
            
        except Exception as e:
            logger.error(f"Erro ao processar aceitação: {e}")
            session.rollback()
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }

# Instância do serviço
blockchain_chat_service = BlockchainChatService()
