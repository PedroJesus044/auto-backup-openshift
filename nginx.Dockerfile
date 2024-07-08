FROM nginx
RUN mkdir /app
COPY ./frontend-controladora-js/release /app
COPY nginx.conf /etc/nginx/nginx.conf
