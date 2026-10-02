# -*- coding: utf-8 -*-
"""
6차시 탈출 게임(그림·그래프) · 로컬 서버 실행 도우미 (학교 인터넷이 막혀 있을 때의 예비 방법)

- 파이썬 기본 모듈만 사용한다. 추가 설치나 인터넷 연결이 필요 없다.
- 보통은 이 저장소를 GitHub Pages 로 열면 된다. 이 서버는 그 주소가 학교에서
  막혀 있을 때만 쓰는 예비 방법이다 — 이 컴퓨터가 수업 내내 켜져 있어야 하고,
  모둠 기기와 같은 교실 와이파이에 있어야 한다.
- 8403번 포트가 이미 쓰이고 있으면 8404, 8405 … 순서로 빈 포트를 찾는다.

실행 방법
  ① 로컬서버_실행.bat 을 더블클릭          (가장 쉬움)
  ② 또는 명령창에서  python server.py
     브라우저를 자동으로 열지 않으려면  python server.py --no-browser
  종료 : 이 창에서 Ctrl + C (또는 창 닫기)
"""

import functools
import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
FIRST_PORT = 8403
TRY_COUNT = 20


def find_free_port(first, count):
    for port in range(first, first + count):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    return None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return None
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    index = os.path.join(ROOT, "index.html")
    if not os.path.exists(index):
        print("[오류] index.html 을 찾을 수 없습니다:", index)
        return 1

    port = find_free_port(FIRST_PORT, TRY_COUNT)
    if port is None:
        print("[오류] %d ~ %d 사이에 빈 포트가 없습니다." % (FIRST_PORT, FIRST_PORT + TRY_COUNT - 1))
        return 1

    local_ip = get_local_ip()
    local_url = "http://localhost:%d/index.html" % port
    handler = functools.partial(Handler, directory=ROOT)

    print("=" * 62)
    print("  6차시 탈출 게임(그림·그래프) · 로컬 서버 (예비 방법)")
    print("=" * 62)
    print("  이 컴퓨터에서 여는 주소 : %s" % local_url)
    print("  폴더 : %s" % ROOT)
    print()
    if local_ip:
        print("  ▶ 모둠 기기(태블릿 등)에서는 이 주소로 접속하세요 ◀")
        print("    http://%s:%d/" % (local_ip, port))
        print()
        print("  ※ 모둠 기기와 이 컴퓨터가 같은 와이파이(교실 와이파이)에 있어야 합니다.")
        print("  ※ 접속이 안 되면 : ① Windows 방화벽이 물으면 '개인 네트워크'에 체크하고")
        print("     허용을 누르세요. ② 학교 와이파이에 기기끼리 통신을 막는 'AP 격리'가")
        print("     걸려 있으면 이 방식도 안 됩니다 — 그때는 폴더를 모둠 기기마다 복사하세요.")
    else:
        print("  [안내] 이 컴퓨터의 와이파이 주소를 찾지 못했습니다.")
    print("=" * 62)
    print("  종료 : 이 창에서 Ctrl + C  (또는 창 닫기)")
    print("=" * 62)

    with Server(("0.0.0.0", port), handler) as httpd:
        if "--no-browser" not in sys.argv:
            threading.Timer(0.7, lambda: webbrowser.open(local_url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
