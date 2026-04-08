# May need to be updated as frontend is developed. This is very basic to start with.

# Use tiny Nginx image
FROM nginx:alpine

# Copy any future frontend files here
COPY . /usr/share/nginx/html

# Expose port 3000
EXPOSE 3000

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]