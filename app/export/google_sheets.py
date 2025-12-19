from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class GoogleSheetsConfig:
    spreadsheet_id: str
    worksheet_name: str
    service_account_json_path: Path


def push_dataframe_to_sheet(df: pd.DataFrame, cfg: GoogleSheetsConfig) -> None:
    """
    Writes a dataframe to a Google Sheet worksheet (clears then updates).
    Requires a service account JSON and the sheet shared with that SA email.
    """
    import gspread  # imported lazily so this remains optional

    gc = gspread.service_account(filename=str(cfg.service_account_json_path))
    sh = gc.open_by_key(cfg.spreadsheet_id)
    try:
        ws = sh.worksheet(cfg.worksheet_name)
    except Exception:
        ws = sh.add_worksheet(title=cfg.worksheet_name, rows=1000, cols=50)

    values = [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
    ws.clear()
    ws.update(values)


