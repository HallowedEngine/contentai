import streamlit as st
import pandas as pd
from app import generate_description
import time

# Sayfa ayarları
st.set_page_config(
    page_title="AI İçerik Asistanı",
    page_icon="🤖",
    layout="wide"
)

# Başlık
st.title("🤖 AI İçerik Asistanı")
st.subheader("E-ticaret için profesyonel ürün açıklamaları - Saniyeler içinde!")

# Sidebar
with st.sidebar:
    st.header("💡 Nasıl Kullanılır?")
    st.markdown("""
    1. **Tek Ürün:** Ürün bilgilerini girin
    2. **Toplu İşlem:** CSV dosyası yükleyin
    3. AI sizin için yazacak!
    
    ---
    
    **💰 Fiyatlandırma:**
    - 100 ürün: 150₺
    - 500 ürün: 500₺
    - Sınırsız: 900₺/ay
    
    ---
    
    **📧 İletişim:** 
    info@contentai.com
    """)
    
    st.metric("🎫 Kalan Kredi", "∞ (Beta)")

# Tab'lar
tab1, tab2, tab3 = st.tabs(["📝 Tek Ürün", "📊 Toplu İşlem (CSV)", "ℹ️ Hakkında"])

# TAB 1: Tek Ürün
with tab1:
    st.markdown("### Tek Ürün İçin Açıklama Oluştur")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        product_name = st.text_input(
            "📦 Ürün Adı",
            placeholder="Örn: Kablosuz Bluetooth Kulaklık"
        )
        
        features = st.text_area(
            "✨ Ürün Özellikleri",
            placeholder="Örn: 20 saat batarya, gürültü önleme...",
            height=120
        )
        
        keywords = st.text_input(
            "🔑 SEO Anahtar Kelimeleri (Opsiyonel)",
            placeholder="Örn: bluetooth kulaklık, kablosuz"
        )
    
    with col2:
        word_count = st.slider("📏 Kelime Sayısı", 50, 300, 150, step=10)
        tone = st.selectbox("🎨 Yazım Tonu", ["samimi", "profesyonel", "lüks"])
    
    if st.button("✍️ Açıklama Oluştur", type="primary"):
        if product_name and features:
            with st.spinner("🤖 AI yazıyor..."):
                time.sleep(0.5)
                
                description = generate_description(
                    product_name=product_name,
                    features=features + (f"\n\nAnahtar kelimeler: {keywords}" if keywords else ""),
                    word_count=word_count,
                    tone=tone
                )
                
                st.success("✅ Tamamlandı!")
                
                st.markdown("### 📄 Ürün Açıklaması:")
                st.info(description)
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Kelime", len(description.split()))
                col_b.metric("Karakter", len(description))
                col_c.metric("Ton", tone.title())
                
                st.download_button(
                    "📥 TXT İndir",
                    description,
                    file_name=f"{product_name.replace(' ', '_')}_aciklama.txt"
                )
        else:
            st.error("⚠️ Lütfen ürün adı ve özellikleri doldurun!")

# TAB 2: Toplu İşlem - TAM DÜZELTİLMİŞ VERSİYON
with tab2:
    st.markdown("### 📊 Toplu Ürün İşleme (CSV)")
    
    st.info("**CSV Formatı:** `urun_adi` ve `ozellikler` kolonları olmalı")
    
    uploaded_file = st.file_uploader("CSV Dosyası Yükle", type=["csv"])
    
    if uploaded_file:
        # CSV'yi oku
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ {len(df)} ürün yüklendi!")
        
        # Önizleme
        st.markdown("**📋 Önizleme:**")
        st.dataframe(df.head(5))
        
        # Ayarlar
        col1, col2 = st.columns(2)
        batch_word_count = col1.slider("Kelime Sayısı", 50, 300, 150, key="bwc")
        batch_tone = col2.selectbox("Ton", ["samimi", "profesyonel", "lüks"], key="bt")
        
        # Toplu oluştur butonu
        if st.button("🚀 Toplu Oluştur", type="primary"):
            
            status_text = st.empty()
            descriptions = []
            
            # Her satır için işlem
            for idx in range(len(df)):
                row = df.iloc[idx]
                
                # Status göster
                status_text.info(f"⏳ İşleniyor: {idx+1}/{len(df)} - {row['urun_adi']}")
                
                # Açıklama üret
                desc = generate_description(
                    product_name=str(row['urun_adi']),
                    features=str(row['ozellikler']),
                    word_count=batch_word_count,
                    tone=batch_tone
                )
                
                descriptions.append(desc)
                time.sleep(1)  # Rate limit
            
            # Sonuçları ekle
            df['ai_aciklama'] = descriptions
            
            # Status temizle
            status_text.empty()
            
            # Başarı mesajı
            st.success(f"🎉 {len(df)} ürün tamamlandı!")
            
            # Sonuçları göster
            st.markdown("**📊 Sonuçlar:**")
            st.dataframe(df)
            
            # İndirme
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Sonuçları İndir (CSV)",
                csv_data,
                "ai_aciklamalar.csv",
                "text/csv"
            )

# TAB 3: Hakkında
with tab3:
    st.markdown("""
    ## 🤖 AI İçerik Asistanı Hakkında
    
    E-ticaret işletmeleri için **GPT-4 teknolojisi** kullanarak profesyonel ürün açıklamaları oluşturur.
    
    ### ✨ Özellikler:
    - **Hızlı:** Saniyeler içinde açıklama
    - **SEO Uyumlu:** Anahtar kelimeler doğal şekilde entegre
    - **Farklı Tonlar:** Profesyonel, samimi veya lüks
    - **Toplu İşlem:** CSV ile yüzlerce ürün tek seferde
    
    ### 🎯 Kimler Kullanabilir?
    - E-ticaret site sahipleri
    - Trendyol/Hepsiburada satıcıları
    - Dijital pazarlama ajansları
    
    ---
    
    **Versiyon:** 1.0 Beta  
    **Yapımcı:** ContentAI Team
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Made with ❤️ by ContentAI | Powered by GPT-4</div>",
    unsafe_allow_html=True
)