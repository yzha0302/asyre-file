"""Asyre File - First-run setup wizard."""
import json, os, secrets, hashlib, time

def _hash_password(password):
    salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{h}"

def needs_setup(config_dir):
    users_path = os.path.join(config_dir, "users.json")
    if not os.path.exists(users_path):
        return True
    try:
        with open(users_path) as f:
            data = json.load(f)
        users = data.get("users", {})
        if not users:
            return True
        return not any(u.get("role") == "admin" for u in users.values())
    except (json.JSONDecodeError, IOError):
        return True

def handle_setup_post(body, config_dir):
    username = body.get("username", "").strip()
    display_name = body.get("display_name", "").strip() or username
    password = body.get("password", "")
    site_name = body.get("site_name", "").strip() or "Asyre File"
    gen_token = body.get("gen_token", False)
    if not username:
        return {"ok": False, "error": "Username is required"}
    if len(password) < 4:
        return {"ok": False, "error": "Password must be at least 4 characters"}
    users_path = os.path.join(config_dir, "users.json")
    users_data = {"users": {username: {"password_hash": _hash_password(password), "name": display_name, "role": "admin", "paths": ["*"], "created": time.strftime("%Y-%m-%d"), "devices": []}}, "settings": {"sessionExpireHours": 72, "allowRegistration": False}}
    with open(users_path, "w") as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    config_path = os.path.join(config_dir, "config.json")
    cfg = {}
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                cfg = json.load(f)
        except Exception:
            pass
    cfg.setdefault("site", {})["name"] = site_name
    with open(config_path, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    try:
        import config as _cfg
        _cfg.reload(config_dir)
    except Exception:
        pass
    result = {"ok": True}
    if gen_token:
        token = f"asf_{secrets.token_hex(16)}"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        tokens_path = os.path.join(config_dir, "api_tokens.json")
        tokens_data = [{"token_hash": token_hash, "name": "default", "created": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "permissions": ["read", "write", "delete"]}]
        with open(tokens_path, "w") as f:
            json.dump(tokens_data, f, indent=2)
        result["token"] = token
    return result

def cli_setup(config_dir):
    import getpass
    print("=" * 50)
    print("  Asyre File - First-time Setup")
    print("=" * 50)
    username = input("Admin username [admin]: ").strip() or "admin"
    display_name = input(f"Display name [{username}]: ").strip() or username
    while True:
        password = getpass.getpass("Admin password: ")
        if len(password) < 4:
            print("  Password must be at least 4 characters.")
            continue
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("  Passwords do not match.")
            continue
        break
    result = handle_setup_post({"username": username, "display_name": display_name, "password": password, "site_name": "Asyre File", "gen_token": False}, config_dir)
    if result.get("ok"):
        print("Admin user created. Run: python3 server.py")
    else:
        print(f"Error: {result.get('error')}")

SETUP_HTML = '<!DOCTYPE html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Asyre File Setup</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0d1117;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh}.card{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:40px;width:420px;max-width:calc(100vw - 32px);box-shadow:0 16px 48px rgba(0,0,0,.4)}h1{font-size:22px;margin-bottom:4px}.sub{color:#8b949e;font-size:13px;margin-bottom:28px}label{display:block;font-size:13px;font-weight:600;margin-bottom:6px;color:#c9d1d9}input{width:100%;padding:10px 12px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#e6edf3;font-size:14px;margin-bottom:16px;outline:none}input:focus{border-color:#a855f7}.row{display:flex;gap:12px}.row>div{flex:1}.btn{width:100%;padding:12px;background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;margin-top:8px}.btn:disabled{opacity:.5}.err{background:rgba(248,81,73,.1);color:#f85149;padding:10px;border-radius:6px;font-size:13px;margin-bottom:16px;display:none}.chk{display:flex;align-items:center;gap:8px;margin-bottom:16px;font-size:13px;color:#8b949e}.chk input{width:auto;margin:0}</style></head><body><div class="card"><h1>Asyre File</h1><div class="sub">First-time setup &mdash; create your admin account</div><div class="err" id="err"></div><form id="f" onsubmit="return go(event)"><div class="row"><div><label>Username</label><input id="u" value="admin" required></div><div><label>Display Name</label><input id="dn" placeholder="Your name"></div></div><label>Password</label><input type="password" id="pw" required minlength="4" placeholder="At least 4 characters"><label>Confirm</label><input type="password" id="pw2" required minlength="4"><label>Site Name</label><input id="sn" value="Asyre File"><label class="chk"><input type="checkbox" id="gt"> Generate API token for agents</label><button type="submit" class="btn" id="sb">Complete Setup</button></form><div id="res" style="display:none"></div></div><script>async function go(e){e.preventDefault();var err=document.getElementById("err");if(document.getElementById("pw").value!==document.getElementById("pw2").value){err.textContent="Passwords do not match";err.style.display="block";return false}err.style.display="none";document.getElementById("sb").disabled=true;document.getElementById("sb").textContent="Setting up...";try{var r=await fetch("/_setup",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:document.getElementById("u").value.trim(),display_name:document.getElementById("dn").value.trim(),password:document.getElementById("pw").value,site_name:document.getElementById("sn").value.trim(),gen_token:document.getElementById("gt").checked})});var d=await r.json();if(d.ok){if(d.token){document.getElementById("f").style.display="none";var res=document.getElementById("res");res.style.display="block";res.innerHTML="<div style=text-align:center><h2 style=color:#3fb950;margin-bottom:16px>Setup Complete</h2><p style=margin-bottom:12px;font-size:13px;color:#8b949e>Save your API token (shown only once):</p><div style=background:#0d1117;border:1px_solid_#30363d;border-radius:8px;padding:12px;font-family:monospace;font-size:14px;color:#a855f7;word-break:break-all;margin-bottom:20px>"+d.token+"</div><a href=./login style=display:inline-block;padding:10px_24px;background:#a855f7;color:#fff;border-radius:8px;text-decoration:none;font-weight:600>Go to Login</a></div>"}else{location.href="./login"}}else{err.textContent=d.error;err.style.display="block";document.getElementById("sb").disabled=false;document.getElementById("sb").textContent="Complete Setup"}}catch(ex){err.textContent="Failed: "+ex.message;err.style.display="block";document.getElementById("sb").disabled=false;document.getElementById("sb").textContent="Complete Setup"}return false}</script></body></html>'
