import React, { useState } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ChevronDown, ChevronUp, ExternalLink, Star, GitFork } from 'lucide-react';

const ResultsDashboard = ({ repos, stats }) => {
  const [expandedCategories, setExpandedCategories] = useState({});
  const [sortBy, setSortBy] = useState('stars');

  const COLORS = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
  ];

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const categoryData = Object.entries(stats.categories_with_percentage || {}).map(([category, data]) => ({
    name: category,
    value: data.count,
    percentage: data.percentage
  }));

  const languageData = Object.entries(stats.languages || {})
    .map(([language, count]) => ({ language, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  const starsByCategory = Object.entries(stats.categories || {}).map(([category, count]) => {
    const categoryRepos = repos.filter(repo => repo.category === category);
    const totalStars = categoryRepos.reduce((sum, repo) => sum + repo.stargazers_count, 0);
    const avgStars = count > 0 ? totalStars / count : 0;
    
    return {
      category,
      count,
      totalStars,
      avgStars: Math.round(avgStars)
    };
  }).sort((a, b) => b.count - a.count);

  const getCategoryRepos = (category) => {
    return repos
      .filter(repo => repo.category === category)
      .sort((a, b) => {
        switch (sortBy) {
          case 'stars': return b.stargazers_count - a.stargazers_count;
          case 'forks': return b.forks_count - a.forks_count;
          case 'updated': return new Date(b.updated_at) - new Date(a.updated_at);
          case 'created': return new Date(b.created_at) - new Date(a.created_at);
          default: return b.stargazers_count - a.stargazers_count;
        }
      });
  };

  return (
    <div className="space-y-6">
      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Distribution / 分类分布</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name} (${percentage}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Languages / 热门语言</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={languageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="language" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Stars by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={starsByCategory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="category" angle={-45} textAnchor="end" height={80} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="avgStars" fill="#10B981" name="Average Stars / 平均星标" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Repository Lists by Category */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900">Repositories by Category / 按分类的仓库</h3>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Sort repositories by: / 排序方式：</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="stars">Stars / 星标</option>
            <option value="forks">Forks / 分支</option>
            <option value="updated">Recently Updated / 最近更新</option>
            <option value="created">Recently Created / 最近创建</option>
          </select>
        </div>

        {Object.entries(stats.categories || {}).map(([category, count]) => (
          <div key={category} className="bg-white rounded-lg shadow-sm">
            <button
              onClick={() => toggleCategory(category)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center">
                <h4 className="text-lg font-semibold text-gray-900">{category}</h4>
                <span className="ml-2 px-2 py-1 text-xs font-semibold bg-gray-100 text-gray-700 rounded-full">{count} repos / {count} 个仓库</span>
              </div>
              {expandedCategories[category] ? <ChevronUp className="h-5 w-5 text-gray-500" /> : <ChevronDown className="h-5 w-5 text-gray-500" />}
            </button>

            {expandedCategories[category] && (
              <div className="px-6 pb-4">
                <div className="space-y-3">
                  {getCategoryRepos(category).map((repo) => (
                    <div key={repo.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h5 className="font-semibold text-gray-900">{repo.full_name}</h5>
                          {repo.description && (
                            <p className="text-sm text-gray-600 mt-1">{repo.description}</p>
                          )}
                          <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                            <span className="flex items-center">
                              <Star className="h-4 w-4 mr-1" /> {repo.stargazers_count}
                            </span>
                            <span className="flex items-center">
                              <GitFork className="h-4 w-4 mr-1" /> {repo.forks_count}
                            </span>
                            <span>{repo.language || 'Unknown / 未知'}</span>
                            <span>Updated {new Date(repo.updated_at).toLocaleDateString()} / 更新于 {new Date(repo.updated_at).toLocaleDateString()}</span>
                          </div>
                          <div className="mt-2">
                            {repo.topics.map((topic) => (
                              <span key={topic} className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded mr-2"
                              >
                                {topic}
                              </span>
                            ))}
                          </div>
                        </div>
                        <a
                          href={repo.html_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-4 text-gray-400 hover:text-gray-600"
                        >
                          <ExternalLink className="h-5 w-5" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsDashboard;