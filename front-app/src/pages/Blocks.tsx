import * as React from 'react';
import TopBar from '../components/topbar/TopBar';
import { Box } from '@mui/material';
import MyBlocks from '../components/blocks/MyBlocksList';

export default () => {

    return(
        <Box>
            <TopBar title='MEUS BLOCOS'></TopBar>
            <MyBlocks/>
        </Box>
    );
}