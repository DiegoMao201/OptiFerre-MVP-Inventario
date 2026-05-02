"""Runner simple para recordatorios de trial, pago y nudges de upgrade."""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.subscription_notifications import run_billing_notification_cycle


def main() -> None:
    summary = run_billing_notification_cycle()
    print(summary)


if __name__ == "__main__":
    main()
