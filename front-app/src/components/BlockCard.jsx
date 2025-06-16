import React from "react";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
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

export default function BlockCard({ block }) {
    const theme = useTheme();
    
    return (
        <Card
            sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                transition: "all 0.3s ease-in-out",
                "&:hover": {
                    transform: "translateY(-8px)",
                    boxShadow: "0 12px 24px rgba(0,0,0,0.15)",
                },
            }}
        >
            <Box sx={{ position: "relative" }}>
                <CardMedia
                    component="img"
                    height="200"
                    image={block.imagem || "https://via.placeholder.com/300x200/8B4513/FFFFFF?text=Stone"}
                    alt={block.titulo}
                />
                <Chip
                    label={`R$ ${block.valor}`}
                    color="success"
                    sx={{
                        position: "absolute",
                        top: 12,
                        right: 12,
                        fontWeight: "bold",
                        backgroundColor: "rgba(255,255,255,0.95)",
                        color: "#2e7d32",
                    }}
                />
            </Box>

            <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" component="h3" gutterBottom fontWeight="bold">
                    {block.titulo}
                </Typography>

                <Stack spacing={1}>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <FitnessCenterIcon color="primary" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                            {block.volume_liquido}m³
                        </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <BusinessIcon color="secondary" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                            {block.pedreira}
                        </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <LocationOnIcon color="error" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                            {block.cidade}, {block.estado}
                        </Typography>
                    </Box>
                </Stack>
            </CardContent>

            <CardActions sx={{ p: 2 }}>
                <Button
                    variant="contained"
                    fullWidth
                    endIcon={<ArrowForwardIcon />}
                    sx={{
                        boxShadow: "0 3px 5px 2px rgba(11, 89, 107, 0.12)",
                        "&:hover": {
                            background: theme.palette.primary.main,
                        },
                    }}
                >
                    Ver Detalhes
                </Button>
            </CardActions>
        </Card>
    );
}