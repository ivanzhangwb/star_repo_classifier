#!/usr/bin/env python3
"""
GitHub Starred Repositories Classifier

A tool to fetch and categorize GitHub starred repositories by project type,
generating both HTML and Markdown reports.

Author: Claude
License: MIT
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
import click
from github import Github
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class GitHubStarClassifier:
    """Main class for classifying GitHub starred repositories."""
    
    # Project type classification based on topics, descriptions, and names
    PROJECT_CATEGORIES = {
        "Web Development": {
            "keywords": ["web", "frontend", "backend", "react", "vue", "angular", "django", "flask", "express", "nodejs", "javascript", "typescript", "html", "css", "sass", "webpack", "vite"],
            "topics": ["web", "frontend", "backend", "react", "vue", "angular", "javascript", "typescript", "nodejs", "web-framework"]
        },
        "Machine Learning & AI": {
            "keywords": ["ml", "ai", "machine-learning", "deep-learning", "neural-network", "tensorflow", "pytorch", "keras", "scikit-learn", "nlp", "computer-vision", "llm", "transformer", "bert", "gpt"],
            "topics": ["machine-learning", "deep-learning", "ai", "neural-networks", "tensorflow", "pytorch", "nlp", "computer-vision", "llm"]
        },
        "Data Science & Analytics": {
            "keywords": ["data", "pandas", "numpy", "matplotlib", "seaborn", "jupyter", "plotly", "dashboard", "visualization", "etl", "data-pipeline", "analytics"],
            "topics": ["data-science", "pandas", "numpy", "visualization", "analytics", "jupyter", "dashboard"]
        },
        "DevOps & Infrastructure": {
            "keywords": ["docker", "kubernetes", "devops", "ci-cd", "ansible", "terraform", "infrastructure", "monitoring", "deployment", "microservices", "cloud"],
            "topics": ["docker", "kubernetes", "devops", "infrastructure", "ci-cd", "terraform", "monitoring"]
        },
        "Mobile Development": {
            "keywords": ["mobile", "ios", "android", "react-native", "flutter", "swift", "kotlin", "dart", "mobile-app", "cross-platform"],
            "topics": ["mobile", "ios", "android", "react-native", "flutter", "swift", "kotlin"]
        },
        "Databases": {
            "keywords": ["database", "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "orm"],
            "topics": ["database", "sql", "nosql", "postgresql", "mysql", "mongodb", "redis"]
        },
        "Tools & Utilities": {
            "keywords": ["cli", "tool", "utility", "automation", "script", "package", "library", "framework", "boilerplate", "generator"],
            "topics": ["cli", "tool", "utility", "automation", "library"]
        },
        "Security": {
            "keywords": ["security", "cryptography", "encryption", "vulnerability", "penetration-testing", "firewall", "auth", "oauth", "ssl"],
            "topics": ["security", "cryptography", "vulnerability", "auth", "oauth"]
        },
        "Documentation & Learning": {
            "keywords": ["documentation", "tutorial", "course", "learning", "book", "guide", "awesome", "resources", "cheatsheet"],
            "topics": ["documentation", "tutorial", "learning", "awesome", "resources"]
        },
        "Testing": {
            "keywords": ["testing", "test", "pytest", "unittest", "jest", "mocha", "cypress", "selenium", "mock", "coverage"],
            "topics": ["testing", "pytest", "jest", "unit-testing", "integration-testing"]
        },
        "Game Development": {
            "keywords": ["game", "gaming", "unity", "unreal", "godot", "game-engine", "3d", "2d", "graphics", "physics"],
            "topics": ["game-development", "unity", "unreal-engine", "godot", "graphics"]
        },
        "Blockchain & Crypto": {
            "keywords": ["blockchain", "crypto", "bitcoin", "ethereum", "defi", "nft", "smart-contract", "web3", "solidity"],
            "topics": ["blockchain", "cryptocurrency", "ethereum", "smart-contracts", "web3"]
        },
        "API & Networking": {
            "keywords": ["api", "rest", "graphql", "http", "websocket", "grpc", "microservice", "server", "client"],
            "topics": ["api", "rest-api", "graphql", "microservices", "networking"]
        }
    }
    
    def __init__(self, token: str = None):
        """Initialize the classifier with GitHub token."""
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token not provided. Set GITHUB_TOKEN environment variable.")
        
        self.github = Github(self.token)
        self.user = self.github.get_user()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_starred_repos(self) -> List[Dict[str, Any]]:
        """Fetch all starred repositories for the authenticated user."""
        print("Fetching starred repositories...")
        starred_repos = []
        
        try:
            # Get starred repos with pagination
            starred = self.user.get_starred()
            
            min_stars = int(os.getenv('MIN_STARS', 0))
            exclude_forks = os.getenv('EXCLUDE_FORKS', 'true').lower() == 'true'
            include_archived = os.getenv('INCLUDE_ARCHIVED', 'false').lower() == 'true'
            
            for repo in starred:
                # Apply filters
                if repo.stargazers_count < min_stars:
                    continue
                if exclude_forks and repo.fork:
                    continue
                if not include_archived and repo.archived:
                    continue
                
                repo_data = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description or '',
                    'html_url': repo.html_url,
                    'language': repo.language or 'Unknown',
                    'stargazers_count': repo.stargazers_count,
                    'forks_count': repo.forks_count,
                    'topics': repo.topics or [],
                    'created_at': repo.created_at.isoformat(),
                    'updated_at': repo.updated_at.isoformat(),
                    'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
                    'archived': repo.archived,
                    'fork': repo.fork,
                    'owner': repo.owner.login,
                    'size': repo.size
                }
                starred_repos.append(repo_data)
            
            print(f"Fetched {len(starred_repos)} repositories")
            return starred_repos
            
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            raise
    
    def classify_repository(self, repo: Dict[str, Any]) -> str:
        """Classify a repository into a project type category."""
        text_to_analyze = ' '.join([
            repo['name'].lower(),
            repo['description'].lower() if repo['description'] else '',
            ' '.join(repo['topics']).lower(),
            repo['language'].lower() if repo['language'] else ''
        ])

        project_name = repo['name']
        print(f"Process repo {project_name}.... ")
        category_scores = {}
        
        for category, criteria in self.PROJECT_CATEGORIES.items():
            score = 0
            
            # Check keywords in combined text
            for keyword in criteria['keywords']:
                if keyword.lower() in text_to_analyze:
                    score += 1
            
            # Check topics
            for topic in criteria['topics']:
                if len(repo['topics'])>0 and topic.lower() in [t.lower() for t in repo['topics']]:
                    score += 2
            
            if score > 0:
                category_scores[category] = score
        
        # Return highest scoring category, or "Other" if no matches
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return "Other"
    
    def classify_repositories(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify all repositories into categories."""
        print("Classifying repositories...")
        classified_repos = []
        
        for repo in repos:
            repo['category'] = self.classify_repository(repo)
            classified_repos.append(repo)
        
        return classified_repos
    
    def generate_statistics(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics about the classified repositories."""
        df = pd.DataFrame(repos)
        print("Generating statistics...")

        stats = {
            'total_repos': len(repos),
            'categories': df['category'].value_counts().to_dict(),
            'languages': df['language'].value_counts().to_dict(),
            'avg_stars': df['stargazers_count'].mean(),
            'total_stars': int(df['stargazers_count'].sum()),
            'oldest_repo': df['created_at'].min(),
            'newest_repo': df['created_at'].max(),
            'most_starred': df.loc[df['stargazers_count'].idxmax()].to_dict(),
            'recently_updated': df.loc[df['updated_at'].idxmax()].to_dict()
        }
        
        return stats
    
    def save_data(self, repos: List[Dict[str, Any]], stats: Dict[str, Any]):
        """Save data to various formats."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        print("Saving data...")
        # Save raw JSON
        json_file = os.path.join(self.output_dir, f'starred_repos_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(repos, f, indent=2, ensure_ascii=False)
        
        # Save CSV
        csv_file = os.path.join(self.output_dir, f'starred_repos_{timestamp}.csv')
        df = pd.DataFrame(repos)
        df.to_csv(csv_file, index=False)
        
        # Save statistics
        stats_file = os.path.join(self.output_dir, f'statistics_{timestamp}.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {self.output_dir}")
        return {
            'json_file': json_file,
            'csv_file': csv_file,
            'stats_file': stats_file
        }

@click.command()
@click.option('--token', help='GitHub Personal Access Token')
@click.option('--output', default='./output', help='Output directory')
@click.option('--min-stars', default=0, help='Minimum star count filter')
@click.option('--exclude-forks/--include-forks', default=True, help='Exclude forked repositories')
def main(token, output, min_stars, exclude_forks):
    """GitHub Starred Repositories Classifier."""
    
    # Set environment variables
    if token:
        os.environ['GITHUB_TOKEN'] = token
    if output:
        os.environ['OUTPUT_DIR'] = output
    os.environ['MIN_STARS'] = str(min_stars)
    os.environ['EXCLUDE_FORKS'] = str(exclude_forks).lower()
    
    try:
        classifier = GitHubStarClassifier()
        repos = classifier.fetch_starred_repos()
        classified_repos = classifier.classify_repositories(repos)
        stats = classifier.generate_statistics(classified_repos)
        files = classifier.save_data(classified_repos, stats)
        
        print(f"\n📊 Classification complete!")
        print(f"Total repositories: {stats['total_repos']}")
        print(f"Categories: {len(stats['categories'])}")
        print(f"\nTop categories:")
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {category}: {count} repos")
        
        print(f"\n📁 Files saved:")
        for file_type, file_path in files.items():
            print(f"  {file_type}: {file_path}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())