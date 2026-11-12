import http.server

import fastserve  # noqa: F401  (internal package, not installed)

PORT = 8080


def main():
    http.server.HTTPServer(("127.0.0.1", PORT), fastserve.Handler).serve_forever()


if __name__ == "__main__":
    main()
