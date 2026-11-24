"""Start the local onboarding web application and open its browser page."""

import sys
import webbrowser
from pathlib import Path

try:
    from .server import make_server
except ImportError:
    from server import make_server


def resource_path(relative_path: str) -> Path:
    """Resolve bundled static assets in source and frozen applications."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return bundle_root / relative_path


def main() -> None:
    """Start on the first available local port from 8080 through 8090."""
    server = None
    for port in range(8080, 8091):
        try:
            server = make_server("127.0.0.1", port, resource_path("static"))
            break
        except OSError:
            continue
    if server is None:
        print("Could not find an available port between 8080 and 8090.")
        return

    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"Employee Onboarding System is running at {url}", flush=True)
    webbrowser.open(url)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        print("\nStopping Employee Onboarding System.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
