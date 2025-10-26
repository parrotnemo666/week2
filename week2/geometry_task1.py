import math

class Point:
    """點類：表示二維平面上的一個點"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        """計算到另一個點的距離"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Line:
    """直線類：由兩個點定義的直線"""
    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.slope = self.calculate_slope()
        self.y_intercept = self.calculate_y_intercept()
    
    def calculate_slope(self):
        """計算直線斜率"""
        if self.point1.x == self.point2.x:
            return None  # 垂直線，斜率無窮大
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
    
    def calculate_y_intercept(self):
        """計算y截距"""
        if self.slope is None:
            return None  # 垂直線沒有y截距
        # y = mx + b，所以 b = y - mx
        return self.point1.y - self.slope * self.point1.x
    
    def is_parallel_to(self, other_line):
        """判斷是否與另一條直線平行"""
        # 兩條垂直線是平行的
        if self.slope is None and other_line.slope is None:
            return True
        # 一條垂直線與一條非垂直線不平行
        if self.slope is None or other_line.slope is None:
            return False
        # 斜率相等則平行
        return abs(self.slope - other_line.slope) < 1e-10  # 使用小誤差避免浮點數精度問題
    
    def is_perpendicular_to(self, other_line):
        """判斷是否與另一條直線垂直"""
        # 一條垂直線與一條水平線垂直
        if (self.slope is None and other_line.slope == 0) or (other_line.slope is None and self.slope == 0):
            return True
        # 都不是垂直線的情況
        if self.slope is not None and other_line.slope is not None:
            # 斜率乘積等於-1則垂直
            return abs(self.slope * other_line.slope + 1) < 1e-10
        return False
    
    def __str__(self):
        if self.slope is None:
            return f"Vertical line through x = {self.point1.x}"
        elif self.slope == 0:
            return f"Horizontal line: y = {self.y_intercept}"
        else:
            return f"Line: y = {self.slope:.3f}x + {self.y_intercept:.3f}"

class Circle:
    """圓類：由圓心和半徑定義的圓"""
    
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def area(self):
        """計算圓的面積"""
        return math.pi * self.radius ** 2
    
    def intersects_with(self, other_circle):
        """判斷是否與另一個圓相交"""
        # 計算兩圓心之間的距離
        distance = self.center.distance_to(other_circle.center)
        # 如果距離小於等於兩半徑之和，則相交
        return distance <= (self.radius + other_circle.radius)
    
    def __str__(self):
        return f"Circle with center {self.center} and radius {self.radius}"

class Polygon:
    """多邊形類：由多個頂點定義的多邊形"""
    
    def __init__(self, vertices):
        self.vertices = vertices
    
    def perimeter(self):
        """計算多邊形的周長"""
        if len(self.vertices) < 2:
            return 0
        
        total_perimeter = 0
        # 計算所有相鄰頂點間的距離
        for i in range(len(self.vertices)):
            current_vertex = self.vertices[i]
            next_vertex = self.vertices[(i + 1) % len(self.vertices)]  # 最後一個頂點連回第一個
            total_perimeter += current_vertex.distance_to(next_vertex)
        
        return total_perimeter
    
    def __str__(self):
        vertices_str = ", ".join(str(vertex) for vertex in self.vertices)
        return f"Polygon with vertices: [{vertices_str}]"

