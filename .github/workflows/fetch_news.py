```python                                                                                                                
   #!/usr/bin/env python3                                                                                                 
   import requests, os, json                                                                                              
   from datetime import datetime                                                                                          
                                                                                                                          
   DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_ URL', '')                                                       
                                                                                                                          
   def get_hackernews():                                                                                                  
       try:                                                                                                               
           r = requests.get("https://hacker-news.firebase.io/v0/topstories.json", timeout=15)                             
           ids = r.json()[:10]                                                                                            
           news = []                                                                                                      
           for i in ids:                                                                                                  
               s = requests.get(f"https://hacker-news.firebase.io/v0/item/{i}.json", timeout=10).json()                   
               if s and s.get('url'):                                                                                     
                   news.append({'title': s.get('title',''), 'url': s.get('url',''), 'source': 'Hacker News'})             
           return news                                                                                                    
       except: return []                                                                                                  
                                                                                                                          
   def send_discord(msg):                                                                                                 
       if DISCORD_WEBHOOK_URL:                                                                                            
           requests.post(DISCORD_WEBHOOK_UR L, json={"content": msg})                                                     
                                                                                                                          
   def main():                                                                                                            
       news = get_hackernews()                                                                                            
       msg = f"🚀 每日科技/AI资讯\\n{datetime.now().strftime('%Y年%m月%d日')}\\n\\n"                                      
       for i,n in enumerate(news[:10], 1):                                                                                
           msg += f"{i}. {n['title'][:50]}\\n"                                                                            
       msg += "\\n🤖 GitHub Actions 自动推送"                                                                             
       print(msg)                                                                                                         
       send_discord(msg)                                                                                                  
       with open('news_output.json','w') as f:                                                                            
           json.dump({'news_count':len(news ),'timestamp':datetime.now().iso format()}, f)                                
                                                                                                                          
   if __name__ == "__main__":                                                                                             
       main()                                                                                                             
 ```                         
