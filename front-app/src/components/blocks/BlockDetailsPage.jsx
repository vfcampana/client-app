import React from "react";
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
} from "@mui/material";
import {
  ArrowBack,
  Favorite,
  FavoriteBorder,
  Share,
  Edit,
  Handshake,
  Star,
  Business,
  LocationOn,
  CalendarToday,
  Info,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";

export default function BlockDetailsPage({ block, onBack, onNegotiate, onInterest }) {
  const theme = useTheme();
  const [isFavorite, setIsFavorite] = React.useState(false);

  const handleFavoriteToggle = () => {
    setIsFavorite(!isFavorite);
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

  return (
    <Container maxWidth="md" sx={{ py: 2 }}>
      {/* Header with navigation */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2, gap: 2 }}>
        <IconButton onClick={onBack} sx={{ color: "white", backgroundColor: theme.palette.primary.main }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h6" sx={{ flexGrow: 1, color: "white" }}>
          {block.titulo}
        </Typography>
        <IconButton onClick={handleFavoriteToggle} sx={{ color: "white" }}>
          {isFavorite ? <Favorite /> : <FavoriteBorder />}
        </IconButton>
        <IconButton sx={{ color: "white" }}>
          <Share />
        </IconButton>
        <IconButton sx={{ color: "white" }}>
          <Edit />
        </IconButton>
      </Box>

      {/* Image Card */}
      <Card sx={{ mb: 3, overflow: "hidden" }}>
        <Box sx={{ position: "relative" }}>
          <CardMedia
            component="img"
            height="300"
            image={block.imagem || "https://via.placeholder.com/400x300/8B4513/FFFFFF?text=Stone+Block"}
            alt={block.titulo}
            sx={{ objectFit: "cover" }}
          />
          {/* Navigation arrows for image gallery could be added here */}
        </Box>
      </Card>

      {/* Price */}
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

      {/* Title and Basic Info */}
      <Typography variant="h6" sx={{ mb: 1, fontWeight: "bold" }}>
        {block.titulo.toUpperCase()}
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Publicado em {formatDate(block.data_criacao)}
      </Typography>

      {/* Description Section */}
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

      {/* Location Section */}
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

      {/* Advertiser Section */}
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

      {/* Action Buttons */}
      <Stack spacing={2} sx={{ mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<Handshake />}
          onClick={() => onNegotiate && onNegotiate(block)}
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
          NEGOCIAR
        </Button>

        <Button
          variant="outlined"
          size="large"
          startIcon={<Star />}
          onClick={() => onInterest && onInterest(block)}
          sx={{
            borderColor: theme.palette.primary.main,
            color: theme.palette.primary.main,
            py: 1.5,
            fontSize: "1rem",
            fontWeight: "bold",
            "&:hover": {
              backgroundColor: theme.palette.primary.main,
              color: "white",
            },
          }}
        >
          INTERESSE
        </Button>
      </Stack>

      {/* Status Chip */}
      {block.status && (
        <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
          <Chip
            label={block.status.toUpperCase()}
            color={block.status.toLowerCase() === "ativo" ? "success" : "default"}
            variant="outlined"
          />
        </Box>
      )}
    </Container>
  );
}