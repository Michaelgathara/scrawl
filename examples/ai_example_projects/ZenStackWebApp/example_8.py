
ZenStack uses Prisma as its ORM, so you need to set it up:

```bash
npx prisma init
```

After initializing Prisma, you will have a `prisma/schema.prisma` file. Update it to define your data models. Here is an example model:

```prisma
model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String
  published Boolean @default(false)
}
```

Then run the following to migrate your database:

```bash
npx prisma migrate dev --name init
```

### 3. Integrating ZenStack with the Next.js Application