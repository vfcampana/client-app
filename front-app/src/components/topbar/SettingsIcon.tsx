import React, { useContext, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import SettingsIcon from '@mui/icons-material/Settings';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Tooltip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../contexts/auth';
import { useAuth } from '../../hooks/useAuth';

interface SettingsIconProps {
  label : string
}

const SettingsMenu: React.FC<SettingsIconProps> = ({label}) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { exit } = useAuth();

  // Funções para abrir e fechar o menu
  const handleClick = (event : any) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleExit = async () => {
    const success = await exit()
    if(success) {
      navigate('/')
    }
  }

  return (
    <div>
      {/* Botão de Configurações */}
      <Tooltip title={label}>
        <IconButton color="inherit" onClick={handleClick}>
          <SettingsIcon />
        </IconButton>
      </Tooltip>

      {/* Menu Dropdown */}
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        {/* Opções do menu */}
        <MenuItem onClick={handleClose}>
          Alterar dados
        </MenuItem>
        <MenuItem onClick={handleClose}>
          Histórico
        </MenuItem>
        <MenuItem onClick={handleExit}>
          Sair
        </MenuItem>
      </Menu>
    </div>
  );
};

export default SettingsMenu;
