import os
from openai import OpenAI

# Streamlit Cloud secrets'tan ya da local .env'den API key al
# Streamlit Cloud'da st.secrets kullanılıyor, local'de .env
try:
    # Streamlit Cloud için
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # Local için (.env dosyasından)
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_description(product_name, features, word_count=150, tone="profesyonel"):
    """
    AI ile ürün açıklaması oluştur
    
    Args:
        product_name: Ürün adı
        features: Ürün özellikleri
        word_count: Hedef kelime sayısı
        tone: Yazım tonu (profesyonel/samimi/lüks)
    """
    
    # Tone'a göre prompt ayarla
    tone_prompts = {
        "profesyonel": "Profesyonel ve güvenilir bir dil kullan.",
        "samimi": "Samimi, sıcak ve arkadaşça bir dil kullan. 'Sen' dili tercih et.",
        "lüks": "Premium, lüks ve sofistike bir dil kullan. Müşteriye özel hissettir."
    }
    
    prompt = f"""Sen bir e-ticaret içerik yazarısın. Aşağıdaki ürün için Türkçe açıklama yaz.

ÜRÜN: {product_name}
ÖZELLİKLER: {features}

KURALLAR:
- Tam olarak {word_count} kelime civarında yaz
- {tone_prompts.get(tone, tone_prompts["profesyonel"])}
- SEO için doğal şekilde anahtar kelimeler kullan
- Müşteriye faydaları vurgula
- Satın almaya teşvik et
- Sadece açıklamayı yaz, başlık veya ek yorum ekleme

AÇIKLAMA:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ucuz model
            messages=[
                {"role": "system", "content": "Sen profesyonel bir e-ticaret içerik yazarısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"HATA: {str(e)}"


# Test kodu
if __name__ == "__main__":
    print("🤖 AI İçerik Asistanı Test\n")
    print("-" * 50)
    
    # Test 1
    test_product = "Kablosuz Bluetooth Kulaklık"
    test_features = "20 saat batarya ömrü, aktif gürültü önleme (ANC), IPX7 su geçirmez, dokunmatik kontrol, hızlı şarj"
    
    print(f"Ürün: {test_product}")
    print(f"Özellikler: {test_features}\n")
    print("AI yazıyor...\n")
    
    result = generate_description(test_product, test_features, word_count=150, tone="samimi")
    
    print("SONUÇ:")
    print(result)
    print("\n" + "-" * 50)
    print(f"Kelime sayısı: {len(result.split())}")
    
    # Bonus: Farklı tonları da test et
    print("\n" + "=" * 50)
    print("📊 FARKLI TONLARDA TEST:\n")
    
    for test_tone in ["profesyonel", "lüks"]:
        print(f"\n🎨 TON: {test_tone.upper()}")
        print("-" * 50)
        result2 = generate_description(test_product, test_features, word_count=100, tone=test_tone)
        print(result2[:200] + "..." if len(result2) > 200 else result2)