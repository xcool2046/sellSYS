#!/usr/bin/env python3
"""
客户管理系统 - 主程序（干净版本）
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    try:
        # 设置应用程序属性
        app.setApplicationName("巨炜科技客户管理信息系统")
        app.setApplicationVersion("1.0.0")
        
        # 加载样式表
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            style_path = os.path.join(script_dir, "ui", "resources", "styles.qss")
            
            if os.path.exists(style_path):
                with open(style_path, 'r', encoding='utf-8') as f:
                    app.setStyleSheet(f.read())
                print("✅ 样式表加载成功")
            else:
                print("⚠️ 样式表文件不存在，使用默认样式")
        except Exception as e:
            print(f"⚠️ 样式表加载失败: {e}")
        
        # 创建并显示主窗口
        from ui.main_window_clean import MainWindow
        window = MainWindow()
        window.show()
        
        print("🚀 应用程序启动成功")
        return app.exec()
        
    except Exception as e:
        print(f"❌ 应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
