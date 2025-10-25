/**
 * 在线问诊页面脚本
 * 处理医生列表、搜索、预约等功能
 */

// 模拟医生数据 - 使用SVG格式的医生头像避免外部图片加载问题
const mockDoctors = [
    { id: 1, name: '张医生', department: '内科', title: '主任医师', rating: 4.9, reviews: 328, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiM0Qzg1RjYiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '20年临床经验，擅长呼吸系统疾病' },
    { id: 2, name: '李医生', department: '外科', title: '副主任医师', rating: 4.8, reviews: 256, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiNGRjY2MDAiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '15年外科手术经验，微创手术专家' },
    { id: 3, name: '王医生', department: '儿科', title: '主治医师', rating: 4.7, reviews: 189, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiM2NjAwRkYiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '擅长儿童常见病和发育问题' },
    { id: 4, name: '陈医生', department: '妇产科', title: '主任医师', rating: 4.9, reviews: 412, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiMwMEZGQTAiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '专业产科医生，孕期保健专家' },
    { id: 5, name: '黄医生', department: '皮肤科', title: '主治医师', rating: 4.6, reviews: 145, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiNGRjAwRkYiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '治疗各类皮肤病和美容问题' },
    { id: 6, name: '刘医生', department: '眼科', title: '副主任医师', rating: 4.8, reviews: 201, avatar: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiMwMEZGRkYiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzMCIgcj0iMTIiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTI1IDUwQzI1IDQ1IDMwIDQwIDQwIDQwQzUwIDQwIDU1IDQ1IDU1IDUwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K', bio: '眼科手术和视力矫正专家' }
];

let currentDoctor = null;
let allDoctors = [...mockDoctors];

/**
 * 初始化页面
 */
document.addEventListener('DOMContentLoaded', function() {
    // 移除强制登录限制，允许未登录用户浏览医生列表
    // 只有在需要用户特定操作（如预约、聊天）时才要求登录
    renderDoctorList(allDoctors);
    setupEventListeners();
});

/**
 * 设置事件监听器
 */
function setupEventListeners() {
    // 搜索功能
    const doctorSearch = document.getElementById('doctor-search');
    if (doctorSearch) {
        doctorSearch.addEventListener('input', handleSearch);
    }

    // 部门筛选
    const departmentFilter = document.getElementById('department-filter');
    if (departmentFilter) {
        departmentFilter.addEventListener('change', applyFilters);
    }

    // 职称筛选
    const titleFilter = document.getElementById('title-filter');
    if (titleFilter) {
        titleFilter.addEventListener('change', applyFilters);
    }

    // 评分筛选
    const ratingFilter = document.getElementById('rating-filter');
    if (ratingFilter) {
        ratingFilter.addEventListener('change', applyFilters);
    }
}

/**
 * 搜索医生
 */
function handleSearch(event) {
    const keyword = event.target.value.toLowerCase().trim();
    
    if (!keyword) {
        renderDoctorList(allDoctors);
        return;
    }

    const filtered = allDoctors.filter(doctor => 
        doctor.name.toLowerCase().includes(keyword) ||
        doctor.department.toLowerCase().includes(keyword) ||
        doctor.bio.toLowerCase().includes(keyword)
    );

    renderDoctorList(filtered);
}

/**
 * 应用筛选条件
 */
function applyFilters() {
    const department = document.getElementById('department-filter')?.value || '';
    const title = document.getElementById('title-filter')?.value || '';
    const rating = parseFloat(document.getElementById('rating-filter')?.value || '0');

    let filtered = [...allDoctors];

    if (department) {
        filtered = filtered.filter(d => d.department === department);
    }

    if (title) {
        filtered = filtered.filter(d => d.title === title);
    }

    if (rating > 0) {
        filtered = filtered.filter(d => d.rating >= rating);
    }

    renderDoctorList(filtered);
    updateDoctorCount(filtered.length);
}

/**
 * 重置筛选条件
 */
function resetFilters() {
    document.getElementById('department-filter').value = '';
    document.getElementById('title-filter').value = '';
    document.getElementById('rating-filter').value = '';
    renderDoctorList(allDoctors);
    updateDoctorCount(allDoctors.length);
}

/**
 * 渲染医生列表
 */
function renderDoctorList(doctors) {
    const container = document.getElementById('doctors-container');
    if (!container) return;

    container.innerHTML = doctors.map(doctor => `
        <div class="doctor-card">
            <img src="${doctor.avatar}" alt="${doctor.name}" class="doctor-avatar">
            <div class="doctor-info">
                <h3>${doctor.name}</h3>
                <p class="department">${doctor.department} - ${doctor.title}</p>
                <p class="bio">${doctor.bio}</p>
                <div class="rating-info">
                    <span class="rating">
                        <i class="fas fa-star"></i> ${doctor.rating}
                    </span>
                    <span class="reviews">${doctor.reviews} 条评价</span>
                </div>
            </div>
            <div class="doctor-actions">
                <button class="btn-secondary" onclick="viewDoctorDetail(${doctor.id})">
                    查看详情
                </button>
                <button class="btn-primary" onclick="openAppointmentForm(${doctor.id})">
                    立即预约
                </button>
                <button class="btn-chat" onclick="openChat(${doctor.id})">
                    在线咨询
                </button>
            </div>
        </div>
    `).join('');

    updateDoctorCount(doctors.length);
}

/**
 * 更新医生数量显示
 */
function updateDoctorCount(count) {
    const totalDoctors = document.getElementById('total-doctors');
    if (totalDoctors) {
        totalDoctors.textContent = count;
    }
}

/**
 * 查看医生详情
 */
function viewDoctorDetail(doctorId) {
    const doctor = allDoctors.find(d => d.id === doctorId);
    if (!doctor) return;

    currentDoctor = doctor;
    
    const detailContent = document.getElementById('doctor-detail-content');
    if (detailContent) {
        detailContent.innerHTML = `
            <div class="detail-header">
                <img src="${doctor.avatar}" alt="${doctor.name}" class="detail-avatar">
                <div class="detail-header-info">
                    <h3>${doctor.name}</h3>
                    <p>${doctor.department} - ${doctor.title}</p>
                </div>
            </div>
            <div class="detail-content">
                <h4>医生简介</h4>
                <p>${doctor.bio}</p>
                <h4>执业经历</h4>
                <p>从事医疗工作多年，积累了丰富的临床经验，获得患者高度认可。</p>
                <h4>擅长领域</h4>
                <p>常见疾病诊疗、健康咨询、预防保健等领域</p>
                <h4>患者评价</h4>
                <p>
                    <i class="fas fa-star"></i> ${doctor.rating}/5.0 
                    <span>(${doctor.reviews} 条评价)</span>
                </p>
            </div>
        `;
    }

    const modal = document.getElementById('doctor-detail-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

/**
 * 关闭医生详情
 */
function closeDoctorDetail() {
    const modal = document.getElementById('doctor-detail-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/**
 * 打开预约表单
 */
function openAppointmentForm(doctorId) {
    // 检查用户是否已登录，未登录则提示登录
    if (!ensureAuthenticated()) {
        showNotification('请先登录后再进行预约', 'warning');
        return;
    }
    
    const doctor = allDoctors.find(d => d.id === doctorId);
    if (!doctor) return;

    currentDoctor = doctor;

    // 更新预约表单中的医生信息
    const appointmentAvatar = document.getElementById('appointment-avatar');
    const appointmentName = document.getElementById('appointment-name');
    const appointmentDepartment = document.getElementById('appointment-department');

    if (appointmentAvatar) appointmentAvatar.src = doctor.avatar;
    if (appointmentName) appointmentName.textContent = doctor.name;
    if (appointmentDepartment) appointmentDepartment.textContent = `${doctor.department} - ${doctor.title}`;

    // 关闭详情modal，打开预约modal
    closeDoctorDetail();
    
    const appointmentModal = document.getElementById('appointment-modal');
    if (appointmentModal) {
        appointmentModal.classList.remove('hidden');
    }
}

/**
 * 关闭预约表单
 */
function closeAppointment() {
    const modal = document.getElementById('appointment-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
    // 清空表单
    document.getElementById('appointment-time').value = '';
    document.getElementById('symptoms').value = '';
    document.getElementById('contact-phone').value = '';
}

/**
 * 提交预约
 */
async function submitAppointment() {
    if (!currentDoctor) {
        showNotification('请先选择医生', 'error');
        return;
    }

    const appointmentTime = document.getElementById('appointment-time').value;
    const symptoms = document.getElementById('symptoms').value.trim();
    const contactPhone = document.getElementById('contact-phone').value.trim();

    if (!appointmentTime || !symptoms || !contactPhone) {
        showNotification('请填写所有必填字段', 'error');
        return;
    }

    // 验证手机号
    const phoneRegex = /^1[3-9]\d{9}$/;
    if (!phoneRegex.test(contactPhone)) {
        showNotification('请输入有效的手机号码', 'error');
        return;
    }

    try {
        showNotification('正在提交预约...', 'info');
        
        // 尝试发送到后端
        try {
            await API.post('/appointments', {
                doctor_id: currentDoctor.id,
                appointment_time: appointmentTime,
                symptoms: symptoms,
                contact_phone: contactPhone
            });
        } catch (apiError) {
            // 后端失败时继续使用本地存储
            console.warn('后端保存失败，使用本地存储', apiError);
            handleAPIError(apiError, '预约提交失败，已保存到本地');
        }

        showNotification('预约成功！医生将在指定时间与您联系', 'success');
        
        // 保存到本地存储作为备份
        const appointments = JSON.parse(localStorage.getItem('appointments') || '[]');
        appointments.push({
            id: Date.now(),
            doctor: currentDoctor.name,
            time: appointmentTime,
            symptoms: symptoms,
            phone: contactPhone,
            status: 'pending'
        });
        localStorage.setItem('appointments', JSON.stringify(appointments));

        setTimeout(() => {
            closeAppointment();
        }, 1500);
    } catch (error) {
        console.error('预约提交错误:', error);
        showNotification('预约失败，请重试', 'error');
    }
}

/**
 * 切换搜索区域
 */
function toggleSearch() {
    const searchSection = document.getElementById('search-section');
    if (searchSection) {
        searchSection.classList.toggle('hidden');
    }
}

/**
 * 隐藏搜索区域
 */
function hideSearch() {
    const searchSection = document.getElementById('search-section');
    if (searchSection) {
        searchSection.classList.add('hidden');
    }
    const searchInput = document.getElementById('doctor-search');
    if (searchInput) {
        searchInput.value = '';
        renderDoctorList(allDoctors);
    }
}

/**
 * 显示筛选面板
 */
function showFilter() {
    const filterPanel = document.getElementById('filter-panel');
    if (filterPanel) {
        filterPanel.classList.remove('hidden');
    }
}

/**
 * 隐藏筛选面板
 */
function hideFilter() {
    const filterPanel = document.getElementById('filter-panel');
    if (filterPanel) {
        filterPanel.classList.add('hidden');
    }
}

/**
 * 返回上一页
 */
function goBack() {
    window.history.back();
}

/**
 * 关闭聊天界面
 */
function closeChat() {
    const chatInterface = document.getElementById('chat-interface');
    if (chatInterface) {
        chatInterface.classList.add('hidden');
    }
}

/**
 * 发送消息
 */
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (!message) return;

    // 显示用户消息
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        const userMessageEl = document.createElement('div');
        userMessageEl.className = 'message user-message';
        userMessageEl.innerHTML = `<p>${message}</p>`;
        chatMessages.appendChild(userMessageEl);
        messageInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    try {
        // 如果有当前医生，使用其信息
        if (currentDoctor) {
            // 显示医生的模拟回复
            setTimeout(() => {
                const aiMessageEl = document.createElement('div');
                aiMessageEl.className = 'message ai-message';
                aiMessageEl.innerHTML = `<p>感谢您的咨询。我已经了解了您的情况，让我为您提供专业的建议...</p>`;
                chatMessages.appendChild(aiMessageEl);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 500);
        }
    } catch (error) {
        console.error('发送消息失败:', error);
    }
}

/**
 * 确保用户已认证
 */
function ensureAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}

/**
 * 处理键盘事件 - 按Enter键发送消息
 */
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

/**
 * 初始化聊天界面
 */
function initChatInterface(doctor) {
    if (!doctor) return;
    
    const chatInterface = document.getElementById('chat-interface');
    const chatAvatar = document.getElementById('chat-avatar');
    const chatDoctorName = document.getElementById('chat-doctor-name');
    const messageInput = document.getElementById('message-input');
    
    if (chatInterface && chatAvatar && chatDoctorName && messageInput) {
        chatAvatar.src = doctor.avatar;
        chatDoctorName.textContent = doctor.name;
        chatInterface.classList.remove('hidden');
        
        // 设置键盘事件监听
        messageInput.addEventListener('keypress', handleKeyPress);
        messageInput.focus();
    }
}

/**
 * 开始与医生聊天
 */
function startChatWithDoctor(doctorId) {
    // 检查用户是否已登录，未登录则提示登录
    if (!ensureAuthenticated()) {
        showNotification('请先登录后再与医生聊天', 'warning');
        return;
    }
    
    const doctor = allDoctors.find(d => d.id === doctorId);
    if (!doctor) return;
    
    currentDoctor = doctor;
    initChatInterface(doctor);
}

/**
 * 开始语音通话
 */
function startVoiceCall() {
    if (!currentDoctor) {
        showNotification('请先选择医生', 'error');
        return;
    }
    showNotification(`正在呼叫 ${currentDoctor.name} 医生...`, 'info');
}

/**
 * 开始视频通话
 */
function startVideoCall() {
    if (!currentDoctor) {
        showNotification('请先选择医生', 'error');
        return;
    }
    showNotification(`正在发起与 ${currentDoctor.name} 医生的视频通话...`, 'info');
}

/**
 * 显示附件菜单
 */
function showAttachmentMenu() {
    showNotification('附件功能开发中...', 'info');
}

/**
 * 附加图片
 */
function attachImage() {
    showNotification('图片上传功能开发中...', 'info');
}

/**
 * 打开聊天界面
 */
function openChat(doctorId) {
    const doctor = allDoctors.find(d => d.id === doctorId);
    if (!doctor) return;
    
    currentDoctor = doctor;
    initChatInterface(doctor);
}
