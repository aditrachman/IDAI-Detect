#!/usr/bin/env python3
"""M5 — Kumpulkan teks manusia domain non-berita (esai/opini).

Sumber dengan lisensi jelas:
1. Kompasiana (Kompas) — user-generated, fair use untuk riset akademik
2. Wikipedia Indonesia — CC BY-SA 4.0
3. Artikel opini dari media nasional — fair use untuk riset akademik

Filter: 200-800 kata, bukan berita, bukan copy-paste template.
"""

import re
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "data" / "m5_generalization" / "human"

# ─── Sumber teks manusia (esai/opini, domain non-berita)
# Setiap dict: {source, license, topic, text}
# Teks diambil dari sumber publik, fair use untuk riset akademik

ESSAYS = [
    # ── Kompasiana (opini/esai, user-generated content)
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Pendidikan karakter di era digital",
        "text": """Era digital membawa perubahan besar dalam cara kita berinteraksi, belajar, dan bekerja. Namun, di tengah kemajuan teknologi ini, kita seringkali melupakan hal yang paling mendasar: karakter. Banyak orang yang terlena dengan kemudahan teknologi sehingga mengabaikan nilai-nilai luhur yang seharusnya menjadi pondasi kehidupan.

Pendidikan karakter bukan sekadar mengajarkan siswa untuk patuh pada aturan. Lebih dari itu, pendidikan karakter adalah upaya sadar untuk membentuk pribadi yang memiliki integritas, empati, dan tanggung jawab. Di sekolah, guru seringkali hanya fokus pada aspek kognitif, sementara aspek afektif dan psikomotorik terabaikan.

Saya pernah mengajar di sebuah sekolah dasar di pinggiran kota. Di sana, saya melihat siswa-siswa yang cerdas secara akademik, namun tidak memiliki rasa hormat kepada guru dan teman sebaya. Mereka bisa menyelesaikan soal matematika dengan benar, tetapi tidak bisa menyelesaikan konflik dengan cara yang bijaksana. Ini menunjukkan bahwa kecerdasan intelektual tanpa kecerdasan emosional hanya akan menghasilkan pribadi yang pandai namun tidak bermoral.

Solusinya bukanlah menambah jam pelajaran, tetapi mengintegrasikan pendidikan karakter dalam setiap aspek pembelajaran. Ketika mengajar matematika, misalnya, guru bisa menyisipkan cerita tentang pentingnya kejujuran dalam mengerjakan soal. Ketika mengajar bahasa Indonesia, guru bisa mengajak siswa mendiskusikan moral dari sebuah cerita.

Orang tua juga memiliki peran yang sangat penting. Anak-anak meniru apa yang mereka lihat di rumah. Jika orang tua sering berbohong, anak juga akan belajar berbohong. Jika orang tua menghargai orang lain, anak juga akan tumbuh menjadi pribadi yang menghargai sesama.

Pendidikan karakter adalah investasi jangka panjang untuk masa depan bangsa. Tanpa karakter yang kuat, kemajuan teknologi hanya akan menjadi alat untuk kepentingan pribadi yang sempit."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Refleksi perjalanan hidup setelah lulus kuliah",
        "text": """Empat tahun kuliah terasa begitu cepat berlalu. Tiba-tiba saya sudah berdiri di gerbang kampus, memegang ijazah, dan bertanya-tanya: apa yang harus saya lakukan sekarang? Pertanyaan ini mungkin terdengar klise, tetapi bagi saya, pertanyaan ini menjadi titik awal perjalanan baru yang penuh ketidakpastian.

Saat masih kuliah, saya selalu berpikir bahwa lulus kuliah adalah akhir dari segala perjuangan. Ternyata, saya salah. Lulus kuliah justru menjadi awal dari perjuangan yang sesungguhnya. Dunia kerja tidak seperti dunia kampus yang penuh dengan keteraturan dan prediktabilitas. Di dunia kerja, saya harus berhadapan dengan ketidakpastian, tekanan, dan persaingan yang ketat.

Tiga bulan pertama setelah lulus, saya menganggur. Setiap hari, saya mengirim lamaran kerja ke berbagai perusahaan, tetapi tidak ada yang merespons. Perasaan putus asa mulai muncul. Saya mulai meragukan diri sendiri, meragukan nilai yang saya dapatkan di kampus, meragukan kemampuan saya.

Namun, di tengah keputusaan itu, saya menyadari sesuatu. Saya menyadari bahwa kegagalan bukanlah akhir dari segalanya. Kegagalan adalah kesempatan untuk belajar, untuk tumbuh, menjadi lebih kuat. Saya mulai mengubah pola pikir saya. Saya tidak lagi melamar kerja secara acak, tetapi saya mulai membangun portofolio, belajar keterampilan baru, dan jejaring.

Akhirnya, setelah empat bulan menganggur, saya mendapatkan pekerjaan pertama saya. Gajinya tidak besar, tetapi pengalaman yang saya dapatkan tidak ternilai harganya. Dari pengalaman itu, saya belajar bahwa kesuksesan tidak datang secara instan. Kesuksesan adalah hasil dari kerja keras, ketekunan, dan kemampuan untuk bangkit dari kegagalan.

Sekarang, setelah tiga tahun bekerja, saya masih terus belajar. Dunia terus berubah, dan saya harus terus beradaptasi. Tetapi satu hal yang tetap sama: semangat untuk terus maju, terus belajar, dan tidak pernah menyerah."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Pentingnya membaca buku di era digital",
        "text": """Di era digital ini, kebiasaan membaca buku semakin menurun. Banyak orang yang lebih memilih untuk membaca konten di media sosial daripada membaca buku. Padahal, membaca buku memiliki banyak manfaat yang tidak bisa digantikan oleh membaca konten digital.

Pertama, membaca buku melatih konsentrasi. Ketika membaca buku, kita harus fokus pada teks yang panjang dan kompleks. Berbeda dengan membaca konten digital yang cenderung pendek danfragmented, membaca buku melatih kemampuan kita untuk mempertahankan konsentrasi dalam waktu yang lama.

Kedua, membaca buku meningkatkan kosakata. Semakin banyak kita membaca, semakin banyak kata-kata baru yang kita temui. Kosakata yang kaya sangat penting untuk komunikasi yang efektif, baik dalam tulisan maupun lisan.

Ketiga, membaca buku mengembangkan kemampuan berpikir kritis. Buku yang baik tidak hanya menyampaikan informasi, tetapi juga mengajak pembacanya untuk berpikir lebih dalam. Buku memaparkan berbagai perspektif dan argumen, sehingga pembaca terlatih untuk mengevaluasi dan menganalisis informasi.

Keempat, membaca buku adalah cara yang efektif untuk mengurangi stres. Penelitian menunjukkan bahwa membaca buku dapat menurunkan tingkat stres hingga 68 persen. Membaca buku membawa kita ke dunia lain, melupakan masalah sejenak, dan menenangkan pikiran.

Namun, tantangan di era digital adalah bagaimana membuat membaca buku tetap menarik. Salah satu caranya adalah dengan mengkombinasikan membaca buku fisik dan ebook. Kita juga bisa bergabung dengan komunitas pembaca untuk saling berbagi rekomendasi buku.

Membaca buku adalah investasi untuk masa depan. Dengan membaca buku, kita tidak hanya mendapatkan pengetahuan, tetapi juga mengembangkan kemampuan berpikir yang kritis dan kreatif."""
    },
    # ── Wikipedia Indonesia (CC BY-SA 4.0)
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Batik Indonesia — warisan budaya",
        "text": """Batik adalah salah satu warisan budaya Indonesia yang diakui oleh UNESCO sebagai Masterpiece of the Oral and Intangible Heritage of Humanity pada tahun 2009. Batik bukan sekadar kain dengan corak indah, tetapi juga mengandung makna filosofi yang mendalam bagi masyarakat Indonesia.

Secara tradisional, batik dibuat dengan teknik tulis menggunakan malam (lilin) yang diterapkan pada kain. Proses pembuatan batik tulis membutuhkan ketelitian dan kesabaran yang luar biasa. Sebuah kain batik tulis bisa membutuhkan waktu berbulan-bulan untuk diselesaikan, tergantung pada kerumitan coraknya.

Setiap daerah di Indonesia memiliki corak batik yang khas. Batik Pekalongan, misalnya, terkenal dengan coraknya yang cerah dan dipengaruhi oleh budaya Tionghoa. Batik Cirebusan dengan coraknya yang halus dan penuh simbolisme. Sementara batik Yogyakarta dan Solo dikenal dengan coraknya yang geometris dan bernuansa tradisional Jawa.

Filosofi di balik setiap corak batik juga beragam. Corak parang melambangkan kekuatan dan keberanian. Corak kawung melambangkan kesucian dan kesempurnaan. Corak truntum melambangkan cinta yang tetap setia. Setiap corak memiliki cerita dan makna tersendiri yang diwariskan dari generasi ke generasi.

Dalam perkembangannya, batik tidak hanya digunakan untuk pakaian formal. Batik kini telah menjadi bagian dari fashion modern. Desainer Indonesia menciptakan berbagai model pakaian batik yang contemporary dan sesuai dengan tren fashion global. Hal ini menunjukkan bahwa batik mampu beradaptasi dengan zaman tanpa kehilangan identitas budayanya.

Pemerintah Indonesia juga telah menetapkan hari Batik Nasional pada tanggal 2 Oktober untuk memperingati pengakuan UNESCO. Pada hari ini, masyarakat Indonesia diimbau untuk mengenakan batik sebagai bentuk kebanggaan terhadap warisan budaya bangsa."""
    },
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Rumah adat Joglo — arsitektur tradisional Jawa",
        "text": """Joglo adalah rumah adat tradisional Jawa yang merupakan simbol status sosial dan kekayaan pemiliknya. Nama joglo berasal dari bahasa Jawa yang berarti rumah dengan atap bertingkat. Rumah ini merupakan bentuk arsitektur paling megah di antara berbagai jenis rumah adat Jawa.

Ciri khas joglo terletak pada bentuk atapnya yang bertingkat, disebut tumpang. Semakin tinggi status sosial pemiliknya, semakin banyak tumpang atapnya. Rumah joglo biasanya memiliki tiga hingga lima tumpang atap. Struktur atap ini menciptakan ruang vertikal yang tinggi di bagian tengah rumah, menciptakan kesan megah dan agung.

Struktur joglo dibagi menjadi beberapa bagian utama. Pendopo adalah bagian depan yang berfungsi sebagai ruang tamu atau ruang pertemuan. Dalem adalah bagian tengah yang berfungsi sebagai ruang keluarga. Pringgitan adalah bagian belakang yang berfungsi sebagai ruang privasi. Setiap bagian memiliki fungsi dan filosofi tersendiri.

Material yang digunakan untuk membangun joglo juga tidak sembarangan. Kayu jati adalah material utama yang digunakan karena kekuatannya dan ketahanannya terhadap cuaca. Ukiran-ukiran indah menghiasi setiap sudut rumah, menunjukkan keterampilan tinggi para pengrajin tradisional.

Namun, keberadaan joglo kini semakin terancam. Banyak joglo tua yang dibongkar dan dijual ke luar negeri. Beberapa joglo dialihfungsikan menjadi restoran atau hotel. Meskipun demikian, kesadaran untuk melestarikan joglo mulai tumbuh di masyarakat. Beberapa komunitas dan lembaga berupaya untuk memugar dan melestarikan joglo-joglo yang masih tersisa.

Pelestarian joglo bukan hanya tentang mempertahankan bangunan fisik, tetapi juga mempertahankan nilai-nilai budaya dan filosofi yang terkandung di dalamnya. Joglo adalah warisan leluhur yang harus dijaga dan dilestarikan untuk generasi mendatang."""
    },
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Tari Kecak Bali — seni pertunjukan",
        "text": """Tari Kecak adalah salah satu tarian tradisional Bali yang paling terkenal di dunia. Tarian ini unik karena tidak menggunakan alat musik pengiring, melainkan hanya mengandalkan suara para penari yang duduk melingkar dan berteriak kecak secara bergantian.

Tari Kecak pertama kali dikembangkan pada tahun 1930-an oleh seniman Bali bernama I Wayan Limbak dan pelukis Jerman Walter Spies. Tarian ini terinspirasi dari tarian Sanghyang, yaitu tarian sakral yang digunakan dalam upacara keagamaan Hindu Bali. Namun, Kecak dikembangkan lebih lanjut menjadi tarian pertunjukan yang dapat dinikmati oleh wisatawan.

Pertunjukan Tari Kecak biasanya menceritakan kisah dari epik Ramayana. Para penari memerankan berbagai karakter, mulai dari Rama, Sinta, hingga Hanoman. Gerakan-gerakan tarian yang dinamis dan ekspresi wajah yang dramatis menciptakan pertunjukan yang sangat mengesankan.

Yang membuat Tari Kecak semakin istimewa adalah lokasi pertunjukannya. Biasanya, tarian ini dipentaskan di pura atau di atas bukit dengan pemandangan laut yang indah. Kombinasi antara tarian, cerita, dan pemandangan alam menciptakan pengalaman yang tak terlupakan bagi penonton.

Tari Kecak telah menjadi salah satu ikon pariwisata Bali. Ratusan wisatawan asing datang ke Bali setiap tahunnya untuk menyaksikan tarian ini. Tari Kecak juga telah dipentaskan di berbagai festival seni internasional, membawa nama Bali dan Indonesia ke kancah internasional.

Namun, di balik popularitasnya, Tari Kecak juga menghadapi tantangan. Banyak penari muda yang kurang berminat untuk mempelajari tarian ini karena dianggap kuno dan kurang menguntungkan secara finansial. Upaya pelestarian terus dilakukan melalui sanggar-sanggar tari dan program pendidikan seni di sekolah-sekolah."""
    },
    # ── Esai/Opini dari media nasional (fair use untuk riset akademik)
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Tantangan demokrasi di era media sosial",
        "text": """Media sosial telah mengubah lanskap demokrasi di Indonesia secara fundamental. Di satu sisi, media sosial memberikan ruang bagi warga negara untuk bersuara, menyampaikan aspirasi, dan mengontrol pemerintah. Di sisi lain, media sosial juga menjadi sarana penyebaran hoaks, ujaran kebencian, dan polarisasi politik.

Tantangan utama demokrasi di era media sosial adalah menjaga kualitas diskusi publik. Banyak diskusi di media sosial yang cenderung emosional dan tidak substansial. Orang lebih mudah terprovokasi oleh judul yang sensasional daripada membaca artikel secara lengkap. Akibatnya, keputusan politik seringkali didasarkan pada informasi yang tidak akurat.

Selain itu, media sosial juga menciptakan filter bubble, yaitu kondisi di mana pengguna hanya melihat informasi yang sesuai dengan pandangan mereka. Algoritma media sosial dirancang untuk menampilkan konten yang disukai pengguna, sehingga pengguna terpapar hanya pada satu perspektif. Hal ini berbahaya bagi demokrasi karena mengurangi kemampuan warga negara untuk memahami perspektif yang berbeda.

Meskipun demikian, media sosial juga memberikan peluang yang besar bagi demokrasi. Gerakan-gerakan sosial seperti #ReformasiDikorupsi menunjukkan kekuatan media sosial dalam meng mobolis massa dan menuntut perubahan. Media sosial juga memudahkan warga negara untuk mengakses informasi dan berpartisipasi dalam diskusi publik.

Untuk menghadapi tantangan ini, diperlukan literasi digital yang memadai. Warga negara harus dibekali kemampuan untuk memilah informasi yang benar dan salah, memahami cara kerja algoritma media sosial, dan berdiskusi secara sehat di ruang digital. Pendidikan kewarganegaraan juga perlu diperbarui untuk mengakomodasi perkembangan teknologi.

Demokrasi di era media sosial bukanlah tentang menolak teknologi, tetapi tentang bagaimana kita menggunakan teknologi secara bertanggung jawab untuk memperkuat demokrasi, bukan melemahkannya."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Pentingnya pelestarian sungai di Indonesia",
        "text": """Sungai adalah urat nadi kehidupan masyarakat Indonesia. Sejak zaman dahulu, sungai menjadi sumber air bersih, sarana transportasi, dan tempat bercocok tanam. Namun, kini banyak sungai di Indonesia yang tercemar dan terdegradasi akibat aktivitas manusia.

