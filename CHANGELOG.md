# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-01-18

### Added
- 🚀 **Automated JSON Generation System**: Complete GitHub Actions workflow for recipe data generation
- 🎯 **100% Parsing Success Rate**: Enhanced parser supporting 324 recipes across 10 categories
- 🔧 **Multi-format Support**: Compatible with dash (-), asterisk (*), and plus (+) list formats
- 📱 **Telegram Bot Integration**: Structured JSON data for cooking bot applications
- 🌍 **Bilingual Documentation**: Complete English and Chinese documentation with language switchers
- 🧪 **Compatibility Testing**: Automated testing script for JSON format validation
- 📊 **Recipe Statistics**: Detailed breakdown by categories with counts

### Enhanced
- **Parser Engine**: Custom regex-based parser with comprehensive error handling
- **File Structure**: Organized scripts and workflows for better maintainability
- **Documentation**: Comprehensive technical documentation with examples and troubleshooting

### Fixed
- **Step Parsing Issues**: Resolved regex pattern problems that caused parsing failures
- **List Format Recognition**: Added support for multiple Markdown list formats
- **Encoding Compatibility**: Ensured UTF-8 handling across all recipe files

### Technical Details
- **Total Recipes**: 324 (100% parsing success)
- **Categories**: 10 (水产, 早餐, 调料, 甜品, 饮品, 荤菜, 半成品加工, 汤羹, 主食, 素菜)
- **Supported Formats**: Dash (-), Asterisk (*), Plus (+), Numbered (1.)
- **Dependencies**: Python standard library only
- **Output Format**: UTF-8 encoded JSON

### Recipe Distribution
- 荤菜 (Meat Dishes): 97 recipes
- 素菜 (Vegetarian): 54 recipes  
- 主食 (Staples): 48 recipes
- 水产 (Seafood): 24 recipes
- 汤羹 (Soups): 22 recipes
- 早餐 (Breakfast): 21 recipes
- 饮品 (Beverages): 21 recipes
- 甜品 (Desserts): 18 recipes
- 半成品加工 (Semi-finished): 10 recipes
- 调料 (Condiments): 9 recipes

## [1.0.0] - Original HowToCook Project

### Base Features
- 📚 **Recipe Collection**: Community-driven collection of cooking recipes
- 📝 **Markdown Format**: Structured recipe documentation in Markdown
- 🔧 **Difficulty Rating**: Star-based difficulty system
- 🏠 **Local Deployment**: Docker-based web service
- 📖 **PDF Export**: Downloadable PDF version
- 🌟 **Community Contributions**: Open-source collaborative development

---

## How to Read This Changelog

### Symbols
- 🚀 Major new features
- 🎯 Performance improvements
- 🔧 Technical enhancements
- 📱 Integration features
- 🌍 Internationalization
- 🧪 Testing improvements
- 📊 Analytics/Statistics
- 📚 Documentation
- 📝 Content updates
- 🔧 Bug fixes
- ⚡ Performance optimizations

### Version Types
- **Major (x.0.0)**: Breaking changes or major new features
- **Minor (x.y.0)**: New features, backwards compatible
- **Patch (x.y.z)**: Bug fixes, backwards compatible

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes
- **Enhanced**: Improvements to existing features
- **Technical Details**: Implementation specifics

---

*This changelog is automatically maintained. Recipe count changes are tracked via the generation script.*