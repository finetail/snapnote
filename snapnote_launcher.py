"""GUI launcher with early-stage error logging."""
import sys
import traceback
from pathlib import Path

# exe と同じフォルダの logs/ にログを出力
if getattr(sys, "frozen", False):
    base_dir = Path(sys.executable).parent
else:
    base_dir = Path(__file__).parent

log_dir = base_dir / "logs"
log_dir.mkdir(exist_ok=True)
log_path = log_dir / "snapnote-error.log"

try:
    from snapnote.gui import main
    main()
except Exception:
    err = traceback.format_exc()
    log_path.write_text(err, encoding="utf-8")
    try:
        import tkinter.messagebox as mb
        mb.showerror("snapnote エラー", err)
    except Exception:
        pass
    sys.exit(1)