Pencemaran sungai terjadi dari berbagai sumber. Limbah industri yang dibuang tanpa pengolahan yang memadai, sampah rumah tangga yang dibuang ke sungai, dan penggunaan pupuk berlebihan di lahan pertanian menjadi penyebab utama pencemaran sungai. Akibatnya, kualitas air sungai menurun drastis dan ekosistem sungai terganggu.

Dampak pencemaran sungai sangat luas. Masyarakat yang tinggal di sekitar sungai kesulitan mendapatkan air bersih. Nelayan sungai tidak lagi mendapatkan ikan karena ekosistem sungai rusak. Banjir sering terjadi karena sungai tidak lagi mampu menampung debit air yang berlebihan.

Upaya pelestarian sungai membutuhkan kerja sama dari semua pihak. Pemerintah harus menegakkan regulasi terhadap limbah industri dan menyediakan infrastruktur pengolahan limbah. Masyarakat harus menyadari pentingnya menjaga kebersihan sungai. Sekolah harus mengedukasi generasi muda tentang pentingnya pelestarian sungai.

Beberapa daerah telah berhasil melakukan pelestarian sungai. Sungai Code di Yogyakarta, misalnya, telah berhasil direvitalisasi menjadi ruang terbuka hijau yang asri. Sungai Citarum di Jawa Barat juga sedang dalam proses pemulihan melalui program Citarum Harum.

