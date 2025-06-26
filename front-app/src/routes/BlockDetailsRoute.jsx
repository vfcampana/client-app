import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import BlockDetailsPage from "../components/blocks/BlockDetailsPage";
import { getBlock } from "../services/blocks";
import { Box, CircularProgress } from "@mui/material";
import { useFavoritos } from "../hooks/useFavoritos";

export default function BlockDetailsRoute() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addFavorito, removeFavoritoById, checkIfFavorite } = useFavoritos();
  
  const [block, setBlock] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);

  const handleNegotiate = async (blockData) => {
    console.log('Iniciando negociação para bloco:', blockData);
    
    try {
      const token = localStorage.getItem('authToken');
      
      if (!token) {
        alert('Você precisa estar logado para negociar');
        return;
      }

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000'}/iniciar-conversa`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bloco_id: blockData.id,
          vendedor_id: blockData.id_usuario,
          mensagem: 'Olá! Tenho interesse neste bloco.'
        })
      });

      if (response.ok) {
        // Redirecionar para o chat
        navigate('/chat');
        alert('Conversa iniciada! Redirecionando para o chat...');
      } else {
        throw new Error('Erro ao iniciar conversa');
      }
    } catch (error) {
      console.error('Erro ao iniciar conversa:', error);
      alert('Erro ao iniciar conversa. Tente novamente.');
    }
  };

  // Buscar o bloco específico usando getBlock
  useEffect(() => {
    const fetchBlock = async () => {
      if (!id) return;
      
      setLoading(true);
      setError(null);
      
      try {
        console.log('Buscando bloco com ID:', id);
        const blockData = await getBlock(parseInt(id));
        console.log('Bloco encontrado:', blockData);
        setBlock(blockData);
      } catch (err) {
        console.error('Erro ao buscar bloco:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBlock();
  }, [id]);

  // Verificar se o bloco já está nos favoritos ao carregar
  useEffect(() => {
    const checkFavoriteStatus = async () => {
      if (block?.id) {
        const result = await checkIfFavorite(block.id);
        if (result.success) {
          setIsFavorite(result.isFavorite);
        }
      }
    };

    checkFavoriteStatus();
  }, [block?.id, checkIfFavorite]);

  const handleInterest = async (blockData) => {
    setFavoriteLoading(true);
    
    if (isFavorite) {
      // Se já é favorito, remove
      const result = await removeFavoritoById(blockData.id);
      if (result.success) {
        setIsFavorite(false);
        window.alert('Bloco removido dos favoritos!');
      } else {
        window.alert(`Erro: ${result.error}`);
      }
    } else {
      // Se não é favorito, adiciona
      const result = await addFavorito(blockData.id);
      if (result.success) {
        setIsFavorite(true);
        window.alert('Bloco adicionado aos favoritos com sucesso!');
      } else {
        window.alert(`Erro: ${result.error}`);
      }
    }
    
    setFavoriteLoading(false);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <p>Erro ao carregar bloco: {error}</p>
      </Box>
    );
  }

  if (!block) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <p>Bloco não encontrado</p>
      </Box>
    );
  }

  return (
    <BlockDetailsPage
      block={block}
      onBack={() => navigate(-1)}
      onNegotiate={handleNegotiate}
      onInterest={handleInterest}
      isFavorite={isFavorite}
      favoriteLoading={favoriteLoading}
    />
  );
}