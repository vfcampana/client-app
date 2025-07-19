from flask import Blueprint, request, jsonify
from models.imagem_supabase import ImagemSupabase
from werkzeug.utils import secure_filename
import os

# Blueprint para rotas de imagens
imagem_bp = Blueprint('imagem', __name__)

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imagem_bp.route('/imagens/upload/<int:id_bloco>', methods=['POST'])
def upload_imagem(id_bloco):
    """
    Upload de imagem para um bloco específico
    
    Args:
        id_bloco: ID do bloco no banco Aiven
        
    Returns:
        JSON com informações da imagem uploadada
    """
    try:
        # Verificar se o arquivo foi enviado
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Nenhuma imagem foi enviada'}), 400
        
        arquivo = request.files['imagem']
        
        if arquivo.filename == '':
            return jsonify({'erro': 'Nenhuma imagem selecionada'}), 400
        
        if not allowed_file(arquivo.filename):
            return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400
        
        # Obter dados do arquivo
        nome_arquivo = secure_filename(arquivo.filename)
        arquivo_bytes = arquivo.read()
        tipo_mime = arquivo.content_type
        
        # Upload para Supabase
        imagem_service = ImagemSupabase()
        resultado = imagem_service.upload_imagem(
            id_bloco=id_bloco,
            arquivo_imagem=arquivo_bytes,
            nome_arquivo=nome_arquivo,
            tipo_mime=tipo_mime
        )
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Imagem uploadada com sucesso',
            'imagem': resultado
        }), 201
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

@imagem_bp.route('/imagens/bloco/<int:id_bloco>', methods=['GET'])
def listar_imagens_bloco(id_bloco):
    """
    Lista todas as imagens de um bloco específico
    
    Args:
        id_bloco: ID do bloco
        
    Returns:
        JSON com lista de imagens
    """
    try:
        imagem_service = ImagemSupabase()
        imagens = imagem_service.listar_imagens_bloco(id_bloco)
        
        return jsonify({
            'sucesso': True,
            'imagens': imagens,
            'total': len(imagens)
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

@imagem_bp.route('/imagens/<string:id_imagem>', methods=['GET'])
def obter_imagem(id_imagem):
    """
    Obtém informações de uma imagem específica
    
    Args:
        id_imagem: UUID da imagem
        
    Returns:
        JSON com dados da imagem
    """
    try:
        imagem_service = ImagemSupabase()
        imagem = imagem_service.obter_imagem(id_imagem)
        
        if not imagem:
            return jsonify({
                'sucesso': False,
                'erro': 'Imagem não encontrada'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'imagem': imagem
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

@imagem_bp.route('/imagens/<string:id_imagem>', methods=['DELETE'])
def deletar_imagem(id_imagem):
    """
    Deleta uma imagem (marca como inativa)
    
    Args:
        id_imagem: UUID da imagem
        
    Returns:
        JSON confirmando a exclusão
    """
    try:
        imagem_service = ImagemSupabase()
        sucesso = imagem_service.deletar_imagem(id_imagem)
        
        if not sucesso:
            return jsonify({
                'sucesso': False,
                'erro': 'Imagem não encontrada ou já deletada'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Imagem deletada com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

@imagem_bp.route('/imagens/<string:id_imagem>', methods=['PUT'])
def atualizar_imagem(id_imagem):
    """
    Atualiza informações de uma imagem
    
    Args:
        id_imagem: UUID da imagem
        
    Returns:
        JSON com dados atualizados da imagem
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                'sucesso': False,
                'erro': 'Nenhum dado foi enviado'
            }), 400
        
        imagem_service = ImagemSupabase()
        imagem_atualizada = imagem_service.atualizar_imagem(id_imagem, dados)
        
        if not imagem_atualizada:
            return jsonify({
                'sucesso': False,
                'erro': 'Imagem não encontrada'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Imagem atualizada com sucesso',
            'imagem': imagem_atualizada
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500
