import React, { ReactElement } from 'react';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import { Link } from 'react-router-dom';

interface TopIconProps {
  icon: ReactElement;
  label: string;
  route: string;
}

const TopIcon: React.FC<TopIconProps> = ({ icon, label, route }) => {
  return (
    <Tooltip title={label} arrow>
      <IconButton color="inherit" component={Link} to={route}>
        {icon}
      </IconButton>
    </Tooltip>
  );
};

export default TopIcon;