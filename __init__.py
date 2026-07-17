"""One-shot bootstrap: WAI Illustrious ckpt + Bai Ning Bing e5 LoRA."""
import os
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMFY = HERE.parent if (HERE.parent / "models").is_dir() else HERE.parents[1]

CKPT = COMFY / "models" / "checkpoints" / "waiNSFWIllustrious_v150.safetensors"
LORA = COMFY / "models" / "loras" / "bai_ning_bing_e5.safetensors"

DEFAULT_CKPT = "https://huggingface.co/SiE69/Illoustrious_Checkpoint_Collection/resolve/main/waiNSFWIllustrious_v150.safetensors"
DEFAULT_LORA = "https://orchestration-new.civitai.com/v2/consumer/blobs/Y8152CCDC3RQ724X6ZSJ143N90.safetensors?sig=CfDJ8EVzXboigx9EiFXpbVmCZiby9XoJJDxF9pyATBXKKe8MRIp0pwMfHDBmqy-piOIrrgwQzlUVo9VMpuE5myBc74R8LbqScM9hwnX5dg7svWuHXf6sqIVPCKOLfxiUgjgX56ntYvJu0-IVrCf3qk-zIzNyvOj6XkO5VXkFQwotCgKvJjobYm4YVIH3Snps3oOZNRmyrGjrTXzPgkH0X3w77OR_ejgGaHaUSrSD_Z_2ighWpykePrknuR-_-0F1NZEjJg&exp=2026-07-24T07:18:59.8321959Z"

def _download(url: str, dest: Path) -> None:
    if not url:
        print(f"[bnb-bootstrap] skip {dest.name}: empty URL")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1_000_000:
        print(f"[bnb-bootstrap] exists {dest} ({dest.stat().st_size} bytes)")
        return
    tmp = dest.with_suffix(dest.suffix + ".partial")
    print(f"[bnb-bootstrap] downloading {dest.name} ...")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(dest)
    print(f"[bnb-bootstrap] saved {dest} ({dest.stat().st_size} bytes)")

def bootstrap():
    ckpt_url = os.environ.get("BOOTSTRAP_CKPT_URL", DEFAULT_CKPT)
    lora_url = os.environ.get("BOOTSTRAP_LORA_URL", DEFAULT_LORA)
    try:
        _download(ckpt_url, CKPT)
        _download(lora_url, LORA)
    except Exception as e:
        print(f"[bnb-bootstrap] ERROR: {e}")

bootstrap()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}