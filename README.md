# trmnl-waveshare-bridge
**Version:** 0.0.2  
**Status:** Early Development (do not use)

An unofficial TRMNL compatibility project for Waveshare e-paper displays.  
Built on a [custom Waveshare EPD image library](https://github.com/Lambda-ex/waveshare-epd-image), this project fetches the current TRMNL screen and renders it on Raspberry Pi–connected Waveshare panels. Its goal is to make all Waveshare EPD devices usable with TRMNL, even when display dimensions or rendering characteristics differ.

This works by updating the show_img script run by go to run a separate python library to display the image.

## Important Notice
Everything is "hacked together" right now, so it is very unfriendly and not ready for public implementation. Please until future updates **do not use**.

## Dependency note

This project depends on the **latest version** of the
[custom Waveshare EPD image library](https://github.com/Lambda-ex/waveshare-epd-image).

During early development, the dependency is pulled directly from the GitHub
repository to ensure compatibility with new displays and rendering changes.

For now, please see refer to that repository on instructions on how to install the library.

## Credits

- **Waveshare** - for the e-paper display hardware and reference drivers that make these devices possible.
- **TRMNL** - for the platform and API that inspired this project and provides the display content it renders.

This project is unofficial and is not affiliated with or endorsed by Waveshare or TRMNL.
