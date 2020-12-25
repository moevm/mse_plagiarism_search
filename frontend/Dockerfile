FROM node:14-buster
COPY package*.json ./
RUN npm i
COPY . .
RUN npm run build
ENV PORT 8080
EXPOSE 8080
CMD ["node", "server.js"]
