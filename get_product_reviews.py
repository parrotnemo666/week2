import requests
import json
import time

def get_product_reviews(product_id):
    """取得商品評價資訊"""
    review_url = f"https://ecapi-cdn.pchome.com.tw/fsapi/reviews/{product_id}/comments?type=all&category=new&attachment=&page=1&limit=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": f"https://24h.pchome.com.tw/prod/{product_id}",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://24h.pchome.com.tw",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        review_response = requests.get(review_url, headers=headers, timeout=10)
        review_response.raise_for_status()
        review_data = review_response.json()
        
        avg_rating = review_data.get('AvgLikes', 0)
        total_reviews = review_data.get('TotalRows', 0)
        
        return avg_rating, total_reviews
    except Exception as e:
        print(f"❌ 取得商品 {product_id} 評價失敗：{e}")
        return 0, 0

def scrape_all_products():
    """爬取所有商品資料 - 不預先知道總頁數"""
    keyword = "asus桌機"
    all_products = []
    page = 1
    
    print(f"🚀 開始爬取關鍵字: {keyword}")
    print("🔄 自動偵測總頁數，逐頁爬取所有商品...")
    print("=" * 60)
    
    while True:
        url = f"https://ecshweb.pchome.com.tw/search/v4.3/all/results?q={keyword}&page={page}&sort=sale/dc"
        print(f"🔍 正在爬取第 {page} 頁...")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            products = data.get("Prods", [])
            
            # 如果沒有商品了，停止爬取
            if not products:
                print(f"✅ 第 {page} 頁無商品，爬取完成！")
                break
            
            print(f"📦 第 {page} 頁找到 {len(products)} 個商品")
            
            # 處理每個商品
            for i, product in enumerate(products, 1):
                product_id = product['Id']
                product_name = product['Name']
                product_price = product['Price']
                product_description = product['Describe'].strip()
                
                # 取得評價資訊
                avg_rating, total_reviews = get_product_reviews(product_id)
                
                product_info = {
                    'id': product_id,
                    'name': product_name,
                    'price': product_price,
                    'description': product_description,
                    'avg_rating': avg_rating,
                    'total_reviews': total_reviews
                }
                
                all_products.append(product_info)
                
                print(f"  {len(all_products)}. {product_name}")
                print(f"      ID: {product_id} | 價格: {product_price}元 | 評分: {avg_rating} | 評價數: {total_reviews}")
                
                time.sleep(1)  # 避免請求過頻
            
            page += 1
            time.sleep(3)  # 每頁之間延遲
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 網路錯誤：{e}")
            break
        except json.JSONDecodeError:
            print("❌ JSON解析失敗")
            break
    
    print(f"\n🎉 爬取完成！總共取得 {len(all_products)} 個商品")
    return all_products

def task1_save_product_ids(products):
    """任務 1: 儲存所有商品ID到products.txt，每行一個ID"""
    print("\n" + "="*50)
    print("📋 任務 1: 儲存所有商品ID...")
    
    with open('products.txt', 'w', encoding='utf-8') as f:
        for product in products:
            f.write(f"{product['id']}\n")
    
    print(f"✅ 任務 1 完成！已儲存 {len(products)} 個商品ID到 products.txt")

def task2_save_best_products(products):
    """任務 2: 儲存高評分商品ID到best-products.txt"""
    print("\n" + "="*50)
    print("⭐ 任務 2: 篩選高評分商品...")
    
    best_products = []
    for product in products:
        # 條件：至少1個評價 且 平均評分大於4.9
        if product['total_reviews'] >= 1 and product['avg_rating'] > 4.9:
            best_products.append(product)
    
    with open('best-products.txt', 'w', encoding='utf-8') as f:
        for product in best_products:
            f.write(f"{product['id']}\n")
    
    print(f"✅ 任務 2 完成！找到 {len(best_products)} 個高評分商品")
    print(f"   篩選條件：至少1個評價 且 評分 > 4.9")
    
    if best_products:
        print("   🌟 高評分商品詳情：")
        for i, product in enumerate(best_products, 1):
            print(f"   {i}. {product['name']}")
            print(f"      評分: {product['avg_rating']} | 評價數: {product['total_reviews']} | 價格: {product['price']}元")
    else:
        print("   ❌ 沒有找到符合條件的高評分商品")

def task3_calculate_i5_average_price(products):
    """任務 3: 計算Intel i5 ASUS PC的平均價格"""
    print("\n" + "="*50)
    print("💻 任務 3: 計算Intel i5 ASUS PC平均價格...")
    
    i5_products = []
    
    for product in products:
        # 簡化檢測：只要商品名稱中有 "i5" 就算
        if 'i5' in product['name'].lower():
            i5_products.append(product)
    
    if i5_products:
        total_price = sum(product['price'] for product in i5_products)
        average_price = total_price / len(i5_products)
        
        print(f"✅ 任務 3 完成！")
        print(f"   📊 找到 {len(i5_products)} 台 i5 ASUS PC")
        print(f"   💰 平均價格: {average_price:.2f} 元")
        print(f"   📈 價格範圍: {min(p['price'] for p in i5_products):,} - {max(p['price'] for p in i5_products):,} 元")
        
        print(f"\n   💻 i5 商品清單：")
        for i, product in enumerate(i5_products, 1):
            print(f"   {i}. {product['name']}")
            print(f"      價格: {product['price']:,} 元 | 評分: {product['avg_rating']} | ID: {product['id']}")
    else:
        print("❌ 任務 3: 未找到 i5 ASUS PC")

def main():
    """主函式"""
    print("🤖 PChome ASUS 桌機爬蟲 - 完整三任務版")
    print("="*60)
    print("📝 任務說明：")
    print("   任務 1: 解析所有商品，儲存ID到 products.txt")
    print("   任務 2: 篩選高評分商品(>4.9分且有評價)，儲存到 best-products.txt") 
    print("   任務 3: 計算 i5 ASUS PC 平均價格")
    print("="*60)
    
    # 爬取所有商品資料（自動偵測頁數）
    products = scrape_all_products()
    
    if not products:
        print("❌ 沒有爬取到任何商品資料，請檢查網路連線")
        return
    
    # 執行三個任務
    task1_save_product_ids(products)
    task2_save_best_products(products)
    task3_calculate_i5_average_price(products)
    
    print("\n" + "="*60)
    print("🎉 所有任務完成！")
    print("📂 產生的檔案：")
    print("  📄 products.txt - 所有商品ID (每行一個)")
    print("  🌟 best-products.txt - 高評分商品ID (評分>4.9且至少1個評價)")
    print("="*60)

if __name__ == "__main__":
    main()