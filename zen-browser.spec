# Repackages Zen's official Linux release tarball as an RPM. Nothing is built
# from source: the tarballs come straight from Zen's GitHub release and %prep
# refuses to continue unless they match the checksums pinned in sha256sums.

%global app_dir /opt/zen
%global debug_package %{nil}
# The browser bundles its own libraries (libxul, NSS, ...). Don't advertise
# them to the rest of the system, and don't require them from it.
%global __provides_exclude_from ^%{app_dir}/.*$
%global __requires_exclude ^(libxul|libmozgtk|libmozsandbox|libmozsqlite3|libmozwayland|liblgpllibs|libgkcodecs|libipcclientcerts|libmozavcodec|libmozavutil|libnspr4|libnss3|libnssutil3|libplc4|libplds4|libsmime3|libsoftokn3|libssl3|libfreeblpriv3|libonnxruntime)\\.so.*$

Name:           zen-browser
Version:        1.24.2b
Release:        1%{?dist}
Summary:        Zen Browser, repackaged from the official release tarball
License:        MPL-2.0
URL:            https://github.com/avegancafe/zen-browser-rpm

Source0:        https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-x86_64.tar.xz
Source1:        https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-aarch64.tar.xz
Source2:        sha256sums
Source3:        zen-browser.desktop
Source4:        zen-browser
Source5:        policies.json

ExclusiveArch:  x86_64 aarch64
Requires(post): gtk-update-icon-cache

%description
Zen Browser (https://zen-browser.app), a Firefox-based browser. This package
installs Zen's own prebuilt release into %{app_dir}, unmodified apart from an
enterprise policy that turns off Zen's self-updater so dnf handles updates.

%prep
cd %{_sourcedir}
sha256sum --check --ignore-missing --strict %{SOURCE2}
%ifarch x86_64
%setup -q -T -c -n zen -a 0
%endif
%ifarch aarch64
%setup -q -T -c -n zen -a 1
%endif

%build

%install
install -d %{buildroot}%{app_dir}
cp -a zen/. %{buildroot}%{app_dir}/
install -D -m 0644 %{SOURCE5} %{buildroot}%{app_dir}/distribution/policies.json
install -D -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/zen-browser
install -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/zen-browser.desktop
for size in 16 32 48 64 128; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  ln -s %{app_dir}/browser/chrome/icons/default/default${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/zen-browser.png
done

%post
gtk-update-icon-cache -q -f -t %{_datadir}/icons/hicolor || :

%postun
gtk-update-icon-cache -q -f -t %{_datadir}/icons/hicolor || :

%files
%{app_dir}
%{_bindir}/zen-browser
%{_datadir}/applications/zen-browser.desktop
%{_datadir}/icons/hicolor/*/apps/zen-browser.png
