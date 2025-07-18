import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from 'react-query';
import toast from 'react-hot-toast';
import { classificationAPI } from '../services/api';
import { Shield, Loader2 } from 'lucide-react';

const ClassificationPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    token: '',
    min_stars: 0,
    exclude_forks: true,
    include_archived: false,
  });

  const mutation = useMutation(
    (config) => classificationAPI.startClassification(config),
    {
      onSuccess: (data) => {
        toast.success('Classification started!');
        navigate(`/results/${data.job_id}`);
      },
      onError: (error) => {
        toast.error('Failed to start classification: ' + error.message);
      },
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.token.trim()) {
      toast.error('Please enter your GitHub token');
      return;
    }
    mutation.mutate(formData);
  };

  if (mutation.isLoading) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <div className="relative mx-auto mb-4">
            <div className="w-16 h-16 mx-auto">
              <Loader2 className="h-16 w-16 animate-spin text-primary-600" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Processing Request / 处理请求中</h2>
          <p className="text-gray-600 mb-4">
            We're preparing your classification job. This won't take long... / 我们正在准备分类任务，很快就完成...
          </p>
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-md p-4">
            <p className="text-sm text-blue-700">
              <strong>Note:</strong> Please don't close this page or refresh. You'll be redirected to results shortly. / 
              <strong>注意：</strong>请不要关闭此页面或刷新，很快将跳转到结果页面。
            </p>
          </div>
        </div>
      </div>
    );
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : type === 'number' ? parseInt(value) : value,
    }));
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Classify Your Stars / 分类你的收藏</h1>
        <p className="text-gray-600 mb-6">Analyze your GitHub starred repositories / 分析你的GitHub收藏仓库</p>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="token" className="block text-sm font-medium text-gray-700 mb-2">
              GitHub Personal Access Token / GitHub个人访问令牌 *
            </label>
            <input
              type="password"
              id="token"
              name="token"
              required
              value={formData.token}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
            />
            <p className="mt-1 text-sm text-gray-500">
              Your token is used only for accessing your starred repositories and is never stored. / 
              您的令牌仅用于访问您的收藏仓库，不会被存储。
            </p>
          </div>

          <div>
            <label htmlFor="min_stars" className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Stars / 最少星标数
            </label>
            <input
              type="number"
              id="min_stars"
              name="min_stars"
              min="0"
              value={formData.min_stars}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <p className="mt-1 text-sm text-gray-500">
              Only include repositories with at least this many stars. / 仅包含至少有这么多星标的仓库。
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="exclude_forks"
                name="exclude_forks"
                checked={formData.exclude_forks}
                onChange={handleInputChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="exclude_forks" className="ml-2 block text-sm text-gray-900">
                Exclude forked repositories / 排除fork的仓库
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="include_archived"
                name="include_archived"
                checked={formData.include_archived}
                onChange={handleInputChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="include_archived" className="ml-2 block text-sm text-gray-900">
                Include archived repositories / 包含已归档的仓库
              </label>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <div className="flex">
              <Shield className="h-5 w-5 text-blue-400 mt-0.5" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">Security Notice / 安全提示</h3>
                <div className="mt-2 text-sm text-blue-700">
                  <p>
                    We recommend creating a token with only the <code className="bg-blue-100 px-1 rounded">public_repo</code> scope for public repositories, 
                    or <code className="bg-blue-100 px-1 rounded">repo</code> scope if you need to access private starred repositories. / 
                    我们建议使用仅包含<code className="bg-blue-100 px-1 rounded">public_repo</code>范围（公开仓库）或<code className="bg-blue-100 px-1 rounded">repo</code>范围（私有仓库）的令牌。
                  </p>
                </div>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={mutation.isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {mutation.isLoading ? (
              <>
                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                Starting Classification... / 开始分类中...
              </>
            ) : (
              'Start Classification / 开始分类'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ClassificationPage;