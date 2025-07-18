import React from 'react';
import { Link } from 'react-router-dom';
import { Star, Zap, BarChart3, Shield } from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      name: 'Smart Classification / 智能分类',
      description: 'Automatically categorize your starred repositories using advanced algorithms. / 使用先进算法自动分类您的收藏仓库。',
      icon: Star,
    },
    {
      name: 'Rich Analytics / 丰富分析',
      description: 'Get detailed insights with charts and statistics about your GitHub stars. / 通过图表和统计数据获取关于您的GitHub收藏的详细见解。',
      icon: BarChart3,
    },
    {
      name: 'Fast Processing / 快速处理',
      description: 'Quickly analyze hundreds of repositories with optimized processing. / 通过优化的处理快速分析数百个仓库。',
      icon: Zap,
    },
    {
      name: 'Secure & Private / 安全私密',
      description: 'Your GitHub token is never stored and all data is processed securely. / 您的GitHub令牌不会被存储，所有数据都安全处理。',
      icon: Shield,
    },
  ];

  return (
    <div className="text-center">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl">
          Analyze Your GitHub Stars / 分析您的GitHub收藏
        </h1>
        <p className="mt-6 text-xl text-gray-600">
          Discover insights about your starred repositories with intelligent classification and beautiful visualizations. / 通过智能分类和精美可视化图表发现您收藏仓库的见解。
        </p>
        
        <div className="mt-10">
          <Link
            to="/classify"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
          >
            <Star className="h-5 w-5 mr-2" />
            Start Classifying / 开始分类
          </Link>
        </div>

        <div className="mt-20">
          <h2 className="text-3xl font-bold text-gray-900 mb-12">
            Features / 功能特性
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature) => (
              <div key={feature.name} className="bg-white p-6 rounded-lg shadow-sm">
                <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-md">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">{feature.name}</h3>
                <p className="mt-2 text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-20 bg-white p-8 rounded-lg shadow-sm">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            How it works / 如何使用
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div>
              <div className="text-primary-600 font-bold text-lg mb-2">1. Connect / 连接</div>
              <p className="text-gray-600">Enter your GitHub token to access your starred repositories. / 输入您的GitHub令牌以访问您的收藏仓库。</p>
            </div>
            <div>
              <div className="text-primary-600 font-bold text-lg mb-2">2. Analyze / 分析</div>
              <p className="text-gray-600">Our AI classifies your repos into categories automatically. / 我们的AI自动将您的仓库分类到不同类别。</p>
            </div>
            <div>
              <div className="text-primary-600 font-bold text-lg mb-2">3. Explore / 探索</div>
              <p className="text-gray-600">View interactive charts and detailed statistics. / 查看交互式图表和详细统计数据。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;