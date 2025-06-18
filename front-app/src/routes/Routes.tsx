import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SignUp from '../pages/SignUp';
import SignIn from '../pages/SignIn';
import Home from '../pages/Home';
import Blocks from '../pages/Blocks';
import Market from '../pages/Market';
import Chat from '../pages/Chat';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/root-reducer';
import Lotes from '../pages/Lotes';
import BlockDetailsRoute from './BlockDetailsRoute';

interface props {
    signed : boolean,
    Item : React.ComponentType<any>
}

const Private = ({ signed, Item } : props) => {
  return signed ? <Item/> : <SignIn/>
}

const Public = ({ signed, Item } : props) => {
  return !signed ? <Item/> : <Navigate to="/Home" replace />
}

const AppRoutes: React.FC = () => {
  const { signed } = useSelector((state : RootState) => state.authReducer)

  return (
    <Routes>
    <Route path="/" element={<Public signed={signed} Item={SignIn} />} />
      <Route path="/SignUp" element={<Public signed={signed} Item={SignUp} />} />
      <Route path="/Home" element={<Private signed={signed} Item={Home} />} />
      <Route path="/Blocks" element={<Private signed={signed} Item={Blocks} />} /> {/*Esse tem recursos legais para usar em algo como "MEUS BLOCOS"*/}
      <Route path="/Market" element={<Private signed={signed} Item={Market} />} />
      <Route path="/Chat" element={<Private signed={signed} Item={Chat} />} />{/* nao serve */}
      <Route path="/Lotes" element={<Private signed={signed} Item={Lotes} />} /> {/* nao serve */}
      <Route path="/blocks/:id" element={<BlockDetailsRoute />} />
    </Routes>
  );
};

export default AppRoutes;