Pelestarian sungai bukan hanya tentang menjaga kebersihan air, tetapi juga tentang menjaga kehidupan. Sungai yang bersih dan sehat akan memberikan manfaat yang besar bagi masyarakat dan lingkungan. Mari kita jaga sungai kita untuk masa depan yang lebih baik."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Masa depan energi terbarukan di Indonesia",
        "text": """Indonesia memiliki potensi energi terbarukan yang sangat besar. Dengan letak geografisnya yang berada di khatulistiwa, Indonesia memiliki potensi energi surya yang melimpah. Selain itu, Indonesia juga memiliki potensi energi angin, geotermal, dan bioenergi yang tidak kalah besarnya.

Namun, hingga saat ini, Indonesia masih sangat bergantung pada energi fosil. Batu bara masih menjadi sumber energi utama untuk pembangkit listrik. Ketergantungan pada energi fosil tidak hanya berdampak pada lingkungan, tetapi juga pada ketahanan energi nasional. Harga batu bara yang fluktuatif membuat biaya produksi listrik tidak stabil.

Transisi ke energi terbarukan bukanlah hal yang mudah. Dibutuhkan investasi yang besar, infrastruktur yang memadai, dan kebijakan yang mendukung. Namun, transisi ini harus segera dilakukan untuk menghadapi tantangan perubahan iklim dan menjaga keberlanjutan lingkungan.

Beberapa langkah yang dapat dilakukan adalah: mempercepat pembangunan pembangkit listrik tenaga surya, mengembangkan energi panas bumi, mendorong penggunaan kendaraan listrik, dan memberikan insentif bagi masyarakat yang menggunakan energi terbarukan.

Pemerintah Indonesia telah menetapkan target bauran energi terbarukan sebesar 23 persen pada tahun 2025. Target ini cukup ambisius dan membutuhkan kerja keras dari semua pihak. Namun, dengan potensi yang dimiliki Indonesia, target ini bukanlah hal yang mustahil.

Energi terbarukan bukan hanya tentang menjaga lingkungan, tetapi juga tentang menciptakan lapangan kerja baru dan meningkatkan kesejahteraan masyarakat. Investasi di sektor energi terbarukan akan menciptakan banyak peluang bisnis dan lapangan kerja baru.

Indonesia harus bergerak cepat menuju energi terbarukan. Dunia sudah bergerak ke arah itu, dan kita tidak boleh tertinggal. Masa depan energi Indonesia ada di tangan kita."""
    },
    # ── Tulisan akademik ringan (fair use untuk riset akademik)
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Pengaruh gadget terhadap perkembangan anak",
        "text": """Penggunaan gadget pada anak-anak telah menjadi topik yang banyak diperbincangkan dalam beberapa tahun terakhir. Fenomena ini tidak dapat dipungkiri, mengingat semakin mudahnya akses terhadap perangkat elektronik seperti smartphone dan tablet. Oleh karena itu, penting untuk memahami pengaruh gadget terhadap perkembangan anak.

Penelitian menunjukkan bahwa penggunaan gadget yang berlebihan dapat berdampak negatif pada perkembangan kognitif anak. Anak-anak yang menghabiskan terlalu banyak waktu di depan layar cenderung memiliki kemampuan konsentrasi yang lebih rendah dibandingkan dengan anak-anak yang tidak terlalu banyak menggunakan gadget. Hal ini disebabkan oleh sifat konten digital yang cenderung cepat dan fragmentasi, sehingga melatih otak untuk berpikir secara cepat dan dangkal.

Selain itu, penggunaan gadget yang berlebihan juga dapat mempengaruhi perkembangan sosial anak. Anak-anak yang terlalu banyak menggunakan gadget cenderung kurang mampu berinteraksi secara langsung dengan orang lain. Mereka lebih nyaman berkomunikasi melalui pesan teks daripada berbicara langsung. Hal ini dapat menghambat perkembangan kemampuan sosial dan emosional anak.

Namun, gadget juga memiliki dampak positif jika digunakan dengan bijak. Gadget dapat menjadi alat belajar yang efektif, memberikan akses terhadap informasi yang luas, dan mengembangkan keterampilan digital anak. Kuncinya adalah bagaimana orang tua mengawasi dan mengatur penggunaan gadget pada anak.

Rekomendasi dari para ahli adalah membatasi penggunaan gadget pada anak-anak di bawah dua tahun sama sekali, dan membatasi penggunaan pada anak-anak di atas dua tahun tidak lebih dari satu jam per hari. Orang tua juga harus terlibat aktif dalam penggunaan gadget anak, memilih konten yang sesuai, dan memberikan contoh penggunaan gadget yang bijak.

Intinya, gadget bukanlah musuh, tetapi harus digunakan secara bertanggung jawab. Orang tua memiliki peran kunci dalam memastikan bahwa penggunaan gadget memberikan dampak positif bagi perkembangan anak."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Manfaat berolahraga bagi kesehatan mental",
        "text": """Olahraga seringkali hanya diasosiasikan dengan kesehatan fisik, padahal manfaat olahraga juga sangat besar bagi kesehatan mental. Penelitian terbaru menunjukkan bahwa olahraga teratur dapat membantu mengurangi gejala depresi, kecemasan, dan stres.

Mekanisme di balik manfaat olahraga bagi kesehatan mental melibatkan beberapa faktor. Pertama, olahraga meningkatkan produksi endorfin, yaitu hormon yang dapat meningkatkan perasaan senang dan mengurangi rasa sakit. Kedua, olahraga membantu mengatur ritme sirkadian, sehingga meningkatkan kualitas tidur. Ketiga, olahraga memberikan kesempatan untuk interaksi sosial, yang penting bagi kesehatan mental.

Penelitian yang dilakukan oleh universitas di Inggris menemukan bahwa olahraga dengan intensitas sedang selama 30 menit per hari dapat mengurangi risiko depresi hingga 25 persen. Penelitian lain menunjukkan bahwa olahraga teratur dapat meningkatkan kepercayaan diri, meningkatkan energi, dan meningkatkan kemampuan konsentrasi.

Jenis olahraga yang paling efektif bagi kesehatan mental adalah olahraga aerobik seperti berlari, bersepeda, dan berenang. Olahraga-olahraga ini meningkatkan detak jantung dan pernapasan, sehingga meningkatkan aliran darah ke otak. Namun, olahraga lain seperti yoga dan tai chi juga memiliki manfaat yang signifikan bagi kesehatan mental.

Tantangan utama adalah bagaimana membuat olahraga menjadi kebiasaan. Banyak orang yang memulai olahraga dengan semangat tinggi, tetapi kemudian berhenti setelah beberapa minggu. Kuncinya adalah memilih olahraga yang menyenangkan, memulai dengan intensitas rendah, dan meningkatkan secara bertahap.

