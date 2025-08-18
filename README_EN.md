# Programmer's Guide to Cooking

[![build](https://github.com/SzeMeng76/HowToCook/actions/workflows/build.yml/badge.svg)](https://github.com/SzeMeng76/HowToCook/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/SzeMeng76/HowToCook)](./LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/SzeMeng76/HowToCook)](https://github.com/SzeMeng76/HowToCook/graphs/contributors)
[![npm](https://img.shields.io/npm/v/how-to-cook)](https://www.npmjs.com/package/how-to-cook)
![Man hours](https://manhours.aiursoft.cn/r/github.com/szemeng76/howtocook.svg)
[![Docker](https://img.shields.io/badge/docker-latest-blue?logo=docker)](https://github.com/SzeMeng76/HowToCook/pkgs/container/how-to-cook)

[🇨🇳 中文版](./README.md) | 🇺🇸 English

Recently staying at home for cooking, as a programmer, I occasionally search for recipes and cooking methods online. However, these recipes are often written in various confusing ways, with ingredients mysteriously appearing in the middle. This is extremely unfriendly for programmers who are accustomed to formal languages.

Therefore, I plan to search for recipes myself and combine them with actual cooking experience to organize common cooking methods with clearer and more precise descriptions, making it easier for programmers to cook at home.

Similarly, I hope it will be a community-driven and maintained open source project, enabling more people to work together on an interesting repository. So contributions are very welcome~

## Automated JSON Generation

This project provides automated JSON data generation functionality, compatible with Telegram cooking bots and other applications:

- 🤖 **Automated Workflow**: Automatically generates structured JSON data from Markdown files via GitHub Actions
- 📊 **Complete Parsing**: Supports 324 recipes with 100% parsing success rate
- 🔄 **Real-time Updates**: Automatically regenerates JSON when recipe files are modified
- 🎯 **Format Compatible**: Fully compatible with cooking module data structure requirements

View detailed documentation: [AUTO_GENERATION.md](./AUTO_GENERATION.md)

## Local Deployment

If you need to deploy the recipe web service locally, you can run the following commands after installing Docker:

```bash
docker pull ghcr.io/szemeng76/how-to-cook:latest
docker run -d -p 5000:80 ghcr.io/szemeng76/how-to-cook:latest
```

For PDF version download, visit [/document.pdf](https://cook.aiursoft.cn/document.pdf) in your browser

## How to Contribute

For discovered issues, directly modify and submit a Pull request.

When writing new recipes, please copy and modify the existing recipe template: [Sample Dish](https://github.com/SzeMeng76/HowToCook/blob/master/dishes/template/%E7%A4%BA%E4%BE%8B%E8%8F%9C/%E7%A4%BA%E4%BE%8B%E8%8F%9C.md?plain=1).

## Kitchen Setup

- [Kitchen Preparation](tips/厨房准备.md)
- [How to Choose What to Eat](tips/如何选择现在吃什么.md)
- [Food Incompatibilities and Taboos](tips/食材相克与禁忌.md)
- [Pressure Cooker](tips/learn/高压力锅.md)
- [Air Fryer](tips/learn/空气炸锅.md)
- [Removing Fishy Smell](tips/learn/去腥.md)
- [Food Safety](tips/learn/食品安全.md)
- [Microwave](tips/learn/微波炉.md)
- [Learning Blanching](tips/learn/学习焯水.md)
- [Learning Stir-frying and Pan-frying](tips/learn/学习炒与煎.md)
- [Learning Cold Dishes](tips/learn/学习凉拌.md)
- [Learning Marinating](tips/learn/学习腌.md)
- [Learning Steaming](tips/learn/学习蒸.md)
- [Learning Boiling](tips/learn/学习煮.md)

## Recipes

### Index by Difficulty

- [1 Star Difficulty](starsystem/1Star.md)
- [2 Star Difficulty](starsystem/2Star.md)
- [3 Star Difficulty](starsystem/3Star.md)
- [4 Star Difficulty](starsystem/4Star.md)
- [5 Star Difficulty](starsystem/5Star.md)

### Vegetarian Dishes

- [Candied Sweet Potato](dishes/vegetable_dish/拔丝土豆/拔丝土豆.md)
- [Blanched Choy Sum](dishes/vegetable_dish/白灼菜心/白灼菜心.md)
- [Cabbage Scrambled Eggs with Vermicelli](dishes/vegetable_dish/包菜炒鸡蛋粉丝/包菜炒鸡蛋粉丝.md)
- [Spinach Scrambled Eggs](dishes/vegetable_dish/菠菜炒鸡蛋/菠菜炒鸡蛋.md)
- [Stir-fried Silky Eggs](dishes/vegetable_dish/炒滑蛋/炒滑蛋.md)
- [Stir-fried Eggplant](dishes/vegetable_dish/炒茄子.md)
- [Stir-fried Greens](dishes/vegetable_dish/炒青菜.md)
- [Scallion Pan-fried Tofu](dishes/vegetable_dish/葱煎豆腐.md)
- [Crispy Tofu](dishes/vegetable_dish/脆皮豆腐.md)
- [Di San Xian (Three Fresh)](dishes/vegetable_dish/地三鲜.md)
- [Dry Pot Cauliflower](dishes/vegetable_dish/干锅花菜/干锅花菜.md)
- [Oyster Sauce Three Fresh Mushrooms](dishes/vegetable_dish/蚝油三鲜菇/蚝油三鲜菇.md)
- [Oyster Sauce Lettuce](dishes/vegetable_dish/蚝油生菜.md)
- [Braised Winter Melon](dishes/vegetable_dish/红烧冬瓜/红烧冬瓜.md)
- [Braised Eggplant](dishes/vegetable_dish/红烧茄子.md)
- [Tiger Skin Green Peppers](dishes/vegetable_dish/虎皮青椒/虎皮青椒.md)
- [Preserved Plum Edamame](dishes/vegetable_dish/话梅煮毛豆/话梅煮毛豆.md)
- [Steamed Egg Custard](dishes/vegetable_dish/鸡蛋羹/鸡蛋羹.md)
- [Microwave Steamed Egg Custard](dishes/vegetable_dish/鸡蛋羹/微波炉鸡蛋羹.md)
- [Steam Oven Egg Custard](dishes/vegetable_dish/鸡蛋羹/蒸箱鸡蛋羹.md)

### Meat Dishes

- [Pakistani Beef Curry](dishes/meat_dish/巴基斯坦牛肉咖喱/巴基斯坦牛肉咖喱.md)
- [Cabbage Pork Stewed Vermicelli](dishes/meat_dish/白菜猪肉炖粉条.md)
- [Steamed White Eel with Black Bean Sauce](dishes/meat_dish/豉汁蒸白鱔/豉汁蒸白鱔食谱.md)
- [Elbow with Handle](dishes/meat_dish/带把肘子.md)
- [Winter Melon Stuffed with Meat](dishes/meat_dish/冬瓜酿肉/冬瓜酿肉.md)
- [Black Bean Dace with Lettuce](dishes/meat_dish/豆豉鲮鱼油麦菜/豆豉鲮鱼油麦菜.md)
- [Tomato Red Sauce](dishes/meat_dish/番茄红酱.md)
- [Steamed Pork with Rice Powder](dishes/meat_dish/粉蒸肉.md)
- [Dry-fried Young Chicken](dishes/meat_dish/干煸仔鸡/干煸仔鸡.md)
- [Kung Pao Chicken](dishes/meat_dish/宫保鸡丁/宫保鸡丁.md)
- [Sweet and Sour Pork](dishes/meat_dish/咕噜肉.md)
- [Cantonese Radish Beef Brisket](dishes/meat_dish/广式萝卜牛腩/广式萝卜牛腩.md)
- [Guizhou Spicy Chicken](dishes/meat_dish/贵州辣子鸡/贵州辣子鸡.md)

### Seafood

- [Blanched Shrimp](dishes/aquatic/白灼虾/白灼虾.md)
- [Bream Fish Stewed with Tofu](dishes/aquatic/鳊鱼炖豆腐/鳊鱼炖豆腐.md)
- [Razor Clam with Egg](dishes/aquatic/蛏抱蛋/蛏抱蛋.md)
- [Scallion Braised Sea Cucumber](dishes/aquatic/葱烧海参/葱烧海参.md)
- [Scallion Oil Mandarin Fish](dishes/aquatic/葱油桂鱼/葱油桂鱼.md)
- [Pan-fried Argentine Red Shrimp](dishes/aquatic/干煎阿根廷红虾/干煎阿根廷红虾.md)
- [Braised Carp](dishes/aquatic/红烧鲤鱼.md)
- [Braised Fish](dishes/aquatic/红烧鱼.md)
- [Braised Fish Head](dishes/aquatic/红烧鱼头.md)

### Breakfast

- [Tea Eggs](dishes/breakfast/茶叶蛋.md)
- [Egg Pan-fried Rice Cake](dishes/breakfast/蛋煎糍粑.md)
- [Longan Red Date Porridge](dishes/breakfast/桂圆红枣粥.md)
- [Egg Sandwich](dishes/breakfast/鸡蛋三明治.md)
- [Pan-fried Dumplings](dishes/breakfast/煎饺.md)
- [Tuna Sauce Sandwich](dishes/breakfast/金枪鱼酱三明治.md)
- [Air Fryer Bread Slices](dishes/breakfast/空气炸锅面包片.md)
- [American Scrambled Eggs](dishes/breakfast/美式炒蛋.md)

### Staple Foods

- [Stir-fried Instant Noodles](dishes/staple/炒方便面.md)
- [Stir-fried Rice Noodles](dishes/staple/炒河粉.md)
- [Stir-fried Mung Bean Jelly](dishes/staple/炒凉粉/炒凉粉.md)
- [Stir-fried Bread](dishes/staple/炒馍.md)
- [Stir-fried Rice Cake](dishes/staple/炒年糕.md)
- [Stir-fried Spaghetti](dishes/staple/炒意大利面/炒意大利面.md)
- [Scallion Oil Noodles](dishes/staple/葱油拌面.md)
- [Omurice](dishes/staple/蛋包饭.md)
- [Egg Fried Rice](dishes/staple/蛋炒饭.md)

### Semi-finished Products

- [Semi-finished Pasta](dishes/semi-finished/半成品意面.md)
- [Air Fryer Chicken Wings](dishes/semi-finished/空气炸锅鸡翅中/空气炸锅鸡翅中.md)
- [Air Fryer Lamb Chops](dishes/semi-finished/空气炸锅羊排/空气炸锅羊排.md)
- [Lazy Egg Tarts](dishes/semi-finished/懒人蛋挞/懒人蛋挞.md)
- [Cold Noodles](dishes/semi-finished/凉皮.md)

### Soups and Porridge

- [Yellow Catfish Tofu Soup](dishes/soup/昂刺鱼豆腐汤/昂刺鱼豆腐汤.md)
- [Tangerine Peel Spare Ribs Soup](dishes/soup/陈皮排骨汤/陈皮排骨汤.md)
- [Tomato Beef Egg Drop Soup](dishes/soup/番茄牛肉蛋花汤.md)
- [Thickened Mushroom Soup](dishes/soup/勾芡香菇汤/勾芡香菇汤.md)
- [Enoki Mushroom Soup](dishes/soup/金针菇汤.md)

### Beverages

- [Ponkan Tea](dishes/drink/耙耙柑茶/耙耙柑茶.md)
- [Passion Fruit Orange Special](dishes/drink/百香果橙子特调/百香果橙子特调.md)
- [Ice Jelly](dishes/drink/冰粉/冰粉.md)
- [Pineapple Coffee Special](dishes/drink/菠萝咖啡特调/菠萝咖啡特调.md)
- [Winter Melon Tea](dishes/drink/冬瓜茶.md)

### Condiments and Other Ingredients

- [Strawberry Jam](dishes/condiment/草莓酱/草莓酱.md)
- [Scallion Oil](dishes/condiment/葱油.md)
- [Simple Caramel Color](dishes/condiment/简易版炒糖色.md)
- [Garlic Soy Sauce](dishes/condiment/蒜香酱油.md)
- [Sweet and Sour Sauce](dishes/condiment/糖醋汁.md)

### Desserts

- [Oreo Ice Cream](dishes/dessert/奥利奥冰淇淋/奥利奥冰淇淋.md)
- [Strawberry Ice Cream](dishes/dessert/草莓冰淇淋/草莓冰淇淋.md)
- [Candied Taro](dishes/dessert/反沙芋头/反沙芋头.md)
- [Herbal Jelly](dishes/dessert/龟苓膏/龟苓膏.md)
- [Red Pomelo Cake](dishes/dessert/红柚蛋糕/红柚蛋糕.md)

## Advanced Cooking Knowledge

If you have made many of the above dishes, have gotten started with cooking, and want to learn more advanced cooking techniques, please continue reading the following content:

- [Seasoning Techniques](tips/advanced/辅料技巧.md)
- [Advanced Professional Terminology](tips/advanced/高级专业术语.md)
- [Caramel Color Preparation](tips/advanced/糖色的炒制.md)
- [Oil Temperature Judgment Techniques](tips/advanced/油温判断技巧.md)

## Recommended Derivative Works

- [HowToCook-mcp Make AI assistants your personal chef for meal planning](https://github.com/worryzyy/HowToCook-mcp)
- [HowToCook-py-mcp Make AI assistants your personal chef for meal planning (Python)](https://github.com/DusKing1/howtocook-py-mcp)

---

## Fork Information

This is a fork of the original [Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook) project with added automated JSON generation features for cooking bot integration.

### What's New in This Fork

- 🚀 **GitHub Actions Integration**: Automated JSON generation workflow
- 📱 **Telegram Bot Compatibility**: Structured data for cooking bots
- 🎯 **100% Parsing Success**: Enhanced Markdown parser supporting multiple list formats
- 🔧 **Continuous Integration**: Auto-updates when recipes are modified

**Original Project**: [github.com/Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook)  
**Fork Maintainer**: [@SzeMeng76](https://github.com/SzeMeng76)