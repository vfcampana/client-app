import React, { useEffect } from 'react';
import { Box, CssBaseline } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AppRoutes from './routes/Routes';
import { useAuth } from './hooks/useAuth';
import Navbar from './components/Navbar';
import { BrowserRouter } from 'react-router-dom';
import { RootState } from './redux/root-reducer';
import { useSelector } from 'react-redux';
import ErrorBoundary from './components/ErrorBoundary';

const theme = createTheme({
  palette: {
    primary: {
      main: '#00334e',
      dark: '#001f2e',
      light: '#335c73',
      contrastText: '#fff',
    },
    background: {
      default: '#fff',
    },
    text: {
      primary: '#00334e',
      secondary: '#335c73',
    },
  },
});

const App: React.FC = () => {
  const { checkAuth } = useAuth();
  const {signed} = useSelector((state: RootState) => state.authReducer);

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <BrowserRouter>
          <Box className="App" minHeight="100vh" bgcolor="background.default">
            {signed && <Navbar />}
            <Box component="main" width="100%">
              <AppRoutes />
            </Box>
          </Box>
        </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  );
};

export default App;