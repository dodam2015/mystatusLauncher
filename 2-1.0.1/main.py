import requests, os, subprocess, sys, zipfile, io, shutil

repo_url = "https://api.github.com/repos/dodam2015/mystatus/git/trees/main?recursive=1"

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
        print('입력할때, 번호를 입력하는게 아니라 진짜 풀네임을 입력합니다.')
        for folder in sorted(folders):
            print(folder)
    else:
        print(f"요청 실패:{response.status_code}")

# 🔽 전체 폴더 다운로드
def download_version_folder(version_name):
    zip_url = "https://github.com/dodam2015/mystatus/archive/refs/heads/main.zip"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    version_dir = os.path.join(base_dir, "version", version_name)

    if os.path.exists(version_dir):
        print(f"{version_name}은 이미 다운로드 되어 있습니다.")
        return

    print("📦 저장소 압축 파일 다운로드 중...")
    response = requests.get(zip_url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            extracted_path_prefix = "mystatus-main/"
            subfolder_path = extracted_path_prefix + version_name + "/"

            members_to_extract = [m for m in zip_file.namelist() if m.startswith(subfolder_path)]

            if not members_to_extract:
                print(f"❌ '{version_name}' 폴더를 찾을 수 없습니다.")
                return

            os.makedirs(version_dir, exist_ok=True)
            for member in members_to_extract:
                filename = os.path.relpath(member, subfolder_path)
                if not filename:
                    continue
                target_path = os.path.join(version_dir, filename)
                if member.endswith("/"):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    with open(target_path, "wb") as f:
                        f.write(zip_file.read(member))
            print(f"✅ '{version_name}' 버전이 다운로드 되었습니다. 경로: {version_dir}")
    else:
        print(f"❌ 다운로드 실패: {response.status_code}")

# ▶️ 저장된 파이썬 파일 실행
def run_downloaded_version():
    version_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version")
    if not os.path.exists(version_root):
        print("게임 설치된게 없습니다.")
        return

    versions = [d for d in os.listdir(version_root) if os.path.isdir(os.path.join(version_root, d))]
    if not versions:
        print("실행할 버전이 없습니다.")
        return

    print("설치한 버전:")
    for i, v in enumerate(versions):
        print(f"{i + 1}: {v}")
    
    try:
        choice = int(input("실행할 번호 선택:")) - 1
        selected_version = versions[choice]
        main_path = os.path.join(version_root, selected_version, "main.py")
        if not os.path.isfile(main_path):
            print("❌ main.py가 없습니다.")
            return
        print(f"🚀 실행 중: {selected_version}")
        os.system("cls" if os.name == "nt" else "clear")
        subprocess.run([sys.executable, main_path])
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
        download_version_folder(user_input)
    elif choice == "2":
        run_downloaded_version()
    else:
        print("잘못된 선택입니다.")
