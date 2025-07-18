"""
GitHub Star Classifier Service

Refactored service layer for API usage
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from github import Github
from dataclasses import dataclass

# Configure proxy for PyGithub
os.environ['HTTP_PROXY'] = os.getenv('HTTP_PROXY', 'http://127.0.0.1:7890')
os.environ['HTTPS_PROXY'] = os.getenv('HTTPS_PROXY', 'http://127.0.0.1:7890')

@dataclass
class ClassificationConfig:
    """Configuration for classification process."""
    token: str
    min_stars: int = 0
    exclude_forks: bool = True
    include_archived: bool = False
    max_repos: Optional[int] = None

class ClassificationResult:
    """Result container for classification."""
    def __init__(self, repos: List[Dict[str, Any]], stats: Dict[str, Any]):
        self.repos = repos
        self.stats = stats
        self.completed_at = datetime.now()
        self.total_repos = len(repos)

class GitHubStarClassifierService:
    """Service layer for GitHub star classification."""
    
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
    
    def __init__(self, config: ClassificationConfig):
        """Initialize the service with configuration."""
        self.config = config
        self.github = Github(config.token)
        self.user = self.github.get_user()
        print(f"Init github object with user:{self.user}, token:{config.token} ")
    
    def fetch_starred_repos(self) -> List[Dict[str, Any]]:
        """Fetch starred repositories based on configuration."""
        starred_repos = []
        try:
            starred = self.user.get_starred()

            print(f"Start process task .User star repo:{starred} ")
            for repo in starred:
                # Apply filters
                if repo.stargazers_count < self.config.min_stars:
                    continue
                if self.config.exclude_forks and repo.fork:
                    continue
                if not self.config.include_archived and repo.archived:
                    continue
                
                # Limit repos if specified
                if self.config.max_repos and len(starred_repos) >= self.config.max_repos:
                    break
                
                repo_data = {
                    'id': repo.id,
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
                    'size': repo.size,
                    'license': repo.license.name if repo.license else None,
                    'homepage': repo.homepage or None,
                    'open_issues_count': repo.open_issues_count,
                    'default_branch': repo.default_branch,
                    'clone_url': repo.clone_url,
                    'ssh_url': repo.ssh_url
                }
                starred_repos.append(repo_data)
            
            return starred_repos
            
        except Exception as e:
            raise Exception(f"Error fetching repositories: {str(e)}")
    
    def classify_repository(self, repo: Dict[str, Any]) -> str:
        """Classify a single repository into a category."""
        text_to_analyze = ' '.join([
            repo['name'].lower(),
            repo['description'].lower() if repo['description'] else '',
            ' '.join(repo['topics']).lower(),
            repo['language'].lower() if repo['language'] else ''
        ])

        category_scores = {}
        
        for category, criteria in self.PROJECT_CATEGORIES.items():
            score = 0
            
            # Check keywords
            for keyword in criteria['keywords']:
                if keyword.lower() in text_to_analyze:
                    score += 1
            
            # Check topics (higher weight)
            for topic in criteria['topics']:
                if repo['topics'] and topic.lower() in [t.lower() for t in repo['topics']]:
                    score += 2
            
            if score > 0:
                category_scores[category] = score
        
        # Return highest scoring category or "Other"
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return "Other"
    
    def classify_repositories(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify all repositories into categories."""
        classified_repos = []
        
        for repo in repos:
            repo['category'] = self.classify_repository(repo)
            classified_repos.append(repo)
        
        return classified_repos
    
    def generate_statistics(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive statistics."""
        if not repos:
            return {
                'total_repos': 0,
                'categories': {},
                'languages': {},
                'avg_stars': 0,
                'total_stars': 0,
                'oldest_repo': None,
                'newest_repo': None,
                'most_starred': None,
                'recently_updated': None
            }
        
        df = pd.DataFrame(repos)
        
        # Convert date strings to datetime for analysis
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        
        stats = {
            'total_repos': len(repos),
            'categories': df['category'].value_counts().to_dict(),
            'languages': df['language'].value_counts().to_dict(),
            'avg_stars': float(df['stargazers_count'].mean()),
            'median_stars': float(df['stargazers_count'].median()),
            'total_stars': int(df['stargazers_count'].sum()),
            'max_stars': int(df['stargazers_count'].max()),
            'min_stars': int(df['stargazers_count'].min()),
            'oldest_repo': df['created_at'].min().isoformat() if not df['created_at'].empty else None,
            'newest_repo': df['created_at'].max().isoformat() if not df['created_at'].empty else None,
            'most_starred': df.loc[df['stargazers_count'].idxmax()].to_dict() if not df.empty else None,
            'recently_updated': df.loc[df['updated_at'].idxmax()].to_dict() if not df.empty else None,
            'archived_count': int(df['archived'].sum()),
            'fork_count': int(df['fork'].sum()),
            'unique_owners': df['owner'].nunique(),
            'top_topics': self._get_top_topics(repos)
        }
        
        # Add category breakdown with percentages
        total_repos = len(repos)
        stats['categories_with_percentage'] = {
            category: {
                'count': count,
                'percentage': round((count / total_repos) * 100, 2)
            }
            for category, count in stats['categories'].items()
        }
        
        return stats
    
    def _get_top_topics(self, repos: List[Dict[str, Any]], top_n: int = 10) -> Dict[str, int]:
        """Get the most common topics across all repositories."""
        all_topics = []
        for repo in repos:
            all_topics.extend(repo.get('topics', []))
        
        if not all_topics:
            return {}
        
        topic_counts = pd.Series(all_topics).value_counts().head(top_n).to_dict()
        return topic_counts
    
    def classify_and_analyze(self) -> ClassificationResult:
        """Complete classification and analysis pipeline."""
        repos = self.fetch_starred_repos()
        classified_repos = self.classify_repositories(repos)
        stats = self.generate_statistics(classified_repos)
        
        return ClassificationResult(classified_repos, stats)