"""Contract checker for future import of the project knowledge workbook.

This is deliberately a schema/coverage validator, not a lossy converter. A production
import should preserve original row, sheet, source and locator before normalization.
"""
import json
from pathlib import Path

REQUIRED_SHEETS={
    "منابع","داده_اولیه_قبولی","رتبه_دانشگاه","قواعد_AI",
    "آخرین_رتبه_قبولی","ردیابی_منابع_رتبه","داده_تازه_1404",
    "مدل_ترجیحات_داوطلب","وزن_عوامل","الگوریتم_مشاوره",
    "فرم_داوطلب","فرم_نتیجه_واقعی","فرم_ارزیابی"
}

def validate_sheet_names(sheet_names):
    missing=sorted(REQUIRED_SHEETS-set(sheet_names))
    return {"ok":not missing,"missing":missing,"expected_count":len(REQUIRED_SHEETS)}

if __name__=="__main__":
    print(json.dumps({
        "required_sheets":sorted(REQUIRED_SHEETS),
        "rule":"Do not discard any source row during normalization; preserve raw_sheet/raw_row/source_locator."
    },ensure_ascii=False,indent=2))
