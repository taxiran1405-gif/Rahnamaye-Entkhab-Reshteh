# Gateهای انتشار

هیچ خروجی کاربر نهایی تا عبور از gateهای مربوطه نباید با زبان قطعی نمایش داده شود.

## G0 — Source
منبع وجود دارد، snapshot ثبت شده و freshness در SLA است.

## G1 — Eligibility
قواعد رسمی، سهمیه، منطقه، شرایط رشته و course_type بررسی شده‌اند.

## G2 — Admission
داده تاریخی به‌اندازه کافی پوشش دارد و uncertainty محاسبه شده است.

## G3 — Personal Fit
ترجیحات داوطلب snapshot شده و utility قابل بازسازی است.

## G4 — Conflict
تعارض منابع آشکار و ثبت شده؛ هیچ conflict بحرانی پنهان نیست.

## G5 — Verification
Red-Team و Verification مستقل PASS داده‌اند.

## G6 — Explainability
هر گزینه دارای reason + confidence + evidence است.

## G7 — Publication
فقط پس از عبور از gateهای بحرانی خروجی publish شود.
