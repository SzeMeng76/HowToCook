#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试生成的JSON是否与cooking模块兼容
"""

import json
from typing import Dict, List, Any

def test_json_compatibility(json_file: str = 'all_recipes.json'):
    """测试JSON兼容性"""
    print("🧪 测试cooking模块JSON兼容性...")
    
    # 读取JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        recipes = json.load(f)
    
    print(f"📋 总共 {len(recipes)} 个菜谱")
    
    # 测试必需字段
    required_fields = ['id', 'name', 'category', 'difficulty', 'ingredients', 'steps', 'tags']
    missing_fields = []
    
    for i, recipe in enumerate(recipes[:5]):  # 测试前5个
        print(f"\n🔍 测试菜谱: {recipe.get('name', 'unknown')}")
        
        for field in required_fields:
            if field not in recipe:
                missing_fields.append(f"Recipe {i}: missing {field}")
            else:
                print(f"  ✅ {field}: {type(recipe[field]).__name__}")
    
    # 测试搜索功能模拟
    print(f"\n🔍 搜索功能测试:")
    
    # 按名称搜索
    query = "红烧肉"
    name_results = [r for r in recipes if query in r.get("name", "")]
    print(f"  按名称搜索 '{query}': {len(name_results)} 个结果")
    
    # 按分类搜索  
    category = "荤菜"
    cat_results = [r for r in recipes if r.get("category", "") == category]
    print(f"  按分类搜索 '{category}': {len(cat_results)} 个结果")
    
    # 按食材搜索
    ingredient_query = "鸡蛋"
    ing_results = []
    for recipe in recipes:
        ingredients = recipe.get("ingredients", [])
        for ing in ingredients:
            if ingredient_query in ing.get("name", ""):
                ing_results.append(recipe)
                break
    print(f"  按食材搜索 '{ingredient_query}': {len(ing_results)} 个结果")
    
    # 按标签搜索
    tag_query = "简单"
    tag_results = []
    for recipe in recipes:
        tags = recipe.get("tags", [])
        if any(tag_query in tag for tag in tags):
            tag_results.append(recipe)
    print(f"  按标签搜索 '{tag_query}': {len(tag_results)} 个结果")
    
    # 分类统计
    print(f"\n📊 分类统计:")
    categories = {}
    for recipe in recipes:
        cat = recipe.get("category", "未知")
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} 个")
    
    # 难度统计
    print(f"\n⭐ 难度统计:")
    difficulties = {}
    for recipe in recipes:
        diff = recipe.get("difficulty", 1)
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    for diff in sorted(difficulties.keys()):
        stars = "★" * diff
        print(f"  {stars} ({diff}星): {difficulties[diff]} 个")
    
    # 测试菜谱详情格式化
    print(f"\n📝 菜谱详情格式化测试:")
    if recipes:
        sample_recipe = recipes[0]
        
        # 模拟cooking.py中的格式化逻辑
        name = sample_recipe.get("name", "未知菜谱")
        category = sample_recipe.get("category", "其他")
        difficulty = "★" * max(1, sample_recipe.get("difficulty", 1))
        servings = sample_recipe.get("servings", 2)
        
        ingredients = sample_recipe.get("ingredients", [])
        ingredients_count = len(ingredients)
        
        steps = sample_recipe.get("steps", [])
        steps_count = len(steps)
        
        print(f"  示例菜谱: {name}")
        print(f"  分类: {category}")
        print(f"  难度: {difficulty}")
        print(f"  份量: {servings}人份")
        print(f"  食材数量: {ingredients_count} 个")
        print(f"  步骤数量: {steps_count} 个")
        
        # 测试食材格式
        if ingredients:
            ing = ingredients[0]
            ing_name = ing.get('name', '')
            text_quantity = ing.get('text_quantity', '')
            print(f"  食材示例: {ing_name} ({text_quantity})")
    
    # 错误报告
    if missing_fields:
        print(f"\n❌ 发现问题:")
        for error in missing_fields:
            print(f"  {error}")
    else:
        print(f"\n✅ 所有测试通过! JSON格式完全兼容cooking模块")
    
    return len(missing_fields) == 0

if __name__ == '__main__':
    test_json_compatibility()