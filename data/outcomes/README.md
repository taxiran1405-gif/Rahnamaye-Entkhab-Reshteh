# Outcome Registry

این پوشه قالب داده واقعی نتیجه داوطلبان را نگه می‌دارد.

## ورودی لازم
- candidate_anonymous_id
- admission_year
- quota_type
- region در صورت سهمیه منطقه
- actual_quota_rank
- actual_national_rank
- choice_code
- selected_choice_order
- accepted
- accepted program/university/course
- result source/evidence

## قاعده
شناسه داوطلب باید ناشناس باشد و هیچ داده هویتی وارد repository نشود.

پیش‌بینی قبل از اعلام نتیجه باید با recommendation_run و candidate_set_hash قفل شده باشد؛ نتیجه بعداً به همان run متصل می‌شود.

هیچ outcome پس از اعلام نتیجه نباید برای بازسازی prediction قبلی استفاده شود.
