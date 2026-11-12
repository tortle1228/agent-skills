# TagList

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

A small SwiftUI component for displaying selectable tags in a settings screen.

## Requirements

The example API targets iOS 17+ and Swift 6.1+. These are design assumptions, not a tested compatibility matrix.

## Add the package

In a consumer package manifest, add the dependency and link its product to your target. Replace the demonstration URL with your published repository before distributing this documentation.

```swift
// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "SettingsFeature",
    platforms: [.iOS(.v17)],
    dependencies: [
        .package(url: "https://example.invalid/tag-list.git", from: "1.0.0")
    ],
    targets: [
        .target(name: "SettingsFeature", dependencies: [
            .product(name: "TagList", package: "tag-list")
        ])
    ]
)
```

## Show a selection

```swift
import SwiftUI
import TagList

struct PreferencesView: View {
    @State private var selected: Set<String> = ["Swift"]

    var body: some View {
        TagPicker(tags: ["Swift", "Design", "Testing"], selection: $selected)
    }
}
```

The illustrative control shows three tags, with Swift selected. Tapping Design adds it to the selection. The app owns the selection; the component does not persist it or send it anywhere.

## Scope

This design covers a small set of unique text tags. It does not specify a searchable or virtualized collection. See the [API contract](docs/api.md) for selection behavior.

## Development and help

In the fictional package repository, run `swift test` from its root for model tests; a consuming iOS app is still needed to check layout and accessibility. No such test suite is included here. A useful issue includes the platform, package version, and a minimal view reproducing the problem.

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
