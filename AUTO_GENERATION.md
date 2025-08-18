# HowToCook 自动化菜谱JSON生成

## 概述

这个项目通过GitHub Actions自动从`dishes/`目录下的Markdown文件生成适配cooking模块的JSON格式菜谱数据。经过优化的解析器已实现**100%解析成功率**，支持324个菜谱的完整数据提取。

## 解析成果

- 📊 **324个菜谱**: 涵盖10个分类的完整菜谱集合
- 🎯 **100%解析成功率**: 所有菜谱均成功提取步骤和食材信息
- 🔧 **多格式支持**: 兼容破折号(-)、星号(*)、加号(+)三种列表格式
- ⚡ **实时更新**: 菜谱修改后自动重新生成JSON数据

## 文件结构

```
.github/
  workflows/
    generate-recipes.yml    # GitHub Action工作流
scripts/
  generate_recipes.py       # Python解析脚本
  test_compatibility.py     # 兼容性测试脚本
all_recipes.json           # 生成的菜谱数据文件 (324个菜谱)
```

## 自动化流程

### 触发条件
- 推送到main/master分支且修改了`dishes/**/*.md`文件
- 手动触发（workflow_dispatch）
- Pull Request包含对`dishes/**/*.md`的修改

### 工作流程
1. 检出代码
2. 设置Python环境
3. 运行解析脚本生成JSON
4. 检查是否有变更
5. 如果有变更，自动提交并推送

## JSON格式说明

生成的JSON完全适配domobot cooking模块，包含以下字段：

```json
{
  "id": "category/dish_name",           // 唯一标识
  "name": "菜谱名称",                    // 菜谱标题
  "description": "菜谱描述",             // 来自MD文件的描述段落
  "source_path": "dishes/path/file.md", // 源文件路径
  "category": "分类",                    // 根据目录映射的中文分类
  "difficulty": 3,                      // 难度等级(1-7星)
  "servings": 2,                        // 份量(人数)
  "tags": ["标签1", "标签2"],            // 自动生成的标签
  "ingredients": [                      // 食材列表
    {
      "name": "食材名",
      "quantity": 100,                  // 数量(可选)
      "unit": "g",                     // 单位(可选)
      "text_quantity": "- 食材 100g",   // 原始文本
      "notes": null                    // 备注(可选)
    }
  ],
  "steps": [                           // 制作步骤
    {
      "step": 1,
      "description": "步骤描述"
    }
  ]
}
```

## 分类映射

| 目录名 | 中文分类 | 菜谱数量 |
|--------|----------|----------|
| aquatic | 水产 | 24 |
| breakfast | 早餐 | 21 |
| condiment | 调料 | 9 |
| dessert | 甜品 | 18 |
| drink | 饮品 | 21 |
| meat_dish | 荤菜 | 97 |
| semi-finished | 半成品加工 | 10 |
| soup | 汤羹 | 22 |
| staple | 主食 | 48 |
| vegetable_dish | 素菜 | 54 |

**总计**: 324个菜谱

## 解析器特性

### 支持的Markdown格式

解析器经过优化，支持多种列表标记格式：

```markdown
# 菜谱名称

简要描述文字。

预估烹饪难度：★★★

## 必备原料和工具

- 食材1          # 破折号格式
* 食材2          # 星号格式  
+ 食材3          # 加号格式

## 计算

每次制作前需要确定计划做几份。一份正好够2个人食用

总量：
- 食材1：100g * 份数
* 食材2：50ml * 份数
+ 食材3：2个 * 份数

## 操作

- 步骤1的描述    # 破折号格式
* 步骤2的描述    # 星号格式
+ 步骤3的描述    # 加号格式
1. 步骤4的描述   # 数字编号格式
```

### 错误处理和调试

解析器包含完善的错误处理机制：
- 解析失败时输出详细调试信息
- 跳过无效或损坏的Markdown文件
- 统计并报告解析成功率

## 本地使用

### 安装依赖
```bash
# 无需额外依赖，Python标准库即可运行
cd HowToCook-master
```

### 运行生成脚本
```bash
python scripts/generate_recipes.py
```

### 运行兼容性测试
```bash
python scripts/test_compatibility.py
```

### 生成统计信息
脚本会输出：
- 处理的菜谱总数 (324个)
- 各分类的菜谱数量统计
- 解析过程中的警告信息
- 解析成功率 (100%)

## 注意事项

1. **编码问题**: 确保所有MD文件使用UTF-8编码
2. **文件名**: 避免在文件名中使用特殊字符
3. **格式一致性**: 保持Markdown格式的一致性以确保正确解析
4. **自动提交**: 修改dishes目录下的文件会触发自动重新生成JSON
5. **列表格式**: 支持`-`、`*`、`+`三种列表标记，无需统一格式

## cooking模块兼容性

生成的JSON格式完全兼容现有的cooking模块代码：

- ✅ 支持按分类搜索 (`recipe.get("category")`)
- ✅ 支持按名称搜索 (`recipe.get("name")`)  
- ✅ 支持按食材搜索 (`ingredient.get("name")`)
- ✅ 支持按标签搜索 (`recipe.get("tags")`)
- ✅ 支持难度显示 (`recipe.get("difficulty")`)
- ✅ 支持份量信息 (`recipe.get("servings")`)
- ✅ 支持详细食材和步骤展示
- ✅ 支持随机推荐功能

## 维护和扩展

### 添加新分类

在`scripts/generate_recipes.py`中的`CATEGORY_MAP`字典添加新映射：

```python
CATEGORY_MAP = {
    'new_category': '新分类名',
    # ... 其他分类
}
```

### 调整解析逻辑

主要解析方法位置：
- `parse_steps()`: 步骤解析逻辑，支持多种列表格式
- `parse_ingredients()`: 食材解析逻辑
- `parse_difficulty()`: 难度等级解析
- `parse_servings()`: 份量信息解析

### 正则表达式优化

当前解析器的关键正则表达式：
```python
# 操作部分匹配 (已修复)
operations_match = re.search(r'## 操作\s*\n(.*?)(?=\n##|\n$)', content, re.DOTALL)

# 支持多种列表格式
if (line.startswith('-') or line.startswith('*') or line.startswith('+')) and len(line) > 2:
```

## 测试和验证

### 解析成功率验证
```bash
# 运行完整测试
python scripts/test_compatibility.py

# 输出示例:
# ✅ 解析成功率: 100.0% (324/324)
# ✅ 所有菜谱均有完整的步骤信息
# ✅ JSON格式验证通过
```

### 常见问题排查

1. **步骤解析失败**: 检查是否使用了支持的列表格式 (`-`, `*`, `+`, `1.`)
2. **食材解析不完整**: 确认"## 必备原料和工具"和"## 计算"部分格式正确
3. **编码错误**: 确保文件保存为UTF-8编码

---

## 技术细节

**开发环境**: Python 3.x  
**依赖库**: 仅使用Python标准库 (re, json, pathlib, os)  
**解析引擎**: 自定义正则表达式解析器  
**数据格式**: UTF-8编码的JSON  
**测试覆盖**: 324个菜谱，10个分类  

🤖 该自动化系统由 Claude Code 协助设计开发，并持续优化至100%解析成功率