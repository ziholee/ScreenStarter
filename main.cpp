#include <windows.h>
#include <commdlg.h>
#include <tchar.h>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <psapi.h>

POINT g_cursorPos;
RECT g_targetMonitor;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// 커서가 있는 모니터 찾기
BOOL CALLBACK MonitorEnumProc(HMONITOR, HDC, LPRECT lprcMonitor, LPARAM lParam) {
    std::vector<RECT>* monitors = reinterpret_cast<std::vector<RECT>*>(lParam);
    monitors->push_back(*lprcMonitor);
    return TRUE;
}

// PID로 실행된 창 핸들 찾기
HWND FindWindowByPID(DWORD pid) {
    HWND hwnd = GetTopWindow(NULL);
    while (hwnd) {
        DWORD winPid;
        GetWindowThreadProcessId(hwnd, &winPid);
        if (winPid == pid && IsWindowVisible(hwnd)) {
            return hwnd;
        }
        hwnd = GetNextWindow(hwnd, GW_HWNDNEXT);
    }
    return NULL;
}

// 파일 선택 창
std::wstring OpenFileDialog(HWND hwnd) {
    wchar_t szFile[MAX_PATH] = { 0 };
    OPENFILENAME ofn = { sizeof(OPENFILENAME) };
    ofn.hwndOwner = hwnd;
    ofn.lpstrFilter = L"Executable Files\0*.exe\0All Files\0*.*\0";
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = MAX_PATH;
    ofn.Flags = OFN_FILEMUSTEXIST;
    if (GetOpenFileName(&ofn)) {
        return std::wstring(szFile);
    }
    return L"";
}

// 프로그램 실행 및 위치 이동
void RunProgramOnCurrentMonitor(std::wstring programPath) {
    GetCursorPos(&g_cursorPos);
    std::vector<RECT> monitors;
    EnumDisplayMonitors(NULL, NULL, MonitorEnumProc, reinterpret_cast<LPARAM>(&monitors));

    for (const auto& monitor : monitors) {
        if (PtInRect(&monitor, g_cursorPos)) {
            g_targetMonitor = monitor;
            break;
        }
    }

    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    if (!CreateProcess(NULL, &programPath[0], NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        MessageBox(NULL, L"프로그램 실행 실패", L"오류", MB_ICONERROR);
        return;
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));

    HWND hwnd = FindWindowByPID(pi.dwProcessId);
    if (hwnd) {
        int width = 800, height = 600;
        SetWindowPos(hwnd, HWND_TOP, g_targetMonitor.left + 100, g_targetMonitor.top + 100, width, height, SWP_SHOWWINDOW);
    }

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}

// 진입점
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    const wchar_t CLASS_NAME[] = L"MultiMonitorLauncher";
    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(0, CLASS_NAME, L"멀티 모니터 프로그램 실행기",
        WS_OVERLAPPEDWINDOW & ~WS_THICKFRAME & ~WS_MAXIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 400, 200,
        NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}

// GUI 처리
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    static HWND hButton;
    static HWND hExitButton; // 종료 버튼 핸들 추가

    switch (msg) {
    case WM_CREATE:
        // 기존 버튼 수정: 레이블 변경, x 좌표 및 너비 조정
        hButton = CreateWindow(L"BUTTON", L"프로그램 실행",
            WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
            50, 60, 140, 40, // x=50, 너비=140
            hwnd, (HMENU)1, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);

        // 새 버튼 "종료" 추가
        hExitButton = CreateWindow(L"BUTTON", L"종료",
            WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
            210, 60, 140, 40, // x=210, 너비=140, y는 동일
            hwnd, (HMENU)2, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
        break;

    case WM_COMMAND:
        if (LOWORD(wParam) == 1) { // "프로그램 실행" 버튼
            std::wstring filePath = OpenFileDialog(hwnd);
            if (!filePath.empty()) {
                RunProgramOnCurrentMonitor(filePath);
            }
        } else if (LOWORD(wParam) == 2) { // "종료" 버튼
            PostQuitMessage(0);
        }
        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, msg, wParam, lParam);
}
