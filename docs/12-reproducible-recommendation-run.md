# اجرای قابل بازتولید توصیه

هر پاسخ نهایی باید یک snapshot غیرقابل‌ابهام داشته باشد.

اجزای snapshot:
- profile داوطلب
- source versions
- evidence versions
- agent versions
- model version
- rule version
- weights version
- candidate set hash
- recommendation hash
- verification result

اگر همان ورودی‌ها و همان نسخه‌های داده دوباره در دسترس باشند، سیستم باید بتواند مسیر تصمیم را بازسازی کند.

نتیجه واقعی بعداً به run متصل می‌شود و snapshot پیش‌بینی را تغییر نمی‌دهد.