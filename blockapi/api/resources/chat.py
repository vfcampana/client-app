from flask import request, jsonify
from flask_restful import Resource
from flask_socketio import emit, join_room, leave_room
from sqlalchemy.orm import sessionmaker
from models.extensions import engine, verificar_jwt, socketio
from models.mensagem import Mensagem
from models.conversa import Conversa
from models.usuario import Usuario
from models.bloco import Bloco
from datetime import datetime
from sqlalchemy import or_, and_

Session = sessionmaker(bind=engine)

class ConversasList(Resource):
    def get(self):
        """Listar todas as conversas do usuário logado"""
        try:
            id_usuario = verificar_jwt()
            print("id_usuario:", id_usuario)
            
            if id_usuario.get('code', 401) != 200 or not id_usuario.get('message'):
                print('token inválido ou não fornecido')
                response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
                response.status_code = id_usuario.get('code', 401)
                return response
            
            user_id = str(id_usuario['message'])
            session = Session()
            
            conversas = session.query(Conversa).filter(
                or_(
                    Conversa.usuario1_id == user_id,
                    Conversa.usuario2_id == user_id
                )
            ).order_by(Conversa.ultima_atividade.desc()).all()
            
            result = []
            for conversa in conversas:
                # Identificar o outro usuário
                outro_usuario_id = conversa.usuario2_id if conversa.usuario1_id == user_id else conversa.usuario1_id
                outro_usuario = session.query(Usuario).filter_by(id=outro_usuario_id).first()
                
                # Buscar informações do bloco separadamente (SEM relacionamento)
                bloco = None
                if conversa.bloco_id:
                    bloco = session.query(Bloco).filter_by(id=conversa.bloco_id).first()
                
                # Buscar a última mensagem
                ultima_mensagem = session.query(Mensagem).filter_by(
                    conversa_id=conversa.id
                ).order_by(Mensagem.data_envio.desc()).first()
                
                # Contar mensagens não lidas
                mensagens_nao_lidas = session.query(Mensagem).filter(
                    and_(
                        Mensagem.conversa_id == conversa.id,
                        Mensagem.usuario_id != user_id,
                        Mensagem.lida == False
                    )
                ).count()
                
                # Montar resultado - CORRIGIDO: sem usar relacionamentos
                conversa_data = {
                    'id': conversa.id,
                    'outro_usuario': {
                        'id': outro_usuario.id if outro_usuario else None,
                        'nome': outro_usuario.nome if outro_usuario else 'Usuário',
                        'email': outro_usuario.email if outro_usuario else ''
                    },
                    'mensagens_nao_lidas': mensagens_nao_lidas,
                    'ultima_atividade': conversa.ultima_atividade.isoformat()
                }
                
                # Adicionar bloco se existir
                if bloco:
                    conversa_data['bloco'] = {
                        'id': bloco.id,
                        'titulo': bloco.titulo,
                        'valor': str(bloco.valor),
                        'imagem': bloco.imagem if hasattr(bloco, 'imagem') else None
                    }
                else:
                    conversa_data['bloco'] = None
                
                # Adicionar última mensagem se existir
                if ultima_mensagem:
                    conversa_data['ultima_mensagem'] = {
                        'texto': ultima_mensagem.texto,
                        'data_envio': ultima_mensagem.data_envio.isoformat(),
                        'de_mim': str(ultima_mensagem.usuario_id) == user_id  # Garantir string
                    }
                else:
                    conversa_data['ultima_mensagem'] = None
                
                result.append(conversa_data)
            
            session.close()
            response = jsonify(result)
            response.status_code = 200
            return response
            
        except Exception as e:
            print(f"Erro detalhado ao buscar conversas: {e}")
            import traceback
            traceback.print_exc()
            response = jsonify({'message': f'Erro ao buscar conversas: {str(e)}'})
            response.status_code = 500
            return response

