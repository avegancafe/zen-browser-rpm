# zen-browser-rpm

An RPM of [Zen Browser](https://zen-browser.app) for Fedora, built from Zen's
**official Linux release tarball** with nothing rebuilt or patched, and
built and published by [Fedora COPR](https://copr.fedorainfracloud.org).

Why not the Flathub Flatpak? A sandboxed browser can't reach the 1Password
desktop app, so the 1Password extension can't unlock with it (fingerprint /
system auth). A regular RPM can.

## Install

```sh
sudo dnf copr enable <copr-owner>/zen-browser   # COPR project link: TBD
sudo dnf install zen-browser
```

Updates come through `dnf upgrade`. Zen's own updater is turned off with an
enterprise policy (`/opt/zen/distribution/policies.json`) so the two don't fight.

### 1Password

1Password for Linux only connects its extension to browsers it knows. Zen
isn't one of them, so allowlist it, then fully quit and reopen 1Password:

```sh
sudo mkdir -p /etc/1password
printf 'zen\nzen-bin\n' | sudo tee -a /etc/1password/custom_allowed_browsers >/dev/null
sudo chown root:root /etc/1password/custom_allowed_browsers
sudo chmod 755 /etc/1password/custom_allowed_browsers
```

## What you're trusting

- **Zen**: the tarballs are downloaded unchanged from
  [zen-browser/desktop releases](https://github.com/zen-browser/desktop/releases).
- **This repo**: [`sha256sums`](sha256sums) pins each tarball's SHA-256 digest
  (as GitHub reports it for Zen's upload). Both the source-RPM build
  ([`.copr/Makefile`](.copr/Makefile)) and `%prep` in
  [`zen-browser.spec`](zen-browser.spec) refuse to continue on a mismatch, so a
  release asset that is swapped after the fact won't be packaged.
- **Fedora COPR**: builds and signs the RPMs.

The spec is short; read it. What it installs:

| Path | What |
|------|------|
| `/opt/zen/` | Zen's release tarball, as shipped |
| `/opt/zen/distribution/policies.json` | `DisableAppUpdate` |
| `/usr/bin/zen-browser` | `exec /opt/zen/zen "$@"` |
| `/usr/share/applications/zen-browser.desktop` | Desktop entry |
| `/usr/share/icons/hicolor/*/apps/zen-browser.png` | Links to Zen's icons |

## How updates happen

[`.github/workflows/bump.yml`](.github/workflows/bump.yml) checks Zen's latest
stable release every 6 hours. When there's a new one, it writes the new version
into the spec and the release's digests into `sha256sums`, and commits. The
COPR webhook rebuilds on that push.

## Building locally

```sh
v=$(rpmspec -q --srpm --qf '%{version}' zen-browser.spec)
mkdir -p src
for a in x86_64 aarch64; do
  curl -fLo src/zen.linux-$a.tar.xz \
    https://github.com/zen-browser/desktop/releases/download/$v/zen.linux-$a.tar.xz
done
cp sha256sums zen-browser zen-browser.desktop policies.json src/
rpmbuild -ba --define "_sourcedir $PWD/src" zen-browser.spec
```

## License

The packaging files here are MIT ([LICENSE](LICENSE)). Zen Browser itself is
[MPL-2.0](https://github.com/zen-browser/desktop/blob/dev/LICENSE).
