import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Box, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
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
  Add,
  ArrowBackIos,
  ArrowForwardIos,
  CameraAlt,
  PhotoLibrary
} from '@mui/icons-material'
import { createBlock } from '../services/blocks'
import StyledButton from '../components/StyledButton'

const stoneImageExample = require('../assets/stone.png') as string

const BlockCreate: React.FC = () => {
  const navigate = useNavigate()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  
  const [form, setForm] = useState({ 
    titulo: '', 
    classificacao: '',
    coloracao: '',
    material: '',
    medida_bruta: '',
    volume_bruto: '',
    medida_liquida: '',
    volume_liquido: '',
    pedreira: '',
    observacoes: '',
    cep: '',
    logradouro: '',
    pais: '',
    cidade: '',
    estado: '',
    valor: '',
    status: 'privado' as 'privado' | 'anunciado'
  })
  const [saving, setSaving] = useState(false)
  const [imageFiles, setImageFiles] = useState<FileList | null>(null)
  const [imagePreviews, setImagePreviews] = useState<string[]>([stoneImageExample])
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  const [cameraSupported, setCameraSupported] = useState(false)

  // Verificar se a câmera está disponível
  useEffect(() => {
    const checkCameraSupport = async () => {
      try {
        if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
          const devices = await navigator.mediaDevices.enumerateDevices()
          const hasCamera = devices.some(device => device.kind === 'videoinput')
          setCameraSupported(hasCamera)
          console.log('📸 Câmera disponível:', hasCamera)
        } else {
          console.log('📸 MediaDevices API não suportada')
          setCameraSupported(false)
        }
      } catch (error) {
        console.log('📸 Erro ao verificar câmera:', error)
        setCameraSupported(false)
      }
    }
    
    checkCameraSupport()
  }, [])

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    console.log('🔍 Evento de mudança de arquivo disparado');
    console.log('📁 Arquivos selecionados:', files?.length || 0);
    
    if (files && files.length > 0) {
      console.log('📷 Processando', files.length, 'imagens...');
      setImageFiles(files)
      
      // Criar previews para todas as imagens
      const previews: string[] = []
      let loadedCount = 0
      
      Array.from(files).forEach((file, index) => {
        console.log(`  ${index + 1}. ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`);
        const reader = new FileReader()
        reader.onload = (e) => {
          previews[index] = e.target?.result as string
          loadedCount++
          
          if (loadedCount === files.length) {
            console.log('✅ Todos os previews carregados!');
            console.log('📸 Previews criados:', previews.length);
            setImagePreviews(previews)
            setCurrentImageIndex(0)
          }
        }
        reader.onerror = () => {
          console.error(`❌ Erro ao carregar preview da imagem ${index + 1}`);
        }
        reader.readAsDataURL(file)
      })
    } else {
      console.log('⚠️ Nenhum arquivo selecionado - voltando para imagem padrão');
      setImageFiles(null)
      setImagePreviews([stoneImageExample])
      setCurrentImageIndex(0)
    }
  }

  const handleCameraCapture = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    console.log('📸 Captura da câmera disparada');
    console.log('📁 Arquivos capturados:', files?.length || 0);
    
    if (files && files.length > 0) {
      // Se já existem imagens, adicionar as novas às existentes
      if (imageFiles && imageFiles.length > 0) {
        const existingFiles = Array.from(imageFiles)
        const newFiles = Array.from(files)
        const allFiles = [...existingFiles, ...newFiles]
        
        // Criar um novo FileList
        const dataTransfer = new DataTransfer()
        allFiles.forEach(file => dataTransfer.items.add(file))
        const newFileList = dataTransfer.files
        
        setImageFiles(newFileList)
        
        // Criar previews para todas as imagens (existentes + novas)
        const previews: string[] = []
        let loadedCount = 0
        
        allFiles.forEach((file, index) => {
          const reader = new FileReader()
          reader.onload = (e) => {
            previews[index] = e.target?.result as string
            loadedCount++
            
            if (loadedCount === allFiles.length) {
              console.log('✅ Todos os previews carregados (incluindo câmera)!');
              setImagePreviews(previews)
              setCurrentImageIndex(previews.length - newFiles.length) // Focar na primeira nova imagem
            }
          }
          reader.readAsDataURL(file)
        })
      } else {
        // Se não existem imagens, usar apenas as da câmera
        handleImageChange(event)
      }
    }
  }

  // Função para verificar se é dispositivo móvel
  const isMobileDevice = () => {
    return /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  }

  // Função para capturar foto usando MediaDevices API
  const handleCameraClick = async () => {
    if (!cameraSupported) {
      alert('Câmera não disponível neste dispositivo')
      return
    }

    try {
      console.log('📸 Iniciando captura via MediaDevices API...')
      
      // Tentar acessar a câmera
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: isMobileDevice() ? 'environment' : 'user',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        } 
      })

      // Criar um elemento de vídeo temporário
      const video = document.createElement('video')
      video.srcObject = stream
      video.autoplay = true
      video.playsInline = true

      // Aguardar o vídeo carregar
      await new Promise((resolve) => {
        video.onloadedmetadata = resolve
      })

      // Criar canvas para capturar a imagem
      const canvas = document.createElement('canvas')
      const context = canvas.getContext('2d')
      
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      // Desenhar o frame atual no canvas
      context?.drawImage(video, 0, 0)
      
      // Parar o stream
      stream.getTracks().forEach(track => track.stop())
      
      // Converter canvas para blob
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], `camera-${Date.now()}.jpg`, { type: 'image/jpeg' })
          
          // Simular o evento de input file
          const dataTransfer = new DataTransfer()
          dataTransfer.items.add(file)
          
          const mockEvent = {
            target: {
              files: dataTransfer.files
            }
          } as React.ChangeEvent<HTMLInputElement>
          
          handleCameraCapture(mockEvent)
          console.log('✅ Foto capturada com sucesso!')
        }
      }, 'image/jpeg', 0.8)

    } catch (error) {
      console.error('❌ Erro ao acessar câmera:', error)
      alert('Erro ao acessar a câmera. Verifique as permissões.')
    }
  }

  const handleSave = async () => {
  setSaving(true)
  try {
    // Criar FormData para enviar imagem
    const formData = new FormData()
    
    // Adicionar todos os campos obrigatórios
    formData.append('titulo', form.titulo)
    formData.append('classificacao', form.classificacao)
    formData.append('coloracao', form.coloracao)
    formData.append('material', form.material)
    formData.append('medida_bruta', form.medida_bruta)
    formData.append('volume_bruto', form.volume_bruto)
    formData.append('medida_liquida', form.medida_liquida)
    formData.append('volume_liquido', form.volume_liquido)
    formData.append('pedreira', form.pedreira)
    formData.append('observacoes', form.observacoes)
    formData.append('cep', form.cep)
    formData.append('logradouro', form.logradouro)
    formData.append('pais', form.pais)
    formData.append('cidade', form.cidade)
    formData.append('estado', form.estado)
    formData.append('valor', form.valor)
    formData.append('status', form.status === 'privado' ? '0' : '1')
    
    // Adicionar múltiplas imagens se existirem
    if (imageFiles && imageFiles.length > 0) {
      Array.from(imageFiles).forEach((file) => {
        formData.append('imagens', file)
      })
    }

    // Debug: Ver o que está sendo enviado
    console.log('FormData contents:');
    const entries = Array.from(formData.entries());
    entries.forEach(([key, value]) => {
      console.log(key, value);
    });

    await createBlock(formData)
    
    alert('Bloco criado com sucesso!')
    navigate('/Blocks')
  } catch (err) {
    console.error(err)
    alert('Erro ao criar bloco')
  } finally {
    setSaving(false)
  }
}

  const handleCancel = () => {
    navigate('/Blocks')
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
              {isMobile ? 'Novo Bloco' : 'Cadastrar Novo Bloco'}
            </Typography>
            <Stack 
              direction={isMobile ? 'column' : 'row'} 
              spacing={1} 
              sx={{ flexWrap: 'wrap' }}
            >
              <Chip
                label="Novo"
                size={isMobile ? 'small' : 'medium'}
                sx={{
                  backgroundColor: 'rgba(34, 197, 94, 0.2)',
                  color: '#22c55e',
                  border: '1px solid rgba(34, 197, 94, 0.3)',
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
          {/* Formulário de Cadastro */}
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
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Título"
                      required
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
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Material"
                      required
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
                  </Grid>
                </Grid>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Classificação"
                      required
                      value={form.classificacao}
                      onChange={(e) => setForm({ ...form, classificacao: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Coloração"
                      required
                      value={form.coloracao}
                      onChange={(e) => setForm({ ...form, coloracao: e.target.value })}
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
                  </Grid>
                </Grid>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Medida Bruta"
                      required
                      value={form.medida_bruta}
                      onChange={(e) => setForm({ ...form, medida_bruta: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Volume Bruto"
                      required
                      value={form.volume_bruto}
                      onChange={(e) => setForm({ ...form, volume_bruto: e.target.value })}
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
                  </Grid>
                </Grid>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Medida Líquida"
                      required
                      value={form.medida_liquida}
                      onChange={(e) => setForm({ ...form, medida_liquida: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Volume Líquido"
                      required
                      value={form.volume_liquido}
                      onChange={(e) => setForm({ ...form, volume_liquido: e.target.value })}
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
                  </Grid>
                </Grid>

                <TextField
                  fullWidth
                  label="Pedreira"
                  required
                  value={form.pedreira}
                  onChange={(e) => setForm({ ...form, pedreira: e.target.value })}
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

                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="CEP"
                      required
                      value={form.cep}
                      onChange={(e) => setForm({ ...form, cep: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={8}>
                    <TextField
                      fullWidth
                      label="Logradouro"
                      required
                      value={form.logradouro}
                      onChange={(e) => setForm({ ...form, logradouro: e.target.value })}
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
                  </Grid>
                </Grid>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="Cidade"
                      required
                      value={form.cidade}
                      onChange={(e) => setForm({ ...form, cidade: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="Estado"
                      required
                      value={form.estado}
                      onChange={(e) => setForm({ ...form, estado: e.target.value })}
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
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="País"
                      required
                      value={form.pais}
                      onChange={(e) => setForm({ ...form, pais: e.target.value })}
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
                  </Grid>
                </Grid>

                <TextField
                  fullWidth
                  label="Valor"
                  type="number"
                  required
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

          {/* Upload de Imagem */}
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
                border: '2px dashed #001f2e',
                mb: 2,
                position: 'relative',
                backgroundColor: '#f8fafc'
              }}>
                {/* Imagem principal */}
                <img 
                  src={imagePreviews[currentImageIndex]}
                  alt="Preview do bloco"
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                />
                
                {/* Navegação do carrossel */}
                {imageFiles && imageFiles.length > 1 && (
                  <>
                    <IconButton
                      sx={{
                        position: 'absolute',
                        left: 8,
                        top: '50%',
                        transform: 'translateY(-50%)',
                        bgcolor: 'rgba(0, 0, 0, 0.5)',
                        color: 'white',
                        '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.7)' }
                      }}
                      onClick={() => setCurrentImageIndex((prev) => 
                        prev === 0 ? imagePreviews.length - 1 : prev - 1
                      )}
                    >
                      <ArrowBackIos />
                    </IconButton>
                    
                    <IconButton
                      sx={{
                        position: 'absolute',
                        right: 8,
                        top: '50%',
                        transform: 'translateY(-50%)',
                        bgcolor: 'rgba(0, 0, 0, 0.5)',
                        color: 'white',
                        '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.7)' }
                      }}
                      onClick={() => setCurrentImageIndex((prev) => 
                        (prev + 1) % imagePreviews.length
                      )}
                    >
                      <ArrowForwardIos />
                    </IconButton>
                    
                    {/* Indicadores */}
                    <Box
                      sx={{
                        position: 'absolute',
                        bottom: 8,
                        left: '50%',
                        transform: 'translateX(-50%)',
                        display: 'flex',
                        gap: 1
                      }}
                    >
                      {imagePreviews.map((_, index) => (
                        <Box
                          key={index}
                          sx={{
                            width: 8,
                            height: 8,
                            borderRadius: '50%',
                            bgcolor: index === currentImageIndex ? 'white' : 'rgba(255, 255, 255, 0.5)',
                            cursor: 'pointer'
                          }}
                          onClick={() => setCurrentImageIndex(index)}
                        />
                      ))}
                    </Box>
                  </>
                )}
                
                {/* Contador de imagens */}
                {imageFiles && imageFiles.length > 1 && (
                  <Chip
                    label={`${currentImageIndex + 1}/${imagePreviews.length}`}
                    size="small"
                    sx={{
                      position: 'absolute',
                      top: 8,
                      right: 8,
                      bgcolor: 'rgba(0, 0, 0, 0.7)',
                      color: 'white'
                    }}
                  />
                )}
                

              </Box>

              <Stack spacing={1.5}>
                <Button
                  variant="outlined"
                  fullWidth
                  component="label"
                  startIcon={<PhotoLibrary />}
                  sx={{
                    backgroundColor: '#f0f9ff',
                    color: '#001f2e',
                    borderColor: '#001f2e',
                    cursor: 'pointer',
                    textTransform: 'none',
                    '&:hover': {
                      backgroundColor: 'transparent',
                      borderColor: '#003547'
                    }
                  }}
                >
                  {imageFiles && imageFiles.length > 0 ? 
                    `📷 Alterar da Galeria (${imageFiles.length} selecionadas)` : 
                    '📷 Selecionar da Galeria'
                  }
                  <input
                    type="file"
                    hidden
                    accept="image/*"
                    multiple
                    onChange={handleImageChange}
                  />
                </Button>

                <Button
                  variant="contained"
                  fullWidth
                  onClick={cameraSupported ? handleCameraClick : undefined}
                  component={cameraSupported ? "button" : "label"}
                  startIcon={<CameraAlt />}
                  sx={{
                    backgroundColor: '#001f2e',
                    color: 'white',
                    cursor: 'pointer',
                    textTransform: 'none',
                    '&:hover': {
                      backgroundColor: '#003547'
                    }
                  }}
                >
                  📸 {cameraSupported ? 'Tirar Foto' : 'Selecionar da Câmera'}
                  {!cameraSupported && (
                    <input
                      type="file"
                      hidden
                      accept="image/*"
                      capture={isMobileDevice() ? "environment" : true}
                      onChange={handleCameraCapture}
                    />
                  )}
                </Button>
              </Stack>

                {/* Informações sobre imagens selecionadas */}
                {imageFiles && imageFiles.length > 0 && (
                  <Box sx={{ mt: 2, p: 2, bgcolor: '#f8fafc', borderRadius: 1 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      📷 {imageFiles.length} imagem(ns) selecionada(s):
                    </Typography>
                    {Array.from(imageFiles).slice(0, 3).map((file, index) => (
                      <Typography key={index} variant="caption" display="block">
                        • {file.name}
                      </Typography>
                    ))}
                    {imageFiles.length > 3 && (
                      <Typography variant="caption" color="text.secondary">
                        ... e mais {imageFiles.length - 3} arquivo(s)
                      </Typography>
                    )}
                  </Box>
                )}

              {/* Informações */}
              <Box sx={{ mt: 3 }}>
                <Typography 
                  variant={isMobile ? 'subtitle2' : 'h6'} 
                  sx={{ 
                    mb: 2, 
                    color: '#001f2e', 
                    fontWeight: 600 
                  }}
                >
                  Dicas
                </Typography>

                <Stack spacing={1.5}>
                  <Box sx={{
                    padding: 1.5,
                    backgroundColor: '#f0f9ff',
                    border: '1px solid #3b82f6',
                    borderRadius: 2,
                  }}>
                    <Typography variant="body2" color="#1e40af" sx={{ fontWeight: 500 }}>
                      📷 IMAGENS & 📸 CÂMERA
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#1e40af' }}>
                      Use a galeria para múltiplas fotos ou tire fotos direto da câmera
                    </Typography>
                  </Box>

                  <Box sx={{
                    padding: 1.5,
                    backgroundColor: '#f0fdf4',
                    border: '1px solid #22c55e',
                    borderRadius: 2,
                  }}>
                    <Typography variant="body2" color="#15803d" sx={{ fontWeight: 500 }}>
                      💡 STATUS
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#15803d' }}>
                      Privado: Apenas você verá. Anunciado: Visível no mercado
                    </Typography>
                  </Box>

                  <Box sx={{
                    padding: 1.5,
                    backgroundColor: '#fef3f2',
                    border: '1px solid #ef4444',
                    borderRadius: 2,
                  }}>
                    <Typography variant="body2" color="#dc2626" sx={{ fontWeight: 500 }}>
                      📱 CÂMERA {cameraSupported ? '✅' : '❌'}
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#dc2626' }}>
                      {cameraSupported 
                        ? (isMobileDevice() 
                            ? 'Câmera detectada! Clique para abrir a câmera traseira' 
                            : 'Câmera detectada! Clique para abrir sua webcam')
                        : 'Câmera não detectada. Será usado o seletor de arquivos'
                      }
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

export default BlockCreate