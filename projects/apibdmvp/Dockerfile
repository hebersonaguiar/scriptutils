FROM php:7.1.3-apache

# UPDATE OS
RUN apt-get update -y 

# INSTALL DRIVER MYSQL
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

# CREATE DIR APP
RUN mkdir -p /var/www/html/appmvp/

# COPY API SCRIPTS
COPY checkuser.php /var/www/html/appmvp/
COPY adduser.php /var/www/html/appmvp/

# INITIALIZE API
CMD ["apache2-foreground"]

