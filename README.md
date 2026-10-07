# Ioannis Papagiannis, PhD

Professional and academic portfolio: **https://papagiai.github.io/**

EU Project Analyst at REZOS Brands, with a background in mechanical engineering, materials science, electrochemistry and applied R&D.

## Structure

- `index.html`: page content, metadata, sections and SVG icons.
- `css/styles.css`: layout, local fonts, responsive and print styles.
- `js/main.js`: mobile menu and active-section navigation.
- `assets/images/favicon.svg`: original initials favicon.
- `assets/fonts/`: Inter and Source Serif 4 with SIL Open Font Licenses.
- `tools/verify_site.py`: offline integrity checks.
- `.nojekyll`: disables Jekyll processing.

Plain HTML, CSS and JavaScript. No framework, package installation or build step. Fonts are served locally; there are no analytics, tracking scripts or contact-form services.

## Update the website

1. Edit the text in `index.html`. Section IDs match the sidebar links; preserve them when renaming sections.
2. Preview and run the checks below.
3. Commit and push to `main`. GitHub Pages publishes the root of `main` automatically. Check the repository's **Actions** tab for the build/deployment result.

GitHub's file editor can also make small corrections directly in `index.html`. Review the diff before committing.

Duplicate an existing project card, timeline item or publication to add content. For publication numbering, change `counter-reset:paper 5` in the stylesheet to one greater than the number of papers. Verify author order, title, year and DOI. Update both the visible footer date and its `datetime` attribute when content changes.

Keep personal involvement dates distinct from project duration, and individual responsibilities distinct from consortium responsibilities.

## Local preview and checks

Open `index.html` in a browser, or run:

```sh
python -m http.server 4174 --bind 127.0.0.1
```

Visit `http://127.0.0.1:4174`; stop the server with Ctrl+C.

```sh
python tools/verify_site.py
node --check js/main.js
```

Also inspect desktop/mobile layouts, navigation, external links and new downloads. Structural checks do not guarantee third-party availability or certify accessibility compliance.

## GitHub Pages settings

- Repository: `papagiai/papagiai.github.io`
- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/ (root)**
- HTTPS: enabled

All asset paths are relative. Keep `.nojekyll`. There is no custom domain or routing/build dependency.

## Optional additions

For a portrait, place an approved, optimised image in `assets/images/`, replace `.monogram` with an image with meaningful alt text and explicit dimensions, and apply a circular border and `object-fit:cover`. The initials mark is a complete photo-free treatment.

The current version has no CV download. To add one, place an up-to-date, publication-approved PDF in `assets/documents/` and add a real download link. Check its contents and download before publishing; never upload private source documents or create dummy links.

Contact currently links to LinkedIn. Add an email only when the owner chooses a public address. Other professional profile links can be added after verifying their exact URLs.

## Design and licensing

Independently implemented in a restrained academic style: navy sidebar, circular identity area, serif headings, pale background, timelines and publication cards. No reference-site personal content, photographs, logos or source code are included. Icons and favicon are original SVG shapes. Organisation logos are stored in `assets/images/logos/`; official source URLs and asset notes are recorded in `assets/images/logos/SOURCES.md`. Preserve logo proportions and check both desktop and mobile when replacing them.

Inter and Source Serif 4 are redistributed under the SIL Open Font License. Keep the included licence files with the fonts.
