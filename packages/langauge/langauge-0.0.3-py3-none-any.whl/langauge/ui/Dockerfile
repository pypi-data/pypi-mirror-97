FROM node:latest

#COPY . /src
WORKDIR /src

# Install dependencies
COPY package.json /src

RUN npm install --loglevel warn
#RUN npm run build

# Add rest of the client code
COPY . /src

EXPOSE 8080

CMD npm start