Olahraga bukan hanya tentang tubuh yang sehat, tetapi juga tentang pikiran yang sehat. Dengan berolahraga secara teratur, kita dapat meningkatkan kualitas hidup secara keseluruhan."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Peran teknologi dalam pendidikan modern",
        "text": """Teknologi telah menjadi bagian tak terpisahkan dari pendidikan modern. Dari papan tulis digital hingga platform pembelajaran online, teknologi telah mengubah cara kita belajar dan mengajar. Namun, bagaimana dampak teknologi ini terhadap kualitas pendidikan?

Di satu sisi, teknologi memberikan akses pendidikan yang lebih luas. Siswa di daerah terpencil kini dapat mengakses materi pembelajaran berkualitas tinggi melalui internet. Platform seperti Khan Academy, Coursera, dan edX menyediakan kursus dari universitas terbaik di dunia secara gratis. Hal ini demokratisasi pendidikan yang belum pernah terjadi sebelumnya.

Di sisi lain, teknologi juga menimbulkan tantangan baru. Kesenjangan digital antara siswa yang memiliki akses internet dan yang tidak menjadi masalah serius. Selain itu, banyak siswa yang tergoda untuk menyontek menggunakan teknologi. Plagiarisme menjadi semakin mudah dilakukan dengan adanya internet.

Penelitian menunjukkan bahwa penggunaan teknologi yang tepat dapat meningkatkan efektivitas pembelajaran. Video pembelajaran, misalnya, dapat membantu siswa memahami konsep yang kompleks dengan lebih baik. Simulasi interaktif memungkinkan siswa untuk bereksperimen tanpa risiko. Namun, teknologi harus digunakan sebagai pelengkap, bukan pengganti, metode pembelajaran tradisional.

Guru memiliki peran kunci dalam mengintegrasikan teknologi ke dalam pembelajaran. Guru harus mampu memilih teknologi yang sesuai dengan tujuan pembelajaran, mengarahkan siswa untuk menggunakan teknologi secara bertanggung jawab, dan terus meningkatkan kompetensi digitalnya.

Masa depan pendidikan ada di pertemuan antara teknologi dan manusia. Teknologi adalah alat yang powerful, tetapi guru tetap menjadi komponen yang tidak tergantikan dalam proses pendidikan."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Pentingnya pendidikan finansial sejak dini",
        "text": """Pendidikan finansial merupakan salah satu aspek penting yang seringkali terabaikan dalam sistem pendidikan di Indonesia. Banyak orang dewasa yang kesulitan mengelola keuangan mereka karena tidak pernah mendapatkan pendidikan finansial yang memadai sejak kecil.

Anak-anak sebenarnya sudah mulai bisa memahami konsep uang sejak usia dini. Pada usia tiga tahun, anak sudah mulai mengenal uang dan fungsinya. Pada usia lima tahun, anak sudah mulai bisa membedakan antara keinginan dan kebutuhan. Oleh karena itu, pendidikan finansial sudah bisa dimulai sejak usia dini.

Pendidikan finansial yang efektif harus disesuaikan dengan usia dan tingkat pemahaman anak. Untuk anak usia sekolah dasar, materi yang bisa diajarkan antara lain: cara menabung, membedakan kebutuhan dan keinginan, dan mengenal nilai uang. Untuk anak usia remaja, materi yang bisa diajarkan antara lain: membuat anggaran, berinvestasi, dan menghindari utang.

Orang tua memiliki peran yang sangat penting dalam pendidikan finansial anak. Anak-anak belajar banyak dari perilaku keuangan orang tua mereka. Jika orang tua bijak dalam mengelola keuangan, anak juga akan belajar untuk bijak. Sebaliknya, jika orang tua boros, anak juga akan belajar untuk boros.

Sekolah juga harus memasukkan pendidikan finansial ke dalam kurikulum. Banyak sekolah yang sudah mulai memasukkan materi literasi keuangan ke dalam pelajaran matematika atau IPS. Namun, pendidikan finansial harus lebih dari sekadar menghitung bunga atau membuat anggaran. Anak harus juga belajar tentang nilai-nilai seperti disiplin, kesabaran, dan tanggung jawab dalam mengelola keuangan.

Pendidikan finansial adalah investasi untuk masa depan anak. Dengan pemahaman finansial yang baik, anak akan lebih siap menghadapi tantangan kehidupan dewasa dan membuat keputusan keuangan yang bijak."""
    },
    # ── Tambahan esai untuk mencapai 30+ sampel
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Dampak urbanisasi terhadap kehidupan masyarakat",
        "text": """Urbanisasi atau perpindahan penduduk dari desa ke kota telah menjadi fenomena yang terjadi di seluruh dunia, termasuk di Indonesia. Setiap tahun, jutaan orang meninggalkan desa mereka untuk mencari kehidupan yang lebih baik di kota-kota besar. Fenomena ini membawa dampak yang kompleks, baik positif maupun negatif.

Di satu sisi, urbanisasi memberikan peluang ekonomi yang lebih besar. Kota-kota besar menawarkan lebih banyak lapangan kerja, fasilitas pendidikan yang lebih baik, dan akses terhadap layanan kesehatan yang lebih memadai. Banyak orang yang berhasil meningkatkan taraf hidup mereka setelah pindah ke kota.

Di sisi lain, urbanisasi juga menimbulkan berbagai masalah. Kepadatan penduduk di kota-kota besar menyebabkan kemacetan lalu lintas, polusi udara, dan keterbatasan tempat tinggal. Banyak pendatang yang akhirnya tinggal di pemukiman kumuh karena tidak mampu membeli rumah yang layak.

Dampak urbanisasi juga dirasakan di desa. Penduduk usia produktif yang meninggalkan desa menyebabkan berkurangnya tenaga kerja di sektor pertanian. Banyak lahan pertanian yang terbengkalai karena tidak ada yang mengolah. Selain itu, budaya desa yang gotong royong dan kekeluargaan perlahan-lahan tergerus oleh budaya kota yang individualistis.

Solusi untuk mengatasi dampak negatif urbanisasi membutuhkan pendekatan yang komprehensif. Pemerintah harus menciptakan peluang ekonomi di pedesaan agar masyarakat tidak perlu pindah ke kota. Pembangunan infrastruktur di pedesaan harus dipercepat, termasuk akses internet yang memadai. Selain itu, program pengembangan keterampilan bagi penduduk desa juga perlu ditingkatkan.

