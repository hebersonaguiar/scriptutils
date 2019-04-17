FROM php:7.1.3-apache

# UPDATE OS
RUN apt-get update -y ; \
    apt-get install -y zip unzip git

# INSTALL COMPOSER
RUN cd /tmp/ ; \
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" ; \
    php -r "if (hash_file('sha384', 'composer-setup.php') === '93b54496392c062774670ac18b134c3b3a95e5a5e5c8f1a9f115f203b75bf9a129d5daa8ba6a13e2cc8a1da0806388a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" ; \
    php composer-setup.php ; \
    php -r "unlink('composer-setup.php');" ; \
    mv composer.phar /usr/bin/composer 

# INSTALL DRIVER MYSQL
RUN docker-php-ext-install mbstring pdo pdo_mysql

# ADD APP
ADD app.tar.gz /opt/

# CHANGE WORDIR
WORKDIR /opt/app

# INSTALL DEPENDENCIES FOR APP
RUN composer update composer.json

# INITIALIZE APP
CMD ["sh", "-c", "'/usr/local/bin/php' -S 0.0.0.0:8000 '/opt/app/server.php'"]

