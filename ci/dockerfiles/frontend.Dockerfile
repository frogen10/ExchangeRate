FROM node:21-alpine3.18 AS frontend
WORKDIR /frontend
RUN npm install -g @vue/cli
RUN npm install vue-router@next --save
RUN npm install vuex@4 --save
RUN npm install axios
RUN npm install moment
RUN npm install vue-chartjs chart.js
COPY ./frontend .
EXPOSE 5000
CMD [ "npm", "run", "dev", "--", "--host" ]