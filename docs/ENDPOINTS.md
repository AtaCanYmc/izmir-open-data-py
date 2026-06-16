# İzmir Open Data API Endpoint Listesi

İzmir Büyükşehir Belediyesi Açık Veri Portalı ve Open API servislerinin `izmir-open-data-py` kütüphanesi içindeki sınıf ve metod dağılımları.

## Afetler (`client.afetler`)
| Metod Adı | Açıklama |
|---|---|
| `get_acil_durum_toplanma_alanlari()` | Afet ve acil durum toplanma alanlarına ait ilçe, mahalle ve konum bilgilerini içeren web servisi. |

## Bisim (`client.bisim`)
| Metod Adı | Açıklama |
|---|---|
| `get_istasyon_list()` | İstasyonların konum, kapasite ve bisiklet sayılarını içeren web servisi. |

## Cografi (`client.cografi`)
| Metod Adı | Açıklama |
|---|---|
| `get_ada_yarimada_list()` | Ada ve yarımada konum bilgilerini içeren web servisi. |
| `get_burunlar_list()` | Burun konum bilgilerini içeren web servisi. |
| `get_dag_tepe_list()` | Dağ ve tepelerin konum bilgilerini içeren web servisi. |
| `get_goller_list()` | Göl konum bilgilerini içeren web servisi. |
| `get_korfez_koylar_list()` | Körfez ve koyların konum bilgilerini içeren web servisi. |
| `get_meydanlar_list()` | Meydanların konum bilgilerini içeren web servisi. |
| `get_nehir_caylar_list()` | Nehir ve çayların konum bilgilerini içeren web servisi. |
| `get_ormanlar_list()` | Ormanların konum bilgilerini içeren web servisi. |

## Eczaneler (`client.eczaneler`)
| Metod Adı | Açıklama |
|---|---|
| `get_list()` | Eczanelerin bilgilerini içeren web servisi. |
| `get_nobetci_list()` | Nöbetçi eczanelerin bilgilerini içeren web servisi. |

## Egitim (`client.egitim`)
| Metod Adı | Açıklama |
|---|---|
| `get_anaokullar_list()` | Anaokulu konum bilgilerini içeren web servisi. |
| `get_engelli_okullari_list()` | Engelliler okulu konum bilgilerini içeren web servisi. |
| `get_etut_merkezleri_list()` | Etüt eğitim merkezleri konum bilgilerini içeren web servisi. |
| `get_halk_egitim_list()` | Halk eğitim merkezleri konum bilgilerini içeren web servisi. |
| `get_ilkokullar_list()` | İlkokullar konum bilgilerini içeren web servisi. |
| `get_kolejler_list()` | Kolejler konum bilgilerini içeren web servisi. |
| `get_liseler_list()` | Liseler konum bilgilerini içeren web servisi. |
| `get_meslek_liseleri_list()` | Meslek liseleri konum bilgilerini içeren web servisi. |
| `get_milli_egitim_list()` | Milli eğitim müdürlükleri konum bilgilerini içeren web servisi. |
| `get_ortaokullar_list()` | Ortaokullar konum bilgilerini içeren web servisi. |
| `get_sanat_okullari_list()` | Sanat okulları konum bilgilerini içeren web servisi. |
| `get_universiteler_list()` | Üniversiteler konum bilgilerini içeren web servisi. |

## Eshot (`client.eshot`)
| Metod Adı | Açıklama |
|---|---|
| `get_baglanti_hatlari()` | Diğer ulaşım araçları ile bağlantılı otobüs hatlarının listesini içeren web servisi (CSV). |
| `get_baglanti_tipleri()` | Otobüs hatlarının diğer ulaşım araçları ile bağlantı tiplerini içeren web servisi (CSV). |
| `get_duraga_yaklasan_otobus_list()` | Bir durağa yaklaşan otobüslerin listesi, konumu ve diğer bilgilerini içeren web servisi. |
| `get_duraklar()` | ESHOT otobüs duraklarının listesini içeren web servisi (CSV). |
| `get_hareket_saatleri()` | ESHOT otobüs hareket saatlerini içeren web servisi (CSV). |
| `get_hat_guzergahlari()` | ESHOT hat güzergahlarını içeren web servisi (CSV). |
| `get_hat_otobus_konumlari()` | Numarası girilen hatta ait otobüslerin anlık konum bilgilerini içeren web servisi. |
| `get_hatlar()` | ESHOT hatlarının listesini içeren web servisi (CSV). |
| `get_hattin_yaklasan_otobusleri()` | Bir hattın belirli bir durağa yaklaşan otobüslerinin konum ve diğer bilgilerini içeren web servisi. |
| `get_yakin_durak_list()` | Koordinat (enlem, boylam) değerlerine göre en yakın durakları listeler. |

