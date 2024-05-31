# syntax=docker/dockerfile:1.4
ARG PLATFORM
FROM --platform=$PLATFORM public.ecr.aws/amazonlinux/amazonlinux:2023 as base

RUN <<EOT
  dnf install -y rpm-build
  dnf install -y php-devel php-pear
EOT

FROM base

ARG PHP_VER
ENV PHP_VER ${PHP_VER}

CMD rpmbuild -ba --clean --define "php_ver ${PHP_VER}" /root/rpmbuild/SPECS/php-pecl-apcu.spec
