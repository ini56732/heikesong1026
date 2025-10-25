/**
 * 认证管理模块
 * 处理用户登录、令牌管理和认证状态
 */

const AUTH = {
    API_URL: 'http://127.0.0.1:5000/api/auth',
    TOKEN_KEY: 'access_token',
    USER_KEY: 'user',

    /**
     * 获取存储的访问令牌
     * @returns {string|null} 令牌或null
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },

    /**
     * 获取当前登录用户信息
     * @returns {Object|null} 用户对象或null
     */
    getCurrentUser() {
        const user = localStorage.getItem(this.USER_KEY);
        return user ? JSON.parse(user) : null;
    },

    /**
     * 检查用户是否已登录
     * @returns {boolean} 是否已登录
     */
    isLoggedIn() {
        return !!this.getToken();
    },

    /**
     * 验证令牌有效性
     * @returns {Promise<boolean>} 令牌是否有效
     */
    async verifyToken() {
        const token = this.getToken();
        if (!token) return false;

        try {
            const response = await fetch(`${this.API_URL}/verify`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            return response.ok;
        } catch (error) {
            console.error('Token verification error:', error);
            return false;
        }
    },

    /**
     * 登出用户
     */
    logout() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
        window.location.href = '/pages/login.html';
    },

    /**
     * 为 API 请求添加授权头
     * @param {Object} headers 请求头对象
     * @returns {Object} 添加授权信息的请求头
     */
    addAuthHeader(headers = {}) {
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    /**
     * 发送经过授权的 API 请求
     * @param {string} endpoint API 端点
     * @param {Object} options 请求选项
     * @returns {Promise<Response>}
     */
    async authorizedFetch(endpoint, options = {}) {
        const headers = this.addAuthHeader(options.headers || {});
        return fetch(endpoint, { ...options, headers });
    }
};

/**
 * 页面加载时检查认证状态
 * 未登录用户将被重定向到登录页
 */
function ensureAuthenticated() {
    if (!AUTH.isLoggedIn()) {
        window.location.href = '/pages/login.html';
    }
}

/**
 * 在页面加载完成后执行认证检查
 */
document.addEventListener('DOMContentLoaded', function() {
    // 如果页面需要认证但用户未登录，重定向
    const requireAuth = document.documentElement.getAttribute('data-require-auth');
    if (requireAuth === 'true' && !AUTH.isLoggedIn()) {
        window.location.href = '/pages/login.html';
    }
});