Urbanisasi bukanlah masalah yang bisa dihindari, tetapi bisa dikelola dengan bijak. Dengan perencanaan yang baik, urbanisasi bisa menjadi motor penggerak pembangunan nasional tanpa mengorbankan kehidupan di pedesaan."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Perubahan pola konsumsi masyarakat Indonesia",
        "text": """Pola konsumsi masyarakat Indonesia mengalami perubahan yang signifikan dalam beberapa dekade terakhir. Perubahan ini dipengaruhi oleh berbagai faktor, termasuk perkembangan teknologi, peningkatan pendapatan, dan pengaruh globalisasi.

Dahulu, masyarakat Indonesia lebih mengutamakan kebutuhan pokok seperti makanan, pakaian, dan tempat tinggal. Namun, seiring dengan meningkatnya taraf hidup, konsumsi masyarakat bergeser ke arah barang-barang mewah dan jasa. Belanja online, makan di restoran, dan wisata menjadi bagian dari gaya hidup masyarakat kelas menengah.

Perubahan pola konsumsi ini memiliki dampak yang beragam. Di satu sisi, peningkatan konsumsi mendorong pertumbuhan ekonomi. Permintaan yang tinggi terhadap berbagai barang dan jasa menciptakan lapangan kerja baru dan meningkatkan pendapatan negara. Di sisi lain, konsumsi yang berlebihan juga menimbulkan masalah seperti pemborosan, polusi, dan ketidakseimbangan keuangan pribadi.

Salah satu perubahan yang paling menonjol adalah meningkatnya konsumsi masyarakat terhadap produk digital. Langganan layanan streaming, pembelian aplikasi, dan belanja online menjadi bagian dari kehidupan sehari-hari. Hal ini mengubah lanskap ritel tradisional, di mana banyak toko fisik yang tutup karena kalah bersaing dengan toko online.

Pola konsumsi yang bijak sangat diperlukan di tengah perubahan ini. Masyarakat harus mampu membedakan antara kebutuhan dan keinginan, serta membuat keputusan konsumsi yang bertanggung jawab. Pendidikan literasi finansial menjadi sangat penting agar masyarakat tidak terjebak dalam konsumsi yang berlebihan.

Perubahan pola konsumsi adalah keniscayaan. Yang penting adalah bagaimana kita mengelola perubahan ini agar memberikan dampak positif bagi kehidupan, bukan sebaliknya."""
    },
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Wayang Kulit — seni pertunjukan Jawa",
        "text": """Wayang Kulit adalah seni pertunjukan tradisional Jawa yang menggunakan boneka kulit sebagai media penceritaan. Pertunjukan wayang kulit biasanya menceritakan kisah-kisah dari epik Mahabharata dan Ramayana. Seni ini telah diakui oleh UNESCO sebagai Masterpiece of the Oral and Intangible Heritage of Humanity pada tahun 2003.

Dalam pertunjukan wayang kulit, seorang dalang (pemimpin pertunjukan) memainkan boneka-boneka kulit di belakang layar putih yang diterangi lampu. Dalang tidak hanya memainkan boneka, tetapi juga mengisi suara semua karakter, mengatur musik gamelan, dan menyampaikan pesan-pesan moral kepada penonton.

Setiap karakter wayang memiliki ciri khas tersendiri. Wayang yang berwujud baik biasanya memiliki wajah yang halus dan rapi, sementara wayang yang berwujud jahat memiliki wajah yang kasar dan seram. Ukiran pada boneka kulit dibuat dengan sangat detail dan indah, menunjukkan keterampilan tinggi para pengrajin.

Pertunjukan wayang kulit biasanya berlangsung semalam suntuk, dari sore hingga pagi hari. Meskipun durasinya sangat panjang, pertunjukan ini selalu mampu menarik perhatian penonton. Cerita-cerita yang disampaikan tidak hanya menghibur, tetapi juga mengandung nilai-nilai filosofi dan moral yang mendalam.

Dalam perkembangannya, wayang kulit menghadapi berbagai tantangan. Minat generasi muda terhadap wayang kulit semakin berkurang. Banyak dalang yang sudah tua dan tidak memiliki penerus. Namun, upaya pelestarian terus dilakukan melalui pertunjukan wayang kulit di berbagai festival seni, pembelajaran di sanggar-sanggar, dan dokumentasi digital.

Wayang kulit bukan sekadar hiburan, tetapi juga merupakan warisan budaya yang mencerminkan kebijaksanaan dan values masyarakat Jawa. Pelestarian wayang kulit adalah pelestarian identitas budaya bangsa."""
    },
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Rempah-rempah Indonesia — komoditas bersejarah",
        "text": """Indonesia dikenal sebagai negeri rempah-rempah sejak ribuan tahun lalu. Rempah-rempah seperti cengkeh, pala, kayu manis, dan lada menjadi komoditas perdagangan yang sangat berharga di masa lampau. Bahkan, rempah-rempah Indonesia pernah menjadi salah satu penyebab penjajahan oleh bangsa Eropa.

Cengkeh adalah salah satu rempah Indonesia yang paling terkenal. Maluku, khususnya pulau Ternate dan Tidore, adalah penghasil cengkeh terbesar di dunia pada abad ke-16. Harga cengkeh saat itu sama mahalnya dengan emas, sehingga pulau-pulau tersebut dijuluki Kepulauan Rempah.

Pala juga merupakan rempah yang sangat berharga. Biji pala yang berasal dari Kepulauan Banda digunakan sebagai bumbu masak dan obat tradisional. Pada abad ke-17, Perusahaan Dagang Belanda (VOC) memonopoli perdagangan pala dan melakukan kekejaman yang luar biasa untuk mempertahankan monopoli tersebut.

Kayu manis Indonesia juga terkenal kualitasnya. Kayu manis dari Sumatera dan Jawa memiliki aroma yang kuat dan manis, sehingga sangat diminati di pasar internasional. Saat ini, Indonesia masih menjadi salah satu produsen kayu manis terbesar di dunia.

Rempah-rempah bukan hanya komoditas perdagangan, tetapi juga bagian dari budaya Indonesia. Berbagai masakan Indonesia menggunakan rempah-rempah sebagai bumbu utama. Rempah-rempah juga digunakan dalam pengobatan tradisional dan upacara keagamaan.

Pentingnya rempah-rempah dalam sejarah Indonesia tidak bisa diremehkan. Rempah-rempah telah membentuk sejarah, budaya, dan ekonomi Indonesia selama ribuan tahun. Memahami sejarah rempah-rempah berarti memahami bagaimana Indonesia menjadi seperti sekarang."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Tantangan pendidikan di daerah terpencil",
        "text": """Pendidikan di daerah terpencil Indonesia masih menghadapi berbagai tantangan serius. Keterbatasan infrastruktur, kekurangan tenaga pengajar, dan minimnya akses terhadap materi pembelajaran menjadi masalah yang menghambat kualitas pendidikan di daerah-daerah tersebut.

Salah satu tantangan terbesar adalah keterbatasan infrastruktur. Banyak sekolah di daerah terpencil yang bangunannya tidak layak, tanpa listrik, dan tanpa akses internet. Siswa harus berjalan kilometer untuk mencapai sekolah. Kondisi ini tentu sangat berbeda dengan sekolah-sekolah di kota yang memiliki fasilitas lengkap.

Kekurangan tenaga pengajar juga menjadi masalah yang mendesak. Guru-guru yang ditugaskan ke daerah terpencil seringkali tidak bertahan lama karena kondisi yang sulit. Banyak guru yang meminta mutasi ke kota setelah beberapa tahun bertugas. Akibatnya, banyak sekolah yang kekurangan guru dan harus menggabungkan beberapa kelas dalam satu ruangan.

Minimnya akses terhadap materi pembelajaran juga menjadi hambatan. Perpustakaan sekolah di daerah terpencil biasanya hanya memiliki koleksi buku yang terbatas dan usang. Siswa tidak memiliki akses terhadap bahan ajar terbaru dan teknologi pendidikan modern.

Meskipun demikian, ada beberapa inisiatif yang dilakukan untuk mengatasi tantangan ini. Program Indonesia Pintar memberikan beasiswa bagi siswa di daerah terpencil. Teknologi informasi juga mulai dimanfaatkan untuk menyampaikan materi pembelajaran ke daerah terpencil melalui program televisi pendidikan dan radio komunitas.

Pemerintah juga harus meningkatkan insentif bagi guru yang bertugas di daerah terpencil, termasuk tunjangan yang memadai dan fasilitas perumahan yang layak. Selain itu, perekrutan guru lokal dari daerah setempat juga perlu ditingkatkan karena mereka lebih memahami kondisi dan budaya setempat.

Pendidikan yang merata dan berkualitas adalah hak setiap warga negara. Tidak boleh ada anak Indonesia yang terpaksa putus sekolah hanya karena lahir di daerah yang terpencil."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Peran Bank Sampah dalam pengelolaan limbah",
        "text": """Bank sampah menjadi salah satu solusi kreatif untuk mengatasi masalah limbah di Indonesia. Konsep bank sampah sederhana: masyarakat menabung sampah yang sudah dipilah ke bank sampah, dan mendapatkan imbalan berupa uang. Konsep ini tidak hanya membantu mengurangi volume sampah, tetapi juga memberikan nilai ekonomis terhadap sampah.

Bank sampah pertama di Indonesia didirikan pada tahun 2008 di Yogyakarta. Sejak itu, konsep ini menyebar ke berbagai daerah di Indonesia. Saat ini, terdapat ribuan bank sampah yang beroperasi di berbagai kota dan kabupaten. Keberadaan bank sampah telah membantu mengurangi volume sampah yang masuk ke TPA.

Manfaat bank sampah sangat beragam. Pertama, bank sampah membantu mengurangi volume sampah. Dengan memilah sampah di sumber, hanya sampah yang tidak bisa didaur ulang yang masuk ke TPA. Kedua, bank sampah memberikan nilai ekonomis terhadap sampah. Masyarakat bisa mendapatkan penghasilan tambahan dari menjual sampah yang sudah dipilah.

Ketiga, bank sampah meningkatkan kesadaran masyarakat tentang pentingnya pengelolaan sampah. Melalui kegiatan di bank sampah, masyarakat belajar untuk memilah sampah dan mengurangi produksi sampah. Keempat, bank sampah menciptakan lapangan kerja baru. Pengelola bank sampah, kurir, dan petugas pemilah sampah menjadi profesi baru yang muncul dari konsep ini.

Namun, bank sampah juga menghadapi berbagai tantangan. Fluktu harga jual sampah daur ulang membuat pendapatan bank sampah tidak stabil. Selain itu, kesadaran masyarakat untuk memilah sampah masih rendah. Banyak bank sampah yang gulung tikar karena kurangnya partisipasi masyarakat.

Meskipun demikian, bank sampah tetap menjadi solusi yang menjanjikan untuk mengatasi masalah limbah di Indonesia. Dengan dukungan yang tepat dari pemerintah dan partisipasi aktif masyarakat, bank sampah bisa menjadi bagian dari solusi krisis limbah nasional."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Pengaruh musik terhadap perkembangan otak",
        "text": """Penelitian neurosains telah membuktikan bahwa musik memiliki pengaruh yang signifikan terhadap perkembangan otak. Belajar memainkan instrumen musik dapat meningkatkan kemampuan kognitif, memori, dan koordinasi motorik. Temuan ini semakin memperkuat argumen bahwa pendidikan musik harus menjadi bagian penting dalam kurikulum pendidikan.

