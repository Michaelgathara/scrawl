// Step 1: Initialize the Vercel AI SDK
import { VercelAI } from '@vercel/ai-sdk';

const ai = new VercelAI({
  apiKey: 'your-vercel-api-key',
  model: 'text-davinci-003',
});

// Step 2: Create a function to handle AI requests
async function generateText(prompt) {
  try {
    const response = await ai.generateText({
      prompt: prompt,
      maxTokens: 150,
    });
    return response.text;
  } catch (error) {
    console.error('Error generating text:', error);
  }
}

// Step 3: Use the function in an Express.js route
const express = require('express');
const app = express();

app.use(express.json());

app.post('/generate', async (req, res) => {
  const prompt = req.body.prompt;
  const aiResponse = await generateText(prompt);
  res.json({ text: aiResponse });
});

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});