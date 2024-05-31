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

build: rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz $(TARGET)

rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz:
	curl -f -o $@ -LO https://pecl.php.net/get/$(@F)

build-%:
	$(eval PLATFORM = $(word 1,$(subst -, ,$*)))
	$(eval PHP_VER = $(word 2,$(subst -, ,$*)))

	docker build --build-arg PLATFORM=linux/$(PLATFORM) --build-arg PHP_VER=$(PHP_VER) -t $(IMAGE):php-$(PHP_VER)-$(PLATFORM) .
	docker run --rm $(MOUNT) $(IMAGE):php-$(PHP_VER)-$(PLATFORM)

clean:
	-$(RM) -r rpmbuild/{RPMS,SRPMS}
	-$(RM) rpmbuild/SOURCES/apcu-$(APCU_VERSION).tgz

clean-image:
	-docker rmi $(shell docker images --filter=reference="$(IMAGE):*" -q)

.PHONY: all build clean clean-image
