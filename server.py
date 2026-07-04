#!/usr/bin/env python3
"""Local server for dropship stores — static files + order/message API."""

import json
import os
import uuid
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
CONFIG_PATH = os.path.join(ROOT, "admin", "config.json")

os.makedirs(DATA_DIR, exist_ok=True)

for fname in ("orders.json", "messages.json", "subscribers.json"):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"password": "dropship2026", "owner_email": "you@localhost"}, f)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def discover_stores():
    stores = []
    for name in sorted(os.listdir(ROOT)):
        if not name.startswith("site"):
            continue
        products_path = os.path.join(ROOT, name, "products.json")
        if not os.path.isfile(products_path):
            continue
        try:
            data = load_json(products_path)
            store = data.get("store", {})
            stores.append({
                "folder": name,
                "name": store.get("name", name),
                "tagline": store.get("tagline", ""),
                "slug": store.get("slug", name),
                "currency": store.get("currency", "USD"),
                "launchReady": data.get("launchReady", True),
                "productCount": len(data.get("products", [])),
                "url": f"/{name}/",
            })
        except (json.JSONDecodeError, OSError):
            continue
    return stores


def revenue_by_currency(orders):
    totals = {}
    for order in orders:
        currency = order.get("currency", "USD")
        totals[currency] = totals.get(currency, 0) + order.get("total", 0)
    return {currency: round(amount, 2) for currency, amount in totals.items()}


class StoreHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        return json.loads(self.rfile.read(length))

    def _json_response(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _check_admin(self):
        config = load_json(CONFIG_PATH)
        key = self.headers.get("X-Admin-Key", "")
        return key == config.get("password", "")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Key")
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/orders":
            body = self._read_body()
            orders = load_json(os.path.join(DATA_DIR, "orders.json"))
            order = {
                "id": str(uuid.uuid4())[:8].upper(),
                "created": now_iso(),
                "status": "new",
                "store": body.get("store", "unknown"),
                "customer": {
                    "name": body.get("name", ""),
                    "email": body.get("email", ""),
                    "phone": body.get("phone", ""),
                    "address": body.get("address", ""),
                    "city": body.get("city", ""),
                    "state": body.get("state", ""),
                    "zip": body.get("zip", ""),
                },
                "items": body.get("items", []),
                "total": body.get("total", 0),
                "currency": body.get("currency", "USD"),
                "notes": body.get("notes", ""),
            }
            orders.insert(0, order)
            save_json(os.path.join(DATA_DIR, "orders.json"), orders)
            self._json_response({"ok": True, "orderId": order["id"]})
            return

        if path == "/api/contact":
            body = self._read_body()
            messages = load_json(os.path.join(DATA_DIR, "messages.json"))
            msg = {
                "id": str(uuid.uuid4())[:8].upper(),
                "created": now_iso(),
                "status": "unread",
                "store": body.get("store", "unknown"),
                "name": body.get("name", ""),
                "email": body.get("email", ""),
                "subject": body.get("subject", "General Inquiry"),
                "message": body.get("message", ""),
            }
            messages.insert(0, msg)
            save_json(os.path.join(DATA_DIR, "messages.json"), messages)
            self._json_response({"ok": True, "messageId": msg["id"]})
            return

        if path == "/api/subscribe":
            body = self._read_body()
            subs = load_json(os.path.join(DATA_DIR, "subscribers.json"))
            email = body.get("email", "").strip().lower()
            store = body.get("store", "unknown")
            if email and not any(s["email"] == email and s["store"] == store for s in subs):
                subs.insert(0, {"id": str(uuid.uuid4())[:8], "created": now_iso(), "email": email, "store": store})
                save_json(os.path.join(DATA_DIR, "subscribers.json"), subs)
            self._json_response({"ok": True})
            return

        if path == "/api/admin/login":
            body = self._read_body()
            config = load_json(CONFIG_PATH)
            if body.get("password") == config.get("password"):
                self._json_response({"ok": True})
            else:
                self._json_response({"ok": False, "error": "Invalid password"}, 401)
            return

        self.send_error(404)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/stores":
            self._json_response({"stores": discover_stores()})
            return

        if path == "/api/admin/dashboard":
            if not self._check_admin():
                self._json_response({"error": "Unauthorized"}, 401)
                return
            orders = load_json(os.path.join(DATA_DIR, "orders.json"))
            messages = load_json(os.path.join(DATA_DIR, "messages.json"))
            subs = load_json(os.path.join(DATA_DIR, "subscribers.json"))
            revenue = revenue_by_currency(orders)
            self._json_response({
                "orders": orders,
                "messages": messages,
                "subscribers": subs,
                "stores": discover_stores(),
                "stats": {
                    "totalOrders": len(orders),
                    "newOrders": len([o for o in orders if o.get("status") == "new"]),
                    "unreadMessages": len([m for m in messages if m.get("status") == "unread"]),
                    "totalRevenue": round(sum(revenue.values()), 2),
                    "revenueByCurrency": revenue,
                    "subscribers": len(subs),
                    "storeCount": len(discover_stores()),
                },
            })
            return

        if path.startswith("/api/admin/orders/") and self._check_admin():
            order_id = path.split("/")[-1]
            orders = load_json(os.path.join(DATA_DIR, "orders.json"))
            for o in orders:
                if o["id"] == order_id:
                    self._json_response(o)
                    return
            self._json_response({"error": "Not found"}, 404)
            return

        return super().do_GET()

    def do_PATCH(self):
        if not self._check_admin():
            self._json_response({"error": "Unauthorized"}, 401)
            return

        path = urlparse(self.path).path
        body = self._read_body()

        if path.startswith("/api/admin/orders/"):
            order_id = path.split("/")[-1]
            orders = load_json(os.path.join(DATA_DIR, "orders.json"))
            for o in orders:
                if o["id"] == order_id:
                    o["status"] = body.get("status", o["status"])
                    save_json(os.path.join(DATA_DIR, "orders.json"), orders)
                    self._json_response({"ok": True})
                    return

        if path.startswith("/api/admin/messages/"):
            msg_id = path.split("/")[-1]
            messages = load_json(os.path.join(DATA_DIR, "messages.json"))
            for m in messages:
                if m["id"] == msg_id:
                    m["status"] = body.get("status", m["status"])
                    save_json(os.path.join(DATA_DIR, "messages.json"), messages)
                    self._json_response({"ok": True})
                    return

        self.send_error(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    stores = discover_stores()
    print(f"Dropship server running at http://localhost:{port}")
    print(f"  Portfolio: http://localhost:{port}/")
    print(f"  Admin:     http://localhost:{port}/admin/  (password in admin/config.json)")
    print(f"  Stores API: http://localhost:{port}/api/stores")
    print(f"  Loaded {len(stores)} store(s):")
    for store in stores:
        status = "live" if store["launchReady"] else "preview"
        print(f"    - {store['folder']}: {store['name']} ({store['currency']}) [{status}]")
    HTTPServer(("", port), StoreHandler).serve_forever()