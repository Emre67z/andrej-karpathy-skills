"""EPİAŞ Piyasa Mesaj Sistemi raporu için küçük yerel sunucu.

Tarayıcı EPİAŞ API'sine doğrudan istek atamaz (CORS engeli), bu yüzden
bu sunucu index.html'i yayınlar ve /api/* isteklerini TGT ekleyerek
EPİAŞ'a iletir. Sadece Python standart kütüphanesi gerekir.

Çalıştırma:  python3 server.py   ->  http://localhost:8000
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

CAS_URL = "https://giris.epias.com.tr/cas/v1/tickets"
API_BASE = "https://seffaflik.epias.com.tr/electricity-service/"
TGT_LIFETIME = 90 * 60  # TGT ~2 saat geçerli; 90 dk'da bir yenile
HERE = Path(__file__).parent

# Kimlik bilgileri yalnızca bellekte tutulur, diske yazılmaz.
state = {"user": None, "password": None, "tgt": None, "tgt_time": 0}


def get_tgt(force=False):
    if not state["user"]:
        raise PermissionError("Önce giriş yapın.")
    if force or not state["tgt"] or time.time() - state["tgt_time"] > TGT_LIFETIME:
        data = urllib.parse.urlencode(
            {"username": state["user"], "password": state["password"]}
        ).encode()
        req = urllib.request.Request(
            CAS_URL,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/plain",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            state["tgt"] = r.read().decode().strip()
            state["tgt_time"] = time.time()
    return state["tgt"]


def call_api(path, method, body):
    """EPİAŞ'a isteği iletir; 401 gelirse TGT'yi yenileyip bir kez tekrar dener."""
    for attempt in range(2):
        req = urllib.request.Request(
            API_BASE + path,
            data=body if method == "POST" else None,
            method=method,
            headers={
                "TGT": get_tgt(force=attempt > 0),
                "Content-Type": "application/json",
                "Accept": "*/*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 401 and attempt == 0:
                continue
            return e.code, dict(e.headers), e.read()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload, headers=None):
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload, ensure_ascii=False).encode()
            headers = {"Content-Type": "application/json; charset=utf-8"}
        self.send_response(code)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _body(self):
        return self.rfile.read(int(self.headers.get("Content-Length") or 0))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (HERE / "index.html").read_bytes()
            return self._send(200, html, {"Content-Type": "text/html; charset=utf-8"})
        if self.path == "/auth/status":
            return self._send(200, {"loggedIn": bool(state["tgt"]), "user": state["user"]})
        if self.path.startswith("/api/"):
            return self._proxy("GET", None)
        self._send(404, {"error": "bulunamadı"})

    def do_POST(self):
        if self.path == "/auth/login":
            creds = json.loads(self._body() or b"{}")
            state.update(user=creds.get("username"), password=creds.get("password"), tgt=None)
            try:
                get_tgt(force=True)
                return self._send(200, {"ok": True})
            except Exception as e:  # noqa: BLE001 - hatayı arayüze göster
                state.update(user=None, password=None, tgt=None)
                return self._send(401, {"error": f"Giriş başarısız: {e}"})
        if self.path == "/auth/logout":
            state.update(user=None, password=None, tgt=None)
            return self._send(200, {"ok": True})
        if self.path.startswith("/api/"):
            return self._proxy("POST", self._body())
        self._send(404, {"error": "bulunamadı"})

    def _proxy(self, method, body):
        path = self.path[len("/api/"):]
        try:
            code, headers, data = call_api(path, method, body)
        except PermissionError as e:
            return self._send(401, {"error": str(e)})
        except Exception as e:  # noqa: BLE001
            return self._send(502, {"error": f"EPİAŞ'a ulaşılamadı: {e}"})
        keep = {k: v for k, v in headers.items()
                if k.lower() in ("content-type", "content-disposition")}
        self._send(code, data, keep)

    def log_message(self, fmt, *args):
        print(time.strftime("%H:%M:%S"), fmt % args)


if __name__ == "__main__":
    print("Rapor arayüzü: http://localhost:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
