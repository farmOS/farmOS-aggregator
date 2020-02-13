# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM tiangolo/node-frontend:10 as build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

# Comment out the next line to disable tests
# RUN npm run test:unit

RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

# Copy env-template.js for configuring the Aggregator with env variables.
COPY --from=build-stage /app/env-template.js /

# Copy entrypoint script for building env template.
COPY --from=build-stage /app/build-env.sh /

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf

ENTRYPOINT ["/build-env.sh"]

CMD ["nginx", "-g", "daemon off;"]
