import json
from typing import Any
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class CVRatingAnalyzer(BaseModel):
    nama_kandidat: str = Field(description="Nama Lengkap Kandidat yang ada dalam CV")

    skor_objektif: int = Field(
        description="Skor untuk ringkasan objektif/profil di CV (Skala rentang: 0 sampai 100)"
    )
    skor_pengalaman_kerja: int = Field(
        description="Skor kelayakan bagian pengalaman kerja dengan kriteria posisi (Skala rentang: 0 sampai 100)"
    )
    skor_pendidikan: int = Field(
        description="Skor relevansi latar belakang pendidikan kandidat (Skala rentang: 0 sampai 100)"
    )
    skor_keterampilan: int = Field(
        description="Skor kesesuaian technical skill kandidat dengan kebutuhan posisi (Skala rentang: 0 sampai 100)"
    )
    kelebihan: str = Field(description="Kelebihan utama kandidat berdasarkan CV")
    kekurangan: str = Field(description="Kekurangan utama kandidat berdasarkan CV")


kriteria_posisi = """
    Posisi: Backend Engineer (Golang)
    Kriteria: Menguasai RESTful API, database SQL/NoSQL, memahami Clean Architecture, 
    dan terbiasa dengan konsep microservices. Berpengalaman di projek nyata lebih disukai.
    """

prompt_instruksi = f"""
Bertindaklah sebagai Technical Recruiter. Analisis dokumen CV yang terlampir secara objektif.
Berikan rating skor dan poin-poin evaluasi berdasarkan kriteria posisi berikut:

{kriteria_posisi}

ATURAN PENTING UNTUK SKORING:
- Semua nilai skor (skor_objektif, skor_pengalaman_kerja, skor_pendidikan, skor_keterampilan) HARUS menggunakan skala angka bulat dari 0 sampai 100.
- Nilai 100 artinya sangat sempurna memenuhi kriteria, nilai 0 artinya tidak ada sama sekali.

Isi dan ekstrak data sesuai dengan skema JSON yang diminta secara akurat.
"""

# initialisasi client GENAI

# genai adalah library untuk berinteraksi dengan Google GenAI API, yang memungkinkan kita untuk memanfaatkan kemampuan AI dalam berbagai aplikasi, termasuk analisis teks, pemrosesan bahasa alami, dan lainnya. Dengan menggunakan genai, kita dapat mengirim permintaan ke model AI untuk mendapatkan respons yang sesuai dengan kebutuhan aplikasi kita.
client = genai.Client()


def analyze_cv(file_path: str) -> CVRatingAnalyzer:
    # Implementation for analyzing CV and returning the rating analyzer object
    try:
        file_uploading = client.files.upload(file=file_path)
        response = client.models.generate_content(
            model="models/gemini-3.1-flash-lite",
            contents=[file_uploading, prompt_instruksi],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",  # Memaksa output berupa JSON
                response_schema=CVRatingAnalyzer,  # Menggunakan struktur Pydantic di atas
                temperature=0.1,  # Suhu rendah agar AI lebih konsisten & objektif
            ),
        )

        if getattr(response, "parsed", None) is not None:
            parsed = response.parsed
            if isinstance(parsed, CVRatingAnalyzer):
                return parsed
            if isinstance(parsed, dict):
                return CVRatingAnalyzer(**parsed)

        if isinstance(response.text, str):
            return CVRatingAnalyzer(**json.loads(response.text))

        raise ValueError("Model response is not valid JSON text.")
    except Exception:
        raise
