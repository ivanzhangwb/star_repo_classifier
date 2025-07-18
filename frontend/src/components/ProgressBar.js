import React from 'react';
import { Loader2 } from 'lucide-react';

const ProgressBar = ({ 
  current, 
  total, 
  status, 
  elapsedTime, 
  estimatedTime,
  label,
  showPercentage = true 
}) => {
  const percentage = total > 0 ? Math.min(Math.round((current / total) * 100), 100) : 0;
  
  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;
  };

  return (
    <div className="w-full space-y-4">
      {label && (
        <div className="flex justify-between items-center text-sm text-gray-600">
          <span>{label}</span>
          {showPercentage && <span>{percentage}%</span>}
        </div>
      )}
      
      <div className="relative">
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${percentage}%` }}
          />
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-2 h-2 bg-white rounded-full opacity-80 animate-pulse" />
        </div>
      </div>

      <div className="flex justify-between text-sm text-gray-500">
        <div className="flex items-center space-x-2">
          <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
          <span>{status}</span>
        </div>
        
        <div className="text-right space-y-1">
          {elapsedTime && (
            <div>Elapsed: {formatTime(elapsedTime)}</div>
          )}
          {estimatedTime && (
            <div className="text-gray-400">Est: {formatTime(estimatedTime)}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export const ProcessingStatus = ({ 
  status, 
  elapsedTime, 
  totalRepos = null,
  currentStep = 1,
  totalSteps = 3 
}) => {
  const steps = [
    { name: 'Fetching repositories / 获取仓库中', icon: '📥' },
    { name: 'Analyzing data / 分析数据中', icon: '🔍' },
    { name: 'Generating report / 生成报告中', icon: '📊' }
  ];

  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="text-center mb-6">
        <div className="w-20 h-20 mx-auto mb-4">
          <Loader2 className="h-20 w-20 animate-spin text-primary-600" />
        </div>
        <h3 className="text-xl font-bold text-gray-900">{status}</h3>
        <p className="text-gray-600 mt-2">Please wait while we process your request / 请等待我们处理您的请求</p>
      </div>

      <div className="space-y-4">
        {/* 步骤指示器 */}
        <div className="flex justify-between items-center">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col items-center space-y-2">
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center text-lg ${
                  index < currentStep 
                    ? 'bg-green-100 text-green-600 ring-2 ring-green-200' 
                    : index === currentStep - 1
                    ? 'bg-blue-100 text-blue-600 ring-2 ring-blue-200 animate-pulse'
                    : 'bg-gray-100 text-gray-400'
                }`}
              >
                {index < currentStep ? '✓' : step.icon}
              </div>
              <span className={`text-xs text-center ${
                index <= currentStep - 1 ? 'text-gray-900 font-medium' : 'text-gray-400'
              }`}
              >
                {step.name}
              </span>
            </div>
          ))}
        </div>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${Math.round((currentStep / totalSteps) * 100)}%` }}
          />
        </div>

        {/* 时间信息 */}
        <div className="flex justify-between text-sm text-gray-500">
          <span>Elapsed: {formatTime(elapsedTime)} / 已用时间: {formatTime(elapsedTime)}</span>
          {totalRepos && <span>{totalRepos} repositories to process / {totalRepos} 个仓库待处理</span>}
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;