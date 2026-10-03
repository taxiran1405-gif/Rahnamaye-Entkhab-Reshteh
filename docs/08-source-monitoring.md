# Source Sentinel

نسخه فعلی یک پایشگر قابل اجرای GitHub Actions دارد که منابع منتخب را هر 6 ساعت بررسی می‌کند و fingerprint محتوا را در state ثبت می‌کند.

این با «شبانه‌روزی واقعی» یکسان نیست؛ اجرای production باید scheduler خارجی یا سرویس همیشه‌فعال داشته باشد تا SLA منبع رسمی را تضمین کند. معماری این محدودیت را صریح نگه می‌دارد.

## قواعد
- تغییر منبع رسمی سنجش = CRITICAL.
- تغییر دفترچه/اصلاحیه = بازاجرای eligibility و admission.
- تغییر داده رتبه/کیفیت = بازاجرای University Quality.
- تغییر WEF/BLS = بازاجرای Career Future.
- خطای fetch نباید به‌عنوان «بدون تغییر» تفسیر شود؛ status=error ثبت می‌شود.

## نکته اجرایی
قبل از فعال‌کردن auto-commit در محیط production، بهتر است یک مرحله review/approval برای تغییرات CRITICAL اضافه شود.
