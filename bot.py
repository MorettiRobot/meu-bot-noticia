import os
import requests
from bs4 import BeautifulSoup

class JornalAlert:
    def __init__(self):
        # O GitHub vai preencher isso secretamente depois
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.url_base = 'https://portaldozacarias.com.br/site/'
        self.url_videos = self.url_base + 'noticias/so-videos/'
        self.arquivo_db = "ultima_noticia.txt"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def enviar_telegram(self, mensagem):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, data={"chat_id": self.chat_id, "text": mensagem, "parse_mode": "Markdown"})

    def verificar(self):
        res = requests.get(self.url_videos, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        item = soup.find('ul', class_='noticias-interna').find('li')
        link_rel = item.find('div', class_='titulo-noticias').find('a').get('href')
        link_full = self.url_base + link_rel
        
        # Lógica para não repetir
        if os.path.exists(self.arquivo_db):
            with open(self.arquivo_db, 'r') as f:
                if f.read().strip() == link_full:
                    print("Nada de novo.")
                    return

        titulo = item.find('div', class_='titulo-noticias').get_text(strip=True)
        msg = f"🔔 *NOVA NOTÍCIA!*\n\n{titulo}\n\n🔗 [Link]({link_full})"
        self.enviar_telegram(msg)
        
        with open(self.arquivo_db, 'w') as f:
            f.write(link_full)

if __name__ == "__main__":
    bot = JornalAlert()
    bot.verificar()
