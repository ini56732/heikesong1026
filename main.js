// 主页功能
document.addEventListener('DOMContentLoaded', function() {
  // 导航栏交互
  const navLinks = document.querySelectorAll('nav a');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
  
  // 模拟健康数据
  const healthData = {
    sleep: 7.5,
    steps: 8500,
    water: 6,
    heartRate: 72
  };
  
  // 更新健康数据展示
  updateHealthData(healthData);
  
  // 表单提交处理
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      handleSubmit(this);
    });
  });
  
  // 为按钮添加交互效果
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      // 添加点击效果
      this.classList.add('clicked');
      setTimeout(() => {
        this.classList.remove('clicked');
      }, 300);
    });
  });
});

// 更新健康数据展示
function updateHealthData(data) {
  const sleepElement = document.getElementById('sleep-hours');
  const stepsElement = document.getElementById('steps-count');
  const waterElement = document.getElementById('water-glasses');
  const heartElement = document.getElementById('heart-rate');
  
  if (sleepElement) sleepElement.textContent = data.sleep;
  if (stepsElement) stepsElement.textContent = data.steps;
  if (waterElement) waterElement.textContent = data.water;
  if (heartElement) heartElement.textContent = data.heartRate;
}

// 处理表单提交
function handleSubmit(form) {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  
  // 模拟提交过程
  showNotification('信息已保存成功！');
  
  // 重置表单
  form.reset();
}

// 显示通知
function showNotification(message) {
  // 检查是否已存在通知
  const existingNotification = document.querySelector('.notification');
  if (existingNotification) {
    existingNotification.remove();
  }
  
  // 创建通知元素
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  
  // 添加样式
  Object.assign(notification.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    backgroundColor: '#48bb78',
    color: 'white',
    padding: '1rem',
    borderRadius: '5px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    zIndex: '1000',
    opacity: '0',
    transition: 'opacity 0.3s'
  });
  
  // 添加到页面
  document.body.appendChild(notification);
  
  // 渐显效果
  setTimeout(() => {
    notification.style.opacity = '1';
  }, 10);
  
  // 3秒后渐隐并移除
  setTimeout(() => {
    notification.style.opacity = '0';
    setTimeout(() => {
      if (notification.parentNode) {
        document.body.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// 模拟数据加载
function loadData() {
  // 模拟加载过程
  const loading = document.getElementById('loading');
  if (loading) {
    loading.style.display = 'block';
    
    setTimeout(() => {
      loading.style.display = 'none';
      document.getElementById('content').style.display = 'block';
    }, 1000);
  }
}

// 健康评估表单处理
function handleAssessmentSubmit(form) {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  
  // 模拟评估过程
  showNotification('正在生成您的健康报告...');
  
  // 模拟处理时间
  setTimeout(() => {
    showNotification('健康评估已完成！您的个性化健康报告已生成。');
  }, 2000);
  
  // 重置表单
  form.reset();
}

// 症状自诊处理
function handleSymptomDiagnosis(form) {
  const symptoms = form.querySelector('#symptoms').value;
  const duration = form.querySelector('#duration').value;
  
  if (!symptoms || !duration) {
    showNotification('请完整填写症状信息');
    return;
  }
  
  // 模拟诊断过程
  showNotification('AI正在分析您的症状...');
  
  // 模拟处理时间
  setTimeout(() => {
    // 显示诊断结果
    const resultElement = document.getElementById('diagnosis-result');
    if (resultElement) {
      resultElement.style.display = 'block';
      showNotification('诊断完成，请查看结果');
    }
  }, 2000);
}

// 连接健康平台
function connectHealthPlatform() {
  showNotification('正在连接健康平台...');
  setTimeout(() => {
    showNotification('已成功连接健康平台！');
  }, 1500);
}

// 手动记录数据
function manualRecord() {
  showNotification('请在弹出窗口中输入您的健康数据');
  // 这里可以打开模态框或新页面进行数据录入
}

// 上传体检报告
function uploadMedicalReport() {
  showNotification('请选择您的体检报告文件');
  // 这里可以触发文件选择对话框
}