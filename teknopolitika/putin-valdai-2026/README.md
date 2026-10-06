# TEKNOPOLİTİKA — Putin'in Valdai 2026 AI konuşması (60 sn · 9:16)

Putin'in 1 Ekim 2026 Valdai Tartışma Kulübü (XXIII. Yıllık Toplantı, plener oturum) konuşmasındaki
yapay zekâ, enerji ve insan kontrolü argümanının analitik çözümlemesi.

- **Video:** `putin-valdai-2026-ai-analiz.mp4` (1080×1920, 30 fps, H.264 + AAC, 60 sn)
- **Canlı önizleme / kaynak:** `index.html` (deterministik canvas motoru; kaydırıcıyla kare kare incelenebilir)

## Yapı

| Zaman | Bölüm | Alt-üç katmanı |
|---|---|---|
| 0:00–0:06 | Kanca: kaynak karesi + altyapı kesmeleri; YAPAY ZEKÂ / ENERJİ / SAVAŞ / İNSAN KONTROLÜ | 01 Putin ne dedi |
| 0:06–0:15 | 1 — İnsan / Makine: hesaplama ↔ muhakeme | 01 → 02 |
| 0:15–0:25 | Petrov, 26.09.1983: SİSTEM → SALDIRI / PETROV → ŞÜPHE | 01 → 03 |
| 0:25–0:35 | 2 — Fiziksel güç: AI = COMPUTE + ENERJİ + ALTYAPI | 01 → 02 |
| 0:35–0:46 | 3 — Karar hızı: TESPİT → ANALİZ → KARAR → MÜDAHALE | 01 → 02 |
| 0:46–0:55 | Teknopolitika analizi: COMPUTE · ENERJİ · KARAR → EGEMENLİK | 03 |
| 0:55–1:00 | HESAPLAMA. ENERJİ. KARAR. → GÜÇ. | — |

Alt-üç notlarında üç kademeli, renk kodlu hiyerarşi var: **01 PUTİN NE DEDİ** (amber, kaynak) →
**02 NE ANLAMA GELİYOR** (açık gri) → **03 NEDEN ÖNEMLİ · TEKNOPOLİTİKA** (camgöbeği, analiz).
Putin her görüldüğü karede "KAYNAK GÖRÜNTÜ" künyesiyle ve amber çerçeveyle işaretlenir.
Analitik ses yalnızca camgöbeği katmandadır. Alt-üç notları en fazla iki satırdır ve 1080×1920
güvenli alanının içinde kalır (y 1338–1470, sağ kenar ≤ 940 px).

## Kaynak görüntü hakkında

Varsayılan sürümdeki konuşmacı **temsili bir siluettir**: göz hizasında, kadrajda küçük ve yüz
detayı yok. Gerçek konuşma görüntüsü kullanmak için lisanslı bir klip verilebilir. kremlin.ru
içerikleri CC BY 4.0 lisanslıdır; kaynak belirtilmelidir.

```bash
node render.mjs --plate kaynak/valdai-2026.mp4
```

Klip kaynak karesinin içine yerleştirilir ve arşiv tonuna göre renklendirilir (desatüre, gren, tarama çizgisi).
Künye, ses dalgası ve zaman kodu aynen kalır.

## Yeniden üretim

```bash
python3 audio/gen_audio.py      # telifsiz sentez ses zemini
node render.mjs --stills 2,17.5 # test kareleri → out/stills
node render.mjs                 # tam video → out/putin-valdai-2026-ai-analiz.mp4
```

Gereksinimler: Node + Playwright (Chromium), ffmpeg, Python 3 + NumPy.
Fontlar `fonts/` içinde: Inter / Inter Display (SIL OFL), Newsreader (OFL), IBM Plex Mono (OFL).

## Olgu kontrolü

- Konuşma tarihi ve oturum: 1 Ekim 2026, Valdai XXIII. Yıllık Toplantı plener oturumu.
- Petrov atfı: Putin, AI'ın eksiklerini anlatırken 1983 yanlış alarmını hatırlattı ve
  "herhangi bir algoritma" bu sinyali misilleme için kesin bir gerekçe sayardı dedi (basın özetleri).
- 26 Eylül 1983, Serpukhov-15: Oko erken uyarı sistemi ABD'den önce bir, sonra beş füze fırlatıldığını
  bildirdi. Nöbetçi subay Yarbay Stanislav Petrov bunu yanlış alarm olarak raporladı. Sebep, yüksek irtifa
  bulutlarından yansıyan güneş ışığıydı.
- "İnsan döngünün içinde / üzerinde / dışında" (in / on / out of the loop) ayrımı otonom silah sistemleri
  literatüründen alınmıştır. Bu ayrım Putin'e değil, TEKNOPOLİTİKA'nın analiz katmanına aittir.
- Karar ağı sahnesindeki hızlanma ve "karar hızı" çubuğu **temsilidir**, ölçülmüş veri değildir.
