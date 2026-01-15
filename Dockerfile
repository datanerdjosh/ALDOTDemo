# Dockerfile for HWBDemo - Bank Employee Portal
# Uses nginx to serve static files

FROM nginx:alpine

# Copy all website files to nginx html directory
COPY . /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (Code Engine default)
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]