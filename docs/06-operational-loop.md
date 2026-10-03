# پایش، Loop و صحت‌سنجی

## Loop اصلی تصمیم
هر پیشنهاد باید دست‌کم یک چرخه کامل داشته باشد:

```text
Draft Recommendation
       ↓
Evidence Check
       ↓
Rule Check
       ↓
Statistical Check
       ↓
Preference Check
       ↓
Conflict Check
       ↓
Final Verification
       ↓
PASS ───────────────→ Publish
  │
  └─ FAIL → mark reason → re-fetch/recompute → verify again
```

## Loop پایش منبع
A01 به صورت مداوم تغییرات را ثبت می‌کند:
```text
Fetch → Fingerprint → Compare → Detect change
      → classify impact → queue affected entities
      → re-run affected agents → verify → publish version
```

## سطح اثر تغییر
- CRITICAL: قواعد پذیرش، دفترچه، سهمیه، زمان‌بندی، شرایط قانونی.
- HIGH: تغییر رتبه/رکورد قبولی/ظرفیت.
- MEDIUM: خوابگاه، امکانات، رضایت، هزینه زندگی.
- LOW: متن توضیحی یا metadata غیرتصمیمی.

## Triggerهای بازتحلیل
- منبع رسمی جدید.
- اصلاحیه دفترچه.
- ورود داده جدید برای سال 1406.
- تغییر در rank/cutoff history.
- تغییر profile داوطلب.
- کشف conflict.
- انقضای freshness SLA.

## Audit Log
برای هر اجرای recommendation:
- run_id
- timestamp
- source versions
- agent versions
- model version
- rule version
- weights version
- candidate set hash
- final recommendation hash
- verification status
- later outcome

## معیارهای پساآزمون
پس از اعلام نتایج:
- hit rate.
- calibration.
- confidence calibration.
- false-safe / false-risk errors.
- سهم خطاهای ناشی از داده.
- سهم خطاهای مدل.
- رضایت داوطلب.
- موارد dangerous error.

هدف اصلی فقط «درصد قبولی» نیست؛ کیفیت تصمیم و قابلیت توضیح نیز باید سنجیده شود.
