FROM python:3.10-slim

# वर्किंग डायरेक्टरी सेट करें
WORKDIR /app

# requirements.txt कॉपी और इंस्टॉल करें
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# बाकी सब कॉपी करें
COPY . .

# Render 'Procfile' का उपयोग करेगा, लेकिन यह CMD एक फॉलबैक है
CMD ["gunicorn", "bot:app", "--bind", "0.0.0.0:$PORT"]
