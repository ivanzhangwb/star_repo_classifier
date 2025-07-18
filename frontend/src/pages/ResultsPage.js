import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { classificationAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Loader2, AlertCircle, BarChart3, GitFork, Star, Clock, ExternalLink, WifiOff } from 'lucide-react';
import ProcessingStatus from '../components/ProgressBar';
import ResultsDashboard from '../components/ResultsDashboard';

const ResultsPage = () => {
  const { jobId } = useParams();
  const [polling, setPolling] = useState(true);
  const [online, setOnline] = useState(navigator.onLine);

  const jobQuery = useQuery(
    ['job', jobId],
    () => classificationAPI.getJobStatus(jobId),
    {
      refetchInterval: polling ? 3000 : false,
      staleTime: 0,
      cacheTime: 0,
      retry: 5,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    }
  );

  const resultsQuery = useQuery(
    ['results', jobId],
    () => classificationAPI.getResults(jobId),
    {
      enabled: jobQuery.data?.status === 'completed',
      staleTime: 0,
      cacheTime: 0,
      retry: 3,
      retryDelay: 2000,
    }
  );

  useEffect(() => {
    const handleOnline = () => {
      setOnline(true);
      toast.success('Connection restored');
      if (jobQuery.data?.status === 'processing') {
        setPolling(true);
      }
    };
    const handleOffline = () => {
      setOnline(false);
      toast.error('Connection lost. Will retry when connection is restored.');
      setPolling(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [jobQuery.data?.status]);

  useEffect(() => {
    if (jobQuery.data?.status === 'completed') {
      setPolling(false);
    }
    if (jobQuery.data?.status === 'failed') {
      setPolling(false);
      toast.error(`Classification failed: ${jobQuery.data.error}`);
    }
  }, [jobQuery.data]);

  const handleRetry = () => {
    setPolling(true);
    jobQuery.refetch();
  };

  if (jobQuery.isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (jobQuery.data?.status === 'failed') {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
            <h3 className="text-lg font-medium text-red-800">Classification Failed</h3>
          </div>
          <p className="mt-2 text-red-700">{jobQuery.data.error}</p>
          <button
            onClick={handleRetry}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (jobQuery.data?.status === 'processing') {
    const elapsedTime = Math.floor((Date.now() - new Date(jobQuery.data.created_at).getTime()) / 1000);
    
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        {!online && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center">
              <WifiOff className="h-5 w-5 text-yellow-600 mr-2" />
              <span className="text-sm text-yellow-800 font-medium">Connection Lost - Will retry when connected / 连接丢失 - 恢复连接后重试</span>
            </div>
          </div>
        )}
        
        <ProcessingStatus
          status="Analyzing your starred repositories / 正在分析您的收藏仓库"
          elapsedTime={elapsedTime}
          totalRepos={jobQuery.data.total_repos}
          currentStep={Math.min(Math.floor(elapsedTime / 30) + 1, 3)}
          totalSteps={3}
        />
        
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <Clock className="h-5 w-5 text-amber-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-amber-800">Processing Information / 处理信息</h3>
              <div className="mt-2 text-sm text-amber-700">
                <p><strong>Started:</strong> {new Date(jobQuery.data.created_at).toLocaleString()} / <strong>开始时间：</strong>{new Date(jobQuery.data.created_at).toLocaleString()}</p>
                {jobQuery.data.total_repos && (
                  <p><strong>Total repositories:</strong> {jobQuery.data.total_repos} / <strong>总仓库数：</strong>{jobQuery.data.total_repos}</p>
                )}
                <p>This process typically takes 2-5 minutes depending on the number of repositories. / 此过程通常需要2-5分钟，取决于仓库数量。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (resultsQuery.data) {
    const { repos, stats } = resultsQuery.data;
    
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Classification Results</h1>
              <p className="text-gray-600 mt-1">Your GitHub stars have been successfully classified!</p>
            </div>
            <a
              href={`http://localhost:8000/view/${jobId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              View Full Report / 查看完整报告
            </a>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-blue-600 mr-2" />
                <div>
                  <p className="text-2xl font-bold text-blue-900">{stats.total_repos}</p>
                  <p className="text-sm text-blue-700">Total Repositories / 总仓库数</p>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-green-600 mr-2" />
                <div>
                  <p className="text-2xl font-bold text-green-900">{stats.total_stars.toLocaleString()}</p>
                  <p className="text-sm text-green-700">Total Stars / 总星标数</p>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center">
                <GitFork className="h-8 w-8 text-purple-600 mr-2" />
                <div>
                  <p className="text-2xl font-bold text-purple-900">{Object.keys(stats.categories).length}</p>
                  <p className="text-sm text-purple-700">Categories / 分类数</p>
                </div>
              </div>
            </div>
            
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-orange-600 mr-2" />
                <div>
                  <p className="text-2xl font-bold text-orange-900">{Math.round(stats.avg_stars)}</p>
                  <p className="text-sm text-orange-700">Avg Stars / 平均星标</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <ResultsDashboard repos={repos} stats={stats} />
      </div>
    );
  }

  return null;
};

export default ResultsPage;