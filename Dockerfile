# syntax=docker/dockerfile:1.4
ARG PLATFORM
FROM --platform=$PLATFORM public.ecr.aws/amazonlinux/amazonlinux:2023

WORKDIR /root/rpmbuild/SPECS

RUN <<EOT
  dnf install -y rpm-build
  dnf install -y php-devel php-pear
EOT

CMD ["rpmbuild", "-ba", "--clean", "/root/rpmbuild/SPECS/php-pecl-apcu.spec"]
