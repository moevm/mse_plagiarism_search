FROM node:14-buster
COPY . .
RUN npm i
RUN npm run build
ENV PORT 8080
EXPOSE 8080
CMD ["node", "server.js"]
