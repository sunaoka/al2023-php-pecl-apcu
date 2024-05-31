APCU_VERSION := 5.1.23

IMAGE := php-pecl-apcu-builder

MOUNT := -v ./rpmbuild/SOURCES:/root/rpmbuild/SOURCES \
         -v ./rpmbuild/SPECS:/root/rpmbuild/SPECS \
         -v ./rpmbuild/RPMS:/root/rpmbuild/RPMS \
         -v ./rpmbuild/SRPMS:/root/rpmbuild/SRPMS

all: build

build: build-arm64 build-amd64

rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz:
	curl -f -o $@ -LO https://pecl.php.net/get/$(@F)

build-%: rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz
	docker build --build-arg PLATFORM=linux/$* -t $(IMAGE):$* .
	docker run --rm $(MOUNT) $(IMAGE):$*

clean:
	-$(RM) -r rpmbuild/{RPMS,SRPMS}
	-$(RM) rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz

.PHONY: all build clean
