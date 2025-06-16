import * as React from 'react';
import TopBar from '../components/topbar/TopBar';
import { Box } from '@mui/material';
import MyLotes from '../components/lotes/MyLotesList';

export default () => {

    return(
        <Box>
            <TopBar title='MEUS LOTES'></TopBar>
            <MyLotes/>
        </Box>
    );
}