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

# 2. Afet Acil Toplanma Alanları
echo "[2] 'cbs/afetaciltoplanmaalani' veriseti çekiliyor:"
izmir-data get cbs/afetaciltoplanmaalani | head -n 20
echo "..."
echo

# 3. İzmir'deki Plajlar
echo "[3] 'cbs/plajlar' veriseti çekiliyor:"
izmir-data get cbs/plajlar | head -n 20
echo "..."
echo

# 4. Hastaneler
echo "[4] 'cbs/hastaneler' veriseti çekiliyor:"
izmir-data get cbs/hastaneler | head -n 20
echo "..."
echo

# 5. Kütüphaneler
echo "[5] 'cbs/kutuphaneler' veriseti çekiliyor:"
izmir-data get cbs/kutuphaneler | head -n 20
echo "..."
echo

# 6. Bankalar
echo "[6] 'cbs/bankalar' veriseti çekiliyor:"
izmir-data get cbs/bankalar | head -n 20
echo "..."
echo