class ConversaMessages(Resource):
    def get(self, conversa_id):
        """Buscar mensagens de uma conversa específica"""
        try:
            id_usuario = verificar_jwt()
            print("id_usuario:", id_usuario)
            
            if id_usuario.get('code', 401) != 200 or not id_usuario.get('message'):
                print('token inválido ou não fornecido')
                response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
                response.status_code = id_usuario.get('code', 401)
                return response
            
            user_id = str(id_usuario['message'])
            session = Session()
            
            # Verificar se o usuário faz parte da conversa
            conversa = session.query(Conversa).filter(
                and_(
                    Conversa.id == conversa_id,
                    or_(
                        Conversa.usuario1_id == user_id,
                        Conversa.usuario2_id == user_id
                    )
                )
            ).first()
            
            if not conversa:
                session.close()
                response = jsonify({'message': 'Conversa não encontrada'})
                response.status_code = 404
                return response
            
            # Buscar mensagens
            mensagens = session.query(Mensagem).filter_by(
                conversa_id=conversa_id
            ).order_by(Mensagem.data_envio.asc()).all()
            
            # Marcar mensagens como lidas
            session.query(Mensagem).filter(
                and_(
                    Mensagem.conversa_id == conversa_id,
                    Mensagem.usuario_id != user_id,
                    Mensagem.lida == False
                )
            ).update({'lida': True})
            session.commit()
            
            result = []
            for msg in mensagens:
                # Buscar usuário da mensagem separadamente (sem relacionamento)
                usuario_msg = session.query(Usuario).filter_by(id=msg.usuario_id).first()
                
                result.append({
                    'id': msg.id,
                    'texto': msg.texto,
                    'tipo': msg.tipo,
                    'data_envio': msg.data_envio.isoformat(),
                    'de_mim': str(msg.usuario_id) == user_id,  # Garantir que seja string
                    'usuario': {
                        'id': usuario_msg.id if usuario_msg else None,
                        'nome': usuario_msg.nome if usuario_msg else 'Usuário'
                    },
                    'lida': msg.lida,
                    'proposta_valor': str(msg.proposta_valor) if msg.proposta_valor else None,
                    'proposta_status': msg.proposta_status
                })
            
            session.close()
            response = jsonify(result)
            response.status_code = 200
            return response
            
        except Exception as e:
            print(f"Erro detalhado ao buscar mensagens: {e}")
            import traceback
            traceback.print_exc()
            response = jsonify({'message': f'Erro ao buscar mensagens: {str(e)}'})
            response.status_code = 500
            return response

    def post(self, conversa_id):
        """Enviar uma nova mensagem"""
        try:
            id_usuario = verificar_jwt()
            
            if id_usuario.get('code', 401) != 200 or not id_usuario.get('message'):
                response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
                response.status_code = id_usuario.get('code', 401)
                return response
            
            user_id = str(id_usuario['message'])
            data = request.get_json()
            
            texto = data.get('texto')
            tipo = data.get('tipo', 'texto')
            proposta_valor = data.get('proposta_valor')
            
            if not texto:
                response = jsonify({'message': 'Texto da mensagem é obrigatório'})
                response.status_code = 400
                return response
            
            session = Session()
            
            try:
                # Verificar se o usuário faz parte da conversa
                conversa = session.query(Conversa).filter(
                    and_(
                        Conversa.id == conversa_id,
                        or_(
                            Conversa.usuario1_id == user_id,
                            Conversa.usuario2_id == user_id
                        )
                    )
                ).first()
                
                if not conversa:
                    response = jsonify({'message': 'Conversa não encontrada'})
                    response.status_code = 404
                    return response
                
                # Criar mensagem
                mensagem = Mensagem(
                    conversa_id=conversa_id,
                    usuario_id=user_id,
                    texto=texto,
                    tipo=tipo,
                    data_envio=datetime.now(),
                    lida=False,
                    proposta_valor=proposta_valor if proposta_valor else None,
                    proposta_status='pendente' if proposta_valor else None
                )
                
                session.add(mensagem)
                
                # Atualizar última atividade da conversa
                conversa.ultima_atividade = datetime.now()
                
                # Commit e refresh para garantir que o ID esteja disponível
                session.commit()
                session.refresh(mensagem)  # CORREÇÃO: Atualizar o objeto
                
                # Agora é seguro acessar o ID
                mensagem_id = mensagem.id
                
                response = jsonify({'message': 'Mensagem enviada', 'id': mensagem_id})
                response.status_code = 201
                return response
                
            finally:
                session.close()
            
        except Exception as e:
            print(f"Erro detalhado ao enviar mensagem: {e}")
            import traceback
            traceback.print_exc()
            response = jsonify({'message': f'Erro ao enviar mensagem: {str(e)}'})
            response.status_code = 500
            return response
        
