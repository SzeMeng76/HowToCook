# HowToCook 自动化菜谱JSON生成

## 概述

这个项目通过GitHub Actions自动从`dishes/`目录下的Markdown文件生成适配cooking模块的JSON格式菜谱数据。

## 文件结构

```
.github/
  workflows/
    generate-recipes.yml    # GitHub Action工作流
scripts/
  generate_recipes.py       # Python解析脚本
all_recipes.json           # 生成的菜谱数据文件
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

| 目录名 | 中文分类 |
|--------|----------|
| aquatic | 水产 |
| breakfast | 早餐 |
| condiment | 调料 |
| dessert | 甜品 |
| drink | 饮品 |
| meat_dish | 荤菜 |
| semi-finished | 半成品加工 |
| soup | 汤羹 |
| staple | 主食 |
| vegetable_dish | 素菜 |

## 本地使用

### 安装依赖
```bash
pip install pyyaml
```

### 运行生成脚本
```bash
python scripts/generate_recipes.py
```

### 生成统计信息
脚本会输出：
- 处理的菜谱总数
- 各分类的菜谱数量统计
- 解析过程中的警告信息

## Markdown文件要求

为了正确解析，Markdown文件应该遵循以下格式：

```markdown
# 菜谱名称

简要描述文字。

预估烹饪难度：★★★

## 必备原料和工具

- 食材1
- 食材2

## 计算

每次制作前需要确定计划做几份。一份正好够2个人食用

总量：
- 食材1：100g * 份数
- 食材2：50ml * 份数

## 操作

- 步骤1的描述
- 步骤2的描述
```

## 注意事项

1. **编码问题**: 确保所有MD文件使用UTF-8编码
2. **文件名**: 避免在文件名中使用特殊字符
3. **格式一致性**: 保持Markdown格式的一致性以确保正确解析
4. **自动提交**: 修改dishes目录下的文件会触发自动重新生成JSON

## cooking模块兼容性

生成的JSON格式完全兼容现有的cooking模块代码：

- ✅ 支持按分类搜索 (`recipe.get("category")`)
- ✅ 支持按名称搜索 (`recipe.get("name")`)  
- ✅ 支持按食材搜索 (`ingredient.get("name")`)
- ✅ 支持按标签搜索 (`recipe.get("tags")`)
- ✅ 支持难度显示 (`recipe.get("difficulty")`)
- ✅ 支持份量信息 (`recipe.get("servings")`)
- ✅ 支持详细食材和步骤展示

## 维护

当添加新的菜谱分类或需要调整解析逻辑时，修改`scripts/generate_recipes.py`中的相应部分：

- `CATEGORY_MAP`: 添加新的分类映射
- `parse_*`方法: 调整解析逻辑
- 正则表达式: 适配不同的Markdown格式

---

🤖 该自动化系统由 Claude Code 协助设计开发