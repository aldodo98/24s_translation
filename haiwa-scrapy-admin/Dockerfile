FROM circleci/node:latest-browsers

WORKDIR /usr/src/app/
USER root
COPY package.json ./
RUN yarn install

COPY ./ ./

CMD ["npm", "run", "build"]