class IniciarConversa(Resource):
    def post(self):
        """Iniciar uma nova conversa sobre um bloco"""
        try:
            id_usuario = verificar_jwt()
            print("id_usuario:", id_usuario)
            
            if id_usuario.get('code', 401) != 200 or not id_usuario.get('message'):
                print('token inválido ou não fornecido')
                response = jsonify({"message": id_usuario.get('message', 'Token inválido ou não fornecido')})
                response.status_code = id_usuario.get('code', 401)
                return response
            
            user_id = str(id_usuario['message'])
            data = request.get_json()
            
            bloco_id = data.get('bloco_id')
            vendedor_id = str(data.get('vendedor_id'))
            mensagem_inicial = data.get('mensagem', 'Olá! Tenho interesse neste bloco.')
            
            if not bloco_id or not vendedor_id:
                response = jsonify({'message': 'bloco_id e vendedor_id são obrigatórios'})
                response.status_code = 400
                return response
            
            # Verificar se o usuário não está tentando conversar consigo mesmo
            if user_id == vendedor_id:
                response = jsonify({'message': 'Você não pode iniciar uma conversa consigo mesmo'})
                response.status_code = 400
                return response
            
            session = Session()
            
            try:
                # Verificar se o bloco existe
                bloco = session.query(Bloco).filter_by(id=bloco_id).first()
                if not bloco:
                    response = jsonify({'message': 'Bloco não encontrado'})
                    response.status_code = 404
                    return response
                
                # Verificar se já existe uma conversa entre esses usuários para este bloco
                conversa_existente = session.query(Conversa).filter(
                    and_(
                        Conversa.bloco_id == bloco_id,
                        or_(
                            and_(Conversa.usuario1_id == user_id, Conversa.usuario2_id == vendedor_id),
                            and_(Conversa.usuario1_id == vendedor_id, Conversa.usuario2_id == user_id)
                        )
                    )
                ).first()
                
                if conversa_existente:
                    response = jsonify({'conversa_id': conversa_existente.id, 'message': 'Conversa já existe'})
                    response.status_code = 200
                    return response
                
                # Criar nova conversa
                nova_conversa = Conversa(
                    usuario1_id=user_id,
                    usuario2_id=vendedor_id,
                    bloco_id=bloco_id,
                    criada_em=datetime.now(),
                    ultima_atividade=datetime.now()
                )
                
                session.add(nova_conversa)
                session.flush()  # Para obter o ID sem commit completo
                
                # CORREÇÃO: Salvar o ID da conversa
                conversa_id = nova_conversa.id
                
                # Criar mensagem inicial
                mensagem = Mensagem(
                    conversa_id=conversa_id,  # Usar o ID salvo
                    usuario_id=user_id,
                    texto=mensagem_inicial,
                    tipo='texto',
                    data_envio=datetime.now(),
                    lida=False
                )
                
                session.add(mensagem)
                session.commit()
                
                # Emitir evento via WebSocket (opcional)
                try:
                    socketio.emit('nova_conversa', {
                        'conversa_id': conversa_id,
                        'de_usuario': user_id,
                        'para_usuario': vendedor_id,
                        'bloco_id': bloco_id
                    }, room=f'user_{vendedor_id}')
                except Exception as socket_error:
                    print(f"Erro ao emitir evento WebSocket: {socket_error}")
                
                response = jsonify({'conversa_id': conversa_id, 'message': 'Conversa iniciada'})
                response.status_code = 201
                return response
                
            finally:
                session.close()
            
        except Exception as e:
            print(f"Erro detalhado ao iniciar conversa: {e}")
            import traceback
            traceback.print_exc()
            response = jsonify({'message': f'Erro ao iniciar conversa: {str(e)}'})
            response.status_code = 500
            return response

# WebSocket Events
@socketio.on('join_room')
def on_join(data):
    """Usuário entra em uma sala de conversa"""
    try:
        conversa_id = data.get('conversa_id')
        user_id = data.get('user_id')
        
        if conversa_id:
            join_room(f'conversa_{conversa_id}')
            print(f'Usuário {user_id} entrou na conversa {conversa_id}')
        
        if user_id:
            join_room(f'user_{user_id}')
            print(f'Usuário {user_id} entrou na sala pessoal')
        
        emit('status', {'msg': f'Usuário {user_id} conectado'})
    except Exception as e:
        print(f"Erro ao entrar na sala: {e}")
        emit('error', {'message': f'Erro ao entrar na sala: {str(e)}'})

@socketio.on('leave_room')
def on_leave(data):
    """Usuário sai de uma sala de conversa"""
    try:
        conversa_id = data.get('conversa_id')
        user_id = data.get('user_id')
        
        if conversa_id:
            leave_room(f'conversa_{conversa_id}')
            print(f'Usuário {user_id} saiu da conversa {conversa_id}')
        
        emit('status', {'msg': f'Usuário {user_id} saiu da conversa {conversa_id}'})
    except Exception as e:
        print(f"Erro ao sair da sala: {e}")
        emit('error', {'message': f'Erro ao sair da sala: {str(e)}'})

