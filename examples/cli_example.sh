#!/bin/bash

# CLI (Komut Satırı Arayüzü) Kullanım Örneği
#
# Bu script, 'izmir-data' CLI aracının nasıl kullanılacağını gösterir.
# Not: Çalıştırmadan önce projeyi kurduğunuzdan emin olun (örn: `uv pip install -e .`)

echo "=== İzmir Açık Veri CLI Örnekleri ==="
echo

# 1. Yardım menüsünü göster
echo "[1] Yardım menüsü görüntüleniyor:"
izmir-data --help
echo
echo "-----------------------------------"
echo

# 2. Portalda veri seti arama
echo "[2] 'tuvalet' anahtar kelimesiyle veri seti arama:"
izmir-data search tuvalet --limit 5
echo
echo "-----------------------------------"
echo

# 3. CKAN Datastore sorgulama
echo "[3] Akıllı tuvaletler datastore kaynağından kayıt çekme:"
izmir-data datastore d87de3c1-9bc0-4a8c-842a-90cd2a30d03a --limit 3
echo
echo "-----------------------------------"
echo

# 4. Afet Acil Toplanma Alanları
echo "[4] 'cbs/afetaciltoplanmaalani' veriseti çekiliyor:"
izmir-data get cbs/afetaciltoplanmaalani | head -n 20
echo "..."
echo

# 5. Hastaneler
echo "[5] 'cbs/hastaneler' veriseti çekiliyor:"
izmir-data get cbs/hastaneler | head -n 20
echo "..."
echo
