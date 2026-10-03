# Runbook استخراج دفترچه‌های پایه ریاضی ۱۴۰۰ تا ۱۴۰۳

چهار دفترچه پایه گروه آزمایشی علوم ریاضی و فنی ابتدا با URL اصلی و fallback بازیابی می‌شوند.

اسکریپت:
1. PDF خام را ذخیره می‌کند.
2. SHA-256 را ثبت می‌کند.
3. متن را صفحه‌به‌صفحه نگه می‌دارد.
4. همه جدول‌های شناسایی‌شده را نگه می‌دارد.
5. جدول‌های محتمل رشته‌محل را flag می‌کند.
6. هیچ مقدار خامی را در normalization بازنویسی نمی‌کند.

پس از استخراج:
raw rows -> mapping -> revision events -> annual offering snapshot -> admission history -> locked predictions -> outcomes -> calibration

Mirror بودن منبع به معنی official بودن نیست؛ authority و verification status در داده حفظ می‌شود.
