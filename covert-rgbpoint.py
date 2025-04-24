import laspy
import open3d as o3d
import numpy as np

# 读取 .las 文件
las = laspy.read("data1/test1_points_1.las")

# 获取点云坐标，垂直方向（按行堆叠）
points = np.vstack((las.x, las.y, las.z)).T # 转置为 (N, 3) 形状

# 获取 RGB 信息并归一化到 [0, 1]，.las 颜色值是 uint16（0~65535）
if all(color in las.point_format.dimension_names for color in ['red', 'green', 'blue']):
    r = las.red / 65535.0
    g = las.green / 65535.0
    b = las.blue / 65535.0
    colors = np.vstack((r, g, b)).T
else:
    colors = np.ones_like(points)  # 默认白色

# 构造 Open3D 点云 dic(pcd):points, colors,normals,has_points(),has_colors(),has_normals()
pcd = o3d.geometry.PointCloud() #创建一个空的点云对象
pcd.points = o3d.utility.Vector3dVector(points) #从numpy转换为C++格式
pcd.colors = o3d.utility.Vector3dVector(colors)

# 保存为 PCD 文件（ASCII 格式便于调试，二进制更高效）
o3d.io.write_point_cloud("output_colored1.pcd", pcd, write_ascii=False)

print("已成功将 .las 转换为含颜色的 .pcd 文件：output_colored.pcd")
