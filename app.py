import io, uuid, dropbox
from flask import Flask, request, render_template_string
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# ΡΥΘΜΙΣΕΙΣ
DROPBOX_TOKEN = 'sl.u.AGa1e72ROguJPSl3-_7Gh8LL6CBnoUQNBmJeUdUO9EJFj_hXzBhKDqK61PNyH6Ilk86yAUCv3xhnEjQnvtIQ5Mn7G2akPq2JhJOn16GSInwT786YU0deQHlscieVrYowkFaW2tQgIyo0EiIApDSZ-qnUmnyay3kMb492rGPqDgSK5W7pBIUpTJOz_oDzVZpbC1nCqD1RWDviIPS5xMihZolu2tdpmtFz5KaKWMUX-ZhzM4X3McaM9ZJwWwN5BoGqPQObQa-TwGwn5QE-U7sjNe8mGekl2LPTaqh88WiX55rILNnXf5w4YPt7sDDbfNq6iAVlsZo3CNLF-VTwXLbykkXPo9uyYqtg8rlPrykLYOZn6XHrJDGNmW481YTk8znLPeETZqki-fG-AEsrEzboJpNLpQnb7dYoEsnDoRxDjhnLV9kTfeJK5SuC4V-qwzoSsj2AE-ksXd6yX1IL-sHM1z2N9LPzFoyXOo4sSvZsJ-4LWBoQQNoen7NxsRjcFFxZPJUonTBbom2hXL3xrkQ35OXElbdOhk7ZUcfaoX1yg_HIc5YtFH0hqsWtt8v_jfG3B0gsoV8SfXC2d_pAdUg68mz_HBTgf4CASiPk3q7-xJfGjt2_hZRDmHv4472zhzCgFu2o_3-9B-FMZb2EqbttV1Javu1442ovxbBAdRQfWP9moyL1bneGhnukLDluan_4_zq0ntbghNMpwKQZ3gyJQdQ1TwCFfEo1aYaVx7sHOilue14Ypq9dajH_6TU3ABDceTxewQnXUi_ZRUFGhPF1ArfAX5KghkoQJ67C1qdiXi-QORQkcE6gPrcm_YOpotLVPY2qzNyZC6-Lrh9P-o1gX11h-tnvIJzxJnkvTShXhryfxI-1aPM2QmNEhYU-z5nJltUV3RjXhZAvjBXxdzwChcAQHKECOAoL6CBh1mRibnxp4a6OJCfC7-doHg1j00qCoZ5-Vda7ajNqJDZMbEPulf4emKr0FBv-tuAlNrD_SUoQOo6NwipymbL3YmqWbzyDV0tDqj4zRDRioVvLUYXJkWVmH66YZZXsusdIPhSOmRmAGEKnf96S-Kf3YUjN_ID_a7UazSRMvDDnC2nphAW6SbvvJk1VNcCZz0bbB8Rzbi4VHAZdGafL3S7LeTHNxA6vvvU4LwUxZDfbcOtZzAlEr8m9Ldm0ABzOIJReckcLfzh75rq2sDanEp7ZFWqdv-YwQAbecgm0eJm06CBUUTrmi-FYXuhu-RtQg1cNxftyQP8JvedkVFLrJmKRmuPqors07iCKbTsUznBTmSfwzVD0vx5h_hcDwhYI1HyCOy2n0Y1Lk2TGBxrPmZG8_XkkiEjD1mFqPLNQ4M2uC6g0HojeWZSY'
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