# Reviewboard MCP

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

Let a coding assistant show a local image for review and retrieve written feedback.

## Requirements

The fictional design uses a local stdio MCP client, Node.js 22+, and a desktop browser. A client must support image tool results. No client compatibility has been tested for this example.

## Connect a client

After obtaining the server source and installing its documented dependencies, point your client's stdio server configuration at its absolute entry path. The following is an illustrative configuration shape, not a universal client file format:

```json
{
  "mcpServers": {
    "reviewboard": {
      "command": "node",
      "args": ["/absolute/path/to/reviewboard/server.js"]
    }
  }
}
```

Use the client's own documentation for the configuration file location and schema, then restart or reconnect it. Confirm that `show_review` and `collect_review` appear in its tool list. A visible tool list confirms connection, not end-to-end browser operation.

## First review

Ask: “Show my local screenshot for review.” The assistant calls `show_review`, and the local page displays the image. Add a comment and submit it. Tell the assistant you are done; it calls `collect_review` and summarizes the submitted comment.

| Tool | Purpose |
| --- | --- |
| `show_review` | Display one local image and return the review URL |
| `collect_review` | Retrieve submitted feedback without waiting for a person |

## Data and limits

The proposed server reads the supplied image path with its OS user's permissions. It passes the selected image and feedback to the MCP client; the client's model provider may receive them. Local browser hosting does not imply local-only model processing.

This design accepts one PNG up to 5 MiB per review. Pending feedback is memory-only and is lost when the server stops. These are illustrative interface requirements, not claims about an existing implementation.

## Troubleshooting and removal

If tools are absent, check the absolute entry path and the client's server log. If the browser does not open, use the returned URL. Remove the server entry and restart the client to disconnect; remove the source directory separately. The proposed server creates no persistent settings.

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
