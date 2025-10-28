#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PChome DSAA31 完整數據收集與分析器 - 合併版
功能:
1. 收集所有頁面的所有產品數據
2. 保存JSON到當前目錄
3. 顯示所有產品詳細資訊
4. 執行4個數據分析任務並生成TXT/CSV文件
"""

import requests
import json
import time
import os
import math
import csv
from datetime import datetime

# ===== 數據收集部分 (保持原有邏輯) =====

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

# ===== 數據分析部分 (保持原有邏輯) =====

def load_json_data(filename="dsaa31_all_data.json"):
    """讀取當前目錄下的JSON數據文件"""
    try:
        # 檢查文件是否存在
        if not os.path.exists(filename):
            print(f"❌ 找不到文件: {filename}")
            print(f"   請確保文件在當前目錄: {os.getcwd()}")
            return None
        
        # 讀取JSON文件
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 成功讀取文件: {filename}")
        
        # 檢查數據結構
        if 'all_products' not in data:
            print(f"❌ JSON文件格式錯誤，找不到 'all_products' 欄位")
            return None
        
        products = data['all_products']
        print(f"📊 數據概況: 共 {len(products)} 個產品")
        
        return products
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式錯誤: {e}")
        return None
    except Exception as e:
        print(f"❌ 讀取文件失敗: {e}")
        return None

def task_1_extract_all_ids(products):
    """
    Task 1: 提取所有產品ID並保存到 products.txt
    每行一個產品ID
    """
    print(f"\n🎯 Task 1: 提取所有產品ID")
    print("="*50)
    
    try:
        product_ids = []
        
        # 提取所有產品ID
        for i, product in enumerate(products):
            product_id = product.get('Id')
            if product_id:
                product_ids.append(product_id)
            else:
                print(f"⚠️  產品 {i+1} 缺少ID")
        
        # 寫入文件
        with open('products.txt', 'w', encoding='utf-8') as f:
            for product_id in product_ids:
                f.write(f"{product_id}\n")
        
        print(f"✅ 成功提取 {len(product_ids)} 個產品ID")
        print(f"📁 已保存到: products.txt")
        
        # 顯示前5個ID作為示例
        print(f"\n📋 前5個產品ID:")
        for i, product_id in enumerate(product_ids[:5]):
            print(f"   {i+1}. {product_id}")
        
        if len(product_ids) > 5:
            print(f"   ... 還有 {len(product_ids)-5} 個")
        
        return product_ids
        
    except Exception as e:
        print(f"❌ Task 1 執行失敗: {e}")
        return []

def task_2_find_best_products(products):
    """
    Task 2: 找出評分>4.9且至少有1個評論的產品
    保存產品ID到 best-products.txt
    """
    print(f"\n🎯 Task 2: 找出高評分且有評論的產品")
    print("="*50)
    
    try:
        best_products = []
        
        # 分析所有產品
        total_with_rating = 0
        total_with_reviews = 0
        
        for product in products:
            product_id = product.get('Id')
            rating = product.get('ratingValue')
            review_count = product.get('reviewCount')
            name = product.get('Name', 'N/A')[:50] + "..."
            
            # 統計有評分和評論的產品
            if rating is not None:
                total_with_rating += 1
            if review_count is not None and review_count > 0:
                total_with_reviews += 1
            
            # 檢查是否符合條件
            if (rating is not None and 
                review_count is not None and 
                rating > 4.9 and 
                review_count >= 1):
                
                best_products.append({
                    'id': product_id,
                    'name': name,
                    'rating': rating,
                    'reviews': review_count
                })
                
                print(f"✨ 找到符合條件產品: {product_id}")
                print(f"   📝 {name}")
                print(f"   ⭐ 評分: {rating}, 💬 評論數: {review_count}")
        
        # 寫入文件
        with open('best-products.txt', 'w', encoding='utf-8') as f:
            for product in best_products:
                f.write(f"{product['id']}\n")
        
        # 統計結果
        print(f"\n📊 篩選結果:")
        print(f"   • 總產品數: {len(products)}")
        print(f"   • 有評分產品: {total_with_rating}")
        print(f"   • 有評論產品: {total_with_reviews}")
        print(f"   • 符合條件產品: {len(best_products)} (評分>4.9且有評論)")
        
        print(f"\n✅ 高評分產品ID已保存到: best-products.txt")
        
        # 顯示所有符合條件的產品
        if best_products:
            print(f"\n🌟 所有符合條件的產品:")
            for i, product in enumerate(best_products, 1):
                print(f"   {i}. {product['id']} (⭐{product['rating']}, 💬{product['reviews']})")
        else:
            print(f"\n⚠️  沒有找到符合條件的產品")
        
        return [p['id'] for p in best_products]
        
    except Exception as e:
        print(f"❌ Task 2 執行失敗: {e}")
        return []

def task_3_calculate_i5_average_price(products):
    """
    Task 3: 計算 ASUS i5 處理器 PC 的平均價格
    直接在控制台打印結果
    """
    print(f"\n🎯 Task 3: 計算 ASUS i5 處理器 PC 平均價格")
    print("="*50)
    
    try:
        i5_products = []
        all_processors = {'i3': 0, 'i5': 0, 'i7': 0, 'i9': 0, 'other': 0}
        
        # 分析所有產品
        for product in products:
            brand = product.get('Brand', '').lower()
            name = product.get('Name', '').lower()
            price = product.get('Price')
            
            # 確保是 ASUS 品牌
            if 'asus' in brand or '華碩' in product.get('Brand', ''):
                # 統計處理器類型
                if 'i3' in name:
                    all_processors['i3'] += 1
                elif 'i5' in name:
                    all_processors['i5'] += 1
                elif 'i7' in name:
                    all_processors['i7'] += 1
                elif 'i9' in name:
                    all_processors['i9'] += 1
                else:
                    all_processors['other'] += 1
                
                # 找到 i5 產品
                if 'i5' in name and price is not None:
                    i5_products.append({
                        'id': product.get('Id'),
                        'name': product.get('Name'),
                        'price': price
                    })
                    print(f"🔍 找到 i5 產品: {product.get('Name')[:60]}...")
                    print(f"   💰 價格: ${price:,}")
        
        # 顯示處理器分布
        print(f"\n📊 ASUS 產品處理器分布:")
        for processor, count in all_processors.items():
            if count > 0:
                print(f"   • {processor.upper()}: {count} 個產品")
        
        # 計算 i5 平均價格
        if i5_products:
            prices = [p['price'] for p in i5_products]
            average_price = sum(prices) / len(prices)
            
            print(f"\n💰 ASUS i5 處理器 PC 分析結果:")
            print(f"   • 找到 i5 產品數量: {len(i5_products)}")
            print(f"   • 價格範圍: ${min(prices):,} - ${max(prices):,}")
            print(f"   • 平均價格: ${average_price:,.2f}")
            
            # 顯示所有 i5 產品
            print(f"\n📋 所有 i5 產品清單:")
            for i, product in enumerate(i5_products, 1):
                print(f"   {i}. {product['id']} - ${product['price']:,}")
                print(f"      {product['name'][:70]}...")
            
            return average_price
        else:
            print(f"\n❌ 沒有找到 ASUS i5 處理器 PC")
            print(f"💡 建議檢查其他處理器類型的產品")
            return None
            
    except Exception as e:
        print(f"❌ Task 3 執行失敗: {e}")
        return None

def task_4_calculate_price_zscore(products):
    """
    Task 4: 使用 z-score 標準化 ASUS PC 價格
    將解析的數據作為統計母體
    """
    print(f"\n🎯 Task 4: ASUS PC 價格 z-score 標準化")
    print("="*50)
    
    try:
        # 找出所有 ASUS 產品且有價格的
        asus_products = []
        
        for product in products:
            brand = product.get('Brand', '').lower()
            price = product.get('Price')
            
            # 確保是 ASUS 品牌且有價格
            if ('asus' in brand or '華碩' in product.get('Brand', '')) and price is not None:
                asus_products.append({
                    'id': product.get('Id'),
                    'name': product.get('Name'),
                    'price': price
                })
        
        print(f"🔍 找到 {len(asus_products)} 個 ASUS 產品")
        
        if len(asus_products) < 2:
            print(f"❌ ASUS 產品數量不足，無法進行 z-score 標準化")
            return None
        
        # 計算統計數據 (作為母體)
        prices = [p['price'] for p in asus_products]
        n = len(prices)
        mean_price = sum(prices) / n
        
        # 計算母體標準差 (除以 N，不是 N-1)
        variance = sum((price - mean_price) ** 2 for price in prices) / n
        std_price = math.sqrt(variance)
        
        print(f"📈 統計數據 (母體):")
        print(f"   • 產品總數: {n}")
        print(f"   • 價格範圍: ${min(prices):,} - ${max(prices):,}")
        print(f"   • 母體平均數 (μ): ${mean_price:,.2f}")
        print(f"   • 母體標準差 (σ): ${std_price:,.2f}")
        
        # 計算每個產品的 z-score
        print(f"\n🔢 z-score 標準化結果:")
        print("="*80)
        print(f"{'產品ID':<20} {'價格':<12} {'z-score':<10} {'分類'}")
        print("="*80)
        
        z_scores = []
        categories = {'極低價': 0, '低價': 0, '正常': 0, '高價': 0, '極高價': 0}
        
        for product in asus_products:
            price = product['price']
            z_score = (price - mean_price) / std_price
            z_scores.append(z_score)
            
            # 分類標籤
            if z_score > 2:
                category = "💰 極高價"
                categories['極高價'] += 1
            elif z_score > 1:
                category = "📈 高價"
                categories['高價'] += 1
            elif z_score < -2:
                category = "💸 極低價"
                categories['極低價'] += 1
            elif z_score < -1:
                category = "📉 低價"
                categories['低價'] += 1
            else:
                category = "💡 正常"
                categories['正常'] += 1
            
            # 顯示結果
            product_id = product['id'][:18]
            print(f"{product_id:<20} ${price:<11,} {z_score:<9.3f} {category}")
        
        print("="*80)
        
        # 顯示分布統計
        print(f"\n📊 z-score 分布統計:")
        print(f"   • 極高價 (z > 2):   {categories['極高價']:3d} 個 ({categories['極高價']/n*100:.1f}%)")
        print(f"   • 高價 (1 < z ≤ 2):  {categories['高價']:3d} 個 ({categories['高價']/n*100:.1f}%)")
        print(f"   • 正常 (-1 ≤ z ≤ 1): {categories['正常']:3d} 個 ({categories['正常']/n*100:.1f}%)")
        print(f"   • 低價 (-2 ≤ z < -1): {categories['低價']:3d} 個 ({categories['低價']/n*100:.1f}%)")
        print(f"   • 極低價 (z < -2):   {categories['極低價']:3d} 個 ({categories['極低價']/n*100:.1f}%)")
        
        # 找出異常值
        extreme_high = [p for p, z in zip(asus_products, z_scores) if z > 2]
        extreme_low = [p for p, z in zip(asus_products, z_scores) if z < -2]
        
        if extreme_high:
            print(f"\n🔥 價格異常高的產品 (z > 2):")
            for product in extreme_high:
                print(f"   • {product['name'][:60]}... - ${product['price']:,}")
        
        if extreme_low:
            print(f"\n❄️  價格異常低的產品 (z < -2):")
            for product in extreme_low:
                print(f"   • {product['name'][:60]}... - ${product['price']:,}")
        
        # 生成 standardization.csv 文件
        print(f"\n💾 生成 standardization.csv 文件...")
        csv_data = []
        
        for i, product in enumerate(asus_products):
            price = product['price']
            z_score = z_scores[i]
            
            # 分類標籤 (去掉emoji)
            if z_score > 2:
                category = "極高價"
            elif z_score > 1:
                category = "高價"
            elif z_score < -2:
                category = "極低價"
            elif z_score < -1:
                category = "低價"
            else:
                category = "正常"
            
            csv_data.append({
                'Product_ID': product['id'],
                'Product_Name': product['name'],
                'Price': price,
                'Z_Score': round(z_score, 4),
                'Category': category
            })
        
        # 寫入CSV文件
        try:
            with open('standardization.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Product_ID', 'Product_Name', 'Price', 'Z_Score', 'Category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # 寫入標題行
                writer.writeheader()
                
                # 寫入數據
                for row in csv_data:
                    writer.writerow(row)
            
            print(f"✅ 成功生成 standardization.csv")
            print(f"📊 包含 {len(csv_data)} 行數據")
            
            # 顯示前5行作為預覽
            print(f"\n📋 CSV文件預覽 (前5行):")
            print(f"{'Product_ID':<20} {'Price':<12} {'Z_Score':<10} {'Category':<10}")
            print("-" * 60)
            for i, row in enumerate(csv_data[:5]):
                print(f"{row['Product_ID']:<20} ${row['Price']:<11,} {row['Z_Score']:<9} {row['Category']:<10}")
            
            if len(csv_data) > 5:
                print(f"... 還有 {len(csv_data)-5} 行數據")
                
        except Exception as e:
            print(f"❌ 生成 CSV 文件失敗: {e}")
        
        return {
            'mean': mean_price,
            'std': std_price,
            'z_scores': z_scores,
            'categories': categories,
            'csv_data': csv_data
        }
        
    except Exception as e:
        print(f"❌ Task 4 執行失敗: {e}")
        return None

def verify_output_files():
    """驗證輸出文件是否正確生成"""
    print(f"\n🔍 驗證輸出文件:")
    print("="*30)
    
    # 檢查 products.txt
    if os.path.exists('products.txt'):
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"✅ products.txt: {len(lines)} 行")
        
        # 顯示前3行
        print("   前3行內容:")
        for i, line in enumerate(lines[:3]):
            print(f"     {i+1}. {line.strip()}")
    else:
        print(f"❌ products.txt 不存在")
    
    # 檢查 best-products.txt
    if os.path.exists('best-products.txt'):
        with open('best-products.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"✅ best-products.txt: {len(lines)} 行")
        
        # 顯示所有內容（通常不會太多）
        if lines:
            print("   所有內容:")
            for i, line in enumerate(lines):
                print(f"     {i+1}. {line.strip()}")
        else:
            print("   (空文件)")
    else:
        print(f"❌ best-products.txt 不存在")
    
    # 檢查 standardization.csv
    if os.path.exists('standardization.csv'):
        with open('standardization.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"✅ standardization.csv: {len(lines)} 行 (含標題)")
        
        # 顯示標題和前2行數據
        if len(lines) > 0:
            print("   標題行:")
            print(f"     {lines[0].strip()}")
            
            if len(lines) > 1:
                print("   前2行數據:")
                for i, line in enumerate(lines[1:3], 1):
                    print(f"     {i}. {line.strip()}")
    else:
        print(f"❌ standardization.csv 不存在")

# ===== 主程序 =====

def main():
    """主程序 - 合併數據收集與分析功能"""
    print("🎯 PChome DSAA31 完整數據收集與分析器")
    print(f"⏰ 執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 當前目錄: {os.getcwd()}")
    print("="*60)
    
    try:
        # ===== 第一部分：數據收集 =====
        print("\n🚀 階段 1: 數據收集")
        print("="*40)
        
        # 1. 收集所有數據
        data = collect_all_dsaa31_data()
        
        # 2. 保存JSON文件
        save_json_data(data)
        
        # 3. 顯示所有產品
        display_all_products(data['all_products'])
        
        # 4. 顯示統計
        show_statistics(data['all_products'])
        
        print(f"\n✅ 數據收集階段完成！")
        print(f"📁 數據已保存到: dsaa31_all_data.json")
        print(f"📊 總共收集了 {len(data['all_products'])} 個產品")
        
        # ===== 第二部分：數據分析 =====
        print(f"\n\n🔬 階段 2: 數據分析")
        print("="*40)
        
        # 使用剛剛收集的數據進行分析
        products = data['all_products']
        
        # 執行 Task 1
        task_1_ids = task_1_extract_all_ids(products)
        
        # 執行 Task 2
        task_2_ids = task_2_find_best_products(products)
        
        # 執行 Task 3
        i5_average_price = task_3_calculate_i5_average_price(products)
        
        # 執行 Task 4
        zscore_result = task_4_calculate_price_zscore(products)
        
        # 驗證輸出文件
        verify_output_files()
        
        # ===== 最終總結 =====
        print(f"\n🎉 所有任務完成！")
        print("="*60)
        print(f"📁 生成的文件:")
        print(f"   • dsaa31_all_data.json - 完整的產品數據 ({len(data['all_products'])} 個產品)")
        print(f"   • products.txt - 所有 {len(task_1_ids)} 個產品ID")
        print(f"   • best-products.txt - {len(task_2_ids)} 個高評分產品ID")
        print(f"   • standardization.csv - ASUS PC價格z-score標準化數據")
        print(f"\n📊 分析結果:")
        if i5_average_price:
            print(f"   • Task 3: ASUS i5 平均價格 = ${i5_average_price:,.2f}")
        else:
            print(f"   • Task 3: 未找到 ASUS i5 產品")
        if zscore_result:
            asus_count = len([p for p in products if 'asus' in p.get('Brand', '').lower() or '華碩' in p.get('Brand', '')])
            print(f"   • Task 4: 已完成 {asus_count} 個ASUS產品的 z-score 標準化")
        
        print(f"\n🏆 完整流程執行成功！")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  用戶中斷")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()