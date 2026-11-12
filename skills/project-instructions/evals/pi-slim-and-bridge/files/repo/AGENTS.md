# Project Guidelines

Welcome! This document describes how to work on the inventory API. Please read it carefully before making any change.

## General principles

- Write clean, maintainable, readable code.
- Follow best practices at all times.
- Think step by step before writing code.
- Be careful and double-check your work.
- Prefer simple solutions over complex ones.

## Setup

1. Install Node.js.
2. Run `npm install` to install dependencies.
3. Run `pnpm dev` to start the server.

## Commands

- Test: `pnpm test`
- Lint: `pnpm lint`
- Typecheck: `pnpm typecheck`
- End-to-end tests: `pnpm e2e`

## Code style

- Use 2-space indentation.
- Use single quotes for strings.
- Always add semicolons.
- Keep lines under 100 characters.
- Sort imports alphabetically.

## Architecture

- HTTP handlers live in `src/api/`. They must not import from `src/db/` directly; go through `src/services/`.
- The router is defined in `src/legacy/router.ts`.
- Never edit migrations in `migrations/` that have already been applied; add a new numbered file instead.

## Example handler

```ts
import { listItems } from "../services/items";

export async function handler(req: Request): Promise<Response> {
  const items = await listItems();
  return new Response(JSON.stringify(items), {
    headers: { "content-type": "application/json" },
  });
}
```

## Final notes

- Ask questions if anything is unclear.
- Make sure all tests pass before finishing.
