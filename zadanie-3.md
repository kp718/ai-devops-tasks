Here's a basic Dockerfile for a Node.js application:

dockerfile

```dockerfile
# Use official Node.js image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Expose application port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

### Recommended `.dockerignore`

dockerignore

```dockerignore
node_modules
npm-debug.log
.git
.env
Dockerfile
.dockerignore
```

### Build and run

bash

```bash
# Build image
docker build -t my-node-app .

# Run container
docker run -p 3000:3000 my-node-app
```

### For production

Replace:

dockerfile

```dockerfile
RUN npm install
```

with:

dockerfile

```dockerfile
RUN npm ci --omit=dev
```

Note: Your `package.json` must have a `start` script, for example:

json

```json
{
  "scripts": {
    "start": "node index.js"
  }
}
```

I can also provide a multi-stage production Dockerfile for Node.js with npm, TypeScript, or Express.


-------------------------------------------------------------------------------------------------------------------------------------------------------

Oto prosty `Dockerfile` dla aplikacji Node.js wykorzystującej Node 18:

dockerfile

```dockerfile

FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### Wyjaśnienie

- `FROM node:18` – używa obrazu bazowego Node.js 18.
- `WORKDIR /app` – ustawia katalog roboczy aplikacji.
- `COPY package.json package-lock.json ./` – kopiuje pliki zależności.
- `RUN npm install` – instaluje zależności.
- `COPY . .` – kopiuje pozostałe pliki aplikacji.
- `EXPOSE 3000` – deklaruje port 3000.
- `CMD ["npm", "start"]` – uruchamia aplikację poleceniem `npm start`.

### Budowanie i uruchamianie

bash

```bash
docker build -t moja-aplikacja .
docker run -p 3000:3000 moja-aplikacja
```

Aplikacja będzie dostępna pod adresem `http://localhost:3000`.





