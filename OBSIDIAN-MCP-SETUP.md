# Obsidian MCP 연동 가이드

이 vault를 Claude Desktop / Claude Code에서 MCP로 읽고 쓰는 방법.
MCP 서버는 별도 설치 없이 Obsidian의 **Local REST API** 플러그인에 내장되어 있다.

## 1. Vault 열기 (PC에서 1회)

```bash
git clone https://github.com/kmskr2000-tech/guru-brain.git
```

Obsidian에서 `guru-brain` 폴더를 vault로 열기.

## 2. Local REST API 플러그인 (Obsidian에서 1회)

1. 설정 → 커뮤니티 플러그인 → 찾아보기 → **"Local REST API"** 검색·설치·활성화
2. 플러그인 설정에서 API 키 복사 (유출 금지)

## 3. MCP 클라이언트 연결

### Claude Desktop

`claude_desktop_config.json`에 추가 (Windows: `%APPDATA%\Claude\`, macOS: `~/Library/Application Support/Claude/`):

```json
{
  "mcpServers": {
    "guru-brain": {
      "command": "npx",
      "args": [
        "mcp-remote@latest",
        "https://127.0.0.1:27124/mcp/",
        "--header",
        "Authorization: Bearer <API 키>"
      ]
    }
  }
}
```

저장 후 Claude Desktop 재시작.

### Claude Code (CLI)

```bash
claude mcp add guru-brain -- npx mcp-remote@latest https://127.0.0.1:27124/mcp/ --header "Authorization: Bearer <API 키>"
```

## 4. 확인

- Obsidian이 켜져 있고 vault가 열려 있어야 MCP가 동작한다.
- 연결되면 노트 읽기/쓰기/검색 도구가 MCP 도구 목록에 뜬다.

## 참고

- 플러그인: https://github.com/coddingtonbear/obsidian-local-rest-api
- API 키는 절대 깃에 올리지 않는다.
