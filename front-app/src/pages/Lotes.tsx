import * as React from 'react';
import { Box } from '@mui/material';
import CreateLoteModal from '../components/lotes/CreateLoteModal';

export default () => {

    return(
        <Box>
            <CreateLoteModal open={false} onClose={function (): void {
                throw new Error('Function not implemented.');
            } } selectedBlocks={[]} blocks={[]} onSuccess={function (): void {
                throw new Error('Function not implemented.');
            } } />
        </Box>
    );
}