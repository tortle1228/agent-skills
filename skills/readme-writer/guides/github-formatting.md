# Images, languages, and linked documentation

[Home](../README.md) · [Working file-layout example](../examples/app/README.md)

## Keep images and detailed docs in files

```markdown
![Preview of the export screen](assets/export-light.svg)
[Advanced configuration](docs/configuration.md)
```

Relative paths start at the current Markdown file. Update them when moving a page. Use descriptive link text. Create your own images or verify permission before copying third-party assets.

## Light and dark images

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/export-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/export-light.svg">
  <img src="assets/export-light.svg" alt="Export screen with three selected notes" width="640">
</picture>
```

This is GitHub's documented theme-aware pattern. Keep fallback content and meaningful alt text, and check contrast in both themes. Do not assume arbitrary JavaScript or CSS works in a README. Viewport breakpoint switching is not a verified pattern in this guide.

## Language files

```markdown
[English](README.md) | [한국어](README.ko.md)
```

Put the links in both files. The official GitHub README guidance consulted does not document automatic selection by reader language. File naming alone does not provide translation or automatic switching. Avoid using flags as language labels.

It is fine to translate only the entry page and keep detailed docs in one language: label that language. Synchronize requirements, support, and limitations across translations.

## Optional details

````markdown
<details>
<summary>Build from source</summary>

Run from the repository root:

```sh
make build
```

</details>
````

The command above illustrates formatting, not a command every repository supports. Keep blank lines around Markdown inside the block. Do not collapse required installation, costs, destructive effects, or critical limitations.

## Screenshots, GIFs, and diagrams

Show one representative task: a screen for an app, input/output for a CLI, or a small diagram for architecture. Provide a static alternative and explanation for motion. Refresh screenshots when the corresponding workflow changes. Label mockups rather than presenting them as shipped interfaces.

Sources: [relative links](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes#relative-links-and-image-paths-in-markdown-files), [theme images](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#adding-an-image-to-suit-your-visitors), [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections).
