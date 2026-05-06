#!/bin/bash
# 낙화검심 서버 런처 — screen으로 완전히 분리 실행 (Hermes 종료돼도 유지)
# 사용법: bash launch.sh

MUD_HOME="/Users/mirdate/projects/mud/MUD"

echo "🔄 기존 서버 정리 중..."
screen -S mud-api -X quit 2>/dev/null
screen -S mud-front -X quit 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 1

echo "⚙️  백엔드 시작 (8000) — 게임 + 프론트엔드 통합..."
screen -dmS mud-api bash -c "cd $MUD_HOME/backend && /Library/Developer/CommandLineTools/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

sleep 2

echo ""
echo "✅ 서버 상태 확인:"
HEALTH=$(curl -s http://localhost:8000/api/health 2>/dev/null)
echo "$HEALTH"
FRONTEND_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ 2>/dev/null)
echo "프론트엔드: HTTP $FRONTEND_CODE ( / → index.html )"

echo ""
echo "📋 실행 중인 screen 세션:"
screen -ls

echo ""
echo "🔑 명령어:"
echo "  screen -r mud-api    → 서버 로그 보기"
echo "  Ctrl+A, D            → screen에서 빠져나오기"
echo "  bash launch.sh       → 서버 재시작"
echo "  screen -S mud-api -X quit  → 서버 중지"
echo ""
echo "🎮 접속 주소: http://$(hostname -s | tr -d '\n' || echo 'localhost'):8000"
echo "   (다른 기기: http://$(ifconfig en0 2>/dev/null | grep 'inet ' | awk '{print $2}'):8000)"
