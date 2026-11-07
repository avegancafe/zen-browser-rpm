# COPR "make_srpm" entry point: COPR runs `make -f .copr/Makefile srpm
# outdir=... spec=...` in a clean chroot. Downloads Zen's official tarballs,
# checks them against sha256sums, and builds the source RPM.
SRCDIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
WORK := $(shell mktemp -d)

srpm:
	dnf -y install rpm-build curl coreutils
	version=$$(rpmspec -q --srpm --qf '%{version}' $(SRCDIR)/zen-browser.spec) && \
	for arch in x86_64 aarch64; do \
		curl -fsSL --retry 3 -o $(WORK)/zen.linux-$$arch.tar.xz \
			https://github.com/zen-browser/desktop/releases/download/$$version/zen.linux-$$arch.tar.xz || exit 1; \
	done
	cp $(SRCDIR)/sha256sums $(SRCDIR)/zen-browser.desktop $(SRCDIR)/zen-browser $(SRCDIR)/policies.json $(WORK)/
	cd $(WORK) && sha256sum --check --strict sha256sums
	rpmbuild -bs --define "_sourcedir $(WORK)" --define "_srcrpmdir $(outdir)" $(SRCDIR)/zen-browser.spec
	rm -rf $(WORK)
