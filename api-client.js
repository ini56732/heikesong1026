/**
 * API 客户端模块
 * 封装所有 API 调用，统一处理错误和认证
 */

class APIClient {
    constructor(baseURL = 'http://127.0.0.1:5000/api') {
        this.baseURL = baseURL;
        this.timeout = 10000; // 10秒超时
    }

    /**
     * 发送请求
     * @param {string} endpoint API 端点
     * @param {Object} options 请求选项
     * @returns {Promise<Object>} 响应数据
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // 添加认证令牌
        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);

            const response = await fetch(url, {
                ...options,
                headers,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            // 检查令牌是否过期
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
                window.location.href = '/pages/login.html';
                throw new Error('登录已过期，请重新登录');
            }

            const data = await response.json();

            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.error || data.message || '请求失败',
                    data: data
                };
            }

            return data;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('请求超时，请检查网络连接');
            }
            throw error;
        }
    }

    /**
     * GET 请求
     */
    get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    /**
     * POST 请求
     */
    post(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * PUT 请求
     */
    put(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * DELETE 请求
     */
    delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}

// 创建全局 API 客户端实例
const API = new APIClient();

/**
 * 统一的错误处理函数
 * @param {Error} error 错误对象
 * @param {string} defaultMessage 默认错误信息
 */
function handleAPIError(error, defaultMessage = '请求失败') {
    let message = defaultMessage;
    let details = '';

    if (typeof error === 'string') {
        message = error;
    } else if (error.message) {
        message = error.message;
        if (error.data) {
            details = JSON.stringify(error.data);
        }
    }

    // 显示错误通知
    showNotification(message, 'error');

    // 输出详细错误日志
    if (details) {
        console.error('[API Error]', message, details);
    } else {
        console.error('[API Error]', message);
    }

    return { error: true, message, details };
}

/**
 * 显示通知信息
 * @param {string} message 消息内容
 * @param {string} type 消息类型 ('success', 'error', 'warning', 'info')
 * @param {number} duration 显示时长（毫秒）
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    const styles = {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem',
        borderRadius: '8px',
        zIndex: '10000',
        maxWidth: '400px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        animation: 'slideIn 0.3s ease-out',
        fontWeight: '500',
        fontSize: '0.95rem'
    };

    // 设置颜色
    const colors = {
        success: { bg: '#f0fff4', text: '#22543d', border: '#9ae6b4' },
        error: { bg: '#fff5f5', text: '#742a2a', border: '#fc8181' },
        warning: { bg: '#fffaf0', text: '#7c2d12', border: '#fbd38d' },
        info: { bg: '#ebf8ff', text: '#2c5282', border: '#90cdf4' }
    };

    const color = colors[type] || colors.info;
    Object.assign(styles, {
        backgroundColor: color.bg,
        color: color.text,
        border: `1px solid ${color.border}`
    });

    Object.assign(notification.style, styles);
    document.body.appendChild(notification);

    // 自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, duration);
}

// 添加动画样式
if (!document.querySelector('style[data-notifications]')) {
    const style = document.createElement('style');
    style.setAttribute('data-notifications', 'true');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}
