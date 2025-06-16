import * as React from 'react';
import TextField from '@mui/material/TextField';
// @ts-ignore
import InputMask from 'react-input-mask';
import { TextFieldProps } from '@mui/material/TextField';


// Componente para campo de CNPJ com mascara aplicada
const CNPJField: React.FC<TextFieldProps> = (props) => {
  const {onChange, value} = props;
  return (
    <InputMask mask="99.999.999/9999-99" maskChar={null} onChange={onChange} value={value}>
      {() => <TextField {...props} />}
    </InputMask>
  )
};

export default CNPJField;