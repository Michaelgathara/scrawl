
Now, fetch data on the front end using React Hooks. You can create a simple component to display and add posts.

```javascript
// components/PostList.tsx
import { useEffect, useState } from 'react';

export default function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('/api/posts')
      .then((response) => response.json())
      .then((data) => setPosts(data));
  }, []);

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

Insert the `PostList` component into any of your pages (e.g., `index.tsx`) to see it in action.

This example showcases ZenStack's seamless integration for full-stack development, leveraging models from backend to frontend efficiently.