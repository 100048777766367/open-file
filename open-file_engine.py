import os, json, hashlib

WORKSPACE = "/tmp/bodhi_dissector"
os.chdir(WORKSPACE)

print("📄 [OPEN-FILE REAL ENGINE] Đang đo dung lượng và băm SHA-256 từng file...")
file_result = {"files": []}

try:
    with open("tree_out.json", "r") as f: paths = json.load(f)["paths"]
    repos = [d for d in os.listdir(".") if os.path.isdir(d) and d not in ["storage"]]
    target_repo = repos[0] if repos else "retina"

    for p in paths:
        full_p = os.path.join(target_repo, p)
        if os.path.isfile(full_p) and not p.endswith((".pyc", ".ipynb")):
            sz = os.path.getsize(full_p)
            try:
                with open(full_p, "rb") as fr: fh = hashlib.sha256(fr.read()).hexdigest()[:12]
            except: fh = "error_hash"
            file_result["files"].append({"path": p, "size_bytes": sz, "hash": fh})

    with open("file_out.json", "w") as f: json.dump(file_result, f)
    print(f"✅ [OPEN-FILE] Đã băm xong {len(file_result['files'])} tệp vào `file_out.json`.")
except Exception as e:
    print(f"🔴 Lỗi ở open-file: {e}")
