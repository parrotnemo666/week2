import math

class Enemy:
    """敵人類別：代表地圖上的敵人單位"""
    
    def __init__(self, name, x, y, dx, dy, life=10):
        """
        初始化敵人
        Args:
            name (str): 敵人名稱 (如 "E1")
            x, y (float): 初始位置座標
            dx, dy (float): 每回合的移動向量
            life (int): 初始生命值，預設為10
        """
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx  # x方向移動量
        self.dy = dy  # y方向移動量
        self.life = life
        self.alive = True  # 是否還活著
    
    def move(self):
        """
        敵人移動：根據移動向量更新位置
        只有活著的敵人才會移動
        """
        if self.alive:
            self.x += self.dx
            self.y += self.dy
    
    def take_damage(self, damage):
        """
        敵人受到傷害
        Args:
            damage (int): 受到的傷害值
        """
        if self.alive:
            self.life -= damage
            # 如果生命值降到0或以下，標記為死亡
            if self.life <= 0:
                self.alive = False
                self.life = 0  # 確保生命值不會是負數
    
    def is_alive(self):
        """檢查敵人是否還活著"""
        return self.alive
    
    def __str__(self):
        """字串表示法，用於輸出結果"""
        return f"{self.name}: 位置({self.x:.1f}, {self.y:.1f}), 生命值: {self.life}"


class Tower:
    """防禦塔類別：代表地圖上的防禦塔"""
    
    def __init__(self, name, x, y, attack_power, attack_range):
        """
        初始化防禦塔
        Args:
            name (str): 防禦塔名稱 (如 "T1", "A1")
            x, y (float): 防禦塔位置座標
            attack_power (int): 攻擊力
            attack_range (int): 攻擊射程
        """
        self.name = name
        self.x = x
        self.y = y
        self.attack_power = attack_power
        self.attack_range = attack_range
    
    def distance_to(self, enemy):
        """
        計算到敵人的歐幾里得距離
        Args:
            enemy (Enemy): 目標敵人
        Returns:
            float: 距離值
        """
        return math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
    
    def can_attack(self, enemy):
        """
        檢查是否可以攻擊指定敵人
        Args:
            enemy (Enemy): 目標敵人
        Returns:
            bool: 如果敵人在射程內且還活著，返回True
        """
        return enemy.is_alive() and self.distance_to(enemy) <= self.attack_range
    
    def attack(self, enemies):
        """
        攻擊射程內的所有敵人
        Args:
            enemies (list): 所有敵人的列表
        Returns:
            list: 被攻擊的敵人名稱列表
        """
        attacked_enemies = []
        for enemy in enemies:
            if self.can_attack(enemy):
                enemy.take_damage(self.attack_power)
                attacked_enemies.append(enemy.name)
        return attacked_enemies


class Game:
    """遊戲主控制類別：管理整個塔防遊戲的運行"""
    
    def __init__(self):
        """初始化遊戲，創建所有敵人和防禦塔"""
        self.current_turn = 0
        self.max_turns = 10
        
        # 創建敵人實例（根據圖片中的座標和移動向量）
        self.enemies = [
            Enemy("E1", -10, 2, 2, -1),    # E1: (-10,2) 移動向量 (2,-1)
            Enemy("E2", -8, 0, 3, 1),     # E2: (-8,0) 移動向量 (3,1)
            Enemy("E3", -9, -1, 3, 0)       # E3: (-9,-1) 移動向量 (3,0)
        ]
        
        # 創建防禦塔實例
        self.towers = [
            # 基本防禦塔（藍色）：攻擊力1，射程2
            Tower("T1", -3, 2, 1, 2),      # T1: (-3,2)
            Tower("T2", -1, -2, 1, 2),     # T2: (-1,-2)
            Tower("T3", 4, 2, 1, 2),       # T3: (4,2)
            Tower("T4", 7, 0, 1, 2),       # T4: (7,0)
            
            # 進階防禦塔（綠色）：攻擊力2，射程4
            Tower("A1", 1, 1, 2, 4),       # A1: (1,1)
            Tower("A2", 4, -3, 2, 4)       # A2: (4,-3)
        ]
    
    def run_turn(self):
        """
        執行一個回合的所有動作
        順序：1.敵人移動 -> 2.防禦塔攻擊 -> 3.顯示回合結果
        """
        self.current_turn += 1
        print(f"\n=== 回合 {self.current_turn} ===")
        
        # 第一階段：所有活著的敵人移動
        print("1. 敵人移動階段：")
        for enemy in self.enemies:
            if enemy.is_alive():
                old_x, old_y = enemy.x, enemy.y
                enemy.move()
                print(f"   {enemy.name}: ({old_x:.1f},{old_y:.1f}) -> ({enemy.x:.1f},{enemy.y:.1f})")
            else:
                print(f"   {enemy.name}: 已死亡，不移動")
        
        # 第二階段：防禦塔攻擊
        print("2. 防禦塔攻擊階段：")
        for tower in self.towers:
            attacked = tower.attack(self.enemies)
            if attacked:
                print(f"   {tower.name} 攻擊: {', '.join(attacked)} (傷害: {tower.attack_power})")
            else:
                print(f"   {tower.name}: 射程內無敵人")
        
        # 第三階段：顯示當前狀態
        print("3. 回合結束狀態：")
        for enemy in self.enemies:
            status = "活著" if enemy.is_alive() else "死亡"
            print(f"   {enemy.name}: 位置({enemy.x:.1f},{enemy.y:.1f}), 生命值:{enemy.life}, 狀態:{status}")
    
    def run_game(self):
        """運行完整的遊戲（10回合）"""
        print("塔防遊戲開始！")
        print("初始狀態：")
        for enemy in self.enemies:
            print(f"  {enemy}")
        
        # 執行10回合
        for _ in range(self.max_turns):
            self.run_turn()
        
        # 遊戲結束，輸出最終結果
        self.print_results()
    
    def print_results(self):
        """輸出遊戲最終結果"""
        print("\n" + "="*50)
        print("遊戲結束！最終結果：")
        print("="*50)
        
        for enemy in self.enemies:
            status = "存活" if enemy.is_alive() else "陣亡"
            print(f"{enemy.name}: 最終位置({enemy.x:.1f}, {enemy.y:.1f}), 剩餘生命值: {enemy.life}, 狀態: {status}")


def main():
    """主函數：創建並運行遊戲"""
    game = Game()
    game.run_game()


# 如果直接執行此檔案，則運行遊戲
if __name__ == "__main__":
    main()