# نقشه راه ۱۴۰۶

## Phase 0 — Foundation (این commit)
- معماری.
- قرارداد ایجنت‌ها.
- مدل evidence.
- مدل recommendation cell.
- source registry.
- تعریف Loop و audit.

## Phase 1 — Data Core
- schema دیتابیس.
- entity master برای دانشگاه/شهر/رشته/دوره.
- ingestion پنج‌ساله.
- اتصال داده‌های موجود کتابخانه دانش.
- importer برای منابع PDF/HTML.
- ثبت archive references.

## Phase 2 — Admission Engine
- مدل آماری.
- backtest سال‌های 1400 تا 1404.
- uncertainty.
- rule engine.
- calibration.

## Phase 3 — Career Future
- تکمیل جدول آینده رشته‌ها.
- نگاشت رشته → occupation.
- کشور/منطقه.
- درآمد و تقاضا.
- مهارت‌ها.
- تفکیک fact و interpretation.

## Phase 4 — University & Student Life
- رتبه‌ها.
- اسکان.
- رضایت.
- امکانات.
- کیفیت برنامه/دانشکده.

## Phase 5 — Recommendation UI
- سلول اصلی + موازی‌ها.
- ریسک و confidence.
- explanation.
- منابع و شواهد.
- export.

## Phase 6 — Monitoring
- source sentinel.
- scheduled checks.
- alerting.
- re-run affected records.
- data lineage.

## Phase 7 — Validation
- prediction lock.
- نتیجه واقعی.
- calibration.
- post-mortem.
- نسخه‌بندی مدل.

## Gateهای انتشار
تا وقتی این چهار مورد پاس نشود، سامانه نباید «پیشنهاد قطعی» نمایش دهد:
1. eligibility coverage کافی.
2. داده قبولی با coverage و provenance مشخص.
3. verification loop موفق.
4. confidence و uncertainty نمایش‌پذیر.

## همکاری مورد نیاز
در مرحله معماری، نیروی AI اضافی لازم نیست.
در Phase 1–2، تقسیم کار به چند توسعه‌دهنده/ایجنت تخصصی مفید است؛ باید در GitHub به issueهای مستقل تبدیل شود تا parallel development بدون تداخل انجام شود.