## Etkinlikler (`client.etkinlikler`)
| Metod Adı | Açıklama |
|---|---|
| `get_etkinlik_by_id()` | Belirli bir etkinliğin detay bilgilerini içeren web servisi. |
| `get_list()` | Güncel kültür sanat etkinlikler listesini içeren web servisi. |

## Hizmet (`client.hizmet`)
| Metod Adı | Açıklama |
|---|---|
| `get_hizmet_nokta_list()` | İzBB bünyesindeki hizmet noktalarını içeren web servisi. |

## Iklim (`client.iklim`)
| Metod Adı | Açıklama |
|---|---|
| `get_gunluk_hava_kalitesi_olcumleri()` | Belirtilen tarihe göre hava kalitesi ölçüm değerlerini içeren web servisi. |
| `get_hava_kalitesi_istasyonlari()` | Hava kalitesi ölçüm istasyonlarının konum bilgilerini içeren web servisi (CSV). |

## Izban (`client.izban`)
| Metod Adı | Açıklama |
|---|---|
| `get_durak_mesafeleri()` | İZBAN istasyonları arasındaki mesafe bilgilerini içeren web servisi (CSV). |
| `get_hareket_saatleri()` | Banliyö hareket saatlerini içeren web servisi. |
| `get_istasyon_list()` | Banliyö İstasyonlarının konum bilgileri içeren web servisi. |
| `get_tarife()` | Banliyö fiyat tarifesi bilgisini içeren web servisi. |

## Izmirimkart (`client.izmirimkart`)
| Metod Adı | Açıklama |
|---|---|
| `get_dolum_noktalari()` | İzmirimKart dolum noktalarının adres ve konum bilgilerini içeren web servisi (CSV). |

## Izsu (`client.izsu`)
| Metod Adı | Açıklama |
|---|---|
| `get_ariza_kaynakli_kesinti_list()` | Arıza kaynaklı düzensiz su kesintilerinin ilçe, mahalle, kesinti süresi, sebebi ve açıklama verilerini içeren web servisi. |
| `get_baraj_doluluk_oranlari()` | Barajların doluluk oranlarını içeren web servisi. |
| `get_baraj_su_kalite_raporlari()` | Baraj su kalite raporlarını içeren web servisi. |
| `get_baraj_ve_kuyu_list()` | Baraj ve kuyuların listesi ve konum bilgilerini içeren web servisi. |
| `get_gunluk_su_uretimi()` | Günlük su üretimi miktarlarını içeren web servisi. |
| `get_haftalik_su_analizi()` | Güncel haftalık analiz sonuçlarını içeren web servisi. |
| `get_izsu_sube_list()` | Şube adresleri, telefonları ve konum bilgilerini içeren web servisi. |
| `get_izsu_vezne_list()` | Vezne adresleri, telefonları ve konum bilgilerini içeren web servisi. |
| `get_su_uretimi_dagilimi()` | Su üretiminin aylara ve kaynaklara göre dağılımını içeren web servisi. |

## Iztek (`client.iztek`)
| Metod Adı | Açıklama |
|---|---|
| `get_askida_izmirim_kart_istatistik()` | Askıda İzmirim Kart istatistiklerini içeren web servisi. |

## Kamu (`client.kamu`)
| Metod Adı | Açıklama |
|---|---|
| `get_bankalar_list()` | Bankalar konum bilgilerini içeren web servisi. |
| `get_belediyeler_list()` | Belediye ve birimler konum bilgilerini içeren web servisi. |
| `get_bolge_mudurlukleri_list()` | Bölge müdürlükleri konum bilgilerini içeren web servisi. |
| `get_defterdarliklar_list()` | Defterdarlık konum bilgilerini içeren web servisi. |
| `get_dernekler_list()` | Dernekler konum bilgilerini içeren web servisi. |
| `get_evlendirme_daireleri_list()` | Evlendirme daireleri konum bilgilerini içeren web servisi. |
| `get_il_ilce_mudurlukleri_list()` | İl ve ilçe müdürlükleri konum bilgilerini içeren web servisi. |
| `get_itfaiye_gruplari_list()` | İtfaiye grupları konum bilgilerini içeren web servisi. |
| `get_konsolosluklar_list()` | Konsolosluklar konum bilgilerini içeren web servisi. |
| `get_maskematik_noktalari_list()` | Maskematik istasyon noktaları konum bilgilerini içeren web servisi. |
| `get_meslek_odalari_list()` | Meslek odaları konum bilgilerini içeren web servisi. |
| `get_noterler_list()` | Noterler konum bilgilerini içeren web servisi. |
| `get_nufus_mudurlukleri_list()` | Nüfus müdürlükleri konum bilgilerini içeren web servisi. |
| `get_ptt_list()` | PTT (Posta ve Telgraf Teşkilatı) konum bilgilerini içeren web servisi. |
| `get_turizm_danisma_list()` | Turizm danışma müdürlükleri konum bilgilerini içeren web servisi. |
| `get_vergi_daireleri_list()` | Vergi daireleri konum bilgilerini içeren web servisi. |