@socketio.on('send_message')
def handle_message(data):
    """Enviar mensagem em tempo real"""
    try:
        conversa_id = data.get('conversa_id')
        user_id = str(data.get('user_id'))
        texto = data.get('texto')
        tipo = data.get('tipo', 'texto')
        proposta_valor = data.get('proposta_valor')
        
        if not conversa_id or not user_id or not texto:
            emit('error', {'message': 'Dados obrigatórios não fornecidos'})
            return
        
        session = Session()
        
        # Verificar se o usuário faz parte da conversa
        conversa = session.query(Conversa).filter(
            and_(
                Conversa.id == conversa_id,
                or_(
                    Conversa.usuario1_id == user_id,
                    Conversa.usuario2_id == user_id
                )
            )
        ).first()
        
        if not conversa:
            session.close()
            emit('error', {'message': 'Conversa não encontrada'})
            return
        
        # Criar mensagem
        mensagem = Mensagem(
            conversa_id=conversa_id,
            usuario_id=user_id,
            texto=texto,
            tipo=tipo,
            data_envio=datetime.now(),
            lida=False,
            proposta_valor=proposta_valor if proposta_valor else None,
            proposta_status='pendente' if proposta_valor else None
        )
        
        session.add(mensagem)
        
        # Atualizar última atividade da conversa
        conversa.ultima_atividade = datetime.now()
        session.commit()
        
        # Buscar dados do usuário
        usuario = session.query(Usuario).filter_by(id=user_id).first()
        
        # Emitir mensagem para todos na sala
        message_data = {
            'id': mensagem.id,
            'conversa_id': conversa_id,
            'texto': texto,
            'tipo': tipo,
            'data_envio': mensagem.data_envio.isoformat(),
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome
            },
            'proposta_valor': str(proposta_valor) if proposta_valor else None,
            'proposta_status': mensagem.proposta_status,
            'de_mim': False  # Será ajustado no frontend
        }
        
        emit('new_message', message_data, room=f'conversa_{conversa_id}')
        print(f"Mensagem enviada para conversa {conversa_id}: {texto}")
        
        session.close()
        
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        emit('error', {'message': f'Erro ao enviar mensagem: {str(e)}'})

@socketio.on('respond_proposal')
def handle_proposal_response(data):
    """Responder a uma proposta (aceitar/rejeitar)"""
    try:
        mensagem_id = data.get('mensagem_id')
        user_id = str(data.get('user_id'))
        resposta = data.get('resposta')  # 'aceita' ou 'rejeitada'
        
        if not mensagem_id or not user_id or not resposta:
            emit('error', {'message': 'Dados obrigatórios não fornecidos'})
            return
        
        session = Session()
        
        # Buscar a mensagem da proposta
        mensagem = session.query(Mensagem).filter_by(id=mensagem_id).first()
        
        if not mensagem:
            session.close()
            emit('error', {'message': 'Proposta não encontrada'})
            return
        
        # Verificar se o usuário pode responder (deve ser o dono do bloco)
        conversa = session.query(Conversa).filter_by(id=mensagem.conversa_id).first()
        bloco = session.query(Bloco).filter_by(id=conversa.bloco_id).first()
        
        if str(bloco.id_usuario) != user_id:
            session.close()
            emit('error', {'message': 'Você não pode responder a esta proposta'})
            return
        
        # Atualizar status da proposta
        mensagem.proposta_status = resposta
        session.commit()
        
        # Criar mensagem de resposta
        texto_resposta = f"Proposta {'ACEITA' if resposta == 'aceita' else 'REJEITADA'}: R$ {mensagem.proposta_valor}"
        
        resposta_msg = Mensagem(
            conversa_id=mensagem.conversa_id,
            usuario_id=user_id,
            texto=texto_resposta,
            tipo='resposta_proposta',
            data_envio=datetime.now(),
            lida=False
        )
        
        session.add(resposta_msg)
        session.commit()
        
        # Emitir resposta para todos na sala
        usuario = session.query(Usuario).filter_by(id=user_id).first()
        
        response_data = {
            'id': resposta_msg.id,
            'conversa_id': mensagem.conversa_id,
            'texto': texto_resposta,
            'tipo': 'resposta_proposta',
            'data_envio': resposta_msg.data_envio.isoformat(),
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome
            },
            'proposta_original_id': mensagem_id,
            'proposta_status': resposta,
            'de_mim': False  # Será ajustado no frontend
        }
        
        emit('proposal_response', response_data, room=f'conversa_{mensagem.conversa_id}')
        emit('new_message', response_data, room=f'conversa_{mensagem.conversa_id}')
        
        print(f"Resposta à proposta enviada: {resposta}")
        session.close()
        
    except Exception as e:
        print(f"Erro ao responder proposta: {e}")
        emit('error', {'message': f'Erro ao responder proposta: {str(e)}'})

@socketio.on('connect')
def handle_connect():
    """Usuário conectou ao WebSocket"""
    print('Cliente conectado ao WebSocket')
    emit('status', {'msg': 'Conectado com sucesso'})

@socketio.on('disconnect')
def handle_disconnect():
    """Usuário desconectou do WebSocket"""
    print('Cliente desconectado do WebSocket')