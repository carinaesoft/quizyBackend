import React from "react";
import { AppBar, Toolbar, Typography, Button, Container } from "@mui/material";

/*
Challenge: Build the Navbar component.
Check the Figma file for the design specifics.
*/

export default function Navibar() {
    return (
        <AppBar position="static" color="default">
            <Container>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        React-MUI
                    </Typography>
                    <Button color="inherit" href="#home">Home</Button>
                    {/* Add more buttons or other elements as needed */}
                </Toolbar>
            </Container>
        </AppBar>
    );
}
