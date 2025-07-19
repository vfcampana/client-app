import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import BusinessIcon from "@mui/icons-material/Business";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import FitnessCenterIcon from "@mui/icons-material/FitnessCenter";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { useTheme } from "@mui/material/styles";
import { useMediaQuery } from "@mui/material";
import { useNavigate } from "react-router-dom";
import ImageCarousel from "../ImageCarousel";

export default function BlockCard({block, onView }) {
    const theme = useTheme();
    const navigate = useNavigate();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    
    return (
        <Card
            sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                transition: "all 0.3s ease-in-out",
                overflow: "hidden", // Previne sobreposição
                "&:hover": {
                    transform: "translateY(-8px)",
                    boxShadow: "0 12px 24px rgba(0,0,0,0.15)",
                },
            }}
        >
            <Box sx={{ 
                position: "relative",
                width: "100%",
                height: { xs: 180, sm: 200, md: 220 }, // Responsivo
                overflow: "hidden"
            }}>
                {/* Usar carrossel se houver imagens, senão usar imagem padrão */}
                {block.imagens && block.imagens.length > 0 ? (
                    <ImageCarousel 
                        imagens={block.imagens} 
                        showDeleteButton={false}
                    />
                ) : (
                    <Box
                        sx={{
                            width: "100%",
                            height: "100%",
                            bgcolor: 'grey.200',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundImage: block.imagem ? `url(${block.imagem})` : 'url(https://via.placeholder.com/300x200/8B4513/FFFFFF?text=Stone)',
                            backgroundSize: 'cover',
                            backgroundPosition: 'center'
                        }}
                    />
                )}
                {/* Chip de preço com posição fixa */}
                <Chip
                    label={`R$ ${block.valor}`}
                    color="success"
                    size={isMobile ? "small" : "medium"}
                    sx={{
                        position: "absolute",
                        top: { xs: 8, sm: 12 },
                        right: { xs: 8, sm: 12 },
                        fontWeight: "bold",
                        backgroundColor: "rgba(255,255,255,0.95)",
                        color: "#2e7d32",
                        zIndex: 2, // Garante que fica acima do carrossel
                        backdropFilter: "blur(4px)"
                    }}
                />
            </Box>

            <CardContent sx={{ 
                flexGrow: 1, 
                p: { xs: 2, sm: 2, md: 3 },
                display: "flex",
                flexDirection: "column",
                gap: { xs: 1.5, sm: 2 }
            }}>
                <Typography 
                    variant={isMobile ? "subtitle1" : "h6"} 
                    component="h3" 
                    fontWeight="bold"
                    sx={{
                        lineHeight: 1.2,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical"
                    }}
                >
                    {block.titulo}
                </Typography>

                <Stack spacing={{ xs: 1, sm: 1.5 }}>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <FitnessCenterIcon 
                            color="primary" 
                            fontSize={isMobile ? "small" : "medium"} 
                        />
                        <Typography 
                            variant={isMobile ? "caption" : "body2"} 
                            color="text.secondary"
                            noWrap
                        >
                            {block.volume_liquido}m³
                        </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <BusinessIcon 
                            color="secondary" 
                            fontSize={isMobile ? "small" : "medium"} 
                        />
                        <Typography 
                            variant={isMobile ? "caption" : "body2"} 
                            color="text.secondary"
                            noWrap
                            sx={{
                                overflow: "hidden",
                                textOverflow: "ellipsis"
                            }}
                        >
                            {block.pedreira}
                        </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <LocationOnIcon 
                            color="error" 
                            fontSize={isMobile ? "small" : "medium"} 
                        />
                        <Typography 
                            variant={isMobile ? "caption" : "body2"} 
                            color="text.secondary"
                            noWrap
                            sx={{
                                overflow: "hidden",
                                textOverflow: "ellipsis"
                            }}
                        >
                            {block.cidade}, {block.estado}
                        </Typography>
                    </Box>
                </Stack>
            </CardContent>

            <CardActions sx={{ 
                p: { xs: 2, sm: 2, md: 3 }, 
                pt: 0 
            }}>
                <Button
                    variant="contained"
                    fullWidth
                    size={isMobile ? "medium" : "large"}
                    endIcon={<ArrowForwardIcon />}
                    sx={{
                        boxShadow: "0 3px 5px 2px rgba(11, 89, 107, 0.12)",
                        fontSize: { xs: "0.875rem", sm: "1rem" },
                        py: { xs: 1, sm: 1.5 },
                        "&:hover": {
                            background: theme.palette.primary.main,
                        },
                    }}
                    onClick={() => navigate(`/blocks/${block.id}`)}
                >
                    Ver Detalhes
                </Button>
            </CardActions>
        </Card>
    );
}