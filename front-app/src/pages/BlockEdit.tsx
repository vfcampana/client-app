import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  Box, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Skeleton,
  IconButton,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Stack,
  Grid,
  useTheme,
  useMediaQuery,
  Chip
} from '@mui/material'
import { 
  ArrowBack, 
  Save, 
  Cancel, 
  PhotoCamera,
  Edit 
} from '@mui/icons-material'
import { useBlocks } from '../hooks/useBlocks'
import { updateBlock } from '../services/blocks'
import StyledButton from '../components/StyledButton'

const stoneImageExample = require('../assets/stone.png') as string

const BlockEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const { blocks, loading, error, refetch } = useBlocks()
  
  const [form, setForm] = useState({ 
    titulo: '', 
    observacoes: '',
    material: '',
    valor: '',
    status: 'privado' as 'privado' | 'anunciado'
  })
  const [saving, setSaving] = useState(false)
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string>('')

  // Encontrar o bloco específico
  const block = blocks.find(b => b.id === Number(id))

  // Função para converter status do banco (0/1) para texto
  const getStatusText = (status: number | string): 'privado' | 'anunciado' => {
    if (typeof status === 'number') {
      return status === 0 ? 'privado' : 'anunciado'
    }
    return status as 'privado' | 'anunciado'
  }

  // Função para converter status de texto para número
  const getStatusNumber = (status: 'privado' | 'anunciado'): number => {
    return status === 'privado' ? 0 : 1
  }

  // Carregar dados do bloco quando encontrado
  useEffect(() => {
    if (block) {
      setForm({
        titulo: block.titulo || '',
        observacoes: block.observacoes || '',
        material: block.material || '',
        valor: block.valor?.toString() || '0',
        status: getStatusText(block.status || 0)
      })
      setImagePreview(block.imagem || stoneImageExample)
    }
  }, [block])

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setImageFile(file)
      const reader = new FileReader()
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      // Criar FormData para enviar imagem
      const formData = new FormData()
      formData.append('titulo', form.titulo)
      formData.append('observacoes', form.observacoes)
      formData.append('material', form.material)
      formData.append('valor', form.valor)
      formData.append('status', getStatusNumber(form.status).toString())
      
      if (imageFile) {
        formData.append('imagem', imageFile)
      }

      await updateBlock(Number(id), formData)
      
      await refetch()
      alert('Bloco atualizado com sucesso!')
      navigate('/Blocks')
    } catch (err) {
      console.error(err)
      alert('Erro ao salvar bloco')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    navigate('/Blocks')
  }

  if (loading) {
    return (
      <Box sx={{ 
        padding: { xs: 1, sm: 2, md: 4 }, 
        maxWidth: '1200px', 
        margin: '0 auto' 
      }}>
        <Stack spacing={2}>
          <Skeleton variant="rectangular" width="100%" height={120} sx={{ borderRadius: 3 }} />
          <Skeleton variant="rectangular" width="100%" height={300} sx={{ borderRadius: 3 }} />
          <Skeleton variant="rectangular" width="100%" height={200} sx={{ borderRadius: 3 }} />
        </Stack>
      </Box>
    )
  }

  if (error || !block) {
    return (
      <Box sx={{ 
        padding: { xs: 2, sm: 3, md: 4 }, 
        maxWidth: '1200px', 
        margin: '0 auto',
        textAlign: 'center'
      }}>
        <Typography variant={isMobile ? 'h6' : 'h5'} color="error" sx={{ mb: 2 }}>
          Bloco não encontrado
        </Typography>
        <Button 
          onClick={() => navigate('/Blocks')} 
          sx={{ mt: 2 }}
          variant="contained"
          fullWidth={isMobile}
        >
          Voltar
        </Button>
      </Box>
    )
  }

  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: '#f8fafc',
      padding: { xs: 1, sm: 2, md: 4 }
    }}>
      <Box sx={{ 
        maxWidth: '1200px', 
        margin: '0 auto',
        px: { xs: 1, sm: 0 }
      }}>
        {/* Header Responsivo */}
        <Paper sx={{
          background: 'linear-gradient(135deg, #001f2e 0%, #003547 100%)',
          color: 'white',
          padding: { xs: 2, sm: 2.5, md: 3 },
          borderRadius: { xs: 2, md: 3 },
          mb: { xs: 2, md: 3 },
          display: 'flex',
          flexDirection: { xs: 'column', sm: 'row' },
          alignItems: { xs: 'flex-start', sm: 'center' },
          gap: { xs: 2, sm: 2, md: 2 }
        }}>
          <IconButton 
            onClick={handleCancel}
            sx={{ 
              color: 'white',
              backgroundColor: 'rgba(255,255,255,0.15)',
              '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' },
              alignSelf: { xs: 'flex-start', sm: 'center' }
            }}
          >
            <ArrowBack />
          </IconButton>
          
          <Box sx={{ flex: 1, width: { xs: '100%', sm: 'auto' } }}>
            <Typography 
              variant={isMobile ? 'h5' : 'h4'} 
              sx={{ 
                fontWeight: 700, 
                mb: 1,
                wordBreak: 'break-word'
              }}
            >
              {isMobile ? 'Editando:' : 'Editando Bloco:'} {block.titulo}
            </Typography>
            <Stack 
              direction={isMobile ? 'column' : 'row'} 
              spacing={1} 
              sx={{ flexWrap: 'wrap' }}
            >
              <Chip
                label={`ID: ${block.id}`}
                size={isMobile ? 'small' : 'medium'}
                sx={{
                  backgroundColor: 'rgba(255,255,255,0.15)',
                  color: 'white',
                  border: '1px solid rgba(255,255,255,0.2)',
                  alignSelf: 'flex-start'
                }}
              />
              <Chip
                label={block.material || 'Material não informado'}
                size={isMobile ? 'small' : 'medium'}
                sx={{
                  backgroundColor: 'rgba(255,255,255,0.15)',
                  color: 'white',
                  border: '1px solid rgba(255,255,255,0.2)',
                  alignSelf: 'flex-start'
                }}
              />
            </Stack>
          </Box>

          <Stack 
            direction={isMobile ? 'column' : 'row'} 
            spacing={1}
            sx={{ 
              width: { xs: '100%', sm: 'auto' },
              mt: { xs: 1, sm: 0 }
            }}
          >
            <StyledButton
              variant="outlined"
              onClick={handleCancel}
              size={isMobile ? 'medium' : 'large'}
              fullWidth={isMobile}
              sx={{
                color: 'white',
                borderColor: 'rgba(255,255,255,0.5)',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: 'rgba(255,255,255,0.1)'
                }
              }}
              startIcon={<Cancel />}
            >
              Cancelar
            </StyledButton>
            <StyledButton
              variant="contained"
              onClick={handleSave}
              disabled={saving}
              size={isMobile ? 'medium' : 'large'}
              fullWidth={isMobile}
              sx={{
                backgroundColor: 'white',
                color: '#001f2e',
                '&:hover': {
                  backgroundColor: '#f8fafc'
                }
              }}
              startIcon={<Save />}
            >
              {saving ? 'Salvando...' : 'Salvar'}
            </StyledButton>
          </Stack>
        </Paper>

        {/* Conteúdo Principal */}
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* Formulário de Edição */}
          <Grid item xs={12} lg={8}>
            <Paper sx={{ 
              padding: { xs: 2, sm: 2.5, md: 3 }, 
              borderRadius: { xs: 2, md: 3 },
              height: 'fit-content'
            }}>
              <Typography 
                variant={isMobile ? 'subtitle1' : 'h6'} 
                sx={{ 
                  mb: { xs: 2, md: 3 }, 
                  color: '#001f2e', 
                  fontWeight: 600 
                }}
              >
                Informações do Bloco
              </Typography>

              <Stack spacing={{ xs: 2, md: 3 }}>
                <TextField
                  fullWidth
                  label="Título"
                  value={form.titulo}
                  onChange={(e) => setForm({ ...form, titulo: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
                  sx={{ 
                    '& .MuiOutlinedInput-root': {
                      '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#001f2e',
                      },
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: '#001f2e',
                    },
                  }}
                />

                <TextField
                  fullWidth
                  label="Material"
                  value={form.material}
                  onChange={(e) => setForm({ ...form, material: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
                  sx={{ 
                    '& .MuiOutlinedInput-root': {
                      '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#001f2e',
                      },
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: '#001f2e',
                    },
                  }}
                />

                <TextField
                  fullWidth
                  label="Valor"
                  type="number"
                  value={form.valor}
                  onChange={(e) => setForm({ ...form, valor: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
                  sx={{ 
                    '& .MuiOutlinedInput-root': {
                      '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#001f2e',
                      },
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: '#001f2e',
                    },
                  }}
                  InputProps={{
                    startAdornment: <Box sx={{ mr: 1, color: '#666' }}>R$</Box>,
                  }}
                />

                <TextField
                  fullWidth
                  label="Observações"
                  multiline
                  rows={isMobile ? 3 : 4}
                  value={form.observacoes}
                  onChange={(e) => setForm({ ...form, observacoes: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
                  sx={{ 
                    '& .MuiOutlinedInput-root': {
                      '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#001f2e',
                      },
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: '#001f2e',
                    },
                  }}
                />

                <FormControl>
                  <FormLabel 
                    sx={{ 
                      color: '#001f2e', 
                      fontWeight: 600,
                      fontSize: { xs: '0.875rem', md: '1rem' },
                      '&.Mui-focused': {
                        color: '#001f2e',
                      },
                    }}
                  >
                    Status do Bloco
                  </FormLabel>
                  <RadioGroup
                    value={form.status}
                    onChange={(e) => setForm({ ...form, status: e.target.value as 'privado' | 'anunciado' })}
                    sx={{ mt: 1 }}
                    row={!isMobile}
                  >
                    <FormControlLabel 
                      value="privado" 
                      control={
                        <Radio 
                          sx={{
                            color: '#001f2e',
                            '&.Mui-checked': {
                              color: '#001f2e',
                            },
                          }}
                        />
                      } 
                      label="Privado"
                      sx={{
                        '& .MuiFormControlLabel-label': {
                          fontSize: { xs: '0.875rem', md: '1rem' }
                        }
                      }}
                    />
                    <FormControlLabel 
                      value="anunciado" 
                      control={
                        <Radio 
                          sx={{
                            color: '#001f2e',
                            '&.Mui-checked': {
                              color: '#001f2e',
                            },
                          }}
                        />
                      } 
                      label="Anunciado"
                      sx={{
                        '& .MuiFormControlLabel-label': {
                          fontSize: { xs: '0.875rem', md: '1rem' }
                        }
                      }}
                    />
                  </RadioGroup>
                </FormControl>
              </Stack>
            </Paper>
          </Grid>

          {/* Imagem do Bloco */}
          <Grid item xs={12} lg={4}>
            <Paper sx={{ 
              padding: { xs: 2, sm: 2.5, md: 3 }, 
              borderRadius: { xs: 2, md: 3 },
              height: 'fit-content'
            }}>
              <Typography 
                variant={isMobile ? 'subtitle1' : 'h6'} 
                sx={{ 
                  mb: { xs: 2, md: 3 }, 
                  color: '#001f2e', 
                  fontWeight: 600 
                }}
              >
                Imagem do Bloco
              </Typography>

              <Box sx={{
                width: '100%',
                height: { xs: 200, sm: 250, md: 300 },
                borderRadius: 2,
                overflow: 'hidden',
                border: '2px solid #001f2e',
                mb: 2,
                position: 'relative'
              }}>
                <img 
                  src={imagePreview}
                  alt={`Imagem do bloco ${block.titulo}`}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src = stoneImageExample;
                  }}
                />
                
                {/* Overlay para alterar imagem */}
                <Box sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  backgroundColor: 'rgba(0, 0, 0, 0.5)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  opacity: 0,
                  '&:hover': {
                    opacity: 1
                  },
                  transition: 'opacity 0.3s ease'
                }}>
                  <IconButton
                    component="label"
                    sx={{
                      backgroundColor: 'white',
                      color: '#001f2e',
                      '&:hover': {
                        backgroundColor: '#f8fafc'
                      }
                    }}
                  >
                    <PhotoCamera />
                    <input
                      type="file"
                      hidden
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                  </IconButton>
                </Box>
              </Box>

              <Button
                variant="outlined"
                component="label"
                fullWidth
                startIcon={<PhotoCamera />}
                sx={{
                  color: '#001f2e',
                  borderColor: '#001f2e',
                  '&:hover': {
                    backgroundColor: '#f0f9ff',
                    borderColor: '#003547'
                  }
                }}
              >
                Alterar Imagem
                <input
                  type="file"
                  hidden
                  accept="image/*"
                  onChange={handleImageChange}
                />
              </Button>

              {/* Informações Atuais */}
              <Box sx={{ mt: 3 }}>
                <Typography 
                  variant={isMobile ? 'subtitle2' : 'h6'} 
                  sx={{ 
                    mb: 2, 
                    color: '#001f2e', 
                    fontWeight: 600 
                  }}
                >
                  Informações Atuais
                </Typography>

                <Stack spacing={1.5}>
                  <Box sx={{
                    padding: 1.5,
                    backgroundColor: '#f0fdf4',
                    border: '1px solid #bbf7d0',
                    borderRadius: 2,
                  }}>
                    <Typography variant="body2" color="#065f46" sx={{ fontWeight: 500 }}>
                      VALOR ATUAL
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 700, color: '#065f46' }}>
                      R$ {block.valor || '0.00'}
                    </Typography>
                  </Box>

                  <Box sx={{
                    padding: 1.5,
                    backgroundColor: '#fef3c7',
                    border: '1px solid #fcd34d',
                    borderRadius: 2,
                  }}>
                    <Typography variant="body2" color="#92400e" sx={{ fontWeight: 500 }}>
                      STATUS ATUAL
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 600, color: '#92400e' }}>
                      {getStatusText(block.status || 0) === 'privado' ? 'Privado' : 'Anunciado'}
                    </Typography>
                  </Box>
                </Stack>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  )
}

export default BlockEdit