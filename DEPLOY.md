# Deployment Guide: TRAE-D-SME-Pricing

本指南将帮助您将项目部署到 **Streamlit Community Cloud**，生成可公开访问的演示链接。

## 1. 准备工作 (Pre-requisites)

*   拥有一个 [GitHub](https://github.com/) 账号。
*   拥有一个 [Streamlit Community Cloud](https://share.streamlit.io/) 账号（可直接用 GitHub 登录）。

## 2. 上传代码到 GitHub (Push to GitHub)

请在您的本地终端（TRAE-D-SME-Pricing 目录下）执行以下命令，将代码推送到 GitHub：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交代码
git commit -m "Initial commit: TRAE Fintech Demo"

# 4. 创建 GitHub 仓库 (需手动操作)
# 请登录 GitHub -> 点击右上角 "+" -> "New repository"
# Repository name 建议填: TRAE-D-SME-Pricing
# 设为 "Public" (公开) -> 点击 "Create repository"

# 5. 关联远程仓库并推送 (将下方 URL 替换为您刚才创建的 GitHub 仓库地址)
git remote add origin https://github.com/YOUR_USERNAME/TRAE-D-SME-Pricing.git
git branch -M main
git push -u origin main
```

## 3. 部署到 Streamlit Cloud (Deploy)

1.  访问 [share.streamlit.io](https://share.streamlit.io/) 并登录。
2.  点击右上角的 **"New app"**。
3.  选择 **"Use existing repo"**。
4.  填写配置信息：
    *   **Repository**: 选择您刚才创建的 `YOUR_USERNAME/TRAE-D-SME-Pricing`。
    *   **Branch**: `main`。
    *   **Main file path**: `ui_streamlit/app.py` (注意：这是关键路径)。
5.  点击 **"Deploy!"**。

## 4. 获取简历链接 (Resume Link)

部署成功后（通常需要 1-2 分钟），Streamlit 会分配一个 URL，通常格式为：

`https://trae-d-sme-pricing.streamlit.app/`

### 简历展示技巧

*   **直接链接**: 在简历的“项目经历”或“作品集”一栏，直接贴上该链接。
*   **二维码**: 使用二维码生成器将链接转为 QR Code，附在简历右上角，标注“扫码体验 Live Demo”。
*   **短链接**: 如果 URL 过长，可以使用 bit.ly 生成短链，例如 `bit.ly/TRAE-Demo`。

---

## 故障排查 (Troubleshooting)

*   **ModuleNotFoundError**: 检查 `requirements.txt` 是否包含所有依赖 (streamlit, pandas, plotly, scikit-learn)。
*   **Path Error**: 确保 Main file path 填对 (`ui_streamlit/app.py`)。
