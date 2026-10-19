#!/usr/bin/env python3
"""나성의현인 스킬용 FRED 조회 헬퍼.

사용법:
    python3 fred.py DGS10                    # 최신값 1개
    python3 fred.py DGS10 CPIAUCSL UNRATE    # 여러 시리즈
    python3 fred.py --list                   # 자주 쓰는 시리즈 목록
    python3 fred.py --api-key 키 DGS10       # 키 직접 전달 (Claude 앱 등 .env 없는 환경)

API 키 우선순위: --api-key 인자 > FRED_API_KEY 환경변수 > ~/workspace/skills/nonggu-lens/.env
"""
import json
import os
import sys
import urllib.request
import urllib.parse

SERIES = {
    # 금리
    "FEDFUNDS": "미국 기준금리",
    "DGS2": "미국 2년물 국채금리",
    "DGS10": "미국 10년물 국채금리",
    "T10Y2Y": "장단기 스프레드 (10Y-2Y)",
    # 물가
    "CPIAUCSL": "미국 CPI",
    "PCEPILFE": "미국 근원 PCE",
    "PPIACO": "미국 PPI",
    # 고용
    "UNRATE": "미국 실업률",
    "PAYEMS": "비농업 고용자수",
    "ICSA": "주간 신규 실업수당 청구",
    # 신용·유동성
    "BAA": "Moody's BAA 회사채 금리",
    "AAA": "Moody's AAA 회사채 금리",
    "BAMLH0A0HYM2": "하이일드 스프레드",
    # 성장·심리
    "INDPRO": "미국 산업생산",
    "RSXFS": "미국 소매판매",
    "UMCSENT": "미시간 소비자심리",
    "NAPM": "ISM 제조업 PMI",
    # 원자재·환율
    "DCOILWTICO": "WTI 유가",
    "DEXKOUS": "원달러 환율 (KRW/USD)",
    "DTWEXBGS": "달러 인덱스 (Broad)",
}

ENV_PATH = os.path.expanduser("~/workspace/skills/nonggu-lens/.env")


def get_key():
    if os.environ.get("FRED_API_KEY"):
        return os.environ["FRED_API_KEY"]
    try:
        with open(ENV_PATH) as f:
            for line in f:
                if line.startswith("FRED_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except FileNotFoundError:
        pass
    return None


def fetch(series_id, key, limit=1):
    params = urllib.parse.urlencode({
        "series_id": series_id, "api_key": key, "file_type": "json",
        "sort_order": "desc", "limit": limit,
    })
    url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
    with urllib.request.urlopen(url, timeout=20) as r:
        d = json.load(r)
    obs = [o for o in d.get("observations", []) if o["value"] != "."]
    return obs


def main():
    args = sys.argv[1:]
    key_arg = None
    if "--api-key" in args:
        i = args.index("--api-key")
        key_arg = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
    if not args or args[0] == "--list":
        for sid, label in SERIES.items():
            print(f"{sid}: {label}")
        return
    key = key_arg or get_key()
    if not key:
        print("FRED_API_KEY 없음", file=sys.stderr)
        sys.exit(1)
    out = {}
    for sid in args:
        sid = sid.upper()
        try:
            obs = fetch(sid, key)
            if obs:
                o = obs[0]
                out[sid] = {"date": o["date"], "value": o["value"],
                            "label": SERIES.get(sid, sid)}
            else:
                out[sid] = {"error": "관측값 없음"}
        except Exception as e:  # noqa: BLE001
            out[sid] = {"error": type(e).__name__}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
