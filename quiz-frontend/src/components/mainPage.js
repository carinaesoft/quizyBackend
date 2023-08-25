import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Card, CardContent, CardActionArea, Button } from '@mui/material';
import StarIcon from '@mui/icons-material/Star';

const QuizCard = ({ quiz }) => (
  <Card sx={{ maxWidth: 345 }}>
    <CardActionArea>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {quiz.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Questions: {quiz.number_of_questions}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Time: {quiz.time}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Difficulty: {quiz.difficulty}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Score to Pass: {quiz.required_score_to_pass}
        </Typography>
      </CardContent>
    </CardActionArea>
  </Card>
);

const QuizCategory = () => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/mainpage/')
      .then(res => {
        setCategories(res.data);
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', padding: 2 }}>
      {categories.map(category => (
        <Box key={category.id} sx={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginBottom: 10 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: 2 }}>
            <StarIcon />
            <Typography variant="h4" component="h1" sx={{ marginLeft: 1 }}>
              {category.name}
            </Typography>
            <Button variant="contained" sx={{ marginLeft: 'auto' }}>See more</Button>
          </Box>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            {category.quizzes.map(quiz => (
              <QuizCard key={quiz.id} quiz={quiz} />
            ))}
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default QuizCategory;
