# 듀얼 모니터 프로그램 실행 위치 선택 프로그램

듀얼 또는 다중 모니터 환경에서 특정 프로그램이 실행될 모니터를 지정해주는 애플리케이션입니다.

## 🌟 주요 기능

- **모니터 감지**: 현재 연결된 모든 모니터 목록을 자동으로 감지합니다.
- **프로그램 실행 위치 지정**: 원하는 프로그램을 선택하고, 어느 모니터에서 실행할지 지정할 수 있습니다.
- **기본값 저장**: 자주 사용하는 프로그램에 대해 기본 실행 모니터를 저장하여 다음 실행 시 자동으로 적용됩니다.

## 🖥️ 현재 상태

이 프로젝트는 현재 **프로토타입 단계**입니다. UI와 핵심 로직(설정 저장 등)은 구현되었으나, 실제 프로그램 창을 지정된 모니터로 이동시키는 기능은 **플레이스홀더(Placeholder)로 구현**되어 있습니다.

향후 각 운영체제(Windows, macOS)에 맞는 실제 창 제어 로직을 추가하여 완성될 예정입니다.

## 🛠️ 설치 및 실행 방법

1.  **의존성 설치**:
    ```bash
    pip install -r monitor_selector/requirements.txt
    ```

2.  **실행**:
    > **참고**: 현재 코드는 그래픽 환경에서만 UI가 표시됩니다. 헤드리스(headless) 환경에서는 실행되지 않습니다.

    애플리케이션을 실행하려면 `monitor_selector/main.py` 파일의 마지막 부분을 다음과 같이 수정해야 합니다.

    ```python
    if __name__ == "__main__":
        # 아래 주석을 해제하여 실행하세요.
        app = App()
        app.mainloop()
        # print("Tkinter App structure created. Cannot run mainloop in headless environment.")
    ```

    수정 후, 다음 명령어로 실행할 수 있습니다.
    ```bash
    python3 -m monitor_selector.main
    ```

## 📦 실행 파일 생성 (.exe)

Python이 설치되지 않은 환경에서도 프로그램을 쉽게 실행할 수 있도록, `pyinstaller`를 사용하여 `.exe` 파일을 생성할 수 있습니다.

1.  **pyinstaller 설치**:
    ```bash
    pip install pyinstaller
    ```

2.  **.exe 파일 생성**:
    프로젝트 루트 폴더에서 다음 명령어를 실행합니다.
    ```bash
    pyinstaller --onefile --windowed --name MonitorSelector monitor_selector/main.py
    ```
    - 빌드가 완료되면 `dist` 폴더 안에 `MonitorSelector.exe` 파일이 생성됩니다. 이 파일을 배포하여 사용할 수 있습니다.

## 🏗️ 향후 개발 계획

- Windows `pywin32`를 이용한 창 이동 기능 구현
- macOS `AppleScript`를 이용한 창 이동 기능 구현
- 드래그 앤 드롭 기능 추가
- 단축키 및 프리셋 기능 추가