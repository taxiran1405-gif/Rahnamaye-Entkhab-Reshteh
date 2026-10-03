# وضعیت اجرایی corpus تاریخی ریاضی

آخرین به‌روزرسانی: 2026-10-03

## اجراشده
- چهار سال 1400، 1401، 1402، 1403 در matrix تعریف شده‌اند.
- هر سال artifact مستقل دارد.
- PDF خام، SHA-256، متن صفحه‌ای، جدول‌ها و candidate rows نگهداری می‌شوند.
- منبع واقعی فایل دانلودشده در source-meta.json نگهداری می‌شود.
- raw catalog و mapping محافظه‌کارانه آماده‌اند.
- canonical annual snapshot و revision materialization آماده‌اند.
- outcome schema و calibration metrics آماده‌اند.

## در حال اجرا / نیازمند GitHub Runner
- دریافت فایل خام چهار دفترچه.
- استخراج کامل همه جدول‌های رشته‌محل.
- تولید artifact سالانه.
- canonicalization کامل artifactها.

## هنوز انجام نشده
- ورود کامل همه کدرشته‌محل‌ها به canonical DB.
- اتصال کامل admission history هم‌سهمیه/هم‌منطقه به همه choice codes.
- outcome واقعی داوطلبان.
- calibration نهایی با نتایج واقعی.

## معیارهای عدم انتشار
تا زمانی که هر چهار سال artifact معتبر و snapshot نهایی تولید نشده‌اند:
- full_corpus = false
- five_year_calibrated = false

تا زمانی که outcome واقعی و prediction snapshot قفل‌شده وجود ندارد:
- calibrated_probability = false

## نکته اعتبار منبع
دفترچه‌های بازیابی‌شده از mirrorها در صورت استفاده با authority پایین‌تر از منبع اولیه نگهداری می‌شوند؛ mirror هرگز خودکار به official ارتقا پیدا نمی‌کند.
