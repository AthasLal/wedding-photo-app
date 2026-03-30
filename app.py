import io, uuid, dropbox
from flask import Flask, request, render_template_string
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# ΡΥΘΜΙΣΕΙΣ
DROPBOX_TOKEN = 'ΤΟ_TOKEN_ΣΟΥ_ΕΔΩ'
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

# HTML ΣΕΛΙΔΑ (Αυτό θα βλέπει ο καλεσμένος)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; background: #f9f9f9; padding: 20px; }
        .upload-btn { background: #d4af37; color: white; padding: 15px 25px; border: none; border-radius: 25px; font-size: 18px; }
    </style>
</head>
<body>
    <h2>💍 Ο Γάμος μας 💍</h2>
    <p>Βγάλτε μια φωτογραφία για να μπει στο αναμνηστικό μας άλμπουμ!</p>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="photo" accept="image/*" capture="environment" required>
        <br><br>
        <button type="submit" class="upload-btn">Ανέβασμα & Πλαίσιο</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('photo')
        if file:
            # 1. Επεξεργασία εικόνας
            img = Image.open(file).convert("RGBA")
            frame = Image.open("frame.png").convert("RGBA")
            
            # Resize frame to match photo
            frame = frame.resize(img.size, Image.Resampling.LANCZOS)
            combined = Image.alpha_composite(img, frame)
            
            # 2. Προετοιμασία για upload
            buffer = io.BytesIO()
            combined.convert("RGB").save(buffer, format="JPEG", quality=85)
            buffer.seek(0)
            
            # 3. Μοναδικό όνομα αρχείου (για να μην σβηστεί καμία!)
            filename = f"/Wedding_Gallery/photo_{datetime.now().strftime('%H%M%S')}_{uuid.uuid4().hex[:4]}.jpg"
            
            dbx.files_upload(buffer.getvalue(), filename)
            return "Η φωτογραφία ανέβηκε! Σας ευχαριστούμε! ❤️"
            
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)