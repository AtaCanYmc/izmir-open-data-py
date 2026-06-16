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

# 2. Belirli bir verisetini çek (örn: hal-fiyatlari)
# CLI, çıktıyı formatlı JSON olarak terminale basacaktır.
echo "[2] 'hal-fiyatlari' veriseti çekiliyor:"
izmir-data get hal-fiyatlari

# İPUCU: Çıktıyı işlemek için 'jq' gibi araçlarla birlikte kullanabilirsiniz:
# izmir-data get hal-fiyatlari | jq '.kayitlar[0]'
