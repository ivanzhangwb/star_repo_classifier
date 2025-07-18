#!/usr/bin/env python3
"""
GitHub Starred Repositories Classifier - Main Entry Point

This script provides a complete solution to fetch, classify, and generate reports
for your GitHub starred repositories.

Usage:
    python main.py
    python main.py --token YOUR_TOKEN --output ./my_stars
    python main.py --min-stars 100 --exclude-forks --include-archived
"""

import os
import sys
import argparse
from datetime import datetime
from github_star_classifier import GitHubStarClassifier
from report_generator import ReportGenerator
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main function to run the complete classification process."""
    parser = argparse.ArgumentParser(
        description='Classify and analyze your GitHub starred repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Use environment variables
  %(prog)s --token YOUR_TOKEN                # Use specific token
  %(prog)s --output ./my_reports             # Custom output directory
  %(prog)s --min-stars 50 --exclude-forks    # Filter repositories
  %(prog)s --include-archived                # Include archived repos
        """
    )
    
    parser.add_argument('--token', help='GitHub Personal Access Token')
    parser.add_argument('--output', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--min-stars', type=int, default=0, help='Minimum star count filter')
    parser.add_argument('--exclude-forks/--include-forks', dest='exclude_forks', 
                       action='store_true', default=True, help='Exclude forked repositories')
    parser.add_argument('--include-archived/--exclude-archived', dest='include_archived', 
                       action='store_true', default=False, help='Include archived repositories')
    parser.add_argument('--no-reports', action='store_true', help='Skip report generation')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup environment variables
    if args.token:
        os.environ['GITHUB_TOKEN'] = args.token
    os.environ['OUTPUT_DIR'] = args.output
    os.environ['MIN_STARS'] = str(args.min_stars)
    os.environ['EXCLUDE_FORKS'] = str(args.exclude_forks).lower()
    os.environ['INCLUDE_ARCHIVED'] = str(args.include_archived).lower()
    
    try:
        # Initialize classifier
        if args.verbose:
            print("🔧 Initializing GitHub Star Classifier...")
        
        classifier = GitHubStarClassifier()
        
        # Fetch repositories
        if args.verbose:
            print("📥 Fetching starred repositories...")
        repos = classifier.fetch_starred_repos()
        
        if not repos:
            print("⚠️  No repositories found matching the criteria.")
            return 0
        
        # Classify repositories
        if args.verbose:
            print("🏷️  Classifying repositories...")
        classified_repos = classifier.classify_repositories(repos)
        
        # Generate statistics
        if args.verbose:
            print("📊 Generating statistics...")
        stats = classifier.generate_statistics(classified_repos)
        
        # Save data
        files = classifier.save_data(classified_repos, stats)
        
        # Generate reports unless skipped
        if not args.no_reports:
            if args.verbose:
                print("📋 Generating reports...")
            
            report_generator = ReportGenerator(args.output)
            reports = report_generator.generate_reports(classified_repos, stats)
            
            print(f"\n🎉 Classification complete!")
            print(f"📊 Statistics:")
            print(f"   Total repositories: {stats['total_repos']}")
            print(f"   Categories: {len(stats['categories'])}")
            print(f"   Languages: {len(stats['languages'])}")
            print(f"   Total stars: {stats['total_stars']:,}")
            
            print(f"\n🏷️  Top categories:")
            for category, count in sorted(stats['categories'].items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                percentage = (count / stats['total_repos']) * 100
                print(f"   {category}: {count} repos ({percentage:.1f}%)")
            
            print(f"\n📁 Files saved:")
            for file_type, file_path in {**files, **reports}.items():
                print(f"   {file_type}: {file_path}")
            
            # Open reports in browser (optional)
            html_report = reports.get('html_report')
            if html_report and os.path.exists(html_report):
                print(f"\n🌐 Open HTML report: file://{os.path.abspath(html_report)}")
                
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())