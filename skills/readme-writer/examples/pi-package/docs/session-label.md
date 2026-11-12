# Session label extension

[Package README](../README.md)

The fictional extension registers `/session-label TEXT`. The proposed UI displays TEXT in the current session; `/session-label` with no text clears it. It performs no network request or persistent write. Reloading discards the label. The host extension API and UI behavior require implementation and verification before a real release.
