#!/usr/bin/env python3
"""Tail a SensESP device's log over HTTP, without resetting the device.

SensESP (main) exposes a ring buffer of the device log at GET /api/log. Polling
it reads the log over the network, so the ESP32-C3 USB-Serial-JTAG port is never
opened and the device is never auto-reset (the "reboot problem" that serial
monitoring causes). New lines are appended to a file you can read at any time.

Requires SensESP main (the /api/log endpoint comes from the upstream log-viewer
work); on older releases the endpoint returns an empty buffer.

  GET /api/log?since=<cursor>  ->  {session, next, gap, lines[]}
    session  changes when the device reboots
    next     cursor to pass as ?since= on the following poll
    gap      true when the buffer overran and lines were lost between polls

The poller holds ONE reused keep-alive connection for the whole run, rather than
opening a fresh TCP connection per poll. This matters on the ESP32-C3: its lwIP
socket pool is small (CONFIG_LWIP_MAX_SOCKETS defaults to 10) and shared with the
Signal K TLS client, mDNS and SNTP. A fresh-connection-per-poll client churns
that pool and makes the device's HTTP server log
"httpd_accept_conn: error in accept (23)" (ENFILE, socket table full). One steady
keep-alive connection costs a single socket and stays out of the way.

Usage:
  python3 web_log_monitor.py <host> [-o OUTFILE] [-i INTERVAL] [--no-filter]

  python3 web_log_monitor.py sensesp.local
  python3 web_log_monitor.py 192.0.2.10 -o /tmp/sensesp-web.log -i 2
"""
import argparse
import http.client
import json
import time


def split_host_port(host):
    h = host.split("://", 1)[-1].rstrip("/")
    if ":" in h:
        name, port = h.rsplit(":", 1)
        return name, int(port)
    return h, 80


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("host", help="device hostname or IP (e.g. sensesp.local, 192.0.2.10)")
    parser.add_argument("-o", "--outfile", help="log file to append to (default /tmp/<host>-web.log)")
    parser.add_argument("-i", "--interval", type=float, default=2.0, help="poll interval seconds (default 2)")
    parser.add_argument("--no-filter", action="store_true",
                        help="keep the endpoint's own '/api/log' request lines (filtered by default)")
    args = parser.parse_args()

    host, port = split_host_port(args.host)
    safe = args.host.replace("://", "_").replace("/", "_")
    outfile = args.outfile or f"/tmp/{safe}-web.log"

    conn = None
    since = None
    session = None
    reachable = None

    def get_log():
        nonlocal conn
        if conn is None:
            conn = http.client.HTTPConnection(host, port, timeout=8)
        path = "/api/log" + (f"?since={since}" if since is not None else "")
        # Explicit keep-alive: reuse this one connection across polls.
        conn.request("GET", path, headers={"Connection": "keep-alive"})
        resp = conn.getresponse()
        body = resp.read()
        if resp.status != 200:
            raise OSError(f"HTTP {resp.status}")
        return json.loads(body)

    with open(outfile, "a", buffering=1) as f:
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n===== web log monitor started {stamp} (http://{host}:{port}) =====\n")
        print(f"Tailing http://{host}:{port}/api/log -> {outfile}  (one keep-alive connection; Ctrl-C to stop)")

        while True:
            try:
                data = get_log()
            except (OSError, http.client.HTTPException, json.JSONDecodeError, ValueError):
                if conn is not None:
                    try:
                        conn.close()
                    except OSError:
                        pass
                    conn = None
                if reachable is not False:
                    f.write("----- device unreachable, retrying -----\n")
                reachable = False
                time.sleep(args.interval)
                continue

            if reachable is False:
                f.write("----- device reachable again -----\n")
            reachable = True

            sid = data.get("session")
            if session is not None and sid != session:
                f.write(f"----- device reboot detected (session {session} -> {sid}) -----\n")
                since = None  # re-read the new session's buffer from the start
            session = sid

            if data.get("gap"):
                f.write("----- [gap: some log lines were dropped] -----\n")

            for line in data.get("lines", []):
                if not args.no_filter and "Handling request: /api/log" in line:
                    continue
                f.write(line + "\n")

            nxt = data.get("next")
            if nxt is not None:
                since = nxt
            time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
