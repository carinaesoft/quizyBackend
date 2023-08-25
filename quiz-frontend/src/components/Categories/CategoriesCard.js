import React from "react";
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const CategoriesCard = ({ categories }) => {
    return (
        <Box
            display="flex"
            flexWrap="wrap"
            justifyContent="center"
            gap={2}
        >
            {categories.map((category, index) => (
                <Card key={index} sx={{ minWidth: 275 }}>
                    <CardContent>
                        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                            {category.description}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        <Button size="small">{category.name}</Button>
                    </CardActions>
                </Card>
            ))}
        </Box>
    );
};

export default CategoriesCard;
