# GitHub Starred Repositories Classifier

A comprehensive tool to fetch, classify, and analyze your GitHub starred repositories by project type. Generates beautiful HTML reports and detailed Markdown documentation.

## ✨ Features

- **🔍 Automatic Classification**: Intelligently categorizes repositories by project type
- **📊 Rich Analytics**: Detailed statistics and visualizations
- **🎨 Beautiful Reports**: HTML and Markdown formats with charts
- **⚙️ Flexible Filtering**: Filter by stars, forks, archived status
- **🔒 Security First**: Uses environment variables for tokens
- **📈 Visual Insights**: Charts showing category distribution, languages, and trends
- **🚀 Easy Setup**: Simple installation and configuration

## 🏷️ Classification Categories

Repositories are automatically classified into these categories:

- **Web Development** - Frontend, backend, frameworks, and web tools
- **Machine Learning & AI** - ML frameworks, AI tools, and neural networks
- **Data Science & Analytics** - Data analysis, visualization, and Jupyter
- **DevOps & Infrastructure** - Docker, Kubernetes, CI/CD tools
- **Mobile Development** - iOS, Android, React Native, Flutter
- **Databases** - SQL, NoSQL, and database tools
- **Tools & Utilities** - CLI tools, automation, and utilities
- **Security** - Cryptography, vulnerability scanning, and auth
- **Documentation & Learning** - Tutorials, guides, and learning resources
- **Testing** - Testing frameworks and tools
- **Game Development** - Game engines and development tools
- **Blockchain & Crypto** - Blockchain, DeFi, and Web3
- **API & Networking** - REST APIs, GraphQL, and networking tools
- **Other** - Everything else

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/ivanzhangwb/star_repo_classifier.git
cd github-star-classifier

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup GitHub Token

Create a GitHub Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo` (for public repos) or `repo` (for private repos)
4. Copy the generated token

### 3. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your token
# GITHUB_TOKEN=your_github_token_here
# OUTPUT_DIR=./output
# MIN_STARS=0
# EXCLUDE_FORKS=true
# INCLUDE_ARCHIVED=false
```

### 4. Run the Classifier

```bash
# Basic usage
python main.py

# With custom token
python main.py --token YOUR_GITHUB_TOKEN

# With filters
python main.py --min-stars 100 --exclude-forks --output ./my_stars

# Include archived repos
python main.py --include-archived

# Skip report generation for faster processing
python main.py --no-reports

# Verbose output
python main.py --verbose
```

## 📋 Usage Examples

### Basic Classification
```bash
python main.py
```

### Filter Popular Repositories
```bash
python main.py --min-stars 500 --exclude-forks --output ./popular_stars
```

### Include All Repositories
```bash
python main.py --min-stars 0 --include-forks --include-archived
```

### Custom Output Location
```bash
python main.py --output ~/Documents/github_stars_analysis
```

## 📊 Output Files

The tool generates several files in your output directory:

### Data Files
- `starred_repos_YYYYMMDD_HHMMSS.json` - Full repository data
- `starred_repos_YYYYMMDD_HHMMSS.csv` - Tabular data
- `statistics_YYYYMMDD_HHMMSS.json` - Summary statistics

### Reports
- `github_stars_report.html` - Interactive HTML report with charts
- `github_stars_report.md` - Detailed Markdown report

### Visualizations
- `category_distribution_YYYYMMDD_HHMMSS.png` - Pie chart of categories
- `language_distribution_YYYYMMDD_HHMMSS.png` - Bar chart of languages
- `stars_analysis_YYYYMMDD_HHMMSS.png` - Stars analysis by category

## 🛠️ Advanced Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | Your GitHub Personal Access Token | Required |
| `OUTPUT_DIR` | Directory for output files | `./output` |
| `MIN_STARS` | Minimum star count filter | `0` |
| `EXCLUDE_FORKS` | Exclude forked repositories | `true` |
| `INCLUDE_ARCHIVED` | Include archived repositories | `false` |
| `MAX_REPOS_PER_REQUEST` | API pagination limit | `100` |

### Custom Classification

You can modify the classification rules in `github_star_classifier.py` by editing the `PROJECT_CATEGORIES` dictionary:

```python
PROJECT_CATEGORIES = {
    "Your Category": {
        "keywords": ["keyword1", "keyword2"],
        "topics": ["topic1", "topic2"]
    }
}
```

## 🔧 Troubleshooting

### Common Issues

**"GitHub token not provided"**
```bash
# Ensure your .env file exists or set the token directly
export GITHUB_TOKEN=your_token_here
python main.py
```

**"Rate limit exceeded"**
- GitHub API has rate limits: 60 requests/hour for unauthenticated, 5000/hour for authenticated
- The tool handles pagination automatically, but large numbers of stars may hit limits
- Wait and retry, or use a token with higher rate limits

**"No repositories found"**
- Check your filters: `min-stars`, `exclude-forks`, etc.
- Verify your GitHub token has necessary permissions
- Ensure you're authenticated to access private starred repos

### Debug Mode

Run with verbose output to see detailed progress:

```bash
python main.py --verbose
```

## 🧪 Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/ivanzhangwb/star_repo_classifier/issues)
- **Discussions**: Join discussions in [GitHub Discussions](https://github.com/ivanzhangwb/star_repo_classifier/discussions)
- **Wiki**: Check the [Wiki](https://github.com/ivanzhangwb/star_repo_classifier/wiki) for advanced usage

## 🙏 Acknowledgments

- [PyGithub](https://pygithub.readthedocs.io/) for GitHub API integration
- [Pandas](https://pandas.pydata.org/) for data analysis
- [Seaborn](https://seaborn.pydata.org/) and [Matplotlib](https://matplotlib.org/) for visualizations
- [Jinja2](https://jinja.palletsprojects.com/) for HTML templating

---

**Happy stargazing! ⭐**

Made with ❤️ by the GitHub community