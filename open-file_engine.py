import os, json, hashlib
SHARED_DIR = "/tmp/bodhi_workspace"
TARGET_REPO = os.environ.get("TARGET_REPO", "retina")

print(f"📄 [OPEN-FILE] Bắt đầu băm SHA-256 tệp tin cho {TARGET_REPO}...")
file_data = {"files": []}

try:
    with open(f"{SHARED_DIR}/tree_data.json", "r") as f: paths = json.load(f)["all_paths"]
    for p in paths:
        full_p = os.path.join(SHARED_DIR, TARGET_REPO, p)
        if os.path.isfile(full_p) and not p.endswith((".pyc", ".ipynb")):
            sz = os.path.getsize(full_p)
            try:
                with open(full_p, "rb") as fr: fh = hashlib.sha256(fr.read()).hexdigest()[:12]
            except: fh = "error"
            file_data["files"].append({"path": p, "size": sz, "hash": fh})
    with open(f"{SHARED_DIR}/file_data.json", "w") as f: json.dump(file_data, f)
    print("✅ [OPEN-FILE] Đã quét xong dung lượng và mã băm.")
except Exception as e: print(f"⚠️ Lỗi: {e}")
