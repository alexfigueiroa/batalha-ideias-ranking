"""
Captura screenshots de evidência das 30 ideias finalistas no AEVO.
Conecta ao Chrome já aberto via depuração remota (CDP).

ANTES DE RODAR:
1. Feche o Chrome completamente
2. Reabra com depuração remota:
   - Windows: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
   - Mac:     /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   - Linux:   google-chrome --remote-debugging-port=9222
3. Faça login no AEVO normalmente
4. Execute este script: python captura_evidencias.py

Dependências: pip install selenium webdriver-manager
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://bbts.aevoinnovate.net/#/ideia/"
OUTPUT_DIR = "evidencias_auditoria"

IDEAS = [
    (49,  "rank01_Plataforma_agentes_IA"),
    (59,  "rank02_IAprovve_Smart_Notes"),
    (315, "rank03_Identificacao_classificacao_preditiva"),
    (294, "rank04_Base_Inteligente_Custos"),
    (303, "rank05_BBTS_Movel_Parceiros"),
    (108, "rank06_Painel_gestao_controle"),
    (279, "rank07_Monitoramento_Licitacoes"),
    (310, "rank08_Atendimento_Camadas"),
    (264, "rank09_BBTeSte"),
    (67,  "rank10_Radar_Contratual"),
    (308, "rank11_Data_Shield_BBTS"),
    (144, "rank12_FQ_Digital"),
    (197, "rank13_HUB_Service_AI"),
    (281, "rank14_TAA_Inteligente"),
    (218, "rank15_Expansao_Comercial"),
    (52,  "rank16_Assistente_Virtual_IA"),
    (56,  "rank17_Busca_Visual_Inteligente"),
    (54,  "rank18_Logistica_Reversa"),
    (269, "rank19_BBTS_Fiscaliza"),
    (156, "rank20_Aplicativo_Consorcio"),
    (87,  "rank21_Rastreabilidade_ID_PARTS"),
    (79,  "rank22_Pre_Validacao_Chamado"),
    (176, "rank23_SLIP_Digital"),
    (243, "rank24_Gestao_Processos"),
    (116, "rank25_Solicitacao_Chamado"),
    (290, "rank26_PSIM_Cognitivo"),
    (313, "rank27_BBTS_Agile_Experience"),
    (96,  "rank28_Antecipacao_Recebiveis"),
    (94,  "rank29_IA_Pesquisa_Diagnostico"),
    (262, "rank30_BBTS_Hub"),
]

# Ideias com problemas identificados — captura extra da aba de avaliações
IDEAS_COM_ALERTA = {191, 316, 131, 158, 183, 213, 278, 311, 117, 152, 197, 255}


def wait_spa_load(driver, timeout=10):
    """Aguarda o conteúdo da SPA carregar (espera elemento principal aparecer)."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "app-ideia, .ideia-container, main, [class*='ideia']"))
        )
    except Exception:
        pass
    time.sleep(2)  # buffer extra para animações


def capture_full_page(driver, filepath):
    """Captura a página inteira via scroll e screenshot."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1440, total_height + 100)
    time.sleep(0.5)
    driver.save_screenshot(filepath)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    print("Conectando ao Chrome em localhost:9222...")
    try:
        driver = webdriver.Chrome(options=options)
        print(f"Conectado. Janela atual: {driver.title}")
    except Exception as e:
        print(f"\nERRO ao conectar: {e}")
        print("\nVerifique se o Chrome foi aberto com --remote-debugging-port=9222")
        return

    capturas_ok = []
    capturas_erro = []

    for idea_id, slug in IDEAS:
        url = f"{BASE_URL}{idea_id}"
        print(f"\n[{slug}] Acessando {url} ...")

        try:
            driver.get(url)
            wait_spa_load(driver)

            # Screenshot da página principal da ideia
            filepath = os.path.join(OUTPUT_DIR, f"{slug}_ideia_{idea_id}.png")
            capture_full_page(driver, filepath)
            print(f"  ✓ Salvo: {filepath}")
            capturas_ok.append(idea_id)

            # Se é ideia com alerta, captura também rolar para seção de avaliações
            if idea_id in IDEAS_COM_ALERTA:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                filepath_aval = os.path.join(OUTPUT_DIR, f"{slug}_ideia_{idea_id}_avaliacoes.png")
                driver.save_screenshot(filepath_aval)
                print(f"  ✓ Avaliações salvas: {filepath_aval}")

        except Exception as e:
            print(f"  ✗ Erro: {e}")
            capturas_erro.append((idea_id, str(e)))

    print(f"\n{'='*60}")
    print(f"CONCLUÍDO: {len(capturas_ok)}/30 capturas realizadas")
    print(f"Salvo em: {os.path.abspath(OUTPUT_DIR)}/")

    if capturas_erro:
        print(f"\nErros ({len(capturas_erro)}):")
        for eid, emsg in capturas_erro:
            print(f"  ID {eid}: {emsg}")

    # Gera índice HTML das evidências
    gerar_indice(capturas_ok)

    driver.quit()


def gerar_indice(ids_ok):
    """Gera index.html navegável com todas as evidências."""
    slug_map = {idea_id: slug for idea_id, slug in IDEAS}
    rows = []
    for idea_id, slug in IDEAS:
        status = "✓" if idea_id in ids_ok else "✗"
        alerta = " ⚠ ALERTA" if idea_id in IDEAS_COM_ALERTA else ""
        img_file = f"{slug}_ideia_{idea_id}.png"
        img_path = os.path.join(OUTPUT_DIR, img_file)
        if os.path.exists(img_path):
            rows.append(f"""
        <div class="card">
          <h3>{status} ID {idea_id}{alerta}</h3>
          <p>{slug.replace('_', ' ')}</p>
          <a href="{img_file}" target="_blank">
            <img src="{img_file}" alt="ID {idea_id}" loading="lazy">
          </a>
        </div>""")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Evidências de Auditoria — Batalha de Ideias BBTS 2026</title>
<style>
  body {{ font-family: sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
  h1 {{ color: #1a237e; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
  .card {{ background: white; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,.1); }}
  .card h3 {{ margin: 0 0 8px; font-size: 14px; color: #333; }}
  .card p {{ margin: 0 0 8px; font-size: 12px; color: #666; }}
  .card img {{ width: 100%; border: 1px solid #ddd; border-radius: 4px; cursor: zoom-in; }}
  .card h3:contains("ALERTA") {{ color: #c62828; }}
</style>
</head>
<body>
<h1>Evidências de Auditoria — Batalha de Ideias BBTS 2026</h1>
<p>Gerado em: {time.strftime('%Y-%m-%d %H:%M:%S')} | Top 30 ideias classificadas</p>
<div class="grid">{"".join(rows)}
</div>
</body>
</html>"""

    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nÍndice gerado: {os.path.abspath(index_path)}")


if __name__ == "__main__":
    main()
