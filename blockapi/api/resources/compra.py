from flask_restful import Resource
from flask import request, jsonify
from models.database import Session
from models.bloco import Bloco
from models.usuario import Usuario
from api.resources.usuario import verificar_jwt
from datetime import datetime


class ComprarBloco(Resource):
    def post(self):
        """Comprar um bloco diretamente via blockchain"""
        try:
            # Verificar autenticação
            id_usuario = verificar_jwt()
            
            if id_usuario.get('code', 401) != 200 or not id_usuario.get('message'):
                response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
                response.status_code = id_usuario.get('code', 401)
                return response
            
            comprador_id = str(id_usuario['message'])
            data = request.get_json()
            
            bloco_id = data.get('bloco_id')
            valor_ofertado = data.get('valor')
            
            if not bloco_id or not valor_ofertado:
                response = jsonify({'message': 'bloco_id e valor são obrigatórios'})
                response.status_code = 400
                return response
            
            session = Session()
            
            try:
                # Buscar o bloco
                bloco = session.query(Bloco).filter_by(id=bloco_id).first()
                if not bloco:
                    response = jsonify({'message': 'Bloco não encontrado'})
                    response.status_code = 404
                    return response
                
                # Verificar se o bloco está à venda
                if bloco.status != "1":
                    response = jsonify({'message': 'Este bloco não está disponível para venda'})
                    response.status_code = 400
                    return response
                
                # Verificar se não é o próprio dono
                if str(bloco.id_usuario) == comprador_id:
                    response = jsonify({'message': 'Você não pode comprar seu próprio bloco'})
                    response.status_code = 400
                    return response
                
                # Buscar dados do vendedor e comprador
                vendedor = session.query(Usuario).filter_by(id=bloco.id_usuario).first()
                comprador = session.query(Usuario).filter_by(id=comprador_id).first()
                
                if not vendedor or not comprador:
                    response = jsonify({'message': 'Usuário não encontrado'})
                    response.status_code = 404
                    return response
                
                # Processar venda via blockchain
                try:
                    from blockchain.blockchain_manager import blockchain_manager
                    
                    # Executar transação blockchain
                    resultado_blockchain = blockchain_manager.processar_venda(
                        vendedor_id=int(bloco.id_usuario),
                        comprador_id=int(comprador_id),
                        bloco_id=bloco.id,
                        valor=float(valor_ofertado)
                    )
                    
                    if resultado_blockchain['success']:
                        # Atualizar proprietário do bloco
                        bloco.id_usuario = int(comprador_id)
                        bloco.status = "0"  # Marcar como vendido
                        session.commit()
                        
                        response = jsonify({
                            'success': True,
                            'message': 'Compra realizada com sucesso!',
                            'transaction_hash': resultado_blockchain.get('transaction_hash'),
                            'bloco': {
                                'id': bloco.id,
                                'titulo': bloco.titulo,
                                'novo_proprietario': comprador.nome,
                                'valor_pago': valor_ofertado
                            }
                        })
                        response.status_code = 200
                        return response
                    else:
                        response = jsonify({
                            'success': False,
                            'message': 'Erro ao processar transação blockchain',
                            'error': resultado_blockchain.get('error', 'Erro desconhecido')
                        })
                        response.status_code = 500
                        return response
                        
                except Exception as blockchain_error:
                    response = jsonify({
                        'success': False,
                        'message': 'Erro ao processar transação blockchain',
                        'error': str(blockchain_error)
                    })
                    response.status_code = 500
                    return response
                
            finally:
                session.close()
            
        except Exception as e:
            response = jsonify({
                'success': False,
                'message': f'Erro ao processar compra: {str(e)}'
            })
            response.status_code = 500
            return response