## Kutuphane (`client.kutuphane`)
| Metod Adı | Açıklama |
|---|---|
| `get_galeri_ve_salonlar_list()` | Sanat galerisi ve sergi salonları konum bilgilerini içeren web servisi. |
| `get_kultur_merkezleri_list()` | Kültür merkezleri konum bilgilerini içeren web servisi. |
| `get_kutuphaneler_list()` | Kütüphaneler konum bilgilerini içeren web servisi. |
| `get_muzeler_list()` | Müzeler konum bilgilerini içeren web servisi. |
| `get_opera_ve_bale_list()` | Opera ve bale konum bilgilerini içeren web servisi. |
| `get_senfoni_orkestrasi_list()` | Senfoni orkestrası konum bilgilerini içeren web servisi. |
| `get_sinemalar_list()` | Sinemalar konum bilgilerini içeren web servisi. |
| `get_tiyatrolar_list()` | Tiyatrolar konum bilgilerini içeren web servisi. |

## Metro (`client.metro`)
| Metod Adı | Açıklama |
|---|---|
| `get_durak_mesafeleri()` | Metro istasyonları arasındaki mesafe bilgilerini içeren web servisi (CSV). |
| `get_istasyon_list()` | Metro istasyonları sıra ve konum verisi bilgileri içeren web servis. |

## Muhtarliklar (`client.muhtarliklar`)
| Metod Adı | Açıklama |
|---|---|
| `get_list()` | Muhtarlıklar hakkında bilgi ve coğrafi konumlarını içeren web servisi. |

## Otopark (`client.otopark`)
| Metod Adı | Açıklama |
|---|---|
| `get_list()` | Otoparkların konumu, dolu-boş adetleri, çalışma saatleri bilgilerini içeren web servisi. |
| `get_ucretler()` | İzelman otopark ücretlerini içeren web servisi (CKAN). |

## Pazarlar (`client.pazarlar`)
| Metod Adı | Açıklama |
|---|---|
| `get_balik_hal_fiyatlari()` | Balık hal fiyatlarını içeren web servisi. |
| `get_list()` | Semt pazar yerlerinin listesi, günleri ve konum bilgileri içeren web servisi. |
| `get_sebze_meyve_hal_fiyatlari()` | Sebze ve meyve hal fiyatlarını içeren web servisi. |

## Plaj (`client.plaj`)
| Metod Adı | Açıklama |
|---|---|
| `get_fuar_list()` | Fuar alanları konum bilgilerini içeren web servisi. |
| `get_hamamlar_list()` | Hamamlar konum bilgilerini içeren web servisi. |
| `get_kaplicalar_list()` | Kaplıcalar konum bilgilerini içeren web servisi. |
| `get_plajlar_list()` | Plajlar konum bilgilerini içeren web servisi. |

## Saglik (`client.saglik`)
| Metod Adı | Açıklama |
|---|---|
| `get_acil_yardim_istasyonlari_list()` | Acil yardım istasyonları konum bilgilerini içeren web servisi. |
| `get_agiz_dis_sagligi_merkezleri_list()` | Ağız ve diş sağlığı merkezleri konum bilgilerini içeren web servisi. |
| `get_aile_sagligi_merkezleri_list()` | Aile sağlığı merkezleri konum bilgilerini içeren web servisi. |
| `get_ana_cocuk_sagligi_merkezleri_list()` | Ana çocuk sağlığı merkezleri konum bilgilerini içeren web servisi. |
| `get_dal_merkezleri_list()` | Dal merkezleri konum bilgilerini içeren web servisi. |
| `get_hastaneler_list()` | Hastaneler konum bilgilerini içeren web servisi. |
| `get_kan_merkezleri_list()` | Kan merkezleri konum bilgilerini içeren web servisi. |
| `get_laboratuvarlar_list()` | Laboratuvarlar konum bilgilerini içeren web servisi. |
| `get_poliklinikler_list()` | Poliklinikler konum bilgilerini içeren web servisi. |
| `get_tip_merkezleri_list()` | Tıp merkezleri konum bilgilerini içeren web servisi. |
| `get_toplum_sagligi_merkezleri_list()` | Toplum sağlığı merkezleri konum bilgilerini içeren web servisi. |
| `get_verem_savas_dispanserleri_list()` | Verem savaş dispanserleri konum bilgilerini içeren web servisi. |
| `get_veterinerlikler_list()` | Veterinerlikler konum bilgilerini içeren web servisi. |

