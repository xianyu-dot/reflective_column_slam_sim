import os

# 配置参数
TUNNEL_LENGTH = 200.0  # 隧道长度 200m
TUNNEL_WIDTH = 8.0     # 隧道宽度
WALL_HEIGHT = 4.0      # 墙高
POLE_INTERVAL = 5.0    # 反光柱间隔
POLE_RETRO = 200.0     # 反光强度

# World 文件头
sdf_header = """<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="tunnel_world">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>
"""

# World 文件尾
sdf_footer = """
  </world>
</sdf>
"""

def get_walls_xml():
    # 生成左右两面超长墙壁
    return f"""
    <model name="tunnel_walls">
      <static>true</static>
      <link name="link">
        <!-- 左墙 -->
        <visual name="wall_left_vis">
          <pose>{TUNNEL_LENGTH/2} {TUNNEL_WIDTH/2} {WALL_HEIGHT/2} 0 0 0</pose>
          <geometry><box><size>{TUNNEL_LENGTH} 0.2 {WALL_HEIGHT}</size></box></geometry>
          <material><script><name>Gazebo/Grey</name></script></material>
        </visual>
        <collision name="wall_left_col">
          <pose>{TUNNEL_LENGTH/2} {TUNNEL_WIDTH/2} {WALL_HEIGHT/2} 0 0 0</pose>
          <geometry><box><size>{TUNNEL_LENGTH} 0.2 {WALL_HEIGHT}</size></box></geometry>
        </collision>

        <!-- 右墙 -->
        <visual name="wall_right_vis">
          <pose>{TUNNEL_LENGTH/2} {-TUNNEL_WIDTH/2} {WALL_HEIGHT/2} 0 0 0</pose>
          <geometry><box><size>{TUNNEL_LENGTH} 0.2 {WALL_HEIGHT}</size></box></geometry>
          <material><script><name>Gazebo/Grey</name></script></material>
        </visual>
        <collision name="wall_right_col">
          <pose>{TUNNEL_LENGTH/2} {-TUNNEL_WIDTH/2} {WALL_HEIGHT/2} 0 0 0</pose>
          <geometry><box><size>{TUNNEL_LENGTH} 0.2 {WALL_HEIGHT}</size></box></geometry>
        </collision>
        
        <!-- 天花板 (可选，为了像隧道) -->
        <visual name="ceiling">
          <pose>{TUNNEL_LENGTH/2} 0 {WALL_HEIGHT} 0 0 0</pose>
          <geometry><box><size>{TUNNEL_LENGTH} {TUNNEL_WIDTH} 0.1</size></box></geometry>
          <material><script><name>Gazebo/DarkGrey</name></script></material>
        </visual>
      </link>
    </model>
    """

def get_pole_xml(x, y, index):
    # 生成单个反光柱的 XML
    return f"""
    <model name="ref_pole_{index}">
      <pose>{x} {y} 0.5 0 0 0</pose>
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><cylinder><radius>0.1</radius><length>1.0</length></cylinder></geometry>
          <laser_retro>{POLE_RETRO}</laser_retro>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.1</radius><length>1.0</length></cylinder></geometry>
          <material><script><name>Gazebo/White</name></script></material>
        </visual>
      </link>
    </model>
    """

if __name__ == "__main__":
    content = sdf_header
    content += get_walls_xml()
    
    # 循环生成反光柱
    num_poles = int(TUNNEL_LENGTH / POLE_INTERVAL)
    for i in range(num_poles + 1):
        x_pos = i * POLE_INTERVAL
        # 放在隧道左侧靠墙位置 (y = 宽度/2 - 1米)
        y_pos = (TUNNEL_WIDTH / 2.0) - 1.0 
        content += get_pole_xml(x_pos, y_pos, i)
        
        # 如果想两边都有，取消下面注释
        # content += get_pole_xml(x_pos, -y_pos, i + 1000)

    content += sdf_footer
    
    # 保存文件
    save_path = "../worlds/tunnel.world" # 假设脚本在 scripts 目录
    with open(save_path, "w") as f:
        f.write(content)
    print(f"Generate success: {save_path}")