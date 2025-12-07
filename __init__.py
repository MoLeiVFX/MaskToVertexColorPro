bl_info = {
    "name": "Mask To Vertex Color Pro",
    "author": "墨泪",
    "version": (2, 0, 4),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > M2VC Pro",
    "description": "将遮罩贴图（黑白或透明）转换为顶点色的Alpha通道 - 专业版",
    "category": "Object",
    "doc_url": "https://www.kiiiii.com",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy
import os
import math
import sys
from bpy_extras.io_utils import ImportHelper
from bpy.props import (StringProperty, BoolProperty, FloatProperty,
                      EnumProperty, IntProperty, PointerProperty,
                      CollectionProperty)
from bpy.types import Panel, Operator, PropertyGroup, UIList

# ============================================
# 辅助函数：获取版本信息
# ============================================

def get_addon_version():
    """获取插件版本号，兼容不同模块加载方式"""
    # 直接使用 globals() 访问模块级变量
    try:
        if 'bl_info' in globals():
            return globals()['bl_info']['version']
    except:
        pass
    # 如果失败，返回默认值
    return (2, 0, 4)

# ============================================
# 国际化翻译系统（Blender的翻译到4.0版本开始就不对劲，搞不懂，干脆直接4.0+版本不支持繁体中文算了！）
# ============================================

# 翻译字典
translations_dict = {
    "en_US": {
        # 属性名称和描述
        ("*", "对象"): "Object",
        ("*", "启用"): "Enable",
        ("*", "是否处理此对象"): "Whether to process this object",
        ("*", "UV层"): "UV Layer",
        ("*", "使用的UV层名称"): "Name of the UV layer to use",
        ("*", "顶点色名称"): "Vertex Color Name",
        ("*", "顶点色层的名称"): "Name of the vertex color layer",
        ("*", "顶点颜色属性名:"): "Vertex Color Attribute Name:",
        ("*", "状态"): "Status",
        ("*", "处理状态"): "Processing status",
        ("*", "图像文件"): "Image File",
        ("*", "用于遮罩转换的图像文件路径"): "Image file path for mask conversion",
        ("*", "遮罩源"): "Mask Source",
        ("*", "选择遮罩信息的来源"): "Select the source of mask information",
        ("*", "混合模式"): "Blend Mode",
        ("*", "遮罩与现有顶点色的混合模式"): "Blending mode between mask and existing vertex colors",
        ("*", "混合强度"): "Blend Factor",
        ("*", "混合效果的强度"): "Strength of the blending effect",
        ("*", "UV包裹"): "UV Wrap",
        ("*", "将UV坐标包裹在0-1范围内（处理超出范围的UV）"): "Wrap UV coordinates within 0-1 range (handles out-of-range UVs)",
        ("*", "UV限制"): "UV Clamp",
        ("*", "将UV坐标限制在0-1范围内（不包裹）"): "Clamp UV coordinates within 0-1 range (no wrapping)",
        ("*", "垂直翻转"): "Flip Vertical",
        ("*", "修复图像上下颠倒的问题"): "Fix upside-down image issues",
        ("*", "水平翻转"): "Flip Horizontal",
        ("*", "修复图像左右颠倒的问题"): "Fix left-right reversed image issues",
        ("*", "调试模式"): "Debug Mode",
        ("*", "显示详细处理信息"): "Show detailed processing information",
        ("*", "单对象处理时创建的顶点色层的名称"): "Vertex color name for single object processing",
        
        # 枚举项
        ("*", "自动检测"): "Auto Detect",
        ("*", "自动检测最佳遮罩源"): "Automatically detect the best mask source",
        ("*", "Alpha通道"): "Alpha Channel",
        ("*", "使用图像的Alpha通道作为遮罩"): "Use image alpha channel as mask",
        ("*", "灰度值"): "Grayscale",
        ("*", "将RGB转换为灰度作为遮罩"): "Convert RGB to grayscale as mask",
        ("*", "红色通道"): "Red Channel",
        ("*", "使用红色通道作为遮罩"): "Use red channel as mask",
        ("*", "绿色通道"): "Green Channel",
        ("*", "使用绿色通道作为遮罩"): "Use green channel as mask",
        ("*", "蓝色通道"): "Blue Channel",
        ("*", "使用蓝色通道作为遮罩"): "Use blue channel as mask",
        ("*", "亮度"): "Luminance",
        ("*", "使用亮度作为遮罩"): "Use luminance as mask",
        ("*", "替换"): "Replace",
        ("*", "替换现有Alpha值"): "Replace existing alpha values",
        ("*", "相乘"): "Multiply",
        ("*", "与现有Alpha值相乘"): "Multiply with existing alpha values",
        ("*", "相加"): "Add",
        ("*", "与现有Alpha值相加"): "Add to existing alpha values",
        ("*", "相减"): "Subtract",
        ("*", "从现有Alpha值中减去"): "Subtract from existing alpha values",
        ("*", "最小值"): "Min",
        ("*", "取最小值"): "Take minimum value",
        ("*", "最大值"): "Max",
        ("*", "取最大值"): "Take maximum value",
        ("*", "叠加"): "Overlay",
        ("*", "叠加模式"): "Overlay mode",
        ("*", "滤色"): "Screen",
        ("*", "滤色模式"): "Screen mode",
        
        # 操作符（同时添加 "*" 和 "Operator" context，）
        ("Operator", "选择图像文件"): "Select Image File",
        ("*", "选择图像文件"): "Select Image File",  # 兼容性
        ("Operator", "选择用于遮罩转换的图像文件"): "Select image file for mask conversion",
        ("*", "选择用于遮罩转换的图像文件"): "Select image file for mask conversion",  # 兼容性
        ("Operator", "应用遮罩到顶点色"): "Apply Mask to Vertex Color",
        ("*", "应用遮罩到顶点色"): "Apply Mask to Vertex Color",  # 兼容性
        ("Operator", "将共享设置中的图像应用到当前选中模型的顶点色Alpha通道"): "Apply the shared image to the currently selected model's vertex color alpha channel",
        ("*", "将共享设置中的图像应用到当前选中模型的顶点色Alpha通道"): "Apply the shared image to the currently selected model's vertex color alpha channel",  # 兼容性
        ("Operator", "添加选中对象"): "Add Selected Objects",
        ("*", "添加选中对象"): "Add Selected Objects",  # 兼容性
        ("Operator", "将选中的对象添加到批量处理列表"): "Add selected objects to batch processing list",
        ("*", "将选中的对象添加到批量处理列表"): "Add selected objects to batch processing list",  # 兼容性
        ("Operator", "移除选中"): "Remove Selected",
        ("*", "移除选中"): "Remove Selected",  # 兼容性
        ("Operator", "从批量处理列表中移除选中的对象"): "Remove selected object from batch processing list",
        ("*", "从批量处理列表中移除选中的对象"): "Remove selected object from batch processing list",  # 兼容性
        ("Operator", "移除启用项"): "Remove Enabled Items",
        ("*", "移除启用项"): "Remove Enabled Items",  # 兼容性
        ("Operator", "从批量处理列表中移除所有启用的对象"): "Remove all enabled objects from batch processing list",
        ("*", "从批量处理列表中移除所有启用的对象"): "Remove all enabled objects from batch processing list",  # 兼容性
        ("Operator", "清空列表"): "Clear All",
        ("*", "清空列表"): "Clear All",  # 兼容性
        ("Operator", "清空批量处理列表中的所有对象"): "Clear all objects from batch processing list",
        ("*", "清空批量处理列表中的所有对象"): "Clear all objects from batch processing list",  # 兼容性
        ("Operator", "全部启用"): "Enable All",
        ("*", "全部启用"): "Enable All",  # 兼容性
        ("Operator", "启用列表中的所有对象"): "Enable all objects in the list",
        ("*", "启用列表中的所有对象"): "Enable all objects in the list",  # 兼容性
        ("Operator", "全部禁用"): "Disable All",
        ("*", "全部禁用"): "Disable All",  # 兼容性
        ("Operator", "禁用列表中的所有对象"): "Disable all objects in the list",
        ("*", "禁用列表中的所有对象"): "Disable all objects in the list",  # 兼容性
        ("Operator", "批量应用遮罩"): "Batch Apply Mask",
        ("*", "批量应用遮罩"): "Batch Apply Mask",  # 兼容性
        ("Operator", "批量将遮罩应用到多个对象的顶点色"): "Batch apply mask to multiple objects' vertex colors",
        ("*", "批量将遮罩应用到多个对象的顶点色"): "Batch apply mask to multiple objects' vertex colors",  # 兼容性
        ("Operator", "修复UV坐标"): "Fix UV Coordinates",
        ("*", "修复UV坐标"): "Fix UV Coordinates",  # 兼容性
        ("Operator", "修复UV坐标中的NaN和无效值"): "Fix NaN and invalid values in UV coordinates",
        ("*", "修复UV坐标中的NaN和无效值"): "Fix NaN and invalid values in UV coordinates",  # 兼容性
        ("Operator", "验证模型"): "Validate Model",
        ("*", "验证模型"): "Validate Model",  # 兼容性
        ("Operator", "检查模型是否适合应用遮罩"): "Check if the model is suitable for applying masks",
        ("*", "检查模型是否适合应用遮罩"): "Check if the model is suitable for applying masks",  # 兼容性
        
        # UI文本
        ("*", "遮罩转顶点色 Pro"): "Mask to Vertex Color Pro",
        ("*", "图像文件:"): "Image file:",
        ("*", "未选择图像"): "No image selected",
        ("*", "选择图像"): "Select Image",
        ("*", "更换图像"): "Change Image",
        ("*", "处理设置:"): "Processing Settings:",
        ("*", "单对象处理:"): "Single Object Processing:",
        ("*", "应用到当前选中对象"): "Apply to Currently Selected Object",
        ("*", "注意: 仅处理当前选中的一个对象"): "Note: Only processes the currently selected single object",
        ("*", "请先选择图像文件"): "Please select an image file first",
        ("*", "批量处理:"): "Batch Processing:",
        ("*", "批量应用到 {} 个对象"): "Batch apply to {} objects",
        ("*", "注意: 将处理列表中所有启用的对象 ({}个)"): "Note: Will process all enabled objects in the list ({} objects)",
        ("*", "请在列表中启用至少一个对象"): "Please enable at least one object in the list",
        ("*", "批量列表为空"): "Batch list is empty",
        ("*", "添加选中对象到列表"): "Add Selected Objects to List",
        ("*", "使用方法:"): "Usage:",
        ("*", "1. 在3D视图中选择多个对象"): "1. Select multiple objects in 3D viewport",
        ("*", "2. 点击'添加选中对象到列表'"): "2. Click 'Add Selected Objects to List'",
        ("*", "3. 在列表中勾选要处理的对象"): "3. Check the objects to process in the list",
        ("*", "4. 点击'批量应用到X个对象'"): "4. Click 'Batch apply to X objects'",
        ("*", "工具:"): "Tools:",
        ("*", "修复UV坐标"): "Fix UV Coordinates",
        ("*", "验证模型"): "Validate Model",
        ("*", "工作流程:"): "Workflow:",
        ("*", "1. 选择图像文件"): "1. Select image file",
        ("*", "2. 配置处理设置"): "2. Configure processing settings",
        ("*", "3. 快速处理单个对象（上）"): "3. Quick process single object (above)",
        ("*", "4. 批量处理多个对象（下）"): "4. Batch process multiple objects (below)",
        ("*", "✓ 所有操作共享同一图像和设置"): "✓ All operations share the same image and settings",
        ("*", "✓ 先处理单个测试效果，再批量应用"): "✓ Process single object first to test, then batch apply",
        ("*", "版本信息:"): "Version Info:",
        ("*", "插件版本: v{}.{}"): "Add-on Version: v{}.{}",
        ("*", "优化: 调整UI布局顺序"): "Optimization: Adjusted UI layout order",
        ("*", "作者: 墨泪"): "Author: 墨泪",
        ("*", "主页: https://www.kiiiii.com"): "Homepage: https://www.kiiiii.com",
        
        # 状态文本
        ("*", "等待"): "Waiting",
        ("*", "处理中"): "Processing",
        ("*", "完成"): "Complete",
        ("*", "错误"): "Error",
        ("*", "无效对象"): "Invalid Object",
        
        # 消息
        ("*", "遮罩已应用到 {}"): "Mask applied to {}",
        ("*", "处理 {} 失败"): "Failed to process {}",
        ("*", "请先选择一个网格对象！"): "Please select a mesh object first!",
        ("*", "请先选择图像文件！"): "Please select an image file first!",
        ("*", "图像文件不存在: {}"): "Image file does not exist: {}",
        ("*", "无法加载图像: {}"): "Unable to load image: {}",
        ("*", "添加了 {} 个对象"): "Added {} objects",
        ("*", "没有可添加的网格对象"): "No mesh objects available to add",
        ("*", "列表为空"): "List is empty",
        ("*", "没有选中的对象"): "No object selected",
        ("*", "移除了: {}"): "Removed: {}",
        ("*", "移除了 {} 个启用的对象"): "Removed {} enabled objects",
        ("*", "清空了 {} 个对象"): "Cleared {} objects",
        ("*", "启用了 {} 个对象"): "Enabled {} objects",
        ("*", "所有对象都已启用"): "All objects are already enabled",
        ("*", "禁用了 {} 个对象"): "Disabled {} objects",
        ("*", "所有对象都已禁用"): "All objects are already disabled",
        ("*", "批量处理完成: {}成功, {}失败"): "Batch processing complete: {} success, {} failed",
        ("*", "批量处理列表中没有启用的对象！"): "No enabled objects in batch processing list!",
        ("*", "修复了 {} 个UV坐标"): "Fixed {} UV coordinates",
        ("*", "未发现需要修复的UV坐标"): "No UV coordinates need fixing",
        ("*", "{}: 不是网格对象"): "{}: Not a mesh object",
        ("*", "{}: 没有UV坐标"): "{}: No UV coordinates",
        ("*", "{}: {}个UV层"): "{}: {} UV layers",
        ("*", "{}.{}: {}个无效UV"): "{}.{}: {} invalid UVs",
        ("*", "{}: 没有顶点色层"): "{}: No vertex color layers",
        ("*", "{}: {}个顶点色层"): "{}: {} vertex color layers",
        ("*", "{}: {}个多边形"): "{}: {} polygons",
        ("*", "{}: {}个顶点"): "{}: {} vertices",
        ("*", "未知对象"): "Unknown Object",
        ("*", "UV修复:{}"): "UV Fixed:{}",
        ("*", "创建的顶点色层的名称"): "Name of the vertex color layer to create",
        ("*", "已选择图像: {}"): "Selected image: {}",
    },
    "zh_CN": {
        # 简体中文（保持原样）
    },
    "zh_TW": {
        # 繁体中文翻译
        ("*", "对象"): "物件",
        ("*", "启用"): "啟用",
        ("*", "是否处理此对象"): "是否處理此物件",
        ("*", "UV层"): "UV圖層",
        ("*", "使用的UV层名称"): "使用的UV圖層名稱",
        ("*", "顶点色名称"): "頂點色名稱",
        ("*", "顶点色层的名称"): "頂點色圖層的名稱",
        ("*", "顶点颜色属性名:"): "頂點顏色屬性名稱:",
        ("*", "状态"): "狀態",
        ("*", "处理状态"): "處理狀態",
        ("*", "图像文件"): "圖像檔案",
        ("*", "用于遮罩转换的图像文件路径"): "用於遮罩轉換的圖像檔案路徑",
        ("*", "遮罩源"): "遮罩來源",
        ("*", "选择遮罩信息的来源"): "選擇遮罩資訊的來源",
        ("*", "混合模式"): "混合模式",
        ("*", "遮罩与现有顶点色的混合模式"): "遮罩與現有頂點色的混合模式",
        ("*", "混合强度"): "混合強度",
        ("*", "混合效果的强度"): "混合效果的強度",
        ("*", "UV包裹"): "UV包裹",
        ("*", "将UV坐标包裹在0-1范围内（处理超出范围的UV）"): "將UV座標包裹在0-1範圍內（處理超出範圍的UV）",
        ("*", "UV限制"): "UV限制",
        ("*", "将UV坐标限制在0-1范围内（不包裹）"): "將UV座標限制在0-1範圍內（不包裹）",
        ("*", "垂直翻转"): "垂直翻轉",
        ("*", "修复图像上下颠倒的问题"): "修復圖像上下顛倒的問題",
        ("*", "水平翻转"): "水平翻轉",
        ("*", "修复图像左右颠倒的问题"): "修復圖像左右顛倒的問題",
        ("*", "调试模式"): "除錯模式",
        ("*", "显示详细处理信息"): "顯示詳細處理資訊",
        ("*", "单对象处理时创建的顶点色层的名称"): "單物件處理時建立的頂點色圖層的名稱",
        
        # 枚举项
        ("*", "自动检测"): "自動偵測",
        ("*", "自动检测最佳遮罩源"): "自動偵測最佳遮罩來源",
        ("*", "Alpha通道"): "Alpha通道",
        ("*", "使用图像的Alpha通道作为遮罩"): "使用圖像的Alpha通道作為遮罩",
        ("*", "灰度值"): "灰階值",
        ("*", "将RGB转换为灰度作为遮罩"): "將RGB轉換為灰階作為遮罩",
        ("*", "红色通道"): "紅色通道",
        ("*", "使用红色通道作为遮罩"): "使用紅色通道作為遮罩",
        ("*", "绿色通道"): "綠色通道",
        ("*", "使用绿色通道作为遮罩"): "使用綠色通道作為遮罩",
        ("*", "蓝色通道"): "藍色通道",
        ("*", "使用蓝色通道作为遮罩"): "使用藍色通道作為遮罩",
        ("*", "亮度"): "亮度",
        ("*", "使用亮度作为遮罩"): "使用亮度作為遮罩",
        ("*", "替换"): "替換",
        ("*", "替换现有Alpha值"): "替換現有Alpha值",
        ("*", "相乘"): "相乘",
        ("*", "与现有Alpha值相乘"): "與現有Alpha值相乘",
        ("*", "相加"): "相加",
        ("*", "与现有Alpha值相加"): "與現有Alpha值相加",
        ("*", "相减"): "相減",
        ("*", "从现有Alpha值中减去"): "從現有Alpha值中減去",
        ("*", "最小值"): "最小值",
        ("*", "取最小值"): "取最小值",
        ("*", "最大值"): "最大值",
        ("*", "取最大值"): "取最大值",
        ("*", "叠加"): "疊加",
        ("*", "叠加模式"): "疊加模式",
        ("*", "滤色"): "濾色",
        ("*", "滤色模式"): "濾色模式",
        
        # 操作符（同时添加 "*" 和 "Operator" context，）
        ("Operator", "选择图像文件"): "選擇圖像檔案",
        ("*", "选择图像文件"): "選擇圖像檔案",  # 兼容性
        ("Operator", "选择用于遮罩转换的图像文件"): "選擇用於遮罩轉換的圖像檔案",
        ("*", "选择用于遮罩转换的图像文件"): "選擇用於遮罩轉換的圖像檔案",  # 兼容性
        ("Operator", "应用遮罩到顶点色"): "應用遮罩到頂點色",
        ("*", "应用遮罩到顶点色"): "應用遮罩到頂點色",  # 兼容性
        ("Operator", "将共享设置中的图像应用到当前选中模型的顶点色Alpha通道"): "將共享設定中的圖像應用到當前選中模型的頂點色Alpha通道",
        ("*", "将共享设置中的图像应用到当前选中模型的顶点色Alpha通道"): "將共享設定中的圖像應用到當前選中模型的頂點色Alpha通道",  # 兼容性
        ("Operator", "添加选中对象"): "新增選中物件",
        ("*", "添加选中对象"): "新增選中物件",  # 兼容性
        ("Operator", "将选中的对象添加到批量处理列表"): "將選中的物件新增到批次處理清單",
        ("*", "将选中的对象添加到批量处理列表"): "將選中的物件新增到批次處理清單",  # 兼容性
        ("Operator", "移除选中"): "移除選中",
        ("*", "移除选中"): "移除選中",  # 兼容性
        ("Operator", "从批量处理列表中移除选中的对象"): "從批次處理清單中移除選中的物件",
        ("*", "从批量处理列表中移除选中的对象"): "從批次處理清單中移除選中的物件",  # 兼容性
        ("Operator", "移除启用项"): "移除啟用項",
        ("*", "移除启用项"): "移除啟用項",  # 兼容性
        ("Operator", "从批量处理列表中移除所有启用的对象"): "從批次處理清單中移除所有啟用的物件",
        ("*", "从批量处理列表中移除所有启用的对象"): "從批次處理清單中移除所有啟用的物件",  # 兼容性
        ("Operator", "清空列表"): "清空清單",
        ("*", "清空列表"): "清空清單",  # 兼容性
        ("Operator", "清空批量处理列表中的所有对象"): "清空批次處理清單中的所有物件",
        ("*", "清空批量处理列表中的所有对象"): "清空批次處理清單中的所有物件",  # 兼容性
        ("Operator", "全部启用"): "全部啟用",
        ("*", "全部启用"): "全部啟用",  # 兼容性
        ("Operator", "启用列表中的所有对象"): "啟用清單中的所有物件",
        ("*", "启用列表中的所有对象"): "啟用清單中的所有物件",  # 兼容性
        ("Operator", "全部禁用"): "全部停用",
        ("*", "全部禁用"): "全部停用",  # 兼容性
        ("Operator", "禁用列表中的所有对象"): "停用清單中的所有物件",
        ("*", "禁用列表中的所有对象"): "停用清單中的所有物件",  # 兼容性
        ("Operator", "批量应用遮罩"): "批次應用遮罩",
        ("*", "批量应用遮罩"): "批次應用遮罩",  # 兼容性
        ("Operator", "批量将遮罩应用到多个对象的顶点色"): "批次將遮罩應用到多個物件的頂點色",
        ("*", "批量将遮罩应用到多个对象的顶点色"): "批次將遮罩應用到多個物件的頂點色",  # 兼容性
        ("Operator", "修复UV坐标"): "修復UV座標",
        ("*", "修复UV坐标"): "修復UV座標",  # 兼容性
        ("Operator", "修复UV坐标中的NaN和无效值"): "修復UV座標中的NaN和無效值",
        ("*", "修复UV坐标中的NaN和无效值"): "修復UV座標中的NaN和無效值",  # 兼容性
        ("Operator", "验证模型"): "驗證模型",
        ("*", "验证模型"): "驗證模型",  # 兼容性
        ("Operator", "检查模型是否适合应用遮罩"): "檢查模型是否適合應用遮罩",
        ("*", "检查模型是否适合应用遮罩"): "檢查模型是否適合應用遮罩",  # 兼容性
        
        # UI文本
        ("*", "遮罩转顶点色 Pro"): "遮罩轉頂點色 Pro",
        ("*", "图像文件:"): "圖像檔案:",
        ("*", "未选择图像"): "未選擇圖像",
        ("*", "选择图像"): "選擇圖像",
        ("*", "更换图像"): "更換圖像",
        ("*", "处理设置:"): "處理設定:",
        ("*", "单对象处理:"): "單物件處理:",
        ("*", "应用到当前选中对象"): "應用到當前選中物件",
        ("*", "注意: 仅处理当前选中的一个对象"): "注意: 僅處理當前選中的一個物件",
        ("*", "请先选择图像文件"): "請先選擇圖像檔案",
        ("*", "批量处理:"): "批次處理:",
        ("*", "批量应用到 {} 个对象"): "批次應用到 {} 個物件",
        ("*", "注意: 将处理列表中所有启用的对象 ({}个)"): "注意: 將處理清單中所有啟用的物件 ({}個)",
        ("*", "请在列表中启用至少一个对象"): "請在清單中啟用至少一個物件",
        ("*", "批量列表为空"): "批次清單為空",
        ("*", "添加选中对象到列表"): "新增選中物件到清單",
        ("*", "使用方法:"): "使用方法:",
        ("*", "1. 在3D视图中选择多个对象"): "1. 在3D視圖中選擇多個物件",
        ("*", "2. 点击'添加选中对象到列表'"): "2. 點擊'新增選中物件到清單'",
        ("*", "3. 在列表中勾选要处理的对象"): "3. 在清單中勾選要處理的物件",
        ("*", "4. 点击'批量应用到X个对象'"): "4. 點擊'批次應用到X個物件'",
        ("*", "工具:"): "工具:",
        ("*", "修复UV坐标"): "修復UV座標",
        ("*", "验证模型"): "驗證模型",
        ("*", "工作流程:"): "工作流程:",
        ("*", "1. 选择图像文件"): "1. 選擇圖像檔案",
        ("*", "2. 配置处理设置"): "2. 配置處理設定",
        ("*", "3. 快速处理单个对象（上）"): "3. 快速處理單個物件（上）",
        ("*", "4. 批量处理多个对象（下）"): "4. 批次處理多個物件（下）",
        ("*", "✓ 所有操作共享同一图像和设置"): "✓ 所有操作共享同一圖像和設定",
        ("*", "✓ 先处理单个测试效果，再批量应用"): "✓ 先處理單個測試效果，再批次應用",
        ("*", "版本信息:"): "版本資訊:",
        ("*", "插件版本: v{}.{}"): "外掛程式版本: v{}.{}",
        ("*", "优化: 调整UI布局顺序"): "優化: 調整UI佈局順序",
        ("*", "作者: 墨泪"): "作者: 墨淚",
        ("*", "主页: https://www.kiiiii.com"): "首頁: https://www.kiiiii.com",
        
        # 状态文本
        ("*", "等待"): "等待",
        ("*", "处理中"): "處理中",
        ("*", "完成"): "完成",
        ("*", "错误"): "錯誤",
        ("*", "无效对象"): "無效物件",
        
        # 消息
        ("*", "遮罩已应用到 {}"): "遮罩已應用到 {}",
        ("*", "处理 {} 失败"): "處理 {} 失敗",
        ("*", "请先选择一个网格对象！"): "請先選擇一個網格物件！",
        ("*", "请先选择图像文件！"): "請先選擇圖像檔案！",
        ("*", "图像文件不存在: {}"): "圖像檔案不存在: {}",
        ("*", "无法加载图像: {}"): "無法載入圖像: {}",
        ("*", "添加了 {} 个对象"): "新增了 {} 個物件",
        ("*", "没有可添加的网格对象"): "沒有可新增的網格物件",
        ("*", "列表为空"): "清單為空",
        ("*", "没有选中的对象"): "沒有選中的物件",
        ("*", "移除了: {}"): "移除了: {}",
        ("*", "移除了 {} 个启用的对象"): "移除了 {} 個啟用的物件",
        ("*", "清空了 {} 个对象"): "清空了 {} 個物件",
        ("*", "启用了 {} 个对象"): "啟用了 {} 個物件",
        ("*", "所有对象都已启用"): "所有物件都已啟用",
        ("*", "禁用了 {} 个对象"): "停用了 {} 個物件",
        ("*", "所有对象都已禁用"): "所有物件都已停用",
        ("*", "批量处理完成: {}成功, {}失败"): "批次處理完成: {}成功, {}失敗",
        ("*", "批量处理列表中没有启用的对象！"): "批次處理清單中沒有啟用的物件！",
        ("*", "修复了 {} 个UV坐标"): "修復了 {} 個UV座標",
        ("*", "未发现需要修复的UV坐标"): "未發現需要修復的UV座標",
        ("*", "{}: 不是网格对象"): "{}: 不是網格物件",
        ("*", "{}: 没有UV坐标"): "{}: 沒有UV座標",
        ("*", "{}: {}个UV层"): "{}: {}個UV圖層",
        ("*", "{}.{}: {}个无效UV"): "{}.{}: {}個無效UV",
        ("*", "{}: 没有顶点色层"): "{}: 沒有頂點色圖層",
        ("*", "{}: {}个顶点色层"): "{}: {}個頂點色圖層",
        ("*", "{}: {}个多边形"): "{}: {}個多邊形",
        ("*", "{}: {}个顶点"): "{}: {}個頂點",
        ("*", "未知对象"): "未知物件",
        ("*", "UV修复:{}"): "UV修復:{}",
        ("*", "创建的顶点色层的名称"): "建立的頂點色圖層的名稱",
        ("*", "已选择图像: {}"): "已選擇圖像: {}",
    },
}

# 翻译辅助函数
def _(message, context="*"):
    """获取翻译文本"""
    # 直接使用pgettext，在翻译字典中查找 ("*", message) 键
    # 由于已经在翻译字典中同时添加了 ("*", message) 和 ("Operator", message) 键
    # 所以无论使用哪个context都能找到翻译
    return bpy.app.translations.pgettext(message)

def iface_(message):
    """获取界面翻译文本"""
    return bpy.app.translations.pgettext_iface(message)

# 版本兼容性检查
def is_blender_3_0_or_newer():
    """检查是否为Blender 3.0或更高版本"""
    return bpy.app.version >= (3, 0, 0)

def is_blender_4_0_or_newer():
    """检查是否为Blender 4.0或更高版本"""
    return bpy.app.version >= (4, 0, 0)

# ============================================
# 属性组定义
# ============================================

class MASK2VC_ObjectItem(PropertyGroup):
    """批量处理中的对象项"""
    obj: PointerProperty(
        name=iface_("对象"),
        type=bpy.types.Object
    )
    
    enabled: BoolProperty(
        name=iface_("启用"),
        description=_("是否处理此对象"),
        default=True
    )
    
    uv_layer: StringProperty(
        name=iface_("UV层"),
        description=_("使用的UV层名称"),
        default=""
    )
    
    vcol_name: StringProperty(
        name=iface_("顶点色名称"),
        description=_("顶点色层的名称"),
        default="MaskAlpha"
    )
    
    status: StringProperty(
        name=iface_("状态"),
        description=_("处理状态"),
        default=_("等待")
    )

class MASK2VC_SceneSettings(PropertyGroup):
    """场景设置"""
    # 批量处理
    batch_objects: CollectionProperty(type=MASK2VC_ObjectItem)
    batch_active_index: IntProperty(
        name="",  # 内部索引，不在UI中显示名称
        default=0,
        options={'HIDDEN'}  # 隐藏此属性，不在UI中显示
    )
    
    # 共享的图像文件路径
    shared_image_path: StringProperty(
        name=iface_("图像文件"),
        description=_("用于遮罩转换的图像文件路径"),
        default="",
        subtype='FILE_PATH'
    )
    
    # 共享的处理设置
    mask_source: EnumProperty(
        name=iface_("遮罩源"),
        description=_("选择遮罩信息的来源"),
        items=[
            ('AUTO', iface_("自动检测"), _("自动检测最佳遮罩源")),
            ('ALPHA', iface_("Alpha通道"), _("使用图像的Alpha通道作为遮罩")),
            ('GRAYSCALE', iface_("灰度值"), _("将RGB转换为灰度作为遮罩")),
            ('RED', iface_("红色通道"), _("使用红色通道作为遮罩")),
            ('GREEN', iface_("绿色通道"), _("使用绿色通道作为遮罩")),
            ('BLUE', iface_("蓝色通道"), _("使用蓝色通道作为遮罩")),
            ('LUMINANCE', iface_("亮度"), _("使用亮度作为遮罩")),
        ],
        default='AUTO'
    )
    
    blend_mode: EnumProperty(
        name=iface_("混合模式"),
        description=_("遮罩与现有顶点色的混合模式"),
        items=[
            ('REPLACE', iface_("替换"), _("替换现有Alpha值")),
            ('MULTIPLY', iface_("相乘"), _("与现有Alpha值相乘")),
            ('ADD', iface_("相加"), _("与现有Alpha值相加")),
            ('SUBTRACT', iface_("相减"), _("从现有Alpha值中减去")),
            ('MIN', iface_("最小值"), _("取最小值")),
            ('MAX', iface_("最大值"), _("取最大值")),
            ('OVERLAY', iface_("叠加"), _("叠加模式")),
            ('SCREEN', iface_("滤色"), _("滤色模式")),
        ],
        default='REPLACE'
    )
    
    blend_factor: FloatProperty(
        name=iface_("混合强度"),
        description=_("混合效果的强度"),
        min=0.0,
        max=1.0,
        default=1.0,
        subtype='FACTOR'
    )
    
    uv_wrap: BoolProperty(
        name=iface_("UV包裹"),
        description=_("将UV坐标包裹在0-1范围内（处理超出范围的UV）"),
        default=True
    )
    
    uv_clamp: BoolProperty(
        name=iface_("UV限制"),
        description=_("将UV坐标限制在0-1范围内（不包裹）"),
        default=False
    )
    
    flip_vertical: BoolProperty(
        name=iface_("垂直翻转"),
        description=_("修复图像上下颠倒的问题"),
        default=False
    )
    
    flip_horizontal: BoolProperty(
        name=iface_("水平翻转"),
        description=_("修复图像左右颠倒的问题"),
        default=False
    )
    
    debug_mode: BoolProperty(
        name=iface_("调试模式"),
        description=_("显示详细处理信息"),
        default=False
    )
    
    # 单对象处理的顶点色名称
    single_vcol_name: StringProperty(
        name=iface_("顶点色名称"),
        description=_("单对象处理时创建的顶点色层的名称"),
        default="MaskAlpha"
    )

# ============================================
# UI列表
# ============================================

class MASK2VC_UL_ObjectList(UIList):
    """批量处理对象列表"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        """绘制列表项"""
        settings = context.scene.mask2vc_settings
        
        row = layout.row(align=True)
        
        # 检查是否选中
        is_selected = False
        try:
            # 尝试获取选中状态
            idx = -1
            for i, obj_item in enumerate(settings.batch_objects):
                if obj_item == item:
                    idx = i
                    break
            is_selected = (idx == settings.batch_active_index)
        except:
            pass
        
        # 启用复选框
        row.prop(item, "enabled", text="")
        
        # 选中状态指示
        if is_selected:
            row.label(icon='RADIOBUT_ON')
        else:
            row.label(icon='RADIOBUT_OFF')
        
        # 对象名称
        if item.obj:
            # 显示对象名称
            row.label(text=item.obj.name, icon='OBJECT_DATA')
            
            # 状态指示器
            status_icons = {
                _("等待"): 'TIME',
                _("处理中"): 'SORTTIME',
                _("完成"): 'CHECKMARK',
                _("错误"): 'ERROR'
            }
            
            icon_name = status_icons.get(item.status, 'QUESTION')
            row.label(icon=icon_name)
            
            # 显示简短状态
            status_text = item.status.split(':')[0] if ':' in item.status else item.status
            if len(status_text) > 6:
                status_text = status_text[:5] + "..."
            row.label(text=status_text)
            
        else:
            row.label(text=_("无效对象"), icon='ERROR')
            row.label(text="", icon='QUESTION')

# ============================================
# 单对象处理操作符（放在前面）
# ============================================

class MASK2VC_OT_select_image(Operator, ImportHelper):
    """选择图像文件"""
    bl_idname = "mask2vc.select_image"
    bl_label = iface_("选择图像文件")
    bl_description = _("选择用于遮罩转换的图像文件", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    # 文件选择属性
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.tga;*.exr',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        """执行操作"""
        settings = context.scene.mask2vc_settings
        settings.shared_image_path = self.filepath
        
        # 获取文件名用于显示
        filename = os.path.basename(self.filepath)
        self.report({'INFO'}, _("已选择图像: {}").format(filename))
        
        return {'FINISHED'}

class MASK2VC_OT_apply_mask(Operator):
    """单对象应用遮罩（使用共享设置）"""
    bl_idname = "mask2vc.apply_mask"
    bl_label = iface_("应用遮罩到顶点色")
    bl_description = _("将共享设置中的图像应用到当前选中模型的顶点色Alpha通道", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    # 顶点色名称（独立于批量处理）
    vcol_name: StringProperty(
        name=iface_("顶点色名称"),
        description=_("创建的顶点色层的名称"),
        default="MaskAlpha"
    )
    
    def invoke(self, context, event):
        """调用操作符，检查文件是否存在"""
        settings = context.scene.mask2vc_settings
        
        # 检查是否设置了图像路径
        if not settings.shared_image_path:
            self.report({'ERROR'}, _("请先选择图像文件！"))
            return {'CANCELLED'}
        
        # 检查文件是否存在
        if not os.path.exists(settings.shared_image_path):
            self.report({'ERROR'}, _("图像文件不存在: {}").format(settings.shared_image_path))
            return {'CANCELLED'}
        
        # 检查选中的对象
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, _("请先选择一个网格对象！"))
            return {'CANCELLED'}
        
        # 执行处理
        return self.execute(context)
    
    def execute(self, context):
        """执行操作"""
        settings = context.scene.mask2vc_settings
        obj = context.active_object
        
        # 加载图像
        try:
            image = bpy.data.images.load(settings.shared_image_path, check_existing=True)
        except Exception as e:
            self.report({'ERROR'}, _("无法加载图像: {}").format(str(e)))
            return {'CANCELLED'}
        
        # 使用场景设置中的顶点色名称
        self.vcol_name = settings.single_vcol_name
        
        # 应用遮罩
        success = self.apply_mask_to_object(context, obj, image)
        
        if success:
            self.report({'INFO'}, _("遮罩已应用到 {}").format(obj.name))
        else:
            self.report({'ERROR'}, _("处理 {} 失败").format(obj.name))
        
        # 清理图像
        if image.users == 1:
            bpy.data.images.remove(image)
        
        return {'FINISHED' if success else 'CANCELLED'}
    
    def apply_mask_to_object(self, context, obj, image):
        """应用遮罩到对象"""
        settings = context.scene.mask2vc_settings
        
        try:
            # 保存当前模式
            original_mode = obj.mode
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            mesh = obj.data
            
            # 获取图像信息
            width, height = image.size
            has_alpha = (image.depth == 32)
            
            # 获取像素数据
            pixels = list(image.pixels)
            
            # 检查UV层
            if not mesh.uv_layers:
                uv_layer = mesh.uv_layers.new(name="Mask_UV")
            else:
                uv_layer = mesh.uv_layers.active
                if not uv_layer:
                    uv_layer = mesh.uv_layers[0]
            
            # 创建或获取顶点色层
            if self.vcol_name in mesh.vertex_colors:
                vcol = mesh.vertex_colors[self.vcol_name]
                has_existing = True
            else:
                vcol = mesh.vertex_colors.new(name=self.vcol_name)
                has_existing = False
            
            # 获取UV数据
            uv_data = uv_layer.data
            
            # 处理每个多边形循环
            for poly in mesh.polygons:
                for loop_idx in poly.loop_indices:
                    uv = uv_data[loop_idx].uv
                    
                    # 安全的UV到像素转换
                    x, y = self.safe_uv_to_pixel(uv.x, uv.y, width, height, settings)
                    
                    # 获取像素颜色
                    r, g, b, a = self.get_pixel_color(pixels, x, y, width, height, has_alpha, settings)
                    
                    # 获取遮罩值
                    mask_value = self.get_mask_value(r, g, b, a, settings)
                    
                    # 应用混合模式
                    if has_existing and settings.blend_mode != 'REPLACE':
                        existing_color = vcol.data[loop_idx].color
                        existing_alpha = existing_color[3]
                        mask_value = self.apply_blend_mode(existing_alpha, mask_value, settings)
                    
                    # 设置顶点色
                    if settings.blend_factor < 1.0:
                        if has_existing:
                            existing_color = vcol.data[loop_idx].color
                            existing_alpha = existing_color[3]
                            final_alpha = existing_alpha * (1 - settings.blend_factor) + mask_value * settings.blend_factor
                        else:
                            final_alpha = mask_value
                    else:
                        final_alpha = mask_value
                    
                    vcol.data[loop_idx].color = (1.0, 1.0, 1.0, final_alpha)
            
            # 设置活动顶点色
            mesh.vertex_colors.active = vcol
            
            # 设置视口显示
            self.setup_viewport_compatible(context)
            
            # 恢复原始模式
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            
            # 更新视口
            context.area.tag_redraw()
            
            return True
            
        except Exception as e:
            self.report({'ERROR'}, _("处理失败: {}").format(str(e)))
            import traceback
            traceback.print_exc()
            return False
    
    def apply_blend_mode(self, existing, new, settings):
        """应用混合模式"""
        if settings.blend_mode == 'MULTIPLY':
            return existing * new
        elif settings.blend_mode == 'ADD':
            return min(1.0, existing + new)
        elif settings.blend_mode == 'SUBTRACT':
            return max(0.0, existing - new)
        elif settings.blend_mode == 'MIN':
            return min(existing, new)
        elif settings.blend_mode == 'MAX':
            return max(existing, new)
        elif settings.blend_mode == 'OVERLAY':
            if existing < 0.5:
                return 2.0 * existing * new
            else:
                return 1.0 - 2.0 * (1.0 - existing) * (1.0 - new)
        elif settings.blend_mode == 'SCREEN':
            return 1.0 - (1.0 - existing) * (1.0 - new)
        else:
            return new
    
    def safe_uv_to_pixel(self, uv_x, uv_y, width, height, settings):
        """安全的UV到像素坐标转换"""
        if math.isnan(uv_x) or math.isnan(uv_y) or \
           math.isinf(uv_x) or math.isinf(uv_y):
            return 0, 0
        
        if settings.uv_wrap:
            uv_x = uv_x % 1.0
            uv_y = uv_y % 1.0
        elif settings.uv_clamp:
            uv_x = max(0.0, min(1.0, uv_x))
            uv_y = max(0.0, min(1.0, uv_y))
        
        try:
            x = int(uv_x * (width - 1))
            y = int(uv_y * (height - 1))
        except (ValueError, OverflowError):
            return 0, 0
        
        return max(0, min(x, width - 1)), max(0, min(y, height - 1))
    
    def get_pixel_color(self, pixels, x, y, width, height, has_alpha, settings):
        """获取指定像素的颜色值"""
        if settings.flip_horizontal:
            x = width - 1 - x
        if settings.flip_vertical:
            y = height - 1 - y
        
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        
        pixel_idx = (y * width + x) * 4
        
        if pixel_idx + 3 < len(pixels):
            r = pixels[pixel_idx]
            g = pixels[pixel_idx + 1]
            b = pixels[pixel_idx + 2]
            a = pixels[pixel_idx + 3] if has_alpha else 1.0
            return r, g, b, a
        else:
            return 0.0, 0.0, 0.0, 1.0
    
    def get_mask_value(self, r, g, b, a, settings):
        """根据设置获取遮罩值"""
        mask_source = settings.mask_source
        if mask_source == 'AUTO':
            mask_source = 'ALPHA' if a < 0.99 else 'GRAYSCALE'
        
        if mask_source == 'ALPHA':
            value = a
        elif mask_source == 'GRAYSCALE':
            value = 0.299 * r + 0.587 * g + 0.114 * b
        elif mask_source == 'RED':
            value = r
        elif mask_source == 'GREEN':
            value = g
        elif mask_source == 'BLUE':
            value = b
        elif mask_source == 'LUMINANCE':
            value = 0.2126 * r + 0.7152 * g + 0.0722 * b
        else:
            value = a
        
        return max(0.0, min(1.0, value))
    
    def setup_viewport_compatible(self, context):
        """兼容不同Blender版本的视口设置"""
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if hasattr(space.shading, 'type'):
                            space.shading.type = 'MATERIAL'
                        if hasattr(space.shading, 'color_type'):
                            space.shading.color_type = 'VERTEX'
                        break

# ============================================
# 批量处理操作符
# ============================================

class MASK2VC_OT_batch_add_objects(Operator):
    """添加对象到批量处理列表"""
    bl_idname = "mask2vc.batch_add_objects"
    bl_label = iface_("添加选中对象")
    bl_description = _("将选中的对象添加到批量处理列表", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        
        added_count = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            
            # 检查是否已存在
            exists = False
            for item in settings.batch_objects:
                if item.obj == obj:
                    exists = True
                    break
            
            if not exists:
                item = settings.batch_objects.add()
                item.obj = obj
                item.vcol_name = "MaskAlpha"
                item.status = _("等待")
                
                # 自动选择第一个UV层
                if obj.data.uv_layers:
                    item.uv_layer = obj.data.uv_layers[0].name
                
                added_count += 1
        
        if added_count > 0:
            self.report({'INFO'}, _("添加了 {} 个对象").format(added_count))
        else:
            self.report({'WARNING'}, _("没有可添加的网格对象"))
        
        return {'FINISHED'}

class MASK2VC_OT_batch_remove_selected(Operator):
    """移除选中的对象"""
    bl_idname = "mask2vc.batch_remove_selected"
    bl_label = iface_("移除选中")
    bl_description = _("从批量处理列表中移除选中的对象", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        
        # 检查是否有选中的项目
        if len(settings.batch_objects) == 0:
            self.report({'WARNING'}, _("列表为空"))
            return {'CANCELLED'}
        
        if settings.batch_active_index < 0 or settings.batch_active_index >= len(settings.batch_objects):
            self.report({'WARNING'}, _("没有选中的对象"))
            return {'CANCELLED'}
        
        # 移除选中的对象
        removed_obj = settings.batch_objects[settings.batch_active_index]
        removed_name = removed_obj.obj.name if removed_obj.obj else _("未知对象")
        
        settings.batch_objects.remove(settings.batch_active_index)
        
        # 确保活动索引有效
        if settings.batch_active_index >= len(settings.batch_objects):
            settings.batch_active_index = max(0, len(settings.batch_objects) - 1)
        
        self.report({'INFO'}, _("移除了: {}").format(removed_name))
        
        return {'FINISHED'}

class MASK2VC_OT_batch_remove_enabled(Operator):
    """移除所有启用的对象"""
    bl_idname = "mask2vc.batch_remove_enabled"
    bl_label = iface_("移除启用项")
    bl_description = _("从批量处理列表中移除所有启用的对象", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        
        # 获取要移除的索引（反向遍历）
        indices = []
        for i, item in enumerate(settings.batch_objects):
            if item.enabled:
                indices.append(i)
        
        if not indices:
            self.report({'WARNING'}, _("没有启用的对象"))
            return {'CANCELLED'}
        
        # 反向移除
        removed_count = 0
        for i in sorted(indices, reverse=True):
            settings.batch_objects.remove(i)
            removed_count += 1
        
        # 确保活动索引有效
        if settings.batch_active_index >= len(settings.batch_objects):
            settings.batch_active_index = max(0, len(settings.batch_objects) - 1)
        
        self.report({'INFO'}, _("移除了 {} 个启用的对象").format(removed_count))
        
        return {'FINISHED'}

class MASK2VC_OT_batch_clear_all(Operator):
    """清空批量处理列表"""
    bl_idname = "mask2vc.batch_clear_all"
    bl_label = iface_("清空列表")
    bl_description = _("清空批量处理列表中的所有对象", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        count = len(settings.batch_objects)
        
        settings.batch_objects.clear()
        settings.batch_active_index = 0
        
        self.report({'INFO'}, _("清空了 {} 个对象").format(count))
        
        return {'FINISHED'}

class MASK2VC_OT_batch_enable_all(Operator):
    """启用所有对象"""
    bl_idname = "mask2vc.batch_enable_all"
    bl_label = iface_("全部启用")
    bl_description = _("启用列表中的所有对象", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        
        enabled_count = 0
        for item in settings.batch_objects:
            if not item.enabled:
                item.enabled = True
                enabled_count += 1
        
        if enabled_count > 0:
            self.report({'INFO'}, _("启用了 {} 个对象").format(enabled_count))
        else:
            self.report({'INFO'}, _("所有对象都已启用"))
        
        return {'FINISHED'}

class MASK2VC_OT_batch_disable_all(Operator):
    """禁用所有对象"""
    bl_idname = "mask2vc.batch_disable_all"
    bl_label = iface_("全部禁用")
    bl_description = _("禁用列表中的所有对象", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        
        disabled_count = 0
        for item in settings.batch_objects:
            if item.enabled:
                item.enabled = False
                disabled_count += 1
        
        if disabled_count > 0:
            self.report({'INFO'}, _("禁用了 {} 个对象").format(disabled_count))
        else:
            self.report({'INFO'}, _("所有对象都已禁用"))
        
        return {'FINISHED'}

class MASK2VC_OT_apply_mask_batch(Operator):
    """批量应用遮罩到顶点色"""
    bl_idname = "mask2vc.apply_mask_batch"
    bl_label = iface_("批量应用遮罩")
    bl_description = _("批量将遮罩应用到多个对象的顶点色", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    # 进度相关
    progress_total: IntProperty(default=0)
    progress_current: IntProperty(default=0)
    
    def invoke(self, context, event):
        """调用操作符，检查文件是否存在"""
        settings = context.scene.mask2vc_settings
        
        # 检查是否设置了图像路径
        if not settings.shared_image_path:
            self.report({'ERROR'}, _("请先选择图像文件！"))
            return {'CANCELLED'}
        
        # 检查文件是否存在
        if not os.path.exists(settings.shared_image_path):
            self.report({'ERROR'}, _("图像文件不存在: {}").format(settings.shared_image_path))
            return {'CANCELLED'}
        
        # 检查批量处理列表
        enabled_objects = [item for item in settings.batch_objects if item.enabled]
        if not enabled_objects:
            self.report({'ERROR'}, _("批量处理列表中没有启用的对象！"))
            return {'CANCELLED'}
        
        # 执行处理
        return self.execute(context)
    
    def execute(self, context):
        """执行批量处理"""
        settings = context.scene.mask2vc_settings
        enabled_objects = [item for item in settings.batch_objects if item.enabled]
        
        # 加载图像
        try:
            image = bpy.data.images.load(settings.shared_image_path, check_existing=True)
        except Exception as e:
            self.report({'ERROR'}, _("无法加载图像: {}").format(str(e)))
            return {'CANCELLED'}
        
        # 批量处理
        success_count = 0
        error_count = 0
        
        self.progress_total = len(enabled_objects)
        self.progress_current = 0
        
        for i, item in enumerate(enabled_objects):
            obj = item.obj
            if not obj or obj.type != 'MESH':
                item.status = _("错误")
                error_count += 1
                continue
            
            # 更新状态
            item.status = _("处理中")
            context.area.tag_redraw()
            
            # 处理对象
            try:
                success = self.apply_mask_to_object(context, obj, item, image)
                
                if success:
                    item.status = _("完成")
                    success_count += 1
                else:
                    item.status = _("错误")
                    error_count += 1
                    
            except Exception as e:
                item.status = _("错误: {}").format(str(e)[:30])
                error_count += 1
            
            self.progress_current = i + 1
        
        # 清理图像
        if image.users == 1:
            bpy.data.images.remove(image)
        
        # 设置视口显示
        self.setup_viewport_compatible(context)
        
        # 报告结果
        self.report({'INFO'}, _("批量处理完成: {}成功, {}失败").format(success_count, error_count))
        
        return {'FINISHED'}
    
    def apply_mask_to_object(self, context, obj, item, image):
        """应用遮罩到单个对象"""
        settings = context.scene.mask2vc_settings
        
        try:
            if settings.debug_mode:
                print(f"开始处理对象: {obj.name}")
            
            # 保存当前模式
            original_mode = obj.mode
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            mesh = obj.data
            
            # 检查UV层
            uv_layer_name = item.uv_layer
            if uv_layer_name and uv_layer_name in mesh.uv_layers:
                uv_layer = mesh.uv_layers[uv_layer_name]
            elif mesh.uv_layers:
                uv_layer = mesh.uv_layers[0]
                item.uv_layer = uv_layer.name
            else:
                if settings.debug_mode:
                    print("创建新的UV层")
                uv_layer = mesh.uv_layers.new(name="Mask_UV")
                item.uv_layer = uv_layer.name
            
            # 获取图像信息
            width, height = image.size
            has_alpha = (image.depth == 32)
            
            # 获取像素数据
            pixels = list(image.pixels)
            
            # 创建或获取顶点色层
            vcol_name = item.vcol_name
            if vcol_name in mesh.vertex_colors:
                vcol = mesh.vertex_colors[vcol_name]
                has_existing = True
            else:
                vcol = mesh.vertex_colors.new(name=vcol_name)
                has_existing = False
            
            # 获取UV数据
            uv_data = uv_layer.data
            
            # 处理每个多边形循环
            for poly in mesh.polygons:
                for loop_idx in poly.loop_indices:
                    uv = uv_data[loop_idx].uv
                    
                    # 安全的UV到像素转换
                    x, y = self.safe_uv_to_pixel(uv.x, uv.y, width, height, settings)
                    
                    # 获取像素颜色（应用方向修正）
                    r, g, b, a = self.get_pixel_color(pixels, x, y, width, height, has_alpha, settings)
                    
                    # 获取遮罩值
                    mask_value = self.get_mask_value(r, g, b, a, settings)
                    
                    # 应用混合模式
                    if has_existing and settings.blend_mode != 'REPLACE':
                        existing_color = vcol.data[loop_idx].color
                        existing_alpha = existing_color[3]
                        mask_value = self.apply_blend_mode(existing_alpha, mask_value, settings)
                    
                    # 设置顶点色
                    if settings.blend_factor < 1.0:
                        # 如果有现有顶点色，混合
                        if has_existing:
                            existing_color = vcol.data[loop_idx].color
                            existing_alpha = existing_color[3]
                            final_alpha = existing_alpha * (1 - settings.blend_factor) + mask_value * settings.blend_factor
                        else:
                            final_alpha = mask_value
                    else:
                        final_alpha = mask_value
                    
                    vcol.data[loop_idx].color = (1.0, 1.0, 1.0, final_alpha)
            
            # 设置活动顶点色
            mesh.vertex_colors.active = vcol
            
            # 恢复原始模式
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            
            return True
            
        except Exception as e:
            if settings.debug_mode:
                print(f"处理对象 {obj.name} 失败: {str(e)}")
                import traceback
                traceback.print_exc()
            
            return False
    
    def apply_blend_mode(self, existing, new, settings):
        """应用混合模式"""
        if settings.blend_mode == 'MULTIPLY':
            return existing * new
        elif settings.blend_mode == 'ADD':
            return min(1.0, existing + new)
        elif settings.blend_mode == 'SUBTRACT':
            return max(0.0, existing - new)
        elif settings.blend_mode == 'MIN':
            return min(existing, new)
        elif settings.blend_mode == 'MAX':
            return max(existing, new)
        elif settings.blend_mode == 'OVERLAY':
            if existing < 0.5:
                return 2.0 * existing * new
            else:
                return 1.0 - 2.0 * (1.0 - existing) * (1.0 - new)
        elif settings.blend_mode == 'SCREEN':
            return 1.0 - (1.0 - existing) * (1.0 - new)
        else:  # REPLACE
            return new
    
    def safe_uv_to_pixel(self, uv_x, uv_y, width, height, settings):
        """安全的UV到像素坐标转换"""
        # 检查NaN或无穷大
        if math.isnan(uv_x) or math.isnan(uv_y) or \
           math.isinf(uv_x) or math.isinf(uv_y):
            return 0, 0
        
        # 处理UV包裹
        if settings.uv_wrap:
            uv_x = uv_x % 1.0
            uv_y = uv_y % 1.0
        elif settings.uv_clamp:
            uv_x = max(0.0, min(1.0, uv_x))
            uv_y = max(0.0, min(1.0, uv_y))
        
        # 转换为像素坐标
        try:
            x = int(uv_x * (width - 1))
            y = int(uv_y * (height - 1))
        except (ValueError, OverflowError):
            return 0, 0
        
        return max(0, min(x, width - 1)), max(0, min(y, height - 1))
    
    def get_pixel_color(self, pixels, x, y, width, height, has_alpha, settings):
        """获取指定像素的颜色值"""
        # 应用方向修正
        if settings.flip_horizontal:
            x = width - 1 - x
        if settings.flip_vertical:
            y = height - 1 - y
        
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        
        # 计算像素索引
        pixel_idx = (y * width + x) * 4
        
        if pixel_idx + 3 < len(pixels):
            r = pixels[pixel_idx]
            g = pixels[pixel_idx + 1]
            b = pixels[pixel_idx + 2]
            a = pixels[pixel_idx + 3] if has_alpha else 1.0
            return r, g, b, a
        else:
            return 0.0, 0.0, 0.0, 1.0
    
    def get_mask_value(self, r, g, b, a, settings):
        """根据设置获取遮罩值"""
        mask_source = settings.mask_source
        if mask_source == 'AUTO':
            mask_source = 'ALPHA' if a < 0.99 else 'GRAYSCALE'
        
        if mask_source == 'ALPHA':
            value = a
        elif mask_source == 'GRAYSCALE':
            value = 0.299 * r + 0.587 * g + 0.114 * b
        elif mask_source == 'RED':
            value = r
        elif mask_source == 'GREEN':
            value = g
        elif mask_source == 'BLUE':
            value = b
        elif mask_source == 'LUMINANCE':
            value = 0.2126 * r + 0.7152 * g + 0.0722 * b
        else:
            value = a
        
        return max(0.0, min(1.0, value))
    
    def setup_viewport_compatible(self, context):
        """兼容不同Blender版本的视口设置"""
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if hasattr(space.shading, 'type'):
                            space.shading.type = 'MATERIAL'
                        if hasattr(space.shading, 'color_type'):
                            space.shading.color_type = 'VERTEX'
                        break

# ============================================
# 工具操作符
# ============================================

class MASK2VC_OT_fix_uv(Operator):
    """修复UV坐标中的NaN值"""
    bl_idname = "mask2vc.fix_uv"
    bl_label = iface_("修复UV坐标")
    bl_description = _("修复UV坐标中的NaN和无效值", "Operator")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        fixed_total = 0
        
        # 批量修复
        if settings.batch_objects:
            for item in settings.batch_objects:
                if item.enabled and item.obj and item.obj.type == 'MESH':
                    fixed = self.fix_object_uv(item.obj)
                    fixed_total += fixed
                    item.status = _("UV修复:{}").format(fixed)
        else:
            # 修复当前选中对象
            obj = context.active_object
            if not obj:
                self.report({'ERROR'}, _("请先选择一个网格对象！"))
                return {'CANCELLED'}
            
            if obj.type != 'MESH':
                self.report({'ERROR'}, _("请先选择一个网格对象！"))
                return {'CANCELLED'}
            
            fixed_total = self.fix_object_uv(obj)
        
        if fixed_total > 0:
            self.report({'INFO'}, _("修复了 {} 个UV坐标").format(fixed_total))
        else:
            self.report({'INFO'}, _("未发现需要修复的UV坐标"))
        
        return {'FINISHED'}
    
    def fix_object_uv(self, obj):
        """修复单个对象的UV"""
        if not obj or obj.type != 'MESH':
            return 0
        
        original_mode = obj.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        mesh = obj.data
        fixed_count = 0
        
        for uv_layer in mesh.uv_layers:
            for uv_data in uv_layer.data:
                uv = uv_data.uv
                
                if math.isnan(uv.x) or math.isnan(uv.y) or \
                   math.isinf(uv.x) or math.isinf(uv.y):
                    uv_data.uv = (0.0, 0.0)
                    fixed_count += 1
        
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)
        
        return fixed_count

class MASK2VC_OT_validate_model(Operator):
    """验证模型"""
    bl_idname = "mask2vc.validate_model"
    bl_label = iface_("验证模型")
    bl_description = _("检查模型是否适合应用遮罩", "Operator")
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        settings = context.scene.mask2vc_settings
        reports = []
        
        if settings.batch_objects:
            # 批量验证
            for item in settings.batch_objects:
                if not item.enabled:
                    continue
                    
                obj = item.obj
                if not obj or obj.type != 'MESH':
                    reports.append(('ERROR', _("{}: 不是网格对象").format(obj.name if obj else _("未知"))))
                    continue
                
                reports.extend(self.validate_single_object(obj))
        else:
            # 验证当前对象
            obj = context.active_object
            if not obj or obj.type != 'MESH':
                self.report({'ERROR'}, _("请先选择一个网格对象！"))
                return {'CANCELLED'}
            
            reports.extend(self.validate_single_object(obj))
        
        # 输出报告
        for report_type, message in reports:
            self.report({report_type}, message)
        
        return {'FINISHED'}
    
    def validate_single_object(self, obj):
        """验证单个对象"""
        reports = []
        mesh = obj.data
        
        # 检查UV
        if not mesh.uv_layers:
            reports.append(('WARNING', _("{}: 没有UV坐标").format(obj.name)))
        else:
            reports.append(('INFO', _("{}: {}个UV层").format(obj.name, len(mesh.uv_layers))))
            
            for uv_layer in mesh.uv_layers:
                invalid_uvs = 0
                for uv_data in uv_layer.data:
                    uv = uv_data.uv
                    if math.isnan(uv.x) or math.isnan(uv.y) or \
                       math.isinf(uv.x) or math.isinf(uv.y):
                        invalid_uvs += 1
                
                if invalid_uvs > 0:
                    reports.append(('WARNING', _("{}.{}: {}个无效UV").format(obj.name, uv_layer.name, invalid_uvs)))
        
        # 检查顶点色
        if not mesh.vertex_colors:
            reports.append(('INFO', _("{}: 没有顶点色层").format(obj.name)))
        else:
            reports.append(('INFO', _("{}: {}个顶点色层").format(obj.name, len(mesh.vertex_colors))))
        
        # 基本信息
        reports.append(('INFO', _("{}: {}个多边形").format(obj.name, len(mesh.polygons))))
        reports.append(('INFO', _("{}: {}个顶点").format(obj.name, len(mesh.vertices))))
        
        return reports

# ============================================
# 主面板（重新调整布局）
# ============================================

class MASK2VC_PT_main_panel(Panel):
    """主面板"""
    bl_label = "Mask To Vertex Color Pro"
    bl_idname = "MASK2VC_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "M2VC Pro"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.mask2vc_settings
        
        # 标题
        box = layout.box()
        row = box.row()
        row.label(text=_("遮罩转顶点色 Pro"), icon='IMAGE_DATA')
        version = get_addon_version()
        row.label(text=f"v{version[0]}.{version[1]}")
        
        col = box.column(align=True)
        col.scale_y = 0.7
        col.label(text=f"Blender {bpy.app.version_string}")
        
        layout.separator()
        
        # 图像文件选择区域
        box = layout.box()
        box.label(text=_("图像文件:"), icon='IMAGE_DATA')
        
        # 文件路径显示和选择按钮
        row = box.row()
        row.scale_y = 0.8
        if settings.shared_image_path:
            filename = os.path.basename(settings.shared_image_path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            row.label(text=filename, icon='IMAGE_DATA')
            
            # 验证文件是否存在
            if not os.path.exists(settings.shared_image_path):
                row.label(icon='ERROR')
        else:
            row.label(text=_("未选择图像"), icon='QUESTION')
        
        row = box.row(align=True)
        row.operator("mask2vc.select_image", 
                    text=_("选择图像") if not settings.shared_image_path else _("更换图像"),
                    icon='FILE_FOLDER')
        
        if settings.shared_image_path:
            row.prop(settings, "shared_image_path", text="", icon_only=True)
        
        # 处理设置区域
        layout.separator()
        box = layout.box()
        box.label(text=_("处理设置:"), icon='SETTINGS')
        
        col = box.column(align=True)
        col.prop(settings, "mask_source")
        col.prop(settings, "blend_mode")
        col.prop(settings, "blend_factor")
        
        row = col.row(align=True)
        row.prop(settings, "uv_wrap", toggle=True)
        row.prop(settings, "uv_clamp", toggle=True)
        
        row = col.row(align=True)
        row.prop(settings, "flip_vertical", toggle=True)
        row.prop(settings, "flip_horizontal", toggle=True)
        
        col.prop(settings, "debug_mode")
        
        layout.separator()
        
        # ============================================
        # 单对象处理（移动到前面）
        # ============================================
        box = layout.box()
        box.label(text=_("单对象处理:"), icon='OBJECT_DATA')
        
        col = box.column(align=True)
        
        # 顶点色名称输入
        row = col.row(align=True)
        row.label(text=_("顶点颜色属性名:"))
        row.prop(settings, "single_vcol_name", text="")
        
        # 应用按钮
        if settings.shared_image_path:
            col.operator("mask2vc.apply_mask", 
                        text=_("应用到当前选中对象"), 
                        icon='IMAGE_ALPHA')
            col.label(text=_("注意: 仅处理当前选中的一个对象"), icon='INFO')
        else:
            col.label(text=_("请先选择图像文件"), icon='INFO')
        
        layout.separator()
        
        # ============================================
        # 批量处理（放在单对象处理后面）
        # ============================================
        box = layout.box()
        box.label(text=_("批量处理:"), icon='OUTLINER_OB_MESH')
        
        # 对象列表
        if settings.batch_objects:
            row = box.row()
            row.template_list(
                "MASK2VC_UL_ObjectList", "",
                settings, "batch_objects",
                settings, "batch_active_index",
                rows=5
            )
            
            # 列表操作按钮
            col = row.column(align=True)
            col.operator("mask2vc.batch_add_objects", icon='ADD', text="")
            col.operator("mask2vc.batch_remove_selected", icon='REMOVE', text="")
            col.separator()
            col.operator("mask2vc.batch_remove_enabled", icon='X', text="")
            col.operator("mask2vc.batch_clear_all", icon='TRASH', text="")
            col.separator()
            col.operator("mask2vc.batch_enable_all", icon='CHECKBOX_HLT', text="")
            col.operator("mask2vc.batch_disable_all", icon='CHECKBOX_DEHLT', text="")
            
            # 批量处理按钮
            enabled_count = sum(1 for item in settings.batch_objects if item.enabled)
            if enabled_count > 0 and settings.shared_image_path:
                box.operator("mask2vc.apply_mask_batch", 
                           text=_("批量应用到 {} 个对象").format(enabled_count),
                           icon='PLAY')
                box.label(text=_("注意: 将处理列表中所有启用的对象 ({}个)").format(enabled_count), icon='INFO')
            elif enabled_count > 0:
                box.label(text=_("请先选择图像文件"), icon='INFO')
            else:
                box.label(text=_("请在列表中启用至少一个对象"), icon='INFO')
        else:
            box.label(text=_("批量列表为空"), icon='INFO')
            row = box.row(align=True)
            row.operator("mask2vc.batch_add_objects", icon='ADD', text=_("添加选中对象到列表"))
            box.label(text=_("使用方法:"), icon='QUESTION')
            box.label(text=_("1. 在3D视图中选择多个对象"))
            box.label(text=_("2. 点击'添加选中对象到列表'"))
            box.label(text=_("3. 在列表中勾选要处理的对象"))
            box.label(text=_("4. 点击'批量应用到X个对象'"))
        
        # 工具区域
        layout.separator()
        box = layout.box()
        box.label(text=_("工具:"), icon='TOOL_SETTINGS')
        
        col = box.column(align=True)
        col.operator("mask2vc.fix_uv",
                    text=_("修复UV坐标"),
                    icon='UV')
        col.operator("mask2vc.validate_model",
                    text=_("验证模型"),
                    icon='CHECKMARK')
        
        # 说明
        layout.separator()
        box = layout.box()
        box.label(text=_("工作流程:"), icon='QUESTION')
        
        col = box.column(align=True)
        col.scale_y = 0.7
        
        col.label(text=_("1. 选择图像文件"), icon='IMAGE_DATA')
        col.label(text=_("2. 配置处理设置"), icon='SETTINGS')
        col.label(text=_("3. 快速处理单个对象（上）"), icon='OBJECT_DATA')
        col.label(text=_("4. 批量处理多个对象（下）"), icon='OUTLINER_OB_MESH')
        col.label(text=_("✓ 所有操作共享同一图像和设置"), icon='CHECKMARK')
        col.label(text=_("✓ 先处理单个测试效果，再批量应用"), icon='LIGHT')
        
        # 版本信息
        layout.separator()
        box = layout.box()
        box.label(text=_("版本信息:"), icon='INFO')
        
        col = box.column(align=True)
        col.scale_y = 0.7
        version = get_addon_version()
        col.label(text=_("插件版本: v{}.{}").format(version[0], version[1]))
        col.label(text=_("优化: 调整UI布局顺序"))
        col.label(text=_("作者: 墨泪"))
        col.label(text=_("主页: https://www.kiiiii.com"))

# ============================================
# 注册和注销
# ============================================

# 注册类列表
classes = [
    MASK2VC_ObjectItem,
    MASK2VC_SceneSettings,
    MASK2VC_UL_ObjectList,
    MASK2VC_OT_select_image,
    MASK2VC_OT_apply_mask,
    MASK2VC_OT_batch_add_objects,
    MASK2VC_OT_batch_remove_selected,
    MASK2VC_OT_batch_remove_enabled,
    MASK2VC_OT_batch_clear_all,
    MASK2VC_OT_batch_enable_all,
    MASK2VC_OT_batch_disable_all,
    MASK2VC_OT_apply_mask_batch,
    MASK2VC_OT_fix_uv,
    MASK2VC_OT_validate_model,
    MASK2VC_PT_main_panel,
]

def register():
    """注册插件"""
    # 注册翻译（如果还没有注册）
    try:
        bpy.app.translations.register(__name__, translations_dict)
    except ValueError:
        # 如果已经注册，先注销再重新注册
        try:
            bpy.app.translations.unregister(__name__)
        except:
            pass
        bpy.app.translations.register(__name__, translations_dict)
    
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"注册类 {cls.__name__} 时出错: {e}")
    
    # 注册属性组
    bpy.types.Scene.mask2vc_settings = PointerProperty(type=MASK2VC_SceneSettings)
    
    version = get_addon_version()
    print(f"Mask To Vertex Color Pro v{version[0]}.{version[1]} 已注册")
    print("优化: 调整UI布局顺序，单对象处理在前")

def unregister():
    """注销插件"""
    # 注销翻译
    bpy.app.translations.unregister(__name__)
    
    # 注销属性组
    if hasattr(bpy.types.Scene, 'mask2vc_settings'):
        del bpy.types.Scene.mask2vc_settings
    
    # 注销类
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass
    
    print("Mask To Vertex Color Pro 已注销")

# 测试代码
if __name__ == "__main__":
    # 清理旧版本
    try:
        unregister()
    except:
        pass
    
    # 注册新版本
    register()