def main():
    """主函數：執行所有幾何計算"""
    
    print("=== Task 1: Geometry Calculations ===")
    print()
    
    # 從圖中創建所有點
    print("📍 Creating points from the graph...")
    
    # Line A 的點
    line_a_point1 = Point(2, 4)
    line_a_point2 = Point(-6, 1)
    
    # Line B 的點
    line_b_point1 = Point(2, 2)
    line_b_point2 = Point(-6, -1)
    
    # Line C 的點
    line_c_point1 = Point(-1, 6)
    line_c_point2 = Point(-4, -4)
    
    # 創建直線
    print("📏 Creating lines...")
    line_a = Line(line_a_point1, line_a_point2)
    line_b = Line(line_b_point1, line_b_point2)
    line_c = Line(line_c_point1, line_c_point2)
    
    print(f"Line A: {line_a}")
    print(f"Line B: {line_b}")
    print(f"Line C: {line_c}")
    print()
    
    # 創建圓形
    print("⭕ Creating circles...")
    circle_a = Circle(Point(6, 3), 2)  # 中心(6,3)，半徑2
    circle_b = Circle(Point(8, 1), 1)  # 中心(8,1)，半徑1
    
    print(f"Circle A: {circle_a}")
    print(f"Circle B: {circle_b}")
    print()
    
    # 創建多邊形
    print("🔷 Creating polygon...")
    polygon_vertices = [
        Point(2, 0),   # 底部中心
        Point(5, -1),  # 右上頂點
        Point(4, -4),  # 右下頂點
        Point(1, -2)   # 左下頂點
    ]
    polygon_a = Polygon(polygon_vertices)
    print(f"Polygon A: {polygon_a}")
    print()
    
    # 執行計算並輸出結果
    print("🧮 Performing calculations...")
    print("=" * 50)
    
    # 1. Line A 和 Line B 是否平行？
    parallel_result = line_a.is_parallel_to(line_b)
    print(f"1. Are Line A and Line B parallel? {parallel_result}")
    print(f"   Line A slope: {line_a.slope:.3f}" if line_a.slope is not None else f"   Line A slope: undefined (vertical)")
    print(f"   Line B slope: {line_b.slope:.3f}" if line_b.slope is not None else f"   Line B slope: undefined (vertical)")
    if parallel_result and line_a.slope is not None and line_b.slope is not None:
        print(f"   Both lines have the same slope: {line_a.slope:.3f}")
    print()
    
    # 2. Line C 和 Line A 是否垂直？
    perpendicular_result = line_c.is_perpendicular_to(line_a)
    print(f"2. Are Line C and Line A perpendicular? {perpendicular_result}")
    print(f"   Line C slope: {line_c.slope:.3f}" if line_c.slope is not None else f"   Line C slope: undefined (vertical)")
    print(f"   Line A slope: {line_a.slope:.3f}" if line_a.slope is not None else f"   Line A slope: undefined (vertical)")
    if line_c.slope is not None and line_a.slope is not None:
        print(f"   Slope product: {line_c.slope * line_a.slope:.3f} (should be -1 for perpendicular)")
    print()
    
    # 3. Circle A 的面積
    area_result = circle_a.area()
    print(f"3. Area of Circle A: {area_result:.6f}")
    print(f"   Formula: π × r² = π × {circle_a.radius}² = {area_result:.6f}")
    print()
    
    # 4. Circle A 和 Circle B 是否相交？
    intersect_result = circle_a.intersects_with(circle_b)
    distance_centers = circle_a.center.distance_to(circle_b.center)
    sum_radii = circle_a.radius + circle_b.radius
    print(f"4. Do Circle A and Circle B intersect? {intersect_result}")
    print(f"   Distance between centers: {distance_centers:.3f}")
    print(f"   Sum of radii: {sum_radii}")
    print(f"   Intersect if distance ≤ sum of radii: {distance_centers:.3f} ≤ {sum_radii} = {intersect_result}")
    print()
    
    # 5. Polygon A 的周長
    perimeter_result = polygon_a.perimeter()
    print(f"5. Perimeter of Polygon A: {perimeter_result:.6f}")
    print("   Edge lengths:")
    for i in range(len(polygon_vertices)):
        current = polygon_vertices[i]
        next_vertex = polygon_vertices[(i + 1) % len(polygon_vertices)]
        edge_length = current.distance_to(next_vertex)
        print(f"   {current} to {next_vertex}: {edge_length:.3f}")
    print()
    
    print("=" * 50)
    print("✅ All calculations completed!")

if __name__ == "__main__":
    main()