import React from 'react';
import Box from '@mui/material/Box';
import Navibar from "./components/navbar"
import MainPage from "./components/mainPage"

function App() {
  return (
          <div>
            <Navibar/>
            <Box pt={2}> {/* This adds padding top of 2 units */}
                <MainPage/>
            </Box>

          </div>
  );
}

export default App;
