import requests, os, subprocess,sys
repo_url = "https://api.github.com/repos/dodam2015/mystatus/git/trees/main?recursive=1"
token = "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"
def list_repo_folders():
    response = requests.get(repo_url)
    if response.status_code == 200:
        data = response.json()
        folders = set()
        for item in data['tree']:
            if item['type'] == 'tree':
                path_parts = item['path'].split('/')
                if len(path_parts) == 1:
                    folders.add(path_parts[0])
        print("mystatus 버전 목록:")
        for folder in sorted(folders):
            print(folder)
    else:
        print(f"요청 실패:{response.status_code}")
# 🔽 main.py 다운로드
def download_main_py(user_input):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join(base_dir, "version")
    os.makedirs(target_folder, exist_ok=True)

    url = f"https://raw.githubusercontent.com/dodam2015/mystatus/main/{user_input}/main.py"
    save_path = os.path.join(target_folder, f"{user_input}.py")

    headers = { "Authorization": f"token {token}" }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"게임이 다운로드 됐습니다. 경로:{save_path}")
    else:
        print(f"실패:{response.status_code}")
        print(f"요청 URL: {url}")

# ▶️ 저장된 파이썬 파일 실행
def run_downloaded_version():
    version_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version")
    if not os.path.exists(version_dir):
        print("게임 설치된게 없습니다.")
        return

    files = [f for f in os.listdir(version_dir) if f.endswith('.py')]
    if not files:
        print("실행할 버전이 없습니다.")
        pass

    print("설치한 버전:")
    for i, f in enumerate(files):
        print(f"{i + 1}:{f}")
    
    try:
        choice = int(input("실행할 번호 선택:")) - 1
        selected = files[choice]
        path = os.path.join(version_dir, selected)
        print(f"🚀 실행 중: {selected}")
        os.system("cls")
        subprocess.run(["python", path])
    except (IndexError, ValueError):
        print("잘못된 선택입니다.")

# 🧭 메인 메뉴
if __name__ == "__main__":
    print("🎮 mystatus 게임 메뉴")
    print("1: 게임 다운로드")
    print("2: 게임 실행하기")
    choice = input("선택:").strip()

    if choice == "1":
        list_repo_folders()
        user_input = input("📥 다운로드할 버전 입력:").strip()
        download_main_py(user_input)
    elif choice == "2":
        run_downloaded_version()
    else:
        print("잘못된 선택입니다.")
