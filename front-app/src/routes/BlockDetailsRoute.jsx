import { useParams, useNavigate } from "react-router-dom";
import BlockDetailsPage from "../components/blocks/BlockDetailsPage";
import { useBlocks } from "../hooks/useBlocks";
import { Box, CircularProgress } from "@mui/material";

export default function BlockDetailsRoute() {
  const { id } = useParams();
  const { blocks } = useBlocks();
  const navigate = useNavigate();
  const { loading, error } = useBlocks();
  const block = blocks.find((b) => String(b.id) === String(id));
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <BlockDetailsPage
      block={block}
      onBack={() => navigate(-1)}
      onNegotiate={() => {/* lógica de negociar */}}
      onInterest={() => {/* lógica de interesse */}}
    />
  );
}