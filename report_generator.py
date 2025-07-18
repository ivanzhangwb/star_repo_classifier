"""
Report Generator for GitHub Starred Repositories Classifier

Generates HTML and Markdown reports with visualizations.
"""

import os
import json
import pandas as pd
from datetime import datetime
from jinja2 import Template
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any

class ReportGenerator:
    """Generates HTML and Markdown reports for classified repositories."""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style for plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def load_data(self, json_file: str) -> List[Dict[str, Any]]:
        """Load repository data from JSON file."""
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_stats(self, stats_file: str) -> Dict[str, Any]:
        """Load statistics from JSON file."""
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_visualizations(self, repos: List[Dict[str, Any]], stats: Dict[str, Any]):
        """Create visualization charts."""
        df = pd.DataFrame(repos)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Category distribution pie chart
        plt.figure(figsize=(12, 8))
        category_counts = df['category'].value_counts()
        colors = plt.cm.Set3(range(len(category_counts)))
        
        plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        plt.title('Repository Distribution by Category', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'category_distribution_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Language distribution
        plt.figure(figsize=(12, 8))
        language_counts = df['language'].value_counts().head(10)
        
        bars = plt.bar(range(len(language_counts)), language_counts.values, 
                       color=plt.cm.viridis(range(len(language_counts))))
        plt.xticks(range(len(language_counts)), language_counts.index, rotation=45, ha='right')
        plt.title('Top 10 Programming Languages', fontsize=16, fontweight='bold')
        plt.xlabel('Language', fontsize=12)
        plt.ylabel('Number of Repositories', fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'language_distribution_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Stars vs Category heatmap
        plt.figure(figsize=(14, 8))
        stars_by_category = df.groupby('category')['stargazers_count'].agg(['mean', 'sum', 'count'])
        stars_by_category = stars_by_category.sort_values('count', ascending=False)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Average stars by category
        bars1 = ax1.barh(range(len(stars_by_category)), stars_by_category['mean'], 
                        color=plt.cm.Blues(stars_by_category['mean']/stars_by_category['mean'].max()))
        ax1.set_yticks(range(len(stars_by_category)))
        ax1.set_yticklabels(stars_by_category.index)
        ax1.set_xlabel('Average Stars')
        ax1.set_title('Average Stars by Category')
        
        # Count by category
        bars2 = ax2.barh(range(len(stars_by_category)), stars_by_category['count'], 
                        color=plt.cm.Greens(stars_by_category['count']/stars_by_category['count'].max()))
        ax2.set_yticks(range(len(stars_by_category)))
        ax2.set_yticklabels(stars_by_category.index)
        ax2.set_xlabel('Number of Repositories')
        ax2.set_title('Repository Count by Category')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'stars_analysis_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            'category_distribution': f'category_distribution_{timestamp}.png',
            'language_distribution': f'language_distribution_{timestamp}.png',
            'stars_analysis': f'stars_analysis_{timestamp}.png'
        }
    
    def generate_html_report(self, repos: List[Dict[str, Any]], stats: Dict[str, Any], 
                           charts: Dict[str, str]) -> str:
        """Generate HTML report."""
        
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GitHub Starred Repositories Report</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
                .card { border: none; box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); }
                .chart-container { background: white; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; }
                .repo-card { transition: transform 0.2s; }
                .repo-card:hover { transform: translateY(-2px); }
                .language-badge { font-size: 0.75rem; }
                .stars { color: #f1c40f; }
                .category-section { margin-bottom: 2rem; }
                .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            </style>
        </head>
        <body>
            <div class="hero py-5 mb-4">
                <div class="container">
                    <h1 class="display-4"><i class="fab fa-github"></i> GitHub Starred Repositories Report</h1>
                    <p class="lead">Comprehensive analysis of your starred repositories</p>
                    <p>Generated on {{ timestamp }}</p>
                </div>
            </div>

            <div class="container">
                <!-- Statistics Overview -->
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <i class="fas fa-star fa-2x text-warning mb-2"></i>
                                <h3 class="card-title">{{ stats.total_repos }}</h3>
                                <p class="card-text">Total Repositories</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <i class="fas fa-folder fa-2x text-primary mb-2"></i>
                                <h3 class="card-title">{{ stats.categories|length }}</h3>
                                <p class="card-text">Categories</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <i class="fas fa-code fa-2x text-success mb-2"></i>
                                <h3 class="card-title">{{ stats.languages|length }}</h3>
                                <p class="card-text">Languages</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <i class="fas fa-heart fa-2x text-danger mb-2"></i>
                                <h3 class="card-title">{{ "{:,}".format(stats.total_stars|int) }}</h3>
                                <p class="card-text">Total Stars</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Charts -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="chart-container">
                            <h4>Category Distribution</h4>
                            <img src="{{ charts.category_distribution }}" alt="Category Distribution" class="img-fluid">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="chart-container">
                            <h4>Top Languages</h4>
                            <img src="{{ charts.language_distribution }}" alt="Language Distribution" class="img-fluid">
                        </div>
                    </div>
                </div>

                <div class="row mb-4">
                    <div class="col-12">
                        <div class="chart-container">
                            <h4>Stars Analysis by Category</h4>
                            <img src="{{ charts.stars_analysis }}" alt="Stars Analysis" class="img-fluid">
                        </div>
                    </div>
                </div>

                <!-- Categories Detail -->
                <div class="row">
                    <div class="col-12">
                        <h2 class="mb-4">Repository Categories</h2>
                        
                        {% for category, repos in categorized_repos.items() %}
                        <div class="category-section">
                            <h3 class="text-primary">{{ category }} ({{ repos|length }} repos)</h3>
                            <div class="row">
                                {% for repo in repos[:6] %}
                                <div class="col-md-6 col-lg-4 mb-3">
                                    <div class="card repo-card">
                                        <div class="card-body">
                                            <h5 class="card-title">
                                                <a href="{{ repo.html_url }}" target="_blank" class="text-decoration-none">
                                                    {{ repo.name }}
                                                </a>
                                            </h5>
                                            <p class="card-text text-muted small">{{ repo.description[:100] }}...{% if repo.description and repo.description|length > 100 %}...{% endif %}</p>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <span class="badge bg-secondary language-badge">{{ repo.language or 'Unknown' }}</span>
                                                <span class="stars">
                                                    <i class="fas fa-star"></i> {{ repo.stargazers_count }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                            
                            {% if repos|length > 6 %}
                            <div class="text-center mb-3">
                                <span class="text-muted">And {{ repos|length - 6 }} more repositories...</span>
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <footer class="mt-5 py-4 text-center text-muted">
                <p>Generated by GitHub Starred Repositories Classifier
                <br>Last updated: {{ timestamp }}</p>
            </footer>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        
        template = Template(html_template)
        
        # Group repositories by category
        categorized_repos = {}
        for repo in repos:
            category = repo['category']
            if category not in categorized_repos:
                categorized_repos[category] = []
            categorized_repos[category].append(repo)
        
        # Sort categories by count
        categorized_repos = dict(sorted(categorized_repos.items(), 
                                      key=lambda x: len(x[1]), reverse=True))
        
        html_content = template.render(
            stats=stats,
            categorized_repos=categorized_repos,
            charts=charts,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        html_file = os.path.join(self.output_dir, 'github_stars_report.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def generate_markdown_report(self, repos: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Generate Markdown report."""
        
        # Group repositories by category
        categorized_repos = {}
        for repo in repos:
            category = repo['category']
            if category not in categorized_repos:
                categorized_repos[category] = []
            categorized_repos[category].append(repo)
        
        # Sort categories by count
        categorized_repos = dict(sorted(categorized_repos.items(), 
                                      key=lambda x: len(x[1]), reverse=True))
        
        markdown_content = f"""# GitHub Starred Repositories Report

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## =� Summary

- **Total Repositories**: {stats['total_repos']}
- **Categories**: {len(stats['categories'])}
- **Languages**: {len(stats['languages'])}
- **Total Stars**: {stats['total_stars']:,}
- **Average Stars per Repository**: {stats['avg_stars']:.1f}

## =� Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
"""
        
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_repos']) * 100
            markdown_content += f"| {category} | {count} | {percentage:.1f}% |"

        markdown_content += f"""
## =$ Top Languages

| Language | Count |
|----------|-------|
"""
        
        for language, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
            markdown_content += f"| {language} | {count} |"
        
        markdown_content += "\n## =� Repository Details\n\n"
        
        for category, repos_in_category in categorized_repos.items():
            markdown_content += f"### {category} ({len(repos_in_category)} repositories)\n\n"
            
            # Sort by stars within category
            repos_sorted = sorted(repos_in_category, key=lambda x: x['stargazers_count'], reverse=True)
            
            for repo in repos_sorted[:10]:  # Show top 10 per category
                markdown_content += f"#### [{repo['full_name']}]({repo['html_url']})"
                markdown_content += f"- P **{repo['stargazers_count']}** stars"
                markdown_content += f"- <t **{repo['forks_count']}** forks"
                markdown_content += f"- < **Language**: {repo['language'] or 'Unknown'}"
                markdown_content += f"- = **Updated**: {repo['updated_at'][:10]}"
                if repo['description']:
                    markdown_content += f"- = **Description**: {repo['description'][:200]}{'...' if len(repo['description']) > 200 else ''}"
                if repo['topics']:
                    topics = ', '.join([f"`{topic}`" for topic in repo['topics'][:5]])
                    markdown_content += f"- < **Topics**: {topics}"
                markdown_content += "\n"
            
            if len(repos_in_category) > 10:
                markdown_content += f"*... and {len(repos_in_category) - 10} more repositories in this category*\n\n"
        
        markdown_content += """
## =
 Quick Links

- [Most Starred Repository]({most_starred_url}): **{most_starred_name}** ({most_starred_stars} P)
- [Recently Updated]({recently_updated_url}): **{recently_updated_name}** (updated {recently_updated_date})

---

*This report was generated using the GitHub Starred Repositories Classifier.*
""".format(
            most_starred_name=stats['most_starred']['full_name'],
            most_starred_url=stats['most_starred']['html_url'],
            most_starred_stars=stats['most_starred']['stargazers_count'],
            recently_updated_name=stats['recently_updated']['full_name'],
            recently_updated_url=stats['recently_updated']['html_url'],
            recently_updated_date=stats['recently_updated']['updated_at'][:10]
        )
        
        markdown_file = os.path.join(self.output_dir, 'github_stars_report.md')
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return markdown_file
    
    def generate_reports(self, repos: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, str]:
        """Generate both HTML and Markdown reports."""
        print("Generating reports...")
        
        # Create visualizations
        charts = self.create_visualizations(repos, stats)
        
        # Generate reports
        html_file = self.generate_html_report(repos, stats, charts)
        markdown_file = self.generate_markdown_report(repos, stats)
        
        print(f" Reports generated:")
        print(f"  HTML: {html_file}")
        print(f"  Markdown: {markdown_file}")
        
        return {
            'html_report': html_file,
            'markdown_report': markdown_file,
            'charts': charts
        }