import * as React from 'react';
import { Box, Modal, Typography, styled } from '@mui/material';
import { Block } from '../../types/Blocks';
import { formatDate } from '../../utils/utils';

const stoneImageExample = require('../../assets/stone.png') as string;

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
  bgcolor: 'background.paper',
  border: '2px solid #0d1b2a',
  borderRadius: 4,
  boxShadow: 24,
  p: 4,
};

const StyledImage = styled('img')({
  border: '4px solid #0d1b2a',
  borderRadius: '8px',
  marginTop: 20,
  width: 200,
  height: 150,
});

const InfoBox = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  paddingLeft: 16,
  marginTop: 20,
  width: '100%',
});

type BlockModalProps = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  chosenBlock: Block;
};

export default function BlockModal({ open, setOpen, chosenBlock }: BlockModalProps) {

  return (
    <Modal
      open={open}
      onClose={() => setOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Typography id="modal-modal-title" align="center" variant="h6" component="h2">
          {chosenBlock.titulo}
        </Typography>

        <Box sx={{ display: 'flex', justifyContent: 'space-around' }}>
          <StyledImage src={stoneImageExample} alt="Imagem do bloco" />
          <InfoBox>
            <Typography variant="subtitle1"><strong>Material:</strong> {chosenBlock.material}</Typography>
            <Typography variant="subtitle1"><strong>Valor:</strong> {chosenBlock.valor}</Typography>
            <Typography variant="subtitle1"><strong>Data de criação:</strong> {`${formatDate(chosenBlock.data_criacao ?? '')}`}</Typography>
          </InfoBox>
        </Box>
      </Box>
    </Modal>
  );
}
