# Research and sources

[Home](../README.md)

This is qualitative research into README patterns, not a ranking or product audit. Distinguish observed content from interpretation. Descriptions summarize rather than reproduce sources.

| Collection | Coverage |
| --- | --- |
| [Established projects](classic.md) | Six different README roles |
| [Trending](trending.md) | 14 weekly + six non-overlapping monthly entries on 2026-11-10 |
| [Distributed packages](packages.md) | Two agents, two skill collections, three pi packages; some overlap with Trending |
| [Awesome README](awesome-readme.md) | Organization, selection criteria, and further reading |

## Official writing and formatting guidance

- [GitHub READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes): purpose, getting started, help, links, and detailed-document separation.
- [GitHub images](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#adding-an-image-to-suit-your-visitors): theme-specific picture sources and fallback.
- [Collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections): details and summary.
- [Google style](https://developers.google.com/style/timeless-documentation): reduce time-dependent wording.
- [SwiftPM dependencies](https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Dependencies/AddingDependencies.md): package and target product linkage, checked through Context7.

Checked 2026-11-10. Recheck installation, APIs, and support policies when writing actual product docs. This sample does not establish an AI documentation error rate.

## A concrete documentation boundary

The [visual-feedback-mcp README](https://github.com/tortle1228/visual-feedback-mcp/blob/fec12a5276b56911543e917a5d5273c4af037f14/README.md) was compared with source as an input to general guidance, not as this repository's primary deliverable. For example, an in-memory storage claim needs to account for [diagnostic logs](https://github.com/tortle1228/visual-feedback-mcp/blob/fec12a5276b56911543e917a5d5273c4af037f14/src/daemon.js#L43-L55), and onboarding inputs need to fit [actual size limits](https://github.com/tortle1228/visual-feedback-mcp/blob/fec12a5276b56911543e917a5d5273c4af037f14/src/viewer.js#L8-L19). That repository was neither modified nor executed during this research.
