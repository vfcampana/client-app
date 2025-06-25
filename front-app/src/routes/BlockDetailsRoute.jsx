import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import BlockDetailsPage from "../components/blocks/BlockDetailsPage";
import { useBlocks } from "../hooks/useBlocks";
import { Box, CircularProgress } from "@mui/material";
import { useFavoritos } from "../hooks/useFavoritos";

export default function BlockDetailsRoute() {
  const { id } = useParams();
  const { blocks, loading, error } = useBlocks();
  const navigate = useNavigate();
  const { addFavorito, removeFavoritoById, checkIfFavorite } = useFavoritos();
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);

  const block = blocks.find((b) => String(b.id) === String(id));

  console.log('BlockDetailsRoute - blocks array:', blocks, 'looking for id:', id, 'found block:', block);
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

  const handleNegotiate = (blockData) => {
    console.log('Negociando bloco:', blockData);
    window.alert('Funcionalidade de negociação em desenvolvimento');
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (!loading && !block) {
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