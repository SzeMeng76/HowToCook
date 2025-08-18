#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToCook Recipe JSON Generator
解析dishes目录下的Markdown文件，生成适配cooking模块的JSON格式
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional


class RecipeParser:
    """菜谱解析器"""
    
    # 分类映射 - 从目录名到中文名
    CATEGORY_MAP = {
        'aquatic': '水产',
        'breakfast': '早餐', 
        'condiment': '调料',
        'dessert': '甜品',
        'drink': '饮品',
        'meat_dish': '荤菜',
        'semi-finished': '半成品加工',
        'soup': '汤羹',
        'staple': '主食',
        'vegetable_dish': '素菜'
    }
    
    def __init__(self, dishes_dir: str = 'dishes'):
        self.dishes_dir = Path(dishes_dir)
        
    def parse_difficulty(self, content: str) -> int:
        """从内容中提取难度等级"""
        match = re.search(r'预估烹饪难度[：:]\s*([★☆]+)', content)
        if match:
            stars = match.group(1)
            return len([c for c in stars if c == '★'])
        return 1  # 默认难度
        
    def parse_servings(self, content: str) -> int:
        """从内容中提取份量信息"""
        # 查找"一份正好够X个人"的模式
        match = re.search(r'一份正好够\s*(\d+)\s*个?人', content)
        if match:
            return int(match.group(1))
        
        # 查找"X人份"的模式  
        match = re.search(r'(\d+)\s*人份', content)
        if match:
            return int(match.group(1))
            
        return 2  # 默认2人份
        
    def parse_ingredients(self, content: str) -> List[Dict[str, Any]]:
        """解析食材列表"""
        ingredients = []
        
        # 查找必备原料和工具部分
        materials_match = re.search(r'## 必备原料和工具\s*\n(.*?)(?=\n##|\n$)', content, re.DOTALL)
        if materials_match:
            materials_section = materials_match.group(1)
            for line in materials_section.split('\n'):
                line = line.strip()
                # 支持破折号、星号和加号格式
                if (line.startswith('-') or line.startswith('*') or line.startswith('+')) and not line.startswith('- 注：'):
                    ingredient_text = line[1:].strip()
                    # 提取食材名称（去掉括号内容和特殊符号）
                    name = re.sub(r'[（(].*?[）)]', '', ingredient_text)
                    name = re.sub(r'[：:：].*$', '', name).strip()
                    if name and '工具' not in name and '锅' not in name and '盆' not in name:
                        ingredients.append({
                            'name': name,
                            'quantity': None,
                            'unit': None,
                            'text_quantity': line,
                            'notes': None
                        })
        
        # 查找计算部分的详细用量
        calc_match = re.search(r'## 计算\s*\n(.*?)(?=\n##|\n$)', content, re.DOTALL)
        if calc_match:
            calc_section = calc_match.group(1)
            for line in calc_section.split('\n'):
                line = line.strip()
                # 支持破折号、星号和加号格式
                if (line.startswith('-') or line.startswith('*') or line.startswith('+')) and ('：' in line or ':' in line):
                    ingredient_text = line[1:].strip()
                    # 解析"食材名：用量"格式
                    separator = '：' if '：' in ingredient_text else ':'
                    if separator in ingredient_text:
                        name_part, quantity_part = ingredient_text.split(separator, 1)
                        name = name_part.strip()
                        
                        # 解析用量和单位  
                        quantity_match = re.search(r'(\d+(?:\.\d+)?)\s*(\w*)', quantity_part)
                        quantity = None
                        unit = None
                        if quantity_match:
                            try:
                                quantity = float(quantity_match.group(1))
                                unit = quantity_match.group(2) if quantity_match.group(2) else None
                            except:
                                pass
                                
                        # 过滤掉工具类物品
                        if name and not any(tool in name for tool in ['工具', '锅', '盆', '刀', '板', '杯', '勺']):
                            ingredients.append({
                                'name': name,
                                'quantity': quantity,
                                'unit': unit, 
                                'text_quantity': line,
                                'notes': None
                            })
                elif (line.startswith('-') or line.startswith('*') or line.startswith('+')) and line not in ['总量：', '- 总量：', '* 总量：', '+ 总量：']:
                    ingredient_text = line[1:].strip()
                    if ingredient_text and '份数' not in ingredient_text:
                        # 提取基本食材名（去掉用量信息）
                        name = re.split(r'\s+\d+', ingredient_text)[0].strip()
                        name = re.sub(r'[（(].*?[）)]', '', name).strip()
                        if name and not any(tool in name for tool in ['工具', '锅', '盆', '刀', '板']):
                            ingredients.append({
                                'name': name,
                                'quantity': None,
                                'unit': None,
                                'text_quantity': line,
                                'notes': None
                            })
        
        # 去重保持顺序
        seen_names = set()
        unique_ingredients = []
        for ing in ingredients:
            if ing['name'] not in seen_names:
                seen_names.add(ing['name'])
                unique_ingredients.append(ing)
        
        return unique_ingredients
        
    def parse_steps(self, content: str) -> List[Dict[str, Any]]:
        """解析制作步骤"""
        steps = []
        
        # 查找操作部分 - 修正正则表达式
        operations_match = re.search(r'## 操作\s*\n(.*?)(?=\n##|\n$)', content, re.DOTALL)
        if operations_match:
            operations_section = operations_match.group(1)
            step_num = 1
            
            for line in operations_section.split('\n'):
                line = line.strip()
                
                # 支持破折号格式: - 步骤描述
                if line.startswith('-') and len(line) > 2:
                    description = line[1:].strip()
                    if description and description != "--":
                        steps.append({
                            'step': step_num,
                            'description': description
                        })
                        step_num += 1
                        
                # 支持星号格式: * 步骤描述
                elif line.startswith('*') and len(line) > 2:
                    description = line[1:].strip()
                    if description and description != "--":
                        steps.append({
                            'step': step_num,
                            'description': description
                        })
                        step_num += 1
                        
                # 支持加号格式: + 步骤描述
                elif line.startswith('+') and len(line) > 2:
                    description = line[1:].strip()
                    if description and description != "--":
                        steps.append({
                            'step': step_num,
                            'description': description
                        })
                        step_num += 1
                        
                # 支持数字编号格式: 1. 步骤描述
                elif re.match(r'^\d+\.\s+', line):
                    description = re.sub(r'^\d+\.\s+', '', line).strip()
                    if description and description != "--":
                        steps.append({
                            'step': step_num,
                            'description': description
                        })
                        step_num += 1
        
        return steps
        
    def parse_tags(self, content: str, category: str, file_path: Path) -> List[str]:
        """生成标签"""
        tags = [category]
        
        # 从文件名添加标签
        dish_name = file_path.stem
        if dish_name not in tags:
            tags.append(dish_name)
            
        # 从难度添加标签
        difficulty = self.parse_difficulty(content)
        if difficulty >= 4:
            tags.append('复杂')
        elif difficulty <= 2:
            tags.append('简单')
            
        return tags
        
    def parse_recipe_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """解析单个菜谱文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取标题（菜谱名称）- 支持开头空行
            title_match = re.search(r'^\s*#\s+(.+)', content, re.MULTILINE)
            if not title_match:
                print(f"警告: {file_path} 没有找到标题")
                return None
                
            name = title_match.group(1).strip()
            
            # 获取分类
            category_dir = file_path.parent.name
            category = self.CATEGORY_MAP.get(category_dir, '其他')
            
            # 对于子目录中的文件，检查上级目录
            if category == '其他' and file_path.parent.parent.name in self.CATEGORY_MAP:
                category = self.CATEGORY_MAP[file_path.parent.parent.name]
            
            # 生成唯一ID
            relative_path = file_path.relative_to(self.dishes_dir)
            recipe_id = str(relative_path).replace('\\', '/').replace('.md', '')
            
            # 提取描述（第一段非标题文本）
            description_match = re.search(r'#[^#\n]+\n\n([^#\n][^\n]*(?:\n[^#\n][^\n]*)*)', content)
            description = description_match.group(1).strip() if description_match else ""
            
            # 解析各个部分
            difficulty = self.parse_difficulty(content)
            servings = self.parse_servings(content)
            ingredients = self.parse_ingredients(content)
            steps = self.parse_steps(content)
            tags = self.parse_tags(content, category, file_path)
            
            # 调试信息：检查步骤解析问题
            if len(steps) == 0:
                print(f"调试: {name} 没有解析到步骤")
            
            recipe = {
                'id': recipe_id,
                'name': name,
                'description': description,
                'source_path': str(relative_path),
                'category': category,
                'difficulty': difficulty,
                'servings': servings,
                'tags': tags,
                'ingredients': ingredients,
                'steps': steps
            }
            
            return recipe
            
        except Exception as e:
            print(f"解析 {file_path} 时出错: {e}")
            return None
            
    def generate_recipes_json(self, output_file: str = 'all_recipes.json') -> None:
        """生成菜谱JSON文件"""
        recipes = []
        
        # 遍历dishes目录下的所有markdown文件
        for md_file in self.dishes_dir.rglob('*.md'):
            # 跳过模板文件
            if 'template' in str(md_file):
                continue
                
            recipe = self.parse_recipe_file(md_file)
            if recipe:
                recipes.append(recipe)
                
        # 按分类和名称排序
        recipes.sort(key=lambda x: (x['category'], x['name']))
        
        # 写入JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
            
        print(f"生成完成! 共处理 {len(recipes)} 个菜谱，输出到 {output_file}")
        
        # 统计信息
        categories = {}
        for recipe in recipes:
            cat = recipe['category']
            categories[cat] = categories.get(cat, 0) + 1
            
        print("分类统计:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count} 个菜谱")


def main():
    """主函数"""
    parser = RecipeParser()
    parser.generate_recipes_json()


if __name__ == '__main__':
    main()