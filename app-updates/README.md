# Android app update hosting

This folder is reserved for the public update feed for **Rajendra Android Test**.

- Android application ID: `com.rajendra.apktest`
- Manifest: `latest.json`
- Raw manifest URL: `https://raw.githubusercontent.com/rajendrabaniya86-rgb/Calculator-app/main/app-updates/latest.json`

The manifest is deliberately marked `available: false` until a signed APK is published. Do not install an APK from this folder until its package ID, version code, signing certificate, and SHA-256 have been verified.

## Next integration steps

1. Configure a stable Android signing key in GitHub Actions Secrets in the private source repository.
2. Add a narrowly scoped GitHub token as `UPDATE_REPO_TOKEN` in the private source repository, allowing release publishing / contents updates to this public repository.
3. Update the private Android build workflow to publish a versioned APK and update this manifest only after a successful build.
4. Add in-app update checking, download, checksum verification, and Android Package Installer handoff. Android will still ask the user to confirm installation.

The existing calculator source files are not changed by this update-hosting setup.