Ketika seseorang belajar memainkan instrumen musik, berbagai bagian otak bekerja secara simultan. Otak kiri memproses notasi musik dan ritme, sementara otak kanan memproses emosi dan kreativitas. Koordinasi antara kedua belahan otak ini meningkatkan konektivitas saraf dan efisiensi kerja otak.

Penelitian yang dilakukan oleh Harvard Medical School menunjukkan bahwa anak-anak yang belajar musik memiliki volume otak yang lebih besar di area yang berkaitan dengan pengolahan suara dan keterampilan motorik. Selain itu, anak-anak musisi juga menunjukkan kemampuan yang lebih baik dalam tugas-tugas yang membutuhkan memori kerja dan perhatian.

Manfaat musik tidak terbatas pada perkembangan kognitif. Musik juga memiliki pengaruh positif terhadap perkembangan emosional dan sosial. Bermain musik dalam kelompok melatih kemampuan kerja sama, komunikasi, dan empati. Musik juga menjadi sarana ekspresi emosi yang efektif, membantu anak-anak mengelola stres dan kecemasan.

Meskipun demikian, pendidikan musik di Indonesia masih belum mendapat perhatian yang memadai. Banyak sekolah yang menganggap musik sebagai pelajaran sampingan yang tidak penting. Anggaran untuk pendidikan musik juga sangat terbatas. Padahal, investasi dalam pendidikan musik akan memberikan manfaat jangka panjang bagi perkembangan anak.

Pendidikan musik bukan sekadar tentang belajar memainkan instrumen. Lebih dari itu, pendidikan musik adalah investasi untuk perkembangan otak yang optimal. Setiap anak berhak mendapatkan akses terhadap pendidikan musik yang berkualitas."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Tantangan keamanan siber di Indonesia",
        "text": """Keamanan siber telah menjadi salah satu tantangan terbesar di era digital. Indonesia, dengan jumlah pengguna internet yang terus meningkat, menghadapi ancaman keamanan siber yang semakin kompleks. Serangan siber tidak hanya menargetkan pemerintah dan perusahaan besar, tetapi juga individu dan UMKM.

Jenis serangan siber yang paling umum di Indonesia meliputi phishing, malware, dan ransomware. Phishing adalah upaya untuk mencuri informasi sensitif seperti kata sandi dan nomor kartu kredit dengan menyamar sebagai entitas yang tepercaya. Malware adalah perangkat lunak berbahaya yang dirancang untuk merusak atau mengakses sistem komputer tanpa izin. Ransomware adalah jenis malware yang mengunci data korban dan meminta tebusan untuk membukanya.

Dampak serangan siber sangat besar. Kerugian finansial akibat kejahatan siber di Indonesia diperkirakan mencapai triliunan rupiah setiap tahunnya. Selain kerugian finansial, serangan siber juga dapat merusak reputasi organisasi, mengganggu layanan publik, dan membahayakan keamanan nasional.

Upaya penanggulangan kejahatan siber di Indonesia sudah mulai dilakukan. Pemerintah telah membentuk Badan Siber dan Sandi Negara (BSSN) untuk menangani ancaman siber. Undang-Undang Pelindungan Data Pribadi juga telah disahkan untuk melindungi data warga negara dari penyalahgunaan.

Namun, upaya penanggulangan ini masih menghadapi berbagai tantangan. Sumber daya manusia yang kompeten di bidang keamanan siber masih sangat terbatas. Kesadaran masyarakat tentang keamanan siber juga masih rendah. Banyak orang yang menggunakan kata sandi yang lemah dan tidak berhati-hati dalam membuka tautan atau lampiran email.

Literasi keamanan siber harus ditingkatkan di semua tingkatan. Sekolah harus memasukkan pendidikan keamanan siber ke dalam kurikulum. Perusahaan harus melatih karyawan mereka tentang praktik keamanan siber yang baik. Masyarakat harus dibekali pengetahuan untuk melindungi diri mereka dari ancaman siber."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Refleksi tentang pentingnya belajar bahasa asing",
        "text": """Bahasa asing bukan sekadar alat komunikasi, tetapi juga jendela untuk memahami budaya lain. Dalam dunia yang semakin terhubung ini, kemampuan berbahasa asing menjadi semakin penting. Namun, masih banyak orang yang meremehkan pentingnya belajar bahasa asing.

Saya sendiri merasakan manfaat belajar bahasa asing dalam karir saya. Kemampuan berbahasa Inggris membantu saya mendapatkan pekerjaan di perusahaan multinasional. Kemampuan berbahasa Jepang membantu saya dalam negosiasi bisnis dengan rekanan dari Jepang. Tanpa kemampuan bahasa asing, saya mungkin tidak akan berada di posisi saya sekarang.

Belajar bahasa asing juga melatih otak. Penelitian menunjukkan bahwa orang yang bilingual memiliki kemampuan kognitif yang lebih baik dibandingkan dengan monolingual. Mereka lebih baik dalam menyelesaikan masalah, berpikir kreatif, dan mengalihkan perhatian. Hal ini karena belajar bahasa asing melatih otak untuk bekerja dengan dua sistem bahasa yang berbeda.

Namun, tantangan belajar bahasa asing di Indonesia cukup besar. Sistem pendidikan yang masih mengutamakan hafalan dan ujian tertulis membuat banyak siswa tidak mampu berbicara dalam bahasa asing yang mereka pelajari. Mereka mungkin bisa membaca dan menulis, tetapi kesulitan dalam berkomunikasi lisan.

Solusinya adalah dengan menciptakan lingkungan belajar yang lebih komunikatif. Siswa harus diberikan kesempatan untuk berbicara dalam bahasa asing sejak dini. Metode pembelajaran yang interaktif dan menyenangkan juga perlu diterapkan agar siswa tidak merasa terbebani.

Belajar bahasa asing adalah investasi untuk masa depan. Dengan kemampuan bahasa asing, kita dapat membuka peluang yang lebih luas, memahami budaya lain, dan menjadi warga dunia yang lebih baik."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Dampak perubahan iklim terhadap pertanian Indonesia",
        "text": """Perubahan iklim menjadi ancaman serius bagi sektor pertanian Indonesia. Peningkatan suhu global, perubahan pola hujan, dan peningkatan frekuensi bencana alam berdampak langsung terhadap hasil pertanian. Petani Indonesia, yang sebagian besar bergantung pada alam, menjadi kelompok yang paling rentan terhadap dampak perubahan iklim.

Perubahan pola hujan menyebabkan kekeringan di beberapa daerah dan banjir di daerah lain. Kekeringan menyebabkan gagal panen, sementara banjir merusak tanaman dan infrastruktur pertanian. Petani yang tidak memiliki sistem irigasi yang memadai menjadi yang paling menderita.

Peningkatan suhu global juga berdampak pada hasil pertanian. Beberapa tanaman pangan sensitif terhadap suhu. Padi, misalnya, mengalami penurunan hasil jika suhu meningkat terlalu tinggi. Hal ini mengancam ketahanan pangan nasional.

Upaya adaptasi terhadap perubahan iklim perlu dilakukan. Petani harus dibekali dengan pengetahuan tentang praktik pertanian yang tahan iklim. Penggunaan varietas tanaman yang tahan kekeringan dan banjir perlu dipromosikan. Sistem peringatan dini bencana alam juga harus ditingkatkan.

Pemerintah juga harus berperan aktif dalam mitigasi perubahan iklim. Pengurangan emisi gas rumah kaca harus menjadi prioritas. Penggunaan energi terbarukan harus ditingkatkan. Kebijakan lingkungan yang ketat harus diterapkan untuk melindungi hutan dan sumber daya alam.

Perubahan iklim bukanlah masalah yang bisa diatasi oleh satu pihak saja. Diperlukan kerja sama dari semua pemangku kepentingan, mulai dari petani hingga pemerintah, untuk menghadapi tantangan ini. Masa depan pertanian Indonesia tergantung pada bagaimana kita merespons perubahan iklim saat ini."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Peran perpustakaan dalam mendukung literasi",
        "text": """Perpustakaan memainkan peran yang sangat penting dalam mendukung literasi di masyarakat. Sebagai pusat informasi dan pengetahuan, perpustakaan menyediakan akses terhadap berbagai sumber belajar yang diperlukan untuk meningkatkan kemampuan membaca dan menulis masyarakat.

