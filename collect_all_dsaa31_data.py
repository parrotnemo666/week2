#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PChome DSAA31 完整數據收集器
- 收集所有頁面的所有產品
- 顯示所有產品詳細資訊
- 保存JSON到當前目錄
"""

import requests
import json
import time
import os
from datetime import datetime

def collect_all_dsaa31_data():
    """收集DSAA31分類的所有產品數據"""
    
    base_url = "https://ecshweb.pchome.com.tw/search/v4.3/all/results"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    }
    
    all_products = []
    all_pages_data = []
    
    print("🚀 開始收集 DSAA31 所有產品數據")
    print("="*60)
    
    page = 1
    while True:
        print(f"📄 爬取第 {page} 頁...", end=" ")
        
        params = {'cateid': 'DSAA31', 'page': page, 'pageCount': 20}
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            products = data.get('Prods', [])
            if not products:
                print("❌ 沒有更多數據")
                break
            
            # 保存這一頁的數據
            all_products.extend(products)
            all_pages_data.append({
                'page': page,
                'count': len(products),
                'data': data
            })
            
            print(f"✅ {len(products)} 個產品 (累計: {len(all_products)})")
            
            # 第一頁顯示總數據
            if page == 1:
                print(f"   📊 API顯示: 總頁數 {data.get('TotalPage')}, 總商品 {data.get('TotalRows')}")
            
            page += 1
            time.sleep(1.5)  # 避免請求過快
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            break
    
    # 組織最終數據
    final_data = {
        'collection_info': {
            'time': datetime.now().isoformat(),
            'category': 'DSAA31',
            'total_products_collected': len(all_products),
            'total_pages_crawled': len(all_pages_data)
        },
        'all_products': all_products,
        'pages_detail': all_pages_data
    }
    
    print(f"\n🎉 數據收集完成！共 {len(all_products)} 個產品")
    return final_data

def save_json_data(data, filename="dsaa31_all_data.json"):
    """保存數據到JSON文件"""
    try:
        # 保存到當前目錄
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        file_size = os.path.getsize(file_path)
        print(f"💾 已保存到: {file_path}")
        print(f"📁 文件大小: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"❌ 保存失敗: {e}")
        return False

def display_all_products(products):
    """顯示所有產品的詳細資訊"""
    total = len(products)
    print(f"\n📋 所有 {total} 個產品詳細資訊:")
    print("="*100)
    
    for i, product in enumerate(products, 1):
        # 處理數據顯示
        id_str = product.get('Id', 'N/A')
        name = product.get('Name', 'N/A')
        price = product.get('Price')
        brand = product.get('Brand', 'N/A')
        rating = product.get('ratingValue')
        review_count = product.get('reviewCount')
        describe = product.get('Describe', 'N/A')
        
        # 格式化顯示
        price_str = f"${price:,}" if price else "無價格"
        rating_str = f"⭐{rating}" if rating else "無評分"
        review_str = f"💬{review_count}" if review_count else "無評論"
        
        print(f"\n🔸 [{i:3d}/{total}] {id_str}")
        print(f"   🏷️  {name}")
        print(f"   💰 {price_str} | 🏢 {brand} | {rating_str} | {review_str}")
        print(f"   📝 {describe[:80]}{'...' if len(describe) > 80 else ''}")
        
        # 每20個產品加個分隔線
        if i % 20 == 0 and i < total:
            print(f"\n{'='*50} 已顯示 {i} 個產品 {'='*50}")

def show_statistics(products):
    """顯示統計資訊"""
    print(f"\n📊 統計分析:")
    print("="*50)
    
    # 價格統計
    prices = [p['Price'] for p in products if p.get('Price')]
    if prices:
        print(f"💰 價格統計:")
        print(f"   • 最低: ${min(prices):,}")
        print(f"   • 最高: ${max(prices):,}")
        print(f"   • 平均: ${sum(prices)/len(prices):,.0f}")
        print(f"   • 有價格商品: {len(prices)}/{len(products)}")
    
    # 品牌統計
    brands = {}
    for p in products:
        brand = p.get('Brand', '未知')
        brands[brand] = brands.get(brand, 0) + 1
    
    print(f"\n🏢 品牌分布:")
    for brand, count in brands.items():
        print(f"   • {brand}: {count} 個")
    
    # 評分統計
    rated = [p for p in products if p.get('ratingValue')]
    if rated:
        ratings = [p['ratingValue'] for p in rated]
        print(f"\n⭐ 評分統計:")
        print(f"   • 有評分商品: {len(rated)}/{len(products)}")
        print(f"   • 平均評分: {sum(ratings)/len(ratings):.2f}")
        print(f"   • 高分商品(≥4.5): {len([r for r in ratings if r >= 4.5])}")

def main():
    """主程序"""
    print("🎯 PChome DSAA31 完整數據收集器")
    print(f"⏰ 執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        # 1. 收集所有數據
        data = collect_all_dsaa31_data()
        
        # 2. 保存JSON文件
        save_json_data(data)
        
        # 3. 顯示所有產品
        display_all_products(data['all_products'])
        
        # 4. 顯示統計
        show_statistics(data['all_products'])
        
        print(f"\n🎉 任務完成！")
        print(f"📁 數據已保存到當前目錄: dsaa31_all_data.json")
        print(f"📊 總共收集了 {len(data['all_products'])} 個產品")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  用戶中斷")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()