---
title: Perplexity
area: connections
summary: Perplexity 대화, 작업 결과, 크레딧이 줄었을 때 알림.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## 읽는 내용

최근 Perplexity 대화, Perplexity 작업(Tasks)이 실행될 때마다의 결과, 크레딧 잔액을 읽어요. 대화가 해야 할 일로 끝나거나 작업이 새 소식을 가져오면 The Machine이 그것을 할 일로 만들 수 있어요. 크레딧이 2 이하로 떨어지면 한 번 알려 주고, 충전한 뒤 다시 줄어들 때만 또 알려 줘요.

Perplexity에 로그인한 OpenClaw 브라우저를 통해 7:00부터 22:00 사이에 약 1시간에 한 번 읽어요. 처음 읽을 때는 1주일 전까지 거슬러 읽어요.

## 할 수 있는 작업

없어요. 읽기만 해요. Perplexity에 질문하지 않고, 대화나 작업을 바꾸거나 이름을 바꾸거나 삭제하지 않아요.

## 연결하기

1. OpenClaw 브라우저에서 Perplexity에 한 번 로그인하세요. 그 브라우저에서 https://www.perplexity.ai/ 을 열고 로그인하면 돼요.
2. 대시보드에서 **연결**을 연 다음 **기타**를 선택하고 Perplexity를 선택하세요. 호스팅된 Machine에서는 설정 페이지의 **더 많은 소스**에서도 찾을 수 있어요. 직접 사용하는 컴퓨터에서는 `assistant connect perplexity`을 실행해도 돼요.

Perplexity에는 대화를 읽는 앱에 로그인을 허용하는 방법이 없어서, 로그인된 브라우저를 사용해요. 키는 필요 없어요.

## 삭제하기

대시보드에서 Perplexity를 열고 **세부 정보**를 선택한 다음 **연결 해제**를 누르세요. 브라우저의 접근도 끝내려면 OpenClaw 브라우저에서 Perplexity에서 로그아웃하세요.
