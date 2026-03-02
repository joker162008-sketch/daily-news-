# 每日科技/AI资讯推送

## 功能
- 每天早上 7:00 自动抓取科技/AI 资讯
- 通过 Discord 推送（免费！）

## 文件
```
.github/workflows/
├── daily-news.yml    # GitHub Actions 工作流
├── fetch_news.py     # Python 抓取脚本
└── README.md        # 本说明
```

## 配置步骤

### 步骤 1: 创建 Discord Webhook

1. 打开你的 Discord 服务器
2. 点击服务器名称 → **服务器设置**
3. 点击 **整合** → **Webhooks**
4. 点击 **新建 Webhook**
5. 填写名称（如 "资讯推送"）
6. 点击 **复制 Webhook URL**

### 步骤 2: 部署到 GitHub

```bash
cd ~/.openclaw/workspace
git add .github/
git commit -m "Add daily news workflow"
git push
```

### 步骤 3: 配置 GitHub Secrets

在 GitHub 仓库设置中添加：

| Secret 名称 | 值 |
|------------|-----|
| `DISCORD_WEBHOOK_URL` | 你的 Discord Webhook URL |

### 步骤 4: 完成！

每天早上 7 点会自动推送资讯到你的 Discord！

---

## 测试

在 GitHub Actions 页面手动触发测试。

## 自定义

- 修改运行时间: 编辑 `daily-news.yml` 中的 cron 表达式
- 修改资讯源: 编辑 `fetch_news.py`
