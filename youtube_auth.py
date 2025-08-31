#!/usr/bin/env python3
"""
YouTube API OAuth授权脚本
用于获取REFRESH_TOKEN，配合视频自动化项目使用
"""
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

# YouTube API作用域
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# 你的OAuth客户端配置
CLIENT_CONFIG = {
    "installed": {
        "client_id": "293420423364-ss00qnpg13va38smechr9g7tvmpot0u.apps.googleusercontent.com",
        "client_secret": "GOCSPX-Ygg2jbUMGGDpbPBG8CYTEFOW8",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8080/"]
    }
}

def get_refresh_token():
    """
    获取YouTube API的refresh token
    这个脚本需要在本地运行，不是在GitHub Actions中运行
    """
    print("🚀 YouTube API 授权流程开始...")
    print("📧 请确保使用Gmail账号: 5460123@gmail.com 进行授权")
    print("-" * 50)
    
    try:
        # 创建OAuth流程
        flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
        
        # 运行本地服务器进行授权
        print("🌐 浏览器即将自动打开...")
        print("💡 如果浏览器没有自动打开，请手动复制显示的URL")
        
        credentials = flow.run_local_server(
            port=8080,
            prompt='select_account'  # 强制选择账号
        )
        
        # 显示结果
        print("\n" + "="*60)
        print("🎉 YouTube API 授权成功！")
        print("="*60)
        print("\n📋 GitHub Secrets 配置信息：")
        print("-" * 30)
        print(f"YOUTUBE_CLIENT_ID:")
        print(f"{CLIENT_CONFIG['installed']['client_id']}")
        print(f"\nYOUTUBE_CLIENT_SECRET:")
        print(f"{CLIENT_CONFIG['installed']['client_secret']}")
        print(f"\nYOUTUBE_REFRESH_TOKEN:")
        print(f"{credentials.refresh_token}")
        print("-" * 30)
        
        # 保存到文件（可选）
        save_credentials = {
            'client_id': CLIENT_CONFIG['installed']['client_id'],
            'client_secret': CLIENT_CONFIG['installed']['client_secret'],
            'refresh_token': credentials.refresh_token
        }
        
        with open('youtube_credentials.json', 'w') as f:
            json.dump(save_credentials, f, indent=2)
        
        print("\n💾 凭据已保存到 youtube_credentials.json")
        print("\n⚠️  重要提醒：")
        print("1. 将上述三个值添加到GitHub仓库的Secrets中")
        print("2. 不要将youtube_credentials.json提交到GitHub")
        print("3. 妥善保管这些凭据信息")
        
        return credentials.refresh_token
        
    except Exception as e:
        print(f"\n❌ 授权失败: {e}")
        print("\n🔧 故障排除建议：")
        print("1. 确保使用正确的Gmail账号登录")
        print("2. 检查网络连接")
        print("3. 确保端口8080未被占用")
        print("4. 重新运行脚本")
        return None

def test_credentials(client_id, client_secret, refresh_token):
    """
    测试获得的凭据是否有效
    """
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        print("\n🔍 测试API连接...")
        
        # 创建凭据对象
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        
        # 刷新凭据
        if creds.expired:
            creds.refresh(Request())
        
        # 构建YouTube服务
        youtube = build('youtube', 'v3', credentials=creds)
        
        # 获取频道信息
        response = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            mine=True
        ).execute()
        
        if response['items']:
            channel = response['items'][0]
            print("✅ API连接测试成功！")
            print(f"📺 频道名称: {channel['snippet']['title']}")
            print(f"👥 订阅者: {channel['statistics'].get('subscriberCount', 'N/A')}")
            print(f"🎬 视频数: {channel['statistics'].get('videoCount', 'N/A')}")
            return True
        else:
            print("❌ 未找到YouTube频道")
            return False
            
    except ImportError:
        print("⚠️  缺少必要的库，跳过连接测试")
        print("💡 在本地环境中运行以下命令安装依赖：")
        print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return None
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
        return False

if __name__ == '__main__':
    print("🎯 YouTube API 配置工具")
    print("="*40)
    print("📝 此脚本用于获取YouTube API所需的REFRESH_TOKEN")
    print("⚠️  请在本地环境中运行，不要在GitHub Actions中运行")
    print("="*40)
    
    # 获取refresh token
    refresh_token = get_refresh_token()
    
    if refresh_token:
        print(f"\n🎉 配置完成！现在可以在GitHub Actions中使用YouTube API了")
        
        # 可选：测试凭据
        test_choice = input("\n❓ 是否测试API连接？(y/n): ").lower().strip()
        if test_choice == 'y':
            test_credentials(
                CLIENT_CONFIG['installed']['client_id'],
                CLIENT_CONFIG['installed']['client_secret'],
                refresh_token
            )
    else:
        print(f"\n❌ 配置失败，请检查错误信息并重试")
