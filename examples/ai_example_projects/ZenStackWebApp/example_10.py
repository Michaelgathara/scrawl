
Create a backend using ZenStack. You can create the following API route in the Next.js `pages/api` directory:

```typescript
// pages/api/posts.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default async function handle(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    const posts = await prisma.post.findMany();
    res.json(posts);
  } else if (req.method === 'POST') {
    const { title, content } = req.body;
    const newPost = await prisma.post.create({
      data: {
        title,
        content,
      },
    });
    res.status(201).json(newPost);
  } else {
    res.status(405).end(); // Method Not Allowed
  }
}
```

### 4. Front-end Integration