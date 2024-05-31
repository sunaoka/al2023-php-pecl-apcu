APCU_VERSION := 5.1.23

IMAGE := php-pecl-apcu-builder

MOUNT := -v ./rpmbuild/SOURCES:/root/rpmbuild/SOURCES \
         -v ./rpmbuild/SPECS:/root/rpmbuild/SPECS \
         -v ./rpmbuild/RPMS:/root/rpmbuild/RPMS \
         -v ./rpmbuild/SRPMS:/root/rpmbuild/SRPMS

TARGET := build-arm64-8.1 \
          build-arm64-8.2 \
          build-amd64-8.1 \
          build-amd64-8.2

all: build

build: $(TARGET)

rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz:
	curl -f -o $@ -LO https://pecl.php.net/get/$(@F)

build-arm64-%: rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz
	docker build --build-arg PLATFORM=linux/arm64 --build-arg PHP_VER=$* -t $(IMAGE):php-$*-arm64 .
	docker run --rm $(MOUNT) $(IMAGE):php-$*-arm64

build-amd64-%:
	docker build --build-arg PLATFORM=linux/amd64 --build-arg PHP_VER=$* -t $(IMAGE):php-$*-amd64 .
	docker run --rm $(MOUNT) $(IMAGE):php-$*-amd64

clean:
	-$(RM) -r rpmbuild/{RPMS,SRPMS}
	-$(RM) rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz

.PHONY: all build clean
