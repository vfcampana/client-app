import React, { useState } from 'react';
import {
    AppBar,
    Toolbar,
    Typography,
    Button,
    IconButton,
    Drawer,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Box,
    useTheme,
    useMediaQuery,
} from '@mui/material';
import {
    Menu as MenuIcon,
    Home as HomeIcon,
    Star as StarIcon,
    ViewInAr as ViewInArIcon,
    Business as BusinessIcon,
    Chat as ChatIcon,
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { LogOutIcon } from 'lucide-react';

export default function Navbar() {
    const [mobileOpen, setMobileOpen] = useState(false);
    const theme = useTheme();
    const navigate = useNavigate();
    const { exit } = useAuth();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));

    const handleExit = async () => {
        console.log('Tentando sair...');
        const sucess = await exit();
        if (sucess) {
            console.log('Usuário saiu com sucesso');    
            navigate('/')
        }

    }

    const menuItems = [
        { icon: <HomeIcon />, label: 'Home', route: '/home' },
        { icon: <StarIcon />, label: 'Favoritos', route: '/favorites' },
        { icon: <ViewInArIcon />, label: 'Meus Blocos', route: '/blocks' },
        { icon: <BusinessIcon />, label: 'Meus Lotes', route: '/lotes' },
        { icon: <ChatIcon />, label: 'Chat', route: '/chat' },
        { icon: <LogOutIcon />, label: 'Sair', action: handleExit },
    ];

    const handleDrawerToggle = () => {
        setMobileOpen((prevOpen) => !prevOpen);
    };

    const handleMenuClick = (route) => {
        console.log(`Navegando para: ${route}`);
        navigate(route);
        setMobileOpen(false);
    };

    return (
        <>
            <AppBar
                position="sticky"
                sx={{
                    background: theme.palette.primary.dark,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                }}
            >
                <Toolbar>
                    <Typography
                        variant="h5"
                        component="div"
                        sx={{
                            fontWeight: 'bold',
                            background: 'linear-gradient(45deg, #FFF 30%, #E3F2FD 90%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            display: 'flex',
                            alignItems: 'center',
                            minHeight: 56,
                        }}
                    >
                        <img
                            src="/assets/stone.png"
                            style={{
                                width: isMobile ? '60px' : '80px',
                                height: isMobile ? '60px' : '80px',
                                verticalAlign: 'middle',
                                marginRight: isMobile ? 1 : 2,
                                transition: 'width 0.2s, height 0.2s',
                            }}
                            alt="Logo"
                        />
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    {!isMobile && (
                        <Box sx={{ display: 'flex', gap: 1 }}>
                            {menuItems.map((item, index) => (
                                <Button
                                    key={index}
                                    color="inherit"
                                    startIcon={item.icon}
                                    onClick={() => item.action ? item.action() : handleMenuClick(item.route)}
                                    sx={{
                                        px: 2,
                                        py: 1,
                                        borderRadius: 2,
                                        textTransform: 'none',
                                        fontWeight: 500,
                                        '&:hover': {
                                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                            transform: 'translateY(-2px)',
                                            transition: 'all 0.2s ease-in-out',
                                        },
                                        transition: 'all 0.2s ease-in-out',
                                    }}
                                >
                                    {item.label}
                                </Button>
                            ))}
                        </Box>
                    )}

                    {isMobile && (
                        <IconButton
                            color="inherit"
                            aria-label="open drawer"
                            edge="end"
                            onClick={handleDrawerToggle}
                            sx={{
                                '&:hover': {
                                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                    transform: 'scale(1.1)',
                                    transition: 'all 0.2s ease-in-out',
                                },
                                transition: 'all 0.2s ease-in-out',
                            }}
                        >
                            <MenuIcon />
                        </IconButton>
                    )}
                </Toolbar>
            </AppBar>

            <Drawer
                variant="temporary"
                anchor="right"
                open={mobileOpen}
                onClose={handleDrawerToggle}
                ModalProps={{
                    keepMounted: true,
                }}
                sx={{
                    display: { xs: 'block', md: 'none' },
                    '& .MuiDrawer-paper': {
                        boxSizing: 'border-box',
                        width: 250,
                        backgroundColor: theme.palette.primary.dark,
                    },
                }}
            >
                <Box sx={{ width: 250 }}>
                    <Box sx={{ p: 2, textAlign: 'center' }}>
                        <img
                            src="/assets/stone.png"
                            alt="MOGAI Logo"
                            style={{ width: '60px', height: '70px', verticalAlign: 'middle' }}
                        />
                        <Typography
                            variant="h6"
                            sx={{
                                fontWeight: 'bold',
                                background: theme.palette.primary.dark,
                                WebkitBackgroundClip: 'text',
                                WebkitTextFillColor: 'transparent',
                            }}
                        ></Typography>
                    </Box>
                    <List>
                        {menuItems.map((item, index) => (
                            <ListItem
                                button
                                key={index}
                                onClick={() => item.action ? item.action() : handleMenuClick(item.route)}
                                sx={{
                                    color: '#fff',
                                    '&:hover': {
                                        backgroundColor: 'rgba(255,255,255,0.12)',
                                        transform: 'translateX(8px)',
                                        transition: 'all 0.2s ease-in-out',
                                    },
                                    transition: 'all 0.2s ease-in-out',
                                }}
                            >
                                <ListItemIcon sx={{ color: '#fff' }}>
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.label}
                                    sx={{
                                        '& .MuiListItemText-primary': {
                                            fontWeight: 500,
                                            color: '#fff',
                                        },
                                    }}
                                />
                            </ListItem>
                        ))}
                    </List>
                </Box>
            </Drawer>
        </>
    );
}
