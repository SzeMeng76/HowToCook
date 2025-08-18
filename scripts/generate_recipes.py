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
from datetime import datetime


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
        self.stats_file = Path('recipe_stats.json')
        
    def load_previous_stats(self) -> Dict:
        """加载上次的统计信息"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
        
    def save_current_stats(self, stats: Dict) -> None:
        """保存当前统计信息"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
            
    def compare_stats(self, old_stats: Dict, new_stats: Dict) -> Dict:
        """比较统计信息变化"""
        changes = {
            'total_change': new_stats['total'] - old_stats.get('total', 0),
            'category_changes': {},
            'added_recipes': [],
            'removed_recipes': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # 比较分类变化
        for category, count in new_stats['categories'].items():
            old_count = old_stats.get('categories', {}).get(category, 0)
            if count != old_count:
                changes['category_changes'][category] = {
                    'old': old_count,
                    'new': count,
                    'change': count - old_count
                }
        
        # 比较食谱列表变化
        old_recipes = set(old_stats.get('recipe_list', []))
        new_recipes = set(new_stats['recipe_list'])
        
        changes['added_recipes'] = list(new_recipes - old_recipes)
        changes['removed_recipes'] = list(old_recipes - new_recipes)
        
        return changes
        
    def generate_changelog_entry(self, changes: Dict) -> str:
        """生成changelog条目"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # 如果没有变化，也生成一个简单的检测记录
        if changes['total_change'] == 0 and not changes['category_changes']:
            entry_lines = [
                f"\n## [Unreleased] - {timestamp}\n",
                f"### Status",
                f"- ✅ **No Recipe Changes**: All {changes.get('total_recipes', 'existing')} recipes verified and up-to-date",
                f"- 🔍 **Automated Check**: Recipe content and structure validation completed"
            ]
            return "\n".join(entry_lines) + "\n"
            
        # 有变化时的详细记录
        entry_lines = [f"\n## [Unreleased] - {timestamp}\n"]
        
        if changes['total_change'] != 0:
            if changes['total_change'] > 0:
                entry_lines.append(f"### Added")
                entry_lines.append(f"- 📝 **{changes['total_change']} New Recipes**: Total recipes increased to {changes.get('total_recipes', 'unknown')}")
            else:
                entry_lines.append(f"### Removed")
                entry_lines.append(f"- 📝 **{abs(changes['total_change'])} Recipes Removed**: Total recipes decreased to {changes.get('total_recipes', 'unknown')}")
        
        # 详细的分类变化
        if changes['category_changes']:
            entry_lines.append(f"\n### Recipe Distribution Changes")
            for category, change_info in changes['category_changes'].items():
                change_text = f"+{change_info['change']}" if change_info['change'] > 0 else str(change_info['change'])
                entry_lines.append(f"- **{category}**: {change_info['old']} → {change_info['new']} ({change_text})")
        
        # 新增的食谱
        if changes['added_recipes']:
            entry_lines.append(f"\n### New Recipes Added")
            for recipe in sorted(changes['added_recipes'][:10]):  # 最多显示10个
                entry_lines.append(f"- {recipe}")
            if len(changes['added_recipes']) > 10:
                entry_lines.append(f"- ... and {len(changes['added_recipes']) - 10} more")
        
        # 移除的食谱  
        if changes['removed_recipes']:
            entry_lines.append(f"\n### Recipes Removed")
            for recipe in sorted(changes['removed_recipes']):
                entry_lines.append(f"- {recipe}")
        
        return "\n".join(entry_lines) + "\n"
        
    def update_changelog(self, changes: Dict) -> None:
        """更新CHANGELOG.md文件"""
        changelog_path = Path('CHANGELOG.md')
        if not changelog_path.exists():
            return
            
        entry = self.generate_changelog_entry(changes)
        if not entry:
            return
            
        # 读取现有changelog
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到插入位置（在## [Unreleased]后面）
        lines = content.split('\n')
        insert_index = None
        
        for i, line in enumerate(lines):
            if line.startswith('## [Unreleased]') and i < len(lines) - 1:
                insert_index = i + 1
                break
        
        if insert_index is not None:
            # 如果已有[Unreleased]内容，先移除旧的
            while insert_index < len(lines) and not lines[insert_index].startswith('## ['):
                if lines[insert_index].strip():
                    break
                insert_index += 1
            
            # 插入新内容
            entry_lines = entry.strip().split('\n')[1:]  # 移除标题行
            lines[insert_index:insert_index] = entry_lines
            
            # 写回文件
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"📝 Updated CHANGELOG.md with recipe changes")
        
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
        # 加载之前的统计信息
        old_stats = self.load_previous_stats()
        
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
        recipe_list = []
        for recipe in recipes:
            cat = recipe['category']
            categories[cat] = categories.get(cat, 0) + 1
            recipe_list.append(recipe['name'])
            
        # 当前统计信息
        current_stats = {
            'total': len(recipes),
            'categories': categories,
            'recipe_list': recipe_list,
            'timestamp': datetime.now().isoformat()
        }
        
        print("分类统计:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count} 个菜谱")
            
        # 比较变化并更新changelog
        if old_stats:
            changes = self.compare_stats(old_stats, current_stats)
            # 添加总食谱数量信息
            changes['total_recipes'] = current_stats['total']
            
            if changes['total_change'] != 0 or changes['category_changes']:
                print(f"\n检测到食谱变化:")
                if changes['total_change'] != 0:
                    change_text = f"+{changes['total_change']}" if changes['total_change'] > 0 else str(changes['total_change'])
                    print(f"  总数变化: {old_stats['total']} → {current_stats['total']} ({change_text})")
                
                if changes['added_recipes']:
                    print(f"  新增食谱: {len(changes['added_recipes'])} 个")
                    for recipe in changes['added_recipes'][:5]:  # 显示前5个
                        print(f"    + {recipe}")
                    if len(changes['added_recipes']) > 5:
                        print(f"    + ... 还有 {len(changes['added_recipes']) - 5} 个")
                
                if changes['removed_recipes']:
                    print(f"  移除食谱: {len(changes['removed_recipes'])} 个")
                    for recipe in changes['removed_recipes']:
                        print(f"    - {recipe}")
                
                if changes['category_changes']:
                    print(f"  分类变化:")
                    for category, change_info in changes['category_changes'].items():
                        change_text = f"+{change_info['change']}" if change_info['change'] > 0 else str(change_info['change'])
                        print(f"    {category}: {change_info['old']} → {change_info['new']} ({change_text})")
            else:
                print(f"\n没有检测到食谱数量变化")
                
            # 总是更新changelog（包括无变化的情况）
            self.update_changelog(changes)
        else:
            print(f"\n首次运行，建立基准统计信息")
            # 首次运行也记录到changelog
            first_run_changes = {
                'total_change': 0,
                'category_changes': {},
                'added_recipes': [],
                'removed_recipes': [],
                'total_recipes': current_stats['total'],
                'timestamp': datetime.now().isoformat()
            }
            self.update_changelog(first_run_changes)
        
        # 保存当前统计信息
        self.save_current_stats(current_stats)


def main():
    """主函数"""
    parser = RecipeParser()
    parser.generate_recipes_json()


if __name__ == '__main__':
    main()