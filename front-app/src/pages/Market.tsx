import * as React from 'react';
import TopBar from '../components/topbar/TopBar';
import SearchBar from '../components/SearchBar';
import { Box } from '@mui/material';
import BlockList from '../components/blocks/BlockList'
import { useState } from 'react';

export default () => {
    const [searchTerm, setSearchTerm] = useState('');

    return(
        <Box>
            <TopBar title='COMÉRCIO'></TopBar>
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
            <BlockList/>
        </Box>
    );
}