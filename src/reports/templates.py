"""
HTML模板模块
严格按照main-backup中的实现，包含图片报告和PDF报告的不同HTML模板
"""


class HTMLTemplates:
    """HTML模板管理类"""
    
    @staticmethod
    def get_image_template() -> str:
        """获取图片报告的HTML模板（使用{{ }}占位符）"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>群聊日常分析报告</title>
    <link href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            min-height: 100%;
        }

        body {
            font-family: 'ZCOOL KuaiLe', 'Ma Shan Zheng', 'Noto Sans SC', sans-serif;
            min-height: 100vh;
            margin: 0;
            background: url('白猫心路.png') repeat;
            background-size: auto;
            position: relative;
            line-height: 1.6;
        }

        /* Glassmorphism overlay */
        .glass-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            min-height: 100vh;
            background: linear-gradient(135deg, rgba(255, 182, 193, 0.75), rgba(255, 192, 203, 0.7), rgba(255, 218, 224, 0.65));
            pointer-events: none;
        }

        .container {
            position: relative;
            width: 100%;
            min-height: 100vh;
            display: grid;
            grid-template-rows: auto 1fr auto;
            padding: 2vh 2vw;
            gap: 2vh;
            z-index: 1;
        }

        /* Header */
        .header {
            background: rgba(255, 240, 245, 0.65);
            border: 2px solid rgba(255, 182, 193, 0.6);
            border-radius: 20px;
            padding: 1.5vh 3vw;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 192, 203, 0.25);
        }

        .header h1 {
            font-size: clamp(1.5rem, 3vh, 2.5rem);
            font-weight: 400;
            color: #ff69b4;
            text-shadow: 0 2px 4px rgba(255, 105, 180, 0.2);
            margin-bottom: 0.5vh;
            letter-spacing: 2px;
        }

        .header .date {
            font-size: clamp(0.9rem, 1.5vh, 1.1rem);
            color: #ff85c0;
            font-weight: 400;
            text-shadow: none;
        }

        /* Main Content Grid */
        .content {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: auto 1fr;
            gap: 2vh 1.5vw;
            align-items: stretch;
        }

        /* Glass Card Base */
        .glass-card {
            background: rgba(255, 240, 245, 0.65);
            border: 2px solid rgba(255, 182, 193, 0.6);
            border-radius: 15px;
            padding: 1.5vh 1.5vw;
            box-shadow: 0 4px 15px rgba(255, 192, 203, 0.25);
            display: flex;
            flex-direction: column;
        }

        /* Stats Section - Full Width */
        .stats-section {
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1vw;
        }

        .section {
            margin-bottom: 0;
        }

        .full-width-section {
            grid-column: 1 / -1;
            margin-bottom: 0;
        }

        .section-title {
            font-size: clamp(1rem, 1.8vh, 1.3rem);
            font-weight: 500;
            color: #ff69b4;
            text-shadow: 0 2px 4px rgba(255, 105, 180, 0.2);
            margin-bottom: 1vh;
            padding-bottom: 0.8vh;
            border-bottom: 2px solid rgba(255, 182, 193, 0.4);
        }

        .stat-card {
            background: rgba(255, 240, 245, 0.65);
            border: 2px solid rgba(255, 182, 193, 0.6);
            border-radius: 12px;
            padding: 1.5vh 1vw;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 192, 203, 0.25);
        }

        .stat-number {
            font-size: clamp(1.5rem, 3vh, 2.5rem);
            font-weight: 400;
            color: #ff69b4;
            text-shadow: 0 2px 4px rgba(255, 105, 180, 0.2);
            margin-bottom: 0.5vh;
        }

        .stat-label {
            font-size: clamp(0.7rem, 1.2vh, 0.9rem);
            color: #ff85c0;
            font-weight: 400;
            text-shadow: none;
        }

        /* Topics Section */
        .topics-section {
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }

        .topic-item {
            background: rgba(255, 250, 252, 0.5);
            border: 1.5px solid rgba(255, 182, 193, 0.5);
            border-radius: 10px;
            padding: 1vh 1vw;
        }

        .topic-header {
            display: flex;
            align-items: center;
            gap: 0.8vw;
            margin-bottom: 0.5vh;
        }

        .topic-number {
            background: linear-gradient(135deg, #ffb6c1, #ff69b4);
            color: #fff;
            width: clamp(25px, 3vh, 35px);
            height: clamp(25px, 3vh, 35px);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
            font-size: clamp(0.8rem, 1.5vh, 1rem);
            box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
            flex-shrink: 0;
        }

        .topic-title {
            font-weight: 500;
            color: #ff69b4;
            font-size: clamp(0.85rem, 1.4vh, 1.05rem);
            text-shadow: none;
        }

        .topic-contributors {
            color: #ff85c0;
            font-size: clamp(0.7rem, 1.1vh, 0.85rem);
            margin-bottom: 0.5vh;
            text-shadow: none;
        }

        .topic-detail {
            color: #ff9ec7;
            line-height: 1.4;
            font-size: clamp(0.75rem, 1.2vh, 0.9rem);
            font-weight: 400;
            text-shadow: none;
        }

        /* Users Section */
        .users-section {
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }

        .user-item {
            background: rgba(255, 250, 252, 0.5);
            border: 1.5px solid rgba(255, 182, 193, 0.5);
            border-radius: 10px;
            padding: 1vh 1vw;
            display: flex;
            align-items: center;
            gap: 1vw;
        }

        .user-avatar {
            width: clamp(35px, 5vh, 50px);
            height: clamp(35px, 5vh, 50px);
            border-radius: 50%;
            border: 2px solid #ffb6c1;
            box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
            flex-shrink: 0;
        }

        .user-avatar-placeholder {
            width: clamp(35px, 5vh, 50px);
            height: clamp(35px, 5vh, 50px);
            border-radius: 50%;
            background: linear-gradient(135deg, #ffb6c1, #ff85c0);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: clamp(1rem, 2vh, 1.5rem);
            color: #fff;
            border: 2px solid #ffb6c1;
            box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
            flex-shrink: 0;
        }

        .user-details {
            flex: 1;
            min-width: 0;
        }

        .user-name {
            font-weight: 500;
            color: #ff69b4;
            margin-bottom: 0.5vh;
            font-size: clamp(0.85rem, 1.4vh, 1.05rem);
            text-shadow: none;
        }

        .user-badges {
            display: flex;
            gap: 0.5vw;
            flex-wrap: wrap;
        }

        .user-badge {
            background: linear-gradient(135deg, #ffb6c1, #ff85c0);
            color: #fff;
            padding: 0.3vh 0.8vw;
            border-radius: 12px;
            font-size: clamp(0.65rem, 1vh, 0.8rem);
            font-weight: 400;
            box-shadow: 0 2px 6px rgba(255, 105, 180, 0.3);
            text-shadow: none;
        }

        /* Quotes Section */
        .quotes-section {
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }

        .quote-item {
            background: rgba(255, 250, 252, 0.5);
            border: 1.5px solid rgba(255, 182, 193, 0.5);
            border-left: 3px solid #ff69b4;
            border-radius: 10px;
            padding: 1vh 1vw;
        }

        .quote-content {
            font-size: clamp(0.8rem, 1.3vh, 0.95rem);
            color: #ff85c0;
            font-weight: 400;
            line-height: 1.4;
            margin-bottom: 0.5vh;
            font-style: italic;
            text-shadow: none;
        }

        .quote-author {
            font-size: clamp(0.7rem, 1.1vh, 0.85rem);
            color: #ff69b4;
            font-weight: 500;
            text-align: right;
            text-shadow: none;
        }

        .quote-reason {
            font-size: clamp(0.65rem, 1vh, 0.8rem);
            color: #ff9ec7;
            font-style: normal;
            background: rgba(255, 182, 193, 0.2);
            padding: 0.5vh 0.8vw;
            border-radius: 8px;
            border-left: 2px solid #ff69b4;
            margin-top: 0.5vh;
        }

        /* Footer */
        .footer {
            background: rgba(255, 240, 245, 0.65);
            border: 2px solid rgba(255, 182, 193, 0.6);
            border-radius: 20px;
            padding: 1.2vh 2vw;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 192, 203, 0.25);
        }

        .footer-text {
            font-size: clamp(0.7rem, 1.1vh, 0.85rem);
            color: #ff85c0;
            font-weight: 400;
            text-shadow: none;
            line-height: 1.6;
        }

        /* Activity Chart Section */
        .activity-section {
            display: flex;
            flex-direction: column;
        }

        .activity-chart {
            display: flex;
            flex-direction: column;
            gap: 0.4vh;
        }

        .hour-bar {
            display: flex;
            align-items: center;
            gap: 0.8vw;
        }

        .hour-label {
            width: 3.5vw;
            text-align: right;
            color: #ff85c0;
            font-size: clamp(0.7rem, 1.1vh, 0.85rem);
            font-weight: 400;
            flex-shrink: 0;
            text-shadow: none;
        }

        .bar-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            gap: 0.5vw;
        }

        .bar {
            height: clamp(8px, 1.2vh, 12px);
            background: linear-gradient(90deg, #ffb6c1, #ff69b4);
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(255, 105, 180, 0.3);
        }

        .bar-value {
            color: #ff69b4;
            font-size: clamp(0.65rem, 1vh, 0.8rem);
            font-weight: 500;
            min-width: 2vw;
            text-align: right;
            flex-shrink: 0;
            text-shadow: none;
        }

        /* Stats Grid - 5 columns */
        .stats-grid {
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1vw;
            margin-bottom: 2vh;
        }

        /* Active Period Card */
        .active-period {
            grid-column: 1 / -1;
            background: rgba(255, 240, 245, 0.65);
            border: 2px solid rgba(255, 182, 193, 0.6);
            border-radius: 15px;
            padding: 2vh 2vw;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 192, 203, 0.25);
            margin-bottom: 2vh;
        }

        .active-period .time {
            font-size: clamp(1.8rem, 3.5vh, 2.8rem);
            font-weight: 400;
            color: #ff69b4;
            text-shadow: 0 2px 4px rgba(255, 105, 180, 0.2);
            margin-bottom: 0.5vh;
        }

        .active-period .label {
            font-size: clamp(0.8rem, 1.3vh, 1rem);
            color: #ff85c0;
            font-weight: 400;
        }

        /* Activity Chart Container */
        .activity-chart-container {
            grid-column: 1 / 2;
        }

        /* Topics Grid - spans column 2 */
        .topics-grid {
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }

        /* Users Grid - spans column 3 */
        .users-grid {
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }

        /* User Title Structure */
        .user-title {
            background: rgba(255, 250, 252, 0.5);
            border: 1.5px solid rgba(255, 182, 193, 0.5);
            border-radius: 10px;
            padding: 1vh 1vw;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1vw;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 1vw;
            flex: 1;
            min-width: 0;
        }

        .user-title-badge {
            background: linear-gradient(135deg, #ffb6c1, #ff85c0);
            color: #fff;
            padding: 0.3vh 0.8vw;
            border-radius: 12px;
            font-size: clamp(0.65rem, 1vh, 0.8rem);
            font-weight: 400;
            box-shadow: 0 2px 6px rgba(255, 105, 180, 0.3);
            text-shadow: none;
            white-space: nowrap;
        }

        .user-mbti {
            background: linear-gradient(135deg, #ff85c0, #ff69b4);
            color: #fff;
            padding: 0.3vh 0.8vw;
            border-radius: 12px;
            font-size: clamp(0.65rem, 1vh, 0.8rem);
            font-weight: 400;
            box-shadow: 0 2px 6px rgba(255, 105, 180, 0.3);
            text-shadow: none;
            white-space: nowrap;
        }

        .user-reason {
            color: #ff9ec7;
            font-size: clamp(0.7rem, 1.1vh, 0.85rem);
            text-align: right;
            line-height: 1.4;
            font-weight: 400;
            flex-shrink: 0;
            max-width: 40%;
        }

    </style>
</head>
<body>
    <div class="glass-overlay"></div>
    <div class="container">
        <div class="header">
            <h1>📊 群聊日常分析报告</h1>
            <div class="date">{{ current_date }}</div>
        </div>
        <div class="content">
            <!-- Stats Section - Full Width -->
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-number">{{ message_count }}</div><div class="stat-label">消息总数</div></div>
                <div class="stat-card"><div class="stat-number">{{ participant_count }}</div><div class="stat-label">参与人数</div></div>
                <div class="stat-card"><div class="stat-number">{{ total_characters }}</div><div class="stat-label">总字符数</div></div>
                <div class="stat-card"><div class="stat-number">{{ emoji_count }}</div><div class="stat-label">表情数量</div></div>
                <div class="stat-card"><div class="stat-number">{{ most_active_period }}</div><div class="stat-label">最活跃时段</div></div>
            </div>

            <!-- Activity Chart Section -->
            <div class="glass-card activity-section">
                <h2 class="section-title">⏱️ 24小时活跃度</h2>
                {{ hourly_chart_html | safe }}
            </div>

            <!-- Topics Section -->
            <div class="glass-card">
                <h2 class="section-title">💬 热门话题</h2>
                <div class="topics-grid">{{ topics_html | safe }}</div>
            </div>

            <!-- Users Section -->
            <div class="glass-card">
                <h2 class="section-title">🏆 群友称号</h2>
                <div class="users-grid">{{ titles_html | safe }}</div>
            </div>

            <!-- Quotes Section -->
            <div class="glass-card">
                <h2 class="section-title">💬 群圣经</h2>
                <div class="quotes-section">{{ quotes_html | safe }}</div>
            </div>
        </div>
        <div class="footer">
            <div class="footer-text">
                由 AstrBot QQ群日常分析插件 生成 | {{ current_datetime }} | SXP-Simon/astrbot-qq-group-daily-analysis<br>
                <small style="opacity: 0.8; font-size: 0.9em;">🤖 AI分析消耗：{{ total_tokens }} tokens (输入: {{ prompt_tokens }}, 输出: {{ completion_tokens }})</small>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    @staticmethod
    def get_pdf_template() -> str:
        """获取PDF报告的HTML模板（使用{}占位符）"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>群聊日常分析报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
            background: #ffffff;
            color: #1a1a1a;
            line-height: 1.6;
            font-size: 14px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: #ffffff;
            padding: 30px;
            text-align: center;
            border-radius: 12px;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .header .date {
            font-size: 16px;
            opacity: 0.9;
        }

        .section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #4a5568;
            border-bottom: 2px solid #4299e1;
            padding-bottom: 8px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: #f8f9ff;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }

        .stat-number {
            font-size: 24px;
            font-weight: 600;
            color: #4299e1;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 12px;
            color: #666666;
            text-transform: uppercase;
        }

        .active-period {
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: #ffffff;
            padding: 25px;
            text-align: center;
            margin: 30px 0;
            border-radius: 8px;
        }

        .active-period .time {
            font-size: 28px;
            font-weight: 300;
            margin-bottom: 5px;
        }

        .active-period .label {
            font-size: 14px;
            opacity: 0.9;
        }

        .topic-item {
            background: #ffffff;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }

        .topic-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }

        .topic-number {
            background: #4299e1;
            color: #ffffff;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            margin-right: 12px;
            font-size: 12px;
        }

        .topic-title {
            font-weight: 600;
            color: #2d3748;
            font-size: 16px;
        }

        .topic-contributors {
            color: #666666;
            font-size: 12px;
            margin-bottom: 10px;
        }

        .topic-detail {
            color: #333333;
            line-height: 1.6;
            font-size: 14px;
        }

        .user-title {
            background: #ffffff;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            page-break-inside: avoid;
        }

        .user-info {
            display: flex;
            align-items: center;
            flex: 1;
        }

        .user-details {
            flex: 1;
        }

        .user-name {
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 16px;
        }

        .user-badges {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .user-title-badge {
            background: #4299e1;
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }

        .user-mbti {
            background: #667eea;
            color: #ffffff;
            padding: 4px 8px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 12px;
        }

        .user-reason {
            color: #666666;
            font-size: 12px;
            max-width: 200px;
            text-align: right;
            line-height: 1.4;
        }

        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 15px;
            border: 2px solid #e2e8f0;
            object-fit: cover;
            flex-shrink: 0;
        }

        .user-avatar-placeholder {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 18px;
            color: #666666;
            flex-shrink: 0;
        }

        .quote-item {
            background: #faf5ff;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }

        .quote-content {
            font-size: 16px;
            color: #2d3748;
            font-weight: 500;
            line-height: 1.6;
            margin-bottom: 10px;
            font-style: italic;
        }

        .quote-author {
            font-size: 14px;
            color: #4299e1;
            font-weight: 600;
            margin-bottom: 8px;
            text-align: right;
        }

        .quote-reason {
            font-size: 12px;
            color: #666666;
            background: rgba(66, 153, 225, 0.1);
            padding: 8px 12px;
            border-radius: 6px;
            border-left: 3px solid #4299e1;
        }

        .footer {
            background: #f8f9ff;
            color: #666666;
            text-align: center;
            padding: 20px;
            font-size: 12px;
            border-radius: 8px;
            margin-top: 40px;
        }

        /* PDF活跃度可视化样式 - 集成版本 */
        .activity-chart-container {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-top: 20px;
            page-break-inside: avoid;
        }

        .chart-header {
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
        }

        .chart-title {
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
        }

        .hour-bar-container {
            display: flex;
            align-items: center;
            margin: 6px 0;
            height: 16px;
        }

        .hour-label {
            width: 45px;
            text-align: left;
            color: #4a5568;
            font-size: 11px;
            font-weight: 500;
            flex-shrink: 0;
        }

        .bar-wrapper {
            display: flex;
            align-items: center;
            flex-grow: 1;
            gap: 8px;
            min-width: 0;
        }

        .bar {
            height: 6px;
            background-color: #4299e1;
            border-radius: 3px;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            overflow: hidden;
        }

        .hourly-value-outside {
            color: #4a5568;
            font-size: 10px;
            font-weight: 600;
            flex-shrink: 0;
            min-width: 25px;
            text-align: right;
        }

        .hourly-value-inside {
            color: white;
            font-size: 9px;
            padding: 0 4px;
            font-weight: 600;
            white-space: nowrap;
        }

        @media print {
            body {
                font-size: 12px;
            }

            .container {
                padding: 10px;
            }

            .header {
                padding: 20px;
            }

            .section {
                margin-bottom: 30px;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <h1>📊 群聊日常分析报告</h1>
            <div class="date">{current_date}</div>
        </div>
        <div class="section">
            <h2 class="section-title">📈 基础统计</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{message_count}</div>
                    <div class="stat-label">消息总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{participant_count}</div>
                    <div class="stat-label">参与人数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_characters}</div>
                    <div class="stat-label">总字符数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{emoji_count}</div>
                    <div class="stat-label">表情数量</div>
                </div>
            </div>
            <div class="active-period">
                <div class="time">{most_active_period}</div>
                <div class="label">最活跃时段</div>
            </div>
            <!-- 活跃度可视化部分 - 集成到基础统计 -->
            <div class="activity-chart-container">
                <div class="chart-header">
                    <div class="chart-title">⏱️ 活跃度分布</div>
                </div>
                {hourly_chart_html}
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">💬 热门话题</h2>
            {topics_html}
        </div>
        <div class="section">
            <h2 class="section-title">🏆 群友称号</h2>
            {titles_html}
        </div>
        <div class="section">
            <h2 class="section-title">💬 群圣经</h2>
            {quotes_html}
        </div>
        <div class="footer">
            由 AstrBot QQ群日常分析插件 生成 | {current_datetime} | SXP-Simon/astrbot-qq-group-daily-analysis<br>
            <small style="opacity: 0.8; font-size: 0.9em;">🤖 AI分析消耗：{total_tokens} tokens (输入: {prompt_tokens}, 输出:
                {completion_tokens})</small>
        </div>
    </div>
</body>

</html>"""
