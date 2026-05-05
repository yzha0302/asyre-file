"""Asyre File — Configuration loader.

Cascade: defaults → config.json → ASF_* environment variables.
"""
import json
import os

__version__ = "1.0.0"

_DEFAULTS = {
    "server": {
        "host": "0.0.0.0",
        "port": 8765,
        "base_url": "",
    },
    "site": {
        "name": "Asyre File",
        "language": "en",
    },
    "workspace": {
        "path": "./data",
        "max_upload_mb": 50,
        "trash_enabled": True,
    },
    "data_dir": {
        "path": "",
    },
    "auth": {
        "session_timeout_hours": 72,
        "allow_registration": False,
    },
    "ai": {
        "enabled": False,
        "provider": "anthropic",
        "api_key": "",
        "model": "claude-sonnet-4-5-20250514",
        "endpoint": "",
        "system_prompt": "",
    },
    "export": {
        "pdf_enabled": True,
        "word_enabled": True,
    },
    "api": {
        "enabled": True,
    },
    "editor": {},
}

_ENV_PREFIX = "ASF_"

# Type coercion for env vars
_BOOL_TRUE = {"1", "true", "yes", "on"}
_BOOL_FALSE = {"0", "false", "no", "off"}


def _deep_merge(base, override):
    """Merge override into base, returning new dict."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _coerce(value, reference):
    """Coerce string env var to the type of the reference value."""
    if isinstance(reference, bool):
        return value.lower() in _BOOL_TRUE
    if isinstance(reference, int):
        try:
            return int(value)
        except ValueError:
            return reference
    if isinstance(reference, float):
        try:
            return float(value)
        except ValueError:
            return reference
    return value


def _apply_env(cfg):
    """Override config with ASF_* environment variables.
    
    Mapping: ASF_SERVER_PORT -> cfg["server"]["port"]
    """
    for key, val in os.environ.items():
        if not key.startswith(_ENV_PREFIX):
            continue
        parts = key[len(_ENV_PREFIX):].lower().split("_", 1)
        if len(parts) != 2:
            continue
        section, field = parts
        if section in cfg and isinstance(cfg[section], dict):
            ref = cfg[section].get(field)
            if ref is not None:
                cfg[section][field] = _coerce(val, ref)
            else:
                cfg[section][field] = val
    return cfg


def load(config_dir=None):
    """Load configuration. config_dir defaults to the directory containing this file."""
    if config_dir is None:
        config_dir = os.path.dirname(os.path.abspath(__file__))
    
    cfg = dict(_DEFAULTS)
    # Deep copy defaults
    cfg = json.loads(json.dumps(_DEFAULTS))
    
    # Layer 2: config.json
    config_path = os.path.join(config_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                user_cfg = json.load(f)
            cfg = _deep_merge(cfg, user_cfg)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[asyre-file] Warning: could not load {config_path}: {e}")
    
    # Layer 3: environment variables
    cfg = _apply_env(cfg)
    
    # Resolve workspace path
    ws = cfg["workspace"]["path"]
    if not os.path.isabs(ws):
        ws = os.path.join(config_dir, ws)
    cfg["workspace"]["path"] = os.path.abspath(ws)
    
    return cfg


# Singleton
_config = None

def get(key=None):
    """Get config value. key like server.port or None for full dict."""
    global _config
    if _config is None:
        _config = load()
    if key is None:
        return _config
    parts = key.split(".")
    val = _config
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p)
        else:
            return None
    return val


def reload(config_dir=None):
    """Force reload config."""
    global _config
    _config = load(config_dir)
    return _config