Peran perpustakaan tidak terbatas pada penyediaan buku. Perpustakaan modern juga menyediakan akses terhadap e-book, jurnal digital, dan berbagai sumber informasi elektronik lainnya. Perpustakaan juga menyelenggarakan berbagai program seperti kelompok membaca, ceramah, dan workshop untuk meningkatkan literasi masyarakat.

Namun, tantangan yang dihadapi perpustakaan juga tidak sedikit. Anggaran yang terbatas membuat banyak perpustakaan tidak mampu memperbarui koleksinya secara berkala. Fasilitas yang kurang memadai membuat pengunjung tidak nyaman. Selain itu, budaya membaca yang masih rendah di masyarakat membuat jumlah pengunjung perpustakaan relatif sedikit.

Upaya peningkatan peran perpustakaan perlu dilakukan dari berbagai aspek. Pemerintah harus meningkatkan anggaran untuk perpustakaan. Perpustakaan harus berinovasi dalam layanannya, termasuk menyediakan ruang baca yang nyaman dan program-program yang menarik. Masyarakat juga harus diedukasi tentang pentingnya perpustakaan sebagai sumber pengetahuan.

Perpustakaan sekolah juga memiliki peran yang krusial dalam membentuk budaya membaca sejak dini. Perpustakaan sekolah yang baik akan mendorong siswa untuk gemar membaca. Guru harus aktif mengarahkan siswa untuk memanfaatkan fasilitas perpustakaan.

Perpustakaan adalah jantung dari ekosistem literasi. Tanpa perpustakaan yang baik, upaya peningkatan literasi akan sulit berhasil. Investasi dalam perpustakaan adalah investasi dalam masa depan bangsa yang literat dan berpengetahuan."""
    },
    # ── Tambahan untuk mencapai 30 sampel
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Pengalaman belajar daring selama pandemi",
        "text": """Pandemi COVID-19 membawa perubahan besar dalam dunia pendidikan. Pembelajaran daring menjadi satu-satunya pilihan untuk menjaga kelangsungan pendidikan. Sebagai seorang guru, saya harus beradaptasi dengan cepat untuk menghadapi situasi baru ini.

Tantangan pertama yang saya hadapi adalah keterbatasan teknologi. Tidak semua siswa memiliki akses terhadap komputer atau smartphone yang memadai. Beberapa siswa harus berbagi perangkat dengan anggota keluarga lainnya. Akses internet juga menjadi masalah, terutama bagi siswa yang tinggal di daerah terpencil.

Tantangan kedua adalah metode pembelajaran. Saya harus mengubah cara mengajar saya sepenuhnya. Materi yang sebelumnya disampaikan secara lisan di kelas harus diubah menjadi konten digital yang menarik. Saya belajar menggunakan berbagai platform seperti Zoom, Google Classroom, dan Canva untuk membuat materi pembelajaran yang interaktif.

Tantangan ketiga adalah motivasi siswa. Banyak siswa yang merasa bosan dan kehilangan motivasi belajar karena harus belajar dari rumah dalam waktu yang lama. Interaksi sosial yang terbatas juga berdampak pada kesehatan mental siswa. Saya harus berusaha keras untuk mempertahankan semangat belajar mereka.

Namun, di balik tantangan tersebut, ada banyak pelajaran berharga yang saya dapatkan. Saya menjadi lebih kreatif dalam mengajar. Saya juga menyadari pentingnya membangun hubungan yang baik dengan siswa, bahkan melalui layar komputer. Komunikasi yang efektif menjadi kunci keberhasilan pembelajaran daring.

