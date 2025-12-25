import sys
from itertools import combinations

INPUT_FILE = r"C:\Users\Lenovo\Desktop\HW4\input.txt"
OUTPUT_FILE = r"C:\Users\Lenovo\Desktop\HW4\output.txt"


def solve_optimization():
    """
    تابع اصلی برای حل مسئله بهینه‌سازی پایداری ستون‌ها.
    """
    try:
        # خط 1: خواندن N (تعداد بلوک‌ها)
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            # 1: خواندن تعداد بلوک‌ها (N)
            N = int(f.readline().strip())

            # 2: خواندن داده‌های بلوک‌ها
            blocks = []
            for i in range(N):
                # 3: خواندن ابعاد بلوک به صورت رشته و تبدیل به لیست اعداد صحیح
                dims = list(map(int, f.readline().strip().split()))

                # 4: مرتب‌سازی ابعاد به طوری که x >= y >= z (قانون نرمال‌سازی)
                dims.sort(reverse=True)
                x, y, z = dims[0], dims[1], dims[2]

                # 5: ذخیره بلوک: (بزرگترین بعد، بعد متوسط، کوچکترین بعد، اندیس اصلی + 1)
                blocks.append((x, y, z, i + 1))

    except FileNotFoundError:
        # 6: اگر فایل یافت نشد، خطا را با متن فارسی نمایش می‌دهیم.
        print("error: input.txt yaft nashod")
        # 7: خروج از تابع
        return
    except Exception as e:
        # 8: مدیریت سایر خطاها (مانند خطای خواندن یا تبدیل)
        print(f"khata dar khandan fail {e}")
        return

    # --- مرحله 1: محاسبه بهترین حالت با 1 بلوک ---
    
    # 9: مقدار اولیه برای بهترین حالت (استفاده از 1 بلوک)
    max_stability = 0
    best_block_count = 1
    best_indices = []

    # 10: پیمایش تمام بلوک‌ها برای یافتن بیشترین پایداری تک بلوکی
    for x, y, z, index in blocks:
        # 11: پایداری یک بلوک برابر است با کوچکترین بعد آن (z)
        stability = z
        # 12: اگر پایداری جدید بیشتر بود، آن را به عنوان بهترین پایداری فعلی ثبت می‌کنیم
        if stability > max_stability:
            max_stability = stability
            best_block_count = 1
            best_indices = [index]

    # --- مرحله 2: گروه‌بندی بلوک‌ها (استفاده از Hash Table/دیکشنری) ---

    # 13: ایجاد دیکشنری برای گروه‌بندی بلوک‌ها بر اساس ابعاد پایه (x, y)
    # کلید: تاپل (x, y)، مقدار: لیستی از ارتفاع‌های z و اندیس‌های اصلی
    blocks_by_base = {}

    # 14: پیمایش همه بلوک‌ها برای پر کردن دیکشنری
    for x, y, z, index in blocks:
        # 15: ابعاد پایه (x, y) به عنوان کلید استفاده می‌شود.
        base_key = (x, y)
        # 16: اگر کلید وجود نداشت، یک لیست جدید با داده‌های فعلی ایجاد می‌کنیم
        if base_key not in blocks_by_base:
            blocks_by_base[base_key] = []
        # 17: اضافه کردن ارتفاع و اندیس به لیست مربوط به آن پایه
        blocks_by_base[base_key].append((z, index))

    # --- مرحله 3: بررسی بهترین حالت با 2 بلوک (در هر گروه) ---

    # 18: پیمایش کلیدها (ابعاد پایه) در دیکشنری
    for base_key, heights_and_indices in blocks_by_base.items():
        # 19: اگر فقط یک بلوک با این پایه وجود داشت، امکان ترکیب نیست، رد می‌کنیم.
        if len(heights_and_indices) < 2:
            continue

        # 20: مرتب‌سازی لیست بر اساس ارتفاع (z) به صورت نزولی
        heights_and_indices.sort(key=lambda item: item[0], reverse=True)

        # 21: انتخاب دو بلوک با بزرگترین ارتفاع‌ها (z1 و z2)
        z1, index1 = heights_and_indices[0]
        z2, index2 = heights_and_indices[1]

        # 22: ابعاد پایه (x, y) از کلید خوانده می‌شود
        x, y = base_key

        # 23: محاسبه پایداری جدید با دو بلوک: min(y, z1 + z2)
        # y همان بعد متوسط است که چون x>=y و ابعاد پایه یکسان است، باید با مجموع ارتفاع‌ها مقایسه شود.
        new_stability = min(y, z1 + z2)

        # 24: بررسی اینکه آیا این ترکیب بهتر از بهترین حالت فعلی است یا خیر
        if new_stability > max_stability:
            max_stability = new_stability
            best_block_count = 2
            # 25: اندیس‌ها باید به صورت صعودی مرتب شوند
            best_indices = sorted([index1, index2])
        # 26: اگر پایداری برابر بود، باید تعداد بلوک کمتر (1 بلوک) را ترجیح دهیم.
        # اما اگر 2 بلوک (که پایداری یکسانی ایجاد کرده‌اند) بهتر از بهترین 1 بلوک فعلی نباشد، تغییری نمی‌دهیم.
        # در این مرحله فقط اگر پایداری بزرگتر بود، به‌روزرسانی می‌کنیم (شرط بالا).

    # --- مرحله 4: نوشتن خروجی در فایل output.txt ---

    # 27: باز کردن فایل خروجی برای نوشتن
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # 28: خط اول: تعداد بلوک‌های استفاده شده (1 یا 2)
        f.write(f"{best_block_count}\n")
        # 29: خط دوم: اندیس‌های 1-based بلوک‌های استفاده شده، جدا شده با فاصله
        f.write(" ".join(map(str, best_indices)) + "\n")
        # 30: خط سوم: حداکثر پایداری به دست آمده (قطر)
        f.write(f"{max_stability}\n")

    # 31: نمایش پیام موفقیت‌آمیز بودن عملیات
    print(f"natayej dar {OUTPUT_FILE} zakhireh shodand.")

# 32: فراخوانی تابع اصلی
solve_optimization()
