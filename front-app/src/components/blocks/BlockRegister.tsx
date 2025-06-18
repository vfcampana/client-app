import * as React from 'react';
import StyledButton from '../StyledButton';
import { TextField, Stack, Box, Modal, Typography, Alert } from '@mui/material';
import { useEffect, useReducer, useState } from 'react';
import { Block } from '../../types/Blocks';
import { createBlock } from '../../services/blocks';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 700,
  bgcolor: 'background.paper',
  border: '2px solid #0d1b2a',
  borderRadius: 4,
  boxShadow: 24,
  p: 4,
};

interface BlockModalProps {
  open: boolean;
  onClose: () => void;
}

export default function BlockModal({ open, onClose }: BlockModalProps) {
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const initialState: Block = {
  id: 0,
  titulo: '', 
  classificacao: '', 
  coloracao: '', 
  material: '',
  medida_bruta: '', 
  medida_liquida: '', 
  volume_bruto: '', 
  volume_liquido: '', 
  pedreira: '', 
  cep: '',
  valor: '', 
  status: '', 
  observacoes: '',
  logradouro: '',
  pais: '',
  cidade: '',
  estado: '',
  data_criacao: '',
  data_alteracao: '',
  imagem: '',
  id_usuario: 0,
};
  
  // useReducer : gerenciamento de estado complexo
  function reducer(state: Block, action: { type: string, payload: string }) {
    return { ...state, [action.type]: action.payload };
  }
  const [formData, dispatch] = useReducer(reducer, initialState);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch({ 
      type: e.target.name as keyof Block, 
      payload: e.target.value 
    }); // recebe uma action como parametro
  };

  // React Query : gerenciamento de requests
  const queryClient = useQueryClient();
  const { mutate: newBlock } = useMutation({
    mutationFn: createBlock,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['blocos'] });
    },
  });
  
  const handleSubmit = async (event : React.FormEvent) => {
    event.preventDefault()
    try{
      newBlock(formData)
      setSuccessMessage('Bloco cadastrado com sucesso!');
    } catch(err : any) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('Erro inesperado ao cadastrar bloco');
      }
    }
  }

  useEffect(() => {
    if (successMessage) {
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  }, [successMessage]);
  
  useEffect(() => {
    if (error) {
      setTimeout(() => setError(''), 5000);
    }
  }, [error]);


  return (
    <div>
      {/*
        A abertura do modal externamente deve ser feito assim:
        <StyledButton onClick={() => setIsModalOpen(true)}>CADASTRAR</StyledButton>
        <BlockModal open={isModalOpen} onClose={() => setIsModalOpen(false)} />
      */}
      <Modal
        open={open}
        onClose={onClose}
      >
        <Box sx={style}>
            <Typography id="modal-modal-title" align='center' variant="h6" component="h2">
                CADASTRO DE BLOCOS
            </Typography>
            <Stack component='form' onSubmit={handleSubmit} marginTop={2} spacing={2}>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                      autoComplete="given-name"
                      name="titulo"
                      required
                      fullWidth
                      id="title"
                      label="Título"
                      autoFocus
                      value={formData.titulo}
                      onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="classificacao"
                      label="Classificação"
                      name="classificacao"
                      autoComplete="class"
                      value={formData.classificacao}
                      onChange={handleChange}
                    />
                </Box>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                    required
                    fullWidth
                    id="color"
                    label="Coloração"
                    name="coloracao"
                    autoComplete="color"
                    value={formData.coloracao}
                    onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="material"
                      label="Material"
                      name="material"
                      autoComplete="material"
                      value={formData.material}
                      onChange={handleChange}
                    />
                </Box>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                    required
                    fullWidth
                    id="measure"
                    label="Medida Bruta"
                    name="medida_bruta"
                    autoComplete="measure"
                    value={formData.medida_bruta}
                    onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="volume"
                      label="Volume Bruto"
                      name="volume_bruto"
                      autoComplete="volume"
                      value={formData.volume_bruto}
                      onChange={handleChange}
                    />
                </Box>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                    required
                    fullWidth
                    id="measureL"
                    label="Medida Líquida"
                    name="medida_liquida"
                    autoComplete="measureL"
                    value={formData.medida_liquida}
                    onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="volumeL"
                      label="Volume Líquido"
                      name="volume_liquido"
                      autoComplete="volumeL"
                      value={formData.volume_liquido}
                      onChange={handleChange}
                    />
                </Box>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                      required
                      fullWidth
                      id="pedreira"
                      label="Pedreira"
                      name="pedreira"
                      autoComplete="pedreira"
                      value={formData.pedreira}
                      onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="cep"
                      label="CEP"
                      name="cep"
                      autoComplete="cep"
                      value={formData.cep}
                      onChange={handleChange}
                    />
                </Box>
                <Box sx={{display:'flex', gap: 2}}>
                    <TextField
                      required
                      fullWidth
                      id="value"
                      label="Valor"
                      name="valor"
                      autoComplete="value"
                      value={formData.valor}
                      onChange={handleChange}
                    />
                    <TextField
                      required
                      fullWidth
                      id="status"
                      label="Status"
                      name="status"
                      autoComplete="status"
                      value={formData.status}
                      onChange={handleChange}
                    />
                </Box>
                <TextField
                  required
                  fullWidth
                  id="obs"
                  label="Observações"
                  name="observacoes"
                  autoComplete="obs"
                  multiline
                  minRows={2}
                  value={formData.observacoes}
                  onChange={handleChange}
                />
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}
                {successMessage && (
                  <Alert severity="success" sx={{ mb: 2 }}>
                    {successMessage}
                  </Alert>
                )}
                <StyledButton
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                  Cadastrar
                </StyledButton>
            </Stack>
        </Box>
      </Modal>
    </div>
  );
}
