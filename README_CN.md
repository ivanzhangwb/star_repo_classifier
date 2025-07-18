# GitHub星标仓库分类器

一个全面的工具，用于获取、分类和分析您的GitHub星标仓库，按项目类型进行智能分类。生成精美的HTML报告和详细的Markdown文档。

## ✨ 功能特性

- **🔍 自动分类**：智能按项目类型对仓库进行分类
- **📊 丰富分析**：详细统计信息和可视化图表
- **🎨 精美报告**：支持HTML和Markdown格式的图表报告
- **⚙️ 灵活筛选**：按stars数、forks数、归档状态进行筛选
- **🔒 安全第一**：使用环境变量存储令牌
- **📈 可视化洞察**：显示类别分布、编程语言和趋势的图表
- **🚀 易于设置**：简单的安装和配置过程

## 🏷️ 分类类别

仓库将自动分类为以下类别：

- **Web开发** - 前端、后端、框架和Web工具
- **机器学习与AI** - ML框架、AI工具和神经网络
- **数据科学与分析** - 数据分析、可视化和Jupyter
- **DevOps与基础设施** - Docker、Kubernetes、CI/CD工具
- **移动开发** - iOS、Android、React Native、Flutter
- **数据库** - SQL、NoSQL和数据库工具
- **工具与实用程序** - CLI工具、自动化和实用程序
- **安全** - 加密、漏洞扫描和认证
- **文档与学习** - 教程、指南和学习资源
- **测试** - 测试框架和工具
- **游戏开发** - 游戏引擎和开发工具
- **区块链与加密** - 区块链、DeFi和Web3
- **API与网络** - REST API、GraphQL和网络工具
- **其他** - 其他所有内容

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/ivanzhangwb/star_repo_classifier.git
cd github-star-classifier

# 安装依赖
pip install -r requirements.txt
```

### 2. 设置GitHub令牌

创建GitHub个人访问令牌：

1. 前往 GitHub 设置 → 开发者设置 → 个人访问令牌
2. 点击"生成新令牌(classic)"
3. 选择作用域：`public_repo`（公开仓库）或 `repo`（私有仓库）
4. 复制生成的令牌

### 3. 配置环境

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入您的令牌
# GITHUB_TOKEN=your_github_token_here
# OUTPUT_DIR=./output
# MIN_STARS=0
# EXCLUDE_FORKS=true
# INCLUDE_ARCHIVED=false
```

### 4. 运行分类器

```bash
# 基本用法
python main.py

# 使用自定义令牌
python main.py --token YOUR_GITHUB_TOKEN

# 使用筛选器
python main.py --min-stars 100 --exclude-forks --output ./my_stars

# 包含已归档仓库
python main.py --include-archived

# 跳过报告生成以加快处理速度
python main.py --no-reports

# 详细输出
python main.py --verbose
```

## 📋 使用示例

### 基本分类
```bash
python main.py
```

### 筛选热门仓库
```bash
python main.py --min-stars 500 --exclude-forks --output ./popular_stars
```

### 包含所有仓库
```bash
python main.py --min-stars 0 --include-forks --include-archived
```

### 自定义输出位置
```bash
python main.py --output ~/Documents/github_stars_analysis
```

## 📊 输出文件

该工具在输出目录中生成以下文件：

### 数据文件
- `starred_repos_YYYYMMDD_HHMMSS.json` - 完整的仓库数据
- `starred_repos_YYYYMMDD_HHMMSS.csv` - 表格数据
- `statistics_YYYYMMDD_HHMMSS.json` - 汇总统计信息

### 报告
- `github_stars_report.html` - 带图表的交互式HTML报告
- `github_stars_report.md` - 详细的Markdown报告

### 可视化
- `category_distribution_YYYYMMDD_HHMMSS.png` - 类别分布饼图
- `language_distribution_YYYYMMDD_HHMMSS.png` - 编程语言柱状图
- `stars_analysis_YYYYMMDD_HHMMSS.png` - 按类别分析stars数

## 🛠️ 高级配置

### 环境变量

| 变量 | 说明 | 默认值 |
|----------|-------------|---------|
| `GITHUB_TOKEN` | 您的GitHub个人访问令牌 | 必需 |
| `OUTPUT_DIR` | 输出文件目录 | `./output` |
| `MIN_STARS` | 最小stars数筛选 | `0` |
| `EXCLUDE_FORKS` | 排除fork的仓库 | `true` |
| `INCLUDE_ARCHIVED` | 包含已归档的仓库 | `false` |
| `MAX_REPOS_PER_REQUEST` | API分页限制 | `100` |

### 自定义分类

您可以通过编辑`github_star_classifier.py`中的`PROJECT_CATEGORIES`字典来修改分类规则：

```python
PROJECT_CATEGORIES = {
    "您的类别": {
        "keywords": ["关键词1", "关键词2"],
        "topics": ["主题1", "主题2"]
    }
}
```

## 🔧 故障排除

### 常见问题

**"未提供GitHub令牌"**
```bash
# 确保您的.env文件存在或直接设置令牌
export GITHUB_TOKEN=your_token_here
python main.py
```

**"超出速率限制"**
- GitHub API有速率限制：未认证60次/小时，已认证5000次/小时
- 该工具自动处理分页，但大量stars可能会达到限制
- 等待后重试，或使用具有更高速率限制的令牌

**"未找到仓库"**
- 检查您的筛选器：`min-stars`、`exclude-forks`等
- 验证您的GitHub令牌是否具有必要权限
- 确保您已认证以访问私有星标仓库

### 调试模式

使用详细输出运行以查看详细进度：

```bash
python main.py --verbose
```

## 🧪 开发

### 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 以开发模式安装
pip install -r requirements.txt

# 运行测试
python -m pytest tests/
```

### 贡献

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature-name`
3. 进行更改
4. 如适用，添加测试
5. 提交：`git commit -am 'Add feature'`
6. 推送：`git push origin feature-name`
7. 提交拉取请求

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🤝 支持

- **问题**：通过 [GitHub Issues](https://github.com/ivanzhangwb/star_repo_classifier/issues) 报告错误和请求功能
- **讨论**：在 [GitHub Discussions](https://github.com/ivanzhangwb/star_repo_classifier/discussions) 中加入讨论
- **维基**：查看 [Wiki](https://github.com/ivanzhangwb/star_repo_classifier/wiki) 了解高级用法

## 🙏 致谢

- [PyGithub](https://pygithub.readthedocs.io/) 用于GitHub API集成
- [Pandas](https://pandas.pydata.org/) 用于数据分析
- [Seaborn](https://seaborn.pydata.org/) 和 [Matplotlib](https://matplotlib.org/) 用于可视化
- [Jinja2](https://jinja.palletsprojects.com/) 用于HTML模板

---

**愉快的星标探索！⭐**

由GitHub社区用❤️制作