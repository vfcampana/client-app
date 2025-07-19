from models.supabase_config import get_supabase_client
from typing import Optional, List, Dict
import uuid
from datetime import datetime

class ImagemSupabase:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "imagens_blocos"
    
    def criar_tabela_se_nao_existir(self):
        """
        Cria a tabela de imagens no Supabase se ela não existir.
        Esta função deve ser chamada uma vez para configurar a estrutura.
        
        Execute este SQL no Supabase Dashboard:
        
        CREATE TABLE IF NOT EXISTS imagens_blocos (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            id_bloco INTEGER NOT NULL,
            url_imagem TEXT NOT NULL,
            nome_arquivo TEXT NOT NULL,
            tamanho_arquivo INTEGER,
            tipo_mime TEXT,
            data_upload TIMESTAMPTZ DEFAULT NOW(),
            data_atualizacao TIMESTAMPTZ DEFAULT NOW(),
            ativo BOOLEAN DEFAULT TRUE
        );
        
        -- Criar índice para melhor performance na busca por bloco
        CREATE INDEX IF NOT EXISTS idx_imagens_blocos_id_bloco ON imagens_blocos(id_bloco);
        """
        pass
    
    def upload_imagem(self, id_bloco: int, arquivo_imagem: bytes, nome_arquivo: str, tipo_mime: str = None) -> Dict:
        """
        Faz upload de uma imagem para o Supabase Storage e salva a referência na tabela
        
        Args:
            id_bloco: ID do bloco no banco Aiven
            arquivo_imagem: Bytes da imagem
            nome_arquivo: Nome do arquivo
            tipo_mime: Tipo MIME da imagem
            
        Returns:
            Dict com informações da imagem inserida
        """
        try:
            # Gerar nome único para o arquivo
            nome_unico = f"{uuid.uuid4()}_{nome_arquivo}"
            
            # Upload para o Storage do Supabase
            storage_response = self.supabase.storage.from_("imagens-blocos").upload(
                nome_unico, 
                arquivo_imagem,
                file_options={
                    "content-type": tipo_mime if tipo_mime else "image/jpeg"
                }
            )
            
            # Verificar se houve erro no upload
            if hasattr(storage_response, 'error') and storage_response.error:
                raise Exception(f"Erro no upload: {storage_response.error}")
            
            # Obter URL pública da imagem
            url_publica = self.supabase.storage.from_("imagens-blocos").get_public_url(nome_unico)
            
            # Salvar referência na tabela
            dados_imagem = {
                "id_bloco": id_bloco,
                "url_imagem": url_publica,
                "nome_arquivo": nome_arquivo,
                "tamanho_arquivo": len(arquivo_imagem),
                "tipo_mime": tipo_mime
            }
            
            response = self.supabase.table(self.table_name).insert(dados_imagem).execute()
            
            # Verificar se houve erro na inserção da tabela
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Erro ao salvar na tabela: {response.error}")
            
            return response.data[0]
            
        except Exception as e:
            raise Exception(f"Erro no upload da imagem: {str(e)}")
    
    def listar_imagens_bloco(self, id_bloco: int) -> List[Dict]:
        """
        Lista todas as imagens de um bloco específico
        
        Args:
            id_bloco: ID do bloco
            
        Returns:
            Lista de dicionários com informações das imagens
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select("*")\
                .eq("id_bloco", id_bloco)\
                .eq("ativo", True)\
                .order("data_upload", desc=True)\
                .execute()
            
            return response.data
            
        except Exception as e:
            raise Exception(f"Erro ao listar imagens: {str(e)}")
    
    def obter_imagem(self, id_imagem: str) -> Optional[Dict]:
        """
        Obtém uma imagem específica pelo ID
        
        Args:
            id_imagem: UUID da imagem
            
        Returns:
            Dados da imagem ou None se não encontrada
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select("*")\
                .eq("id", id_imagem)\
                .eq("ativo", True)\
                .single()\
                .execute()
            
            return response.data
            
        except Exception as e:
            return None
    
    def deletar_imagem(self, id_imagem: str) -> bool:
        """
        Deleta uma imagem (marca como inativa)
        
        Args:
            id_imagem: UUID da imagem
            
        Returns:
            True se deletada com sucesso, False caso contrário
        """
        try:
            # Marcar como inativa ao invés de deletar fisicamente
            response = self.supabase.table(self.table_name)\
                .update({"ativo": False, "data_atualizacao": datetime.now().isoformat()})\
                .eq("id", id_imagem)\
                .execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            return False
    
    def atualizar_imagem(self, id_imagem: str, novos_dados: Dict) -> Optional[Dict]:
        """
        Atualiza dados de uma imagem
        
        Args:
            id_imagem: UUID da imagem
            novos_dados: Dicionário com os novos dados
            
        Returns:
            Dados atualizados da imagem
        """
        try:
            novos_dados["data_atualizacao"] = datetime.now().isoformat()
            
            response = self.supabase.table(self.table_name)\
                .update(novos_dados)\
                .eq("id", id_imagem)\
                .execute()
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            raise Exception(f"Erro ao atualizar imagem: {str(e)}")
