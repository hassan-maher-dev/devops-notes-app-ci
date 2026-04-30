# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تحديد مسار العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المكتبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع (بما فيها مجلد templates تلقائياً)
COPY . .

# إعطاء صلاحيات كاملة للمجلد لضمان قدرة التطبيق على كتابة ملف الـ DB
RUN chmod -R 777 /app

# فتح البورت الذي يعمل عليه التطبيق
EXPOSE 5000

# أمر التشغيل
CMD ["python", "app.py"]