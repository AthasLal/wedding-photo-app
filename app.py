import io, uuid, dropbox
from flask import Flask, request, render_template_string
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# ΡΥΘΜΙΣΕΙΣ
DROPBOX_TOKEN = 'sl.u.AGbSXmynDAQHbfxpfk-7pA0zF0btKLbJw2iPaJl2rzmW5AhyuyV3j6_-48toiiVi8OtkRLDi10MbFP4CHh5B3XQfml4ab7M6W5taViFfZyuIx3aw7YoAei4tHejzZ_iZUu9T940BXdOEeoKYqJrA_-mmVGCx4NRsv1sw7JyZcxa6wTzOLEHyrkJQ4Mx6tpFg5Z4ivLU1RXYIbfKarCQ4b2Qgq5JRI4Y9teVBuVAo4qvI8Q6QtRjrCsh6gzqYSesVt4qL2bzEALmjFaf3oio4yi5kLUU_rhPFh3z1t_Wm5NQ3ntwUs2Y4NYOwRNO2lPoZRsX3PreNqAmsRRX_zRMGI57g9iDn-xYuYKO2raagnDhBSpWFm47f7fpkNIg0dVvFf3CQuMkOmluuVIMUVIGfIcBJVaAENH4XSeiJOHWSsu0VxjRHDv2x3nVdd5lMUuBYqt9_JZgXj8jIOPBZIS3bsPlBlhMqjD6uQon0UGEbCDjSw-xGS2Iz_KjYgaUedDgzgrMa-yfGI6eczt8QHX-xnWFyqBkPrZeKAM80ZClCtQ87c_DV3-PE9KHEuTKuwODdpfpEZrZmMb-I4DpnhYxSHWeg7Icgw1PW2wNt2uL43OM67q8dxWLQEJjGouSwPEs7ie9UDbsuO8Yp2lAQ0cP9iw7J-B5jL44eOuO2H2EEsHlgnKhME7Dutegatd_mHd1rDc2Bap_J6Fg-PqeqDKqLXr7JXc4mi1cww3SkV4IkebmCBnVdFFvsFVmcZ2nqr1musg0e-qtZ3ug5EyAmSFwlLkudE-jxc0LyoMr7_G9oFm848xwJQJ6xsRyDtFczDDpmaWwNBGPR-ECrrM28XVn6MRtnWUcAgStzsJpW-ji56LGBV0L9KkTNzehmTmas2hW-srZ0qgHtFetaMg_AJeeY5F4ueeFmbsGn73XNgHBHtgcsIiavFj3et39RLQOe1p-epp8_fiHEcTeeS5YfOSTStJ--o7RJ6QMJkU5PVMgnbxu9S-TPDCCcoLmvS8YfGZ5hUpI6A4n9f8DzDaC2iYeIZf23rsQAumxWVTM_PFF9TlPdvoa--e8qXws7YepNNnV4HH9qUoR1ei4jcKmGHS0cetEArEk946RuSWrWQPWyW8pyAMO_dr0t4wYz4hsY1XRpbwargFC-2KC2viudU7YxFLCwk3rHhMFUfqsBohvP0mwaNtKOI5DC_kNIjm2Moq02SeJlzInT6TP34u6Rzr7h29JB760ZvOAL2wOawjqpm6tK0CUo1NKg7oqAv_sz8dPzVH0VbIA-SMt34PHDg7H4597MRwl2q4ewRGVDsZh8BgDCmWRwtC_ugSPXppXaybJ83vrYdKeojweFlKSMxv2tKN_P'
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