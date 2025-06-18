import * as React from 'react';
import SearchBar from '../components/SearchBar';
import { Box } from '@mui/material';
import BlockList from '../components/blocks/BlockList'
import { useState } from 'react';

export default () => {
    const [searchTerm, setSearchTerm] = useState('');

    return(
        <Box>
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
            <BlockList/>
        </Box>
    );
}