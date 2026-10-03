# Canonical Database v0.1

پایگاه داده منبع تصمیم است؛ LLM نباید محل نگهداری حقیقت باشد.

## قواعد اصلی
- raw evidence و canonical entity هر دو حفظ شوند.
- هر رکورد تصمیمی باید به source/evidence متصل باشد.
- حذف داده conflicting ممنوع؛ وضعیت آن ثبت شود.
- admission key: year × group × program × university × campus × course_type × quota × region.
- رتبه دانشگاه: source × edition × metric_scope.
- درآمد بازار کار: occupation × country × year × statistic_type.
- profile داوطلب snapshot می‌شود تا نتیجه بعداً قابل بازتولید باشد.

## انتشار
رکوردهای provisional با برچسب خود وارد آزمون می‌شوند و تا تأیید منبع اصلی، واقعیت قطعی تلقی نمی‌شوند.
