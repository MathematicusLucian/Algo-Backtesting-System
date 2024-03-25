FROM nginx:alpine
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
###
RUN chmod 777 /usr/share/nginx/html 
###
EXPOSE 80 443
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]