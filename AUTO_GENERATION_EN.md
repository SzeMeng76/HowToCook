# HowToCook Automated Recipe JSON Generation

[🇨🇳 中文版](./AUTO_GENERATION.md) | 🇺🇸 English

## Overview

This project automatically generates JSON recipe data compatible with cooking modules from Markdown files in the `dishes/` directory via GitHub Actions. The optimized parser has achieved **100% parsing success rate**, supporting complete data extraction from 324 recipes.

## Parsing Results

- 📊 **324 Recipes**: Complete recipe collection covering 10 categories
- 🎯 **100% Parsing Success Rate**: All recipes successfully extract steps and ingredients information
- 🔧 **Multi-format Support**: Compatible with dash (-), asterisk (*), and plus (+) list formats
- ⚡ **Real-time Updates**: Automatically regenerates JSON data when recipes are modified

## File Structure

```
.github/
  workflows/
    generate-recipes.yml    # GitHub Action workflow
scripts/
  generate_recipes.py       # Python parsing script
  test_compatibility.py     # Compatibility testing script
all_recipes.json           # Generated recipe data file (324 recipes)
```

## Automation Workflow

### Trigger Conditions
- Push to main/master branch with modifications to `dishes/**/*.md` files
- Manual trigger (workflow_dispatch)
- Pull Request containing modifications to `dishes/**/*.md`

### Workflow Steps
1. Checkout code
2. Setup Python environment
3. Run parsing script to generate JSON
4. Check for changes
5. Auto-commit and push if changes detected

## JSON Format Specification

Generated JSON is fully compatible with domobot cooking module, containing the following fields:

```json
{
  "id": "category/dish_name",           // Unique identifier
  "name": "Recipe Name",                // Recipe title
  "description": "Recipe description",   // Description from MD file
  "source_path": "dishes/path/file.md", // Source file path
  "category": "Category",               // Chinese category mapped from directory
  "difficulty": 3,                      // Difficulty level (1-7 stars)
  "servings": 2,                        // Serving size (people)
  "tags": ["Tag1", "Tag2"],             // Auto-generated tags
  "ingredients": [                      // Ingredients list
    {
      "name": "Ingredient Name",
      "quantity": 100,                  // Amount (optional)
      "unit": "g",                     // Unit (optional)
      "text_quantity": "- Ingredient 100g", // Original text
      "notes": null                    // Notes (optional)
    }
  ],
  "steps": [                           // Cooking steps
    {
      "step": 1,
      "description": "Step description"
    }
  ]
}
```

## Category Mapping

| Directory | Chinese Category | Recipe Count |
|-----------|------------------|--------------|
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

**Total**: 324 recipes

## Parser Features

### Supported Markdown Formats

The parser is optimized to support multiple list marker formats:

```markdown
# Recipe Name

Brief description text.

Estimated cooking difficulty: ★★★

## Essential Ingredients and Tools

- Ingredient1          # Dash format
* Ingredient2          # Asterisk format  
+ Ingredient3          # Plus format

## Calculation

Determine how many servings to make before cooking. One serving feeds 2 people.

Total amount:
- Ingredient1: 100g * servings
* Ingredient2: 50ml * servings
+ Ingredient3: 2 pieces * servings

## Instructions

- Step 1 description    # Dash format
* Step 2 description    # Asterisk format
+ Step 3 description    # Plus format
1. Step 4 description   # Numbered format
```

### Error Handling and Debugging

The parser includes comprehensive error handling mechanisms:
- Outputs detailed debugging information on parsing failures
- Skips invalid or corrupted Markdown files
- Reports parsing success statistics

## Local Usage

### Install Dependencies
```bash
# No additional dependencies required, Python standard library only
cd HowToCook-master
```

### Run Generation Script
```bash
python scripts/generate_recipes.py
```

### Run Compatibility Tests
```bash
python scripts/test_compatibility.py
```

### Generation Statistics
The script outputs:
- Total number of processed recipes (324)
- Recipe count statistics by category
- Warning messages during parsing
- Parsing success rate (100%)

## Important Notes

1. **Encoding Issues**: Ensure all MD files use UTF-8 encoding
2. **File Names**: Avoid special characters in file names
3. **Format Consistency**: Maintain Markdown format consistency for proper parsing
4. **Auto-commit**: Modifying files in dishes directory triggers automatic JSON regeneration
5. **List Formats**: Supports `-`, `*`, `+` list markers, no need for unified format

## Cooking Module Compatibility

Generated JSON format is fully compatible with existing cooking module code:

- ✅ Supports category search (`recipe.get("category")`)
- ✅ Supports name search (`recipe.get("name")`)  
- ✅ Supports ingredient search (`ingredient.get("name")`)
- ✅ Supports tag search (`recipe.get("tags")`)
- ✅ Supports difficulty display (`recipe.get("difficulty")`)
- ✅ Supports serving information (`recipe.get("servings")`)
- ✅ Supports detailed ingredient and step display
- ✅ Supports random recommendation feature

## Maintenance and Extension

### Adding New Categories

Add new mappings to the `CATEGORY_MAP` dictionary in `scripts/generate_recipes.py`:

```python
CATEGORY_MAP = {
    'new_category': 'New Category Name',
    # ... other categories
}
```

### Adjusting Parsing Logic

Main parsing method locations:
- `parse_steps()`: Step parsing logic, supports multiple list formats
- `parse_ingredients()`: Ingredient parsing logic
- `parse_difficulty()`: Difficulty level parsing
- `parse_servings()`: Serving information parsing

### Regular Expression Optimization

Key regular expressions in current parser:
```python
# Operations section matching (fixed)
operations_match = re.search(r'## 操作\s*\n(.*?)(?=\n##|\n$)', content, re.DOTALL)

# Support multiple list formats
if (line.startswith('-') or line.startswith('*') or line.startswith('+')) and len(line) > 2:
```

## Testing and Validation

### Parsing Success Rate Verification
```bash
# Run complete tests
python scripts/test_compatibility.py

# Example output:
# ✅ Parsing success rate: 100.0% (324/324)
# ✅ All recipes have complete step information
# ✅ JSON format validation passed
```

### Common Issue Troubleshooting

1. **Step parsing failure**: Check if supported list formats are used (`-`, `*`, `+`, `1.`)
2. **Incomplete ingredient parsing**: Confirm "## 必备原料和工具" and "## 计算" sections are properly formatted
3. **Encoding errors**: Ensure files are saved with UTF-8 encoding

---

## Technical Details

**Development Environment**: Python 3.x  
**Dependencies**: Python standard library only (re, json, pathlib, os)  
**Parsing Engine**: Custom regular expression parser  
**Data Format**: UTF-8 encoded JSON  
**Test Coverage**: 324 recipes, 10 categories  

🤖 This automation system was designed and developed with assistance from Claude Code, continuously optimized to achieve 100% parsing success rate