## Sosyal (`client.sosyal`)
| Metod Adı | Açıklama |
|---|---|
| `get_aile_dayanisma_merkezleri_list()` | Aile dayanışma merkezleri konum bilgilerini içeren web servisi. |
| `get_cocuk_genclik_merkezleri_list()` | Çocuk ve gençlik merkezleri konum bilgilerini içeren web servisi. |
| `get_cocuk_yuvalari_list()` | Çocuk yuvaları konum bilgilerini içeren web servisi. |
| `get_huzurevleri_list()` | Huzurevleri konum bilgilerini içeren web servisi. |
| `get_toplum_merkezleri_list()` | Toplum merkezleri konum bilgilerini içeren web servisi. |
| `get_yetistirme_yurtlari_list()` | Yetiştirme yurtları konum bilgilerini içeren web servisi. |

## Spor (`client.spor`)
| Metod Adı | Açıklama |
|---|---|
| `get_hipodrom_list()` | Hipodrom konum bilgilerini içeren web servisi. |
| `get_spor_salonlari_list()` | Spor salonları ve sahaları konum bilgilerini içeren web servisi. |
| `get_stadyumlar_list()` | Stadyumlar konum bilgilerini içeren web servisi. |
| `get_yuruyus_yollari()` | Yürüyüş ve bisiklet parkurlarının bilgilerini içeren web servisi (CSV). |

## Taksi (`client.taksi`)
| Metod Adı | Açıklama |
|---|---|
| `get_durak_list()` | Taksi durak bilgilerini içeren web servisi. |

## Tarihi (`client.tarihi`)
| Metod Adı | Açıklama |
|---|---|
| `get_antik_kent_yapilari_list()` | Antik kent yapıları konum bilgilerini içeren web servisi. |
| `get_antik_kentler_list()` | Antik kentler konum bilgilerini içeren web servisi. |
| `get_kosk_ve_konaklar_list()` | Köşk ve konaklar konum bilgilerini içeren web servisi. |
| `get_kule_anit_heykeller_list()` | Kule, anıt ve heykeller konum bilgilerini içeren web servisi. |
| `get_tarihi_carsi_hanlar_list()` | Tarihi çarşı ve hanlar konum bilgilerini içeren web servisi. |
| `get_tarihi_su_yapilari_list()` | Tarihi su yapıları konum bilgilerini içeren web servisi. |
| `get_tarihi_yapilar_list()` | Tarihi yapılar konum bilgilerini içeren web servisi. |

## Trafik (`client.trafik`)
| Metod Adı | Açıklama |
|---|---|
| `get_kamera_list()` | İzmir'deki trafik kameralarının listesini içeren web servisi (CSV). |

## Tramvay (`client.tramvay`)
| Metod Adı | Açıklama |
|---|---|
| `get_durak_mesafeleri()` | Tramvay hatları için durak mesafelerini içeren web servisi (CSV). |
| `get_hat_list()` | Tramvay hatları bilgisini içeren web servis: |
| `get_istasyon_list()` | Sefer numarasına göre tramvay istasyonları listesini içeren web servis. |
| `get_planlanani_sefer_sayilari()` | Metro ve tramvay hatları için aylık planlanan sefer sayılarını içeren web servisi (CSV). |
| `get_sefer_list()` | Tramvay sefer ve istasyon id bilgilerini içeren web servisi. |
| `get_sefer_siklik_list()` | Sefer numarasına göre tramvay sefer sıklıkları bilgisini veren web servisi. |

## Tren (`client.tren`)
| Metod Adı | Açıklama |
|---|---|
| `get_arac_muayene_istasyonlari_list()` | Araç muayene istasyonları konum bilgilerini içeren web servisi. |
| `get_havaalani_list()` | Havaalanı konum bilgilerini içeren web servisi. |
| `get_otobus_terminalleri_list()` | Şehirlerarası otobüs terminalleri konum bilgilerini içeren web servisi. |
| `get_tren_garlari_list()` | Tren garları konum bilgilerini içeren web servisi. |

## Vapur (`client.vapur`)
| Metod Adı | Açıklama |
|---|---|
| `get_calisma_gunleri()` | Vapurların çalışma günlerini içeren web servisi. |
| `get_detay_list()` | Vapurların detaylı bilgilerini içeren web servisi (CSV). |
| `get_hareket_saatleri()` | Vapur hareket saatleri bilgisini içeren web servisi. |
| `get_hareket_saatleri_by_hat()` | İskele bazlı vapur hareket saatleri bilgisini içeren web servisi. |
| `get_iskele_list()` | Vapur ve arabalı vapur iskele bilgilerini içeren web servisi. |

## Wizmirnet (`client.wizmirnet`)
| Metod Adı | Açıklama |
|---|---|
| `get_list()` | Ücretsiz-kablosuz internet hizmet noktaları ve lokasyon bilgilerini içeren web servisi. |
