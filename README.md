# DRILL 9: 소년 상하좌우 이동 및 방향 바꾸기

`pico2d`로 배경 위의 소년을 방향키로 움직이는 과제입니다.

## 실행

Python에 `pico2d`를 설치한 후 저장소 폴더에서 다음 명령을 실행합니다.

```text
python move_character_with_key.py
```

- 방향키: 상하좌우 이동. 두 방향키를 함께 누르면 대각선으로 이동합니다.
- 좌우 방향키: 캐릭터가 바라보는 방향을 바꿉니다. 위아래로 이동할 때는 이 방향을 유지합니다.
- 방향키를 놓으면 현재 방향의 대기 애니메이션이 실행됩니다.
- Escape 또는 창 닫기: 종료합니다.

배경은 `TUK_GROUND.png`, 캐릭터 스프라이트는 `animation_sheet.png`를 사용합니다.
캐릭터 프레임 전체가 화면 안에 있도록 위치를 제한합니다.

## 테스트

```text
python -m unittest discover -s tests -v
```

설계와 스프라이트 시트 구조는 [개발 문서](DEVELOPMENT.md)에 정리했습니다.
