import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import CNPJField from '../components/Cnpj';
import { useNavigate } from 'react-router-dom';
import { useContext, useState } from 'react';
import { AuthContext } from '../contexts/auth';
import { useAuth } from '../hooks/useAuth';
import Stack from '@mui/material/Stack';

// ??? FALTA UTILIZAR O REDUX AQUI
export default function SignUp() {
  const { signup } = useAuth();

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [document, setDocument] = useState('')
  const [phone, setPhone] = useState('')
  const [cep, setCep] = useState('')
  const [passwordError, setPasswordError] = useState('');
  const navigate = useNavigate();

  const handlesubmit = async (event: React.FormEvent) =>{
    event.preventDefault()  

    if (password !== confirmPassword) {
      setPasswordError("As senhas não coincidem");
      return;
    }

    const credentials = {
      nome : name,
      email : email, 
      documento : document, 
      senha : password, 
      telefone : phone, 
      cep : cep
    }
    console.log('Dados do cadastro:', credentials);
    const success = await signup(credentials)
    if (success) {
      navigate('/home')
    } else {
      window.alert('Email ou senha incorretos. Tente novamente.')
    }
  }

  return (
      <Container component="main" maxWidth="md"> {/* Aumentamos o tamanho do container */}
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5">
            Cadastro
          </Typography>
          <Box component="form" noValidate onSubmit={handlesubmit} sx={{ mt: 3, width:'100%' }}>
            <Stack spacing={2}>
              <TextField
                autoComplete="given-name"
                name="userName"
                required
                fullWidth
                id="userName"
                label="Nome Fantasia"
                autoFocus
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <CNPJField
                required
                fullWidth
                id="CNPJ"
                label="CNPJ"
                name="CNPJ"
                autoComplete="CNPJ"
                value={document}
                onChange={(e) => setDocument(e.target.value)}
              />
              <TextField
                required
                fullWidth
                id="email"
                label="Email"
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextField
                required
                fullWidth
                id="razaosocial"
                label="Razão Social"
                name="razaosocial"
                autoComplete="razaosocial"
                disabled
              />
              <TextField
                required
                fullWidth
                id="cep"
                label="Cep"
                name="cep"
                autoComplete="cep"
                value={cep}
                onChange={(e) => setCep(e.target.value)}
              />
              <TextField
                required
                fullWidth
                id="telefone"
                label="Telefone"
                name="telefone"
                autoComplete="telefone"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
              <TextField
                required
                fullWidth
                name="password"
                label="Senha"
                type="password"
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <TextField
                required
                fullWidth
                name="confpassword"
                label="Confirme Senha"
                type="password"
                id="confpassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                error={!!passwordError}
                helperText={passwordError}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Cadastrar
              </Button>
            </Stack>
            <Link href="/" variant="body1">
              Já possui uma conta? Faça login
            </Link>
          </Box>
        </Box>
      </Container>
  );
}