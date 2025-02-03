import json
import requests
import yt_dlp
import whisper
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def gerar_resumo(transcricao):
    """Envia a transcrição para a API da OpenAI e retorna um resumo."""
    if not transcricao.strip():
        return "Erro: A transcrição está vazia."
    
    prompt = f"""
    Abaixo está a transcrição de um vídeo do YouTube:
    {transcricao}
    
    Por favor, gere um resumo conciso e informativo destacando os principais pontos abordados no vídeo.
    Deve estar disposto de modo que facilite meus estudos, e no final, hajam perguntas ou exercícios para aprimorar
    meu conhecimento na área citada.
    """
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    link = "https://api.openai.com/v1/chat/completions"
    id_modelo = "gpt-4o-mini"
    
    body_mensagem = {
        "model": id_modelo,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    body_mensagem = json.dumps(body_mensagem)
    requisicao = requests.post(link, headers=headers, data=body_mensagem)
    
    if requisicao.status_code == 200:
        resposta = requisicao.json()
        mensagem = resposta["choices"][0]["message"]["content"]
        return mensagem
    else:
        return f"Erro na requisição: {requisicao.status_code} - {requisicao.text}"

def download_audio(youtube_url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': output_path
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Erro na transcrição: {e}"

if __name__ == "__main__":
    youtube_url = input("Digite a URL do vídeo do YouTube: ")
    audio_path = "audio.mp3"

    print("Baixando áudio...")
    download_audio(youtube_url, audio_path)

    print("Transcrevendo áudio...")
    transcricao = transcribe_audio(audio_path)
    
    if "Erro" in transcricao:
        print(transcricao)
    else:
        print("Gerando resumo...")
        resumo = gerar_resumo(transcricao)
        print("\nResumo do vídeo:")
        print(resumo)
    
    os.remove(audio_path)
