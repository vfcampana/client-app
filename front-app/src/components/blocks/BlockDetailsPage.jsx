import {
  Box,
  Typography,
  Button,
  Card,
  CardMedia,
  Divider,
  Stack,
  Chip,
  IconButton,
  Container,
  CircularProgress,
  Alert,
} from "@mui/material";
import {
  ArrowBack,
  ShoppingCart,
  Star,
  Business,
  LocationOn,
} from "@mui/icons-material";
import { useState } from 'react';
import { useTheme } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import ImageCarousel from '../ImageCarousel';
import CompraModal from '../CompraModal';

export default function BlockDetailsPage({ 
  block, 
  onBack, 
  onInterest, 
  isFavorite = false, 
  favoriteLoading = false 
}) {
  const theme = useTheme();
  const navigate = useNavigate();
  
  // Estados para compra direta
  const [compraModalOpen, setCompraModalOpen] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  const getCurrentUserId = () => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        return user.id;
      } catch (e) {
        console.error('Erro ao fazer parse dos dados do usuário:', e);
      }
    }
    return null;
  };
  
  const isUserLoggedIn = () => {
    return !!localStorage.getItem('authToken');
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleDateString("pt-BR");
  };

  const formatCurrency = (value) => {
    if (!value) return "R$ 0,00";
    const numValue = typeof value === "string" ? parseFloat(value.replace(/[^\d,.-]/g, "").replace(",", ".")) : value;
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(numValue);
  };

  const handleIniciarCompra = () => {
    const currentUserId = getCurrentUserId();
    
    if (!isUserLoggedIn()) {
      setError('Você precisa estar logado para comprar.');
      return;
    }
    
    if (currentUserId && Number(block.id_usuario) === Number(currentUserId)) {
      setError('Você não pode comprar seu próprio bloco.');
      return;
    }
    
    setCompraModalOpen(true);
    setError(null);
    setSuccess(null);
  };

  return (
    <Container maxWidth="md" sx={{ py: 2 }}>
      {/* Cabeçalho com navegação */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2, gap: 2 }}>
        <IconButton onClick={onBack} sx={{ color: "white", backgroundColor: theme.palette.primary.main }}>
          <ArrowBack />
        </IconButton>
      </Box>

      {/* Cartão de imagem */}
      <Card sx={{ mb: 3, overflow: "hidden" }}>
        <Box sx={{ 
          position: "relative", 
          height: { xs: 250, sm: 300, md: 400 },
          width: "100%"
        }}>
          {block.imagens && block.imagens.length > 0 ? (
            <Box sx={{ height: "100%", width: "100%" }}>
              <ImageCarousel 
                imagens={block.imagens} 
                showDeleteButton={false}
              />
            </Box>
          ) : (
            <CardMedia
              component="img"
              height="100%"
              image="assets/stone.png" 
              alt={block.titulo}
              sx={{ 
                objectFit: "cover",
                width: "100%",
                height: "100%"
              }}
            />
          )}
        </Box>
      </Card>

      {/* Preço */}
      <Typography
        variant="h4"
        sx={{
          fontWeight: "bold",
          color: theme.palette.primary.main,
          mb: 1,
        }}
      >
        {formatCurrency(block.valor)}
      </Typography>

      {/* Título e informações básicas */}
      <Typography variant="h6" sx={{ mb: 1, fontWeight: "bold" }}>
        {block.titulo.toUpperCase()}
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Publicado em {formatDate(block.data_criacao)}
      </Typography>

      {/* Seção de descrição */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold" }}>
          Descrição
        </Typography>
        
        <Stack spacing={1}>
          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Classificação:</strong>
            </Typography>
            <Typography variant="body2">{block.classificacao}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Coloração:</strong>
            </Typography>
            <Typography variant="body2">{block.coloracao}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Material:</strong>
            </Typography>
            <Typography variant="body2">{block.material}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Medida Bruta:</strong>
            </Typography>
            <Typography variant="body2">{block.medida_bruta}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Volume Bruto:</strong>
            </Typography>
            <Typography variant="body2">{block.volume_bruto}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Medida Líquida:</strong>
            </Typography>
            <Typography variant="body2">{block.medida_liquida}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Volume Líquido:</strong>
            </Typography>
            <Typography variant="body2">{block.volume_liquido}</Typography>
          </Box>

          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Pedreira:</strong>
            </Typography>
            <Typography variant="body2">{block.pedreira}</Typography>
          </Box>
        </Stack>

        {block.observacoes && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              <strong>Outras Informações:</strong>
            </Typography>
            <Typography variant="body2">{block.observacoes}</Typography>
          </Box>
        )}
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* Seção de localização */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold" }}>
          Localização
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <LocationOn color="error" />
          <Typography variant="body2">
            {block.logradouro && `${block.logradouro}, `}
            {block.cidade}, {block.estado}, {block.pais}
            {block.cep && ` - CEP: ${block.cep}`}
          </Typography>
        </Box>
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* Seção do anunciante */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold" }}>
          Anunciante
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <Business color="primary" />
          <Box>
            <Typography variant="body1" sx={{ fontWeight: "bold" }}>
              Empresa Teste S.A
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Anunciante desde {formatDate(block.data_criacao)}
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Botões de ação */}
      <Stack spacing={2} sx={{ mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<ShoppingCart />}
          onClick={handleIniciarCompra}
          sx={{
            backgroundColor: theme.palette.primary.main,
            color: "white",
            py: 1.5,
            fontSize: "1rem",
            fontWeight: "bold",
            "&:hover": {
              backgroundColor: theme.palette.primary.dark,
            },
          }}
        >
          COMPRAR AGORA
        </Button>

        <Button
          variant={isFavorite ? "contained" : "outlined"}
          size="large"
          startIcon={favoriteLoading ? <CircularProgress size={20} /> : <Star />}
          onClick={() => onInterest && onInterest(block)}
          disabled={favoriteLoading}
          sx={{
            borderColor: theme.palette.primary.main,
            color: isFavorite ? "white" : theme.palette.primary.main,
            backgroundColor: isFavorite ? theme.palette.primary.main : "transparent",
            py: 1.5,
            fontSize: "1rem",
            fontWeight: "bold",
            "&:hover": {
              backgroundColor: theme.palette.primary.main,
              color: "white",
            },
          }}
        >
          {isFavorite ? "FAVORITADO" : "INTERESSE"}
        </Button>
      </Stack>

      {/* Chip de status */}
      {block.status && (
        <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
          <Chip
            label={block.status.toUpperCase()}
            color={block.status.toLowerCase() === "ativo" ? "success" : "default"}
            variant="outlined"
          />
        </Box>
      )}

      {/* Mensagens de erro e sucesso */}
      {error && (
        <Box sx={{ mb: 2 }}>
          <Alert severity="error">{error}</Alert>
        </Box>
      )}

      {success && (
        <Box sx={{ mb: 2 }}>
          <Alert severity="success">{success}</Alert>
        </Box>
      )}

      {/* Modal de Compra */}
      <CompraModal
        open={compraModalOpen}
        onClose={() => setCompraModalOpen(false)}
        bloco={block}
        onCompraRealizada={() => {
          setCompraModalOpen(false);
          setSuccess('Compra realizada com sucesso!');
          // Recarregar a página após 2 segundos
          setTimeout(() => {
            window.location.reload();
          }, 2000);
        }}
      />
    </Container>
  );
}