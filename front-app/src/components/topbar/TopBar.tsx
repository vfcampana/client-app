import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  useMediaQuery,
  useTheme,
  Button,
  InputBase,
  Divider,
} from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import ViewInArIcon from '@mui/icons-material/ViewInAr';
import Inventory2OutlinedIcon from '@mui/icons-material/Inventory2Outlined';
import SettingsIcon from '@mui/icons-material/Settings';
import NotificationsIcon from '@mui/icons-material/Notifications';
import PersonIcon from '@mui/icons-material/Person';
import TopIcon from './TopIcon';
import SettingsMenu from './SettingsIcon';

interface TopBarProps {
  title?: string;
}

// Styled Components
const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: '#0d1b2a', // Azul escuro similar ao tema
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
}));

const LogoContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginRight: theme.spacing(3),
  '& .MuiTypography-root': {
    fontWeight: 700,
    fontSize: '1.8rem',
    color: '#ffffff',
    letterSpacing: '0.5px',
    cursor: 'pointer',
    '&:hover': {
      opacity: 0.9,
    }
  }
}));

const SearchContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  borderRadius: '24px',
  marginRight: theme.spacing(2),
  marginLeft: theme.spacing(2),
  width: '100%',
  maxWidth: '400px',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.2),
  },
  '&:focus-within': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
    border: '1px solid rgba(255, 255, 255, 0.4)',
  }
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: 'rgba(255, 255, 255, 0.7)',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'white',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    fontSize: '0.9rem',
    '&::placeholder': {
      color: 'rgba(255, 255, 255, 0.7)',
      opacity: 1,
    }
  },
}));

const NavButton = styled(Button)(({ theme }) => ({
  color: 'white',
  textTransform: 'none',
  fontSize: '0.9rem',
  fontWeight: 500,
  padding: '8px 16px',
  borderRadius: '20px',
  marginRight: theme.spacing(1),
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.1),
    transform: 'translateY(-1px)',
  }
}));

const ActionButton = styled(Button)(({ theme }) => ({
  backgroundColor: '#f97316', // Laranja similar ao OLX
  color: 'white',
  textTransform: 'none',
  fontWeight: 600,
  padding: '10px 24px',
  borderRadius: '24px',
  marginLeft: theme.spacing(2),
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: '#ea580c',
    transform: 'translateY(-1px)',
    boxShadow: '0 4px 12px rgba(249, 115, 22, 0.3)',
  }
}));

const MobileDrawer = styled(Drawer)(({ theme }) => ({
  '& .MuiDrawer-paper': {
    width: 280,
    backgroundColor: '#0d1b2a',
    color: 'white',
  }
}));

const DrawerHeader = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: theme.spacing(2),
  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
}));

const MobileListItemButton = styled(ListItemButton)(({ theme }) => ({
  padding: theme.spacing(1.5, 2),
  borderRadius: '8px',
  margin: theme.spacing(0.5, 1),
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.1),
  },
  '& .MuiListItemIcon-root': {
    color: 'rgba(255, 255, 255, 0.8)',
    minWidth: '40px',
  },
  '& .MuiListItemText-primary': {
    fontSize: '0.95rem',
    fontWeight: 500,
  }
}));

const TopBar: React.FC<TopBarProps> = ({ title = "Dashboard" }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    { icon: <HomeIcon />, label: 'Home', route: '/Home' },
    { icon: <ShoppingCartIcon />, label: 'Comércio', route: '/Market' },
    { icon: <ViewInArIcon />, label: 'Meus Blocos', route: '/Blocks' },
    { icon: <Inventory2OutlinedIcon />, label: 'Meus Lotes', route: '/Lotes' },
    { icon: <ChatIcon />, label: 'Chat', route: '/Chat' },
  ];

  const mobileDrawer = (
    <MobileDrawer
      variant="temporary"
      anchor="left"
      open={mobileOpen}
      onClose={handleDrawerToggle}
      ModalProps={{ keepMounted: true }}
    >
      <DrawerHeader>
        <Typography variant="h6" sx={{ fontWeight: 700, fontSize: '1.5rem' }}>
          MOGAI
        </Typography>
        <IconButton onClick={handleDrawerToggle} sx={{ color: 'white' }}>
          <CloseIcon />
        </IconButton>
      </DrawerHeader>

    <List sx={{ flex: 1, pt: 2 }}>
      {menuItems.map((item) => (
        <MobileListItemButton key={item.label}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.label} />
        </MobileListItemButton>
      ))}

      <Divider sx={{ backgroundColor: 'rgba(255, 255, 255, 0.1)', margin: '16px' }} />

      <MobileListItemButton>
        <ListItemIcon><NotificationsIcon /></ListItemIcon>
        <ListItemText primary="Notificações" />
      </MobileListItemButton>

      <MobileListItemButton>
        <ListItemIcon><SettingsIcon /></ListItemIcon>
        <ListItemText primary="Configurações" />
      </MobileListItemButton>
    </List>
    </MobileDrawer>
  );

  return (
    <>
      <StyledAppBar position="static">
        <Toolbar sx={{ px: { xs: 2, md: 4 }, py: 1 }}>
          {/* Mobile Menu Button */}
          {isMobile && (
            <IconButton
              color="inherit"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}

          {/* Logo */}
          <LogoContainer>
            <Typography variant="h6" component="div">
              MOGAI
            </Typography>
          </LogoContainer>

          {/* Search Bar - Hidden on mobile */}
          {!isMobile && (
            <SearchContainer>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase
                placeholder={`Buscar em ${title}...`}
                inputProps={{ 'aria-label': 'search' }}
              />
            </SearchContainer>
          )}

          <Box sx={{ flexGrow: 1 }} />

          {/* Desktop Navigation */}
          {!isMobile && (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {menuItems.map((item) => (
                <TopIcon
                  key={item.label}
                  icon={item.icon}
                  label={item.label}
                  route={item.route}
                />
              ))}
              
              <IconButton sx={{ color: 'white', mx: 1 }}>
                <NotificationsIcon />
              </IconButton>
              
              <SettingsMenu label="Configurações" />
              
            </Box>
          )}
        </Toolbar>
      </StyledAppBar>

      {/* Mobile Drawer */}
      {mobileDrawer}
    </>
  );
};

export default TopBar;