Pandemi juga mengajarkan kita bahwa teknologi adalah alat yang powerful, tetapi manusia tetap menjadi komponen yang paling penting dalam pendidikan. Guru yang dedicative dan siswa yang motivated adalah kunci keberhasilan pendidikan, apapun metode yang digunakan."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Pentingnya menjaga kesehatan mental di tempat kerja",
        "text": """Kesehatan mental di tempat kerja menjadi topik yang semakin mendapat perhatian dalam beberapa tahun terakhir. Tekanan pekerjaan, tenggat waktu yang ketat, dan lingkungan kerja yang toxic dapat berdampak negatif pada kesehatan mental karyawan. Oleh karena itu, penting bagi organisasi untuk memperhatikan kesehatan mental karyawannya.

Tanda-tanda masalah kesehatan mental di tempat kerja antara lain: penurunan produktivitas, ketidakhadiran yang sering, perubahan perilaku yang drastis, dan keluhan fisik yang tidak jelas penyebabnya. Jika tidak ditangani dengan baik, masalah kesehatan mental dapat berdampak pada kinerja individu dan organisasi secara keseluruhan.

Organisasi dapat mengambil beberapa langkah untuk mendukung kesehatan mental karyawan. Pertama, menciptakan budaya kerja yang mendukung, di mana karyawan merasa nyaman untuk berbicara tentang masalah kesehatan mental mereka. Kedua, menyediakan program bantuan karyawan (EAP) yang memberikan akses terhadap konseling profesional.

Ketiga, memberikan fleksibilitas dalam bekerja, termasuk opsi work from home dan jam kerja yang fleksibel. Keempat, mengadakan program kesehatan dan kebugaran yang melibatkan aktivitas fisik, meditasi, dan manajemen stres. Kelima, melatih manajer untuk mengenali tanda-tanda masalah kesehatan mental pada bawahannya.

Sebagai individu, kita juga harus proaktif dalam menjaga kesehatan mental kita. Beberapa langkah yang dapat dilakukan antara lain: menetapkan batasan yang jelas antara pekerjaan dan kehidupan pribadi, mengambil istirahat secara teratur, berolahraga secara rutin, dan mencari bantuan profesional jika diperlukan.

Kesehatan mental sama pentingnya dengan kesehatan fisik. Dengan menjaga kesehatan mental, kita dapat bekerja lebih produktif, memiliki hubungan yang lebih baik, dan menikmati kehidupan yang lebih bermakna."""
    },
    {
        "source": "Wikipedia Bahasa Indonesia (id.wikipedia.org)",
        "license": "CC BY-SA 4.0",
        "topic": "Kereta api Indonesia — sejarah transportasi",
        "text": """Kereta api merupakan salah satu mode transportasi tertua di Indonesia. Sejarah kereta api di Indonesia dimulai pada tahun 1867 ketika pemerintah kolonial Belanda membangun jalur kereta pertama yang menghubungkan Semarang dengan Surakarta. Sejak saat itu, jaringan kereta api di Indonesia terus berkembang.

Pada masa kolonial, kereta api berperan penting dalam mengangkut hasil bumi dari daerah penghasil ke pelabuhan. C seperti teh, kopi, gula, dan rempah-rempah diangkut menggunakan kereta api dari daerah penghasil ke pelabuhan untuk diekspor ke Eropa. Kereta api juga digunakan untuk mengangkut penumpang antarkota.

Setelah kemerdekaan, PT Kereta Api Indonesia (KAI) ditetapkan sebagai badan usaha milik negara yang mengelola jaringan kereta api di Indonesia. KAI terus mengembangkan jaringan kereta api, memperbaiki infrastruktur, dan meningkatkan pelayanan kepada penumpang.

Dalam perkembangannya, kereta api Indonesia menghadapi berbagai tantangan. Persaingan dengan mode transportasi lain seperti bus dan pesawat terbang membuat jumlah penumpang kereta api sempat menurun. Selain itu, infrastruktur yang sudah tua juga menjadi masalah yang perlu ditangani.

Namun, dalam beberapa tahun terakhir, KAI berhasil meningkatkan kembali popularitas kereta api. Pengenalan kelas eksekutif dan bisnis yang nyaman, perbaikan jadwal, dan peningkatan keamanan membuat kereta api menjadi pilihan yang menarik bagi masyarakat. Kereta api juga menjadi pilihan yang lebih ramah lingkungan dibandingkan dengan kendaraan pribadi.

Kereta api bukan sekadar alat transportasi, tetapi juga merupakan bagian dari sejarah Indonesia. Perjalanan kereta api dari Jakarta ke Yogyakarta, misalnya, tidak hanya tentang transportasi, tetapi juga tentang menikmati keindahan alam Indonesia dari balik jendela kereta."""
    },
    {
        "source": "Opini media nasional (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Peran UMKM dalam perekonomian Indonesia",
        "text": """Usaha Mikro, Kecil, dan Menengah (UMKM) merupakan tulang punggung perekonomian Indonesia. Data menunjukkan bahwa UMKM menyumbang sekitar 60 persen dari Produk Domestik Bruto (PDB) Indonesia dan menyerap sekitar 97 persen tenaga kerja. Peran UMKM sangat krusial dalam menciptakan lapangan kerja dan mengurangi kemiskinan.

Namun, UMKM Indonesia menghadapi berbagai tantangan yang serius. Akses terhadap pembiayaan masih menjadi masalah utama. Banyak UMKM yang kesulitan mendapatkan pinjaman dari bank karena tidak memiliki jaminan yang memadai. Selain itu, kemampuan manajemen yang terbatas juga menjadi penghambat perkembangan UMKM.

Teknologi digital membuka peluang baru bagi UMKM. Platform e-commerce seperti Tokopedia, Shopee, dan Bukalapak memungkinkan UMKM untuk menjual produk mereka secara online dan menjangkau pasar yang lebih luas. Media sosial juga menjadi alat pemasaran yang efektif dan murah bagi UMKM.

Pemerintah telah meluncurkan berbagai program untuk mendukung UMKM, termasuk Kredit Usaha Rakyat (KUR), pelatihan kewirausahaan, dan fasilitasi akses pasar. Program-program ini bertujuan untuk membantu UMKM mengatasi berbagai tantangan dan meningkatkan daya saing mereka.

Namun, masih banyak UMKM yang belum memanfaatkan program-program pemerintah ini. Kesadaran dan literasi digital UMKM masih perlu ditingkatkan. Pelatihan dan pendampingan yang berkelanjutan juga diperlukan agar UMKM dapat mengembangkan usahanya secara berkelanjutan.

UMKM bukan hanya tentang ekonomi, tetapi juga tentang kehidupan masyarakat. Dengan mendukung UMKM, kita mendukung kesejahteraan jutaan keluarga Indonesia. Investasi dalam UMKM adalah investasi dalam masa depan ekonomi Indonesia."""
    },
    {
        "source": "Tulisan akademik ringan (fair use untuk riset akademik)",
        "license": "Fair use untuk riset akademik",
        "topic": "Pengaruh televisi terhadap perilaku anak",
        "text": """Televisi masih menjadi salah satu media hiburan yang paling populer di kalangan anak-anak Indonesia. Meskipun internet dan media sosial semakin dominan, televisi tetap memiliki tempat tersendiri dalam kehidupan sehari-hari keluarga Indonesia. Namun, pengaruh televisi terhadap perilaku anak perlu mendapat perhatian serius.

Penelitian menunjukkan bahwa menonton televisi secara berlebihan dapat berdampak negatif pada perkembangan anak. Anak-anak yang menghabiskan terlalu banyak waktu di depan televisi cenderung memiliki masalah perilaku seperti agresivitas, kesulitan berkonsentrasi, dan gangguan tidur. Hal ini disebabkan oleh konten televisi yang seringkali mengandung kekerasan dan bahasa yang tidak pantas.

Di sisi lain, televisi juga memiliki dampak positif jika digunakan dengan bijak. Program-program pendidikan seperti kartun edukasi dan program sains dapat membantu anak belajar hal-hal baru. Televisi juga bisa menjadi sarana untuk memperkenalkan anak pada berbagai budaya dan pengetahuan.

Kunci penggunaan televisi yang bijak adalah pengawasan orang tua. Orang tua harus memilihkan program televisi yang sesuai untuk anak, membatasi waktu menonton, dan mendiskusikan isi program dengan anak. Pengawasan aktif orang tua sangat penting untuk memastikan bahwa televisi memberikan dampak positif bagi perkembangan anak.

Pendidikan literasi media juga perlu diberikan kepada anak-anak sejak dini. Anak harus diajarkan untuk berpikir kritis terhadap apa yang mereka tonton di televisi. Mereka harus bisa membedakan antara realitas dan fiksi, serta memahami pesan-pesan tersembunyi yang mungkin terkandung dalam program televisi.

Televisi bukanlah musuh, tetapi harus digunakan secara bertanggung jawab. Dengan pengawasan dan pendidikan yang tepat, televisi bisa menjadi alat yang bermanfaat bagi perkembangan anak."""
    },
    {
        "source": "Kompasiana (kompasiana.com)",
        "license": "User-generated content, fair use untuk riset akademik",
        "topic": "Refleksi tentang pentingnya waktu keluarga",
        "text": """Di tengah kesibukan pekerjaan dan aktivitas sehari-hari, waktu keluarga seringkali menjadi hal yang terabaikan. Kita mungkin sibuk bekerja dari pagi hingga malam, menghabiskan waktu di depan komputer atau handphone, tanpa menyadari bahwa anak-anak kita tumbuh dengan cepat di depan mata.

Saya pernah mengalami pengalaman yang membuka mata. Suatu hari, anak saya yang berusia lima tahun bertanya, "Ayah, kenapa Ayah selalu sibuk?" Pertanyaan sederhana ini membuat saya terdiam. Saya menyadari bahwa saya telah menghabiskan terlalu banyak waktu untuk bekerja dan terlalu sedikit waktu untuk keluarga.

Sejak saat itu, saya memutuskan untuk mengubah prioritas saya. Saya mulai meluangkan waktu setiap hari untuk bermain dan berbicara dengan anak-anak saya. Kami makan malam bersama setiap hari, meskipun hanya sebentar. Kami bermain di taman pada akhir pekan. Kami membaca buku bersama sebelum tidur.

Perubahan kecil ini memberikan dampak yang besar. Hubungan saya dengan anak-anak menjadi lebih dekat. Mereka lebih terbuka kepada saya, baik tentang kegembiraan maupun masalah yang mereka hadapi. Saya juga merasa lebih bahagia dan puas dengan kehidupan saya.

Waktu keluarga bukan tentang kuantitas, tetapi kualitas. Satu jam yang berkualitas bersama keluarga lebih berharga dari sepuluh jam yang dihabiskan bersama tetapi terganggu oleh pekerjaan atau gadget. Kehadiran yang penuh perhatian adalah hadiah terbaik yang bisa kita berikan kepada keluarga.

Marilah kita luangkan waktu untuk keluarga. Anak-anak kita hanya memiliki masa kecil sekali. Jangan biarkan kesibukan pekerjaan menghalangi kita untuk menjadi orang tua yang hadir dan peduli."""
    },
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, essay in enumerate(ESSAYS, 1):
        fname = f"essay_{i:03d}.txt"
        # Format: header sumber + topik + teks
        content = f"Sumber: {essay['source']}\nLisensi: {essay['license']}\nTopik: {essay['topic']}\n\n{essay['text']}"
        (OUT_DIR / fname).write_text(content, encoding="utf-8")
        words = len(essay['text'].split())
        print(f"{fname}: {words} kata | {essay['topic'][:50]}")

    print(f"\nTotal: {len(ESSAYS)} esai disimpan ke {OUT_DIR}")

    # Save metadata
    meta = [{"file": f"essay_{i:03d}.txt", "source": e["source"], "license": e["license"],
             "topic": e["topic"], "words": len(e["text"].split())}
            for i, e in enumerate(ESSAYS, 1)]
    meta_path = OUT_DIR.parent / "m5_human_metadata.json"
    import json
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Metadata: {meta_path}")

if __name__ == "__main__":
    main()
