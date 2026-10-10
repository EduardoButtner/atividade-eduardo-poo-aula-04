import argparse
import csv
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
import psutil

# 1. Classe base abstrata que define a estrutura de uma métrica (Requisito 1)
class Metrica(ABC):
    def __init__(self, nome: str, unidade: str):
        self.nome = nome
        self.unidade = unidade

    # Método abstrato que será implementado pelas subclasses (Polimorfismo)
    @abstractmethod
    def coletar_valor((self):
        pass

    def obter_dados(self):
        """Retorna os dados formatados para gravação."""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valor = self.coletar_valor()
        return [agora, self.nome, valor, self.unidade]


# 2. Subclasses especificas utilizando Herança (Requisito 3)
class CpuMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="CPU", unidade="%")

    def coletar_valor(self):
        # Retorna o uso da CPU em percentual
        return psutil.cpu_percent(interval=1)


class MemoriaMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="Memoria", unidade="MB")

    def coletar_valor(self):
        # Retorna a memória usada em Megabytes (MB)
        memoria = psutil.virtual_memory()
        return round(memoria.used / (1024 * 1024), 2)


class DiscoMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="Disco", unidade="MB")

    def coletar_valor(self):
        # Retorna o espaço livre no disco em Megabytes (MB)
        disco = psutil.disk_usage("/")
        return round(disco.free / (1024 * 1024), 2)


# 3. Gerenciador para salvar e rodar as coletas (Requisitos 4 e 5)
class ColetorMetricas:
    def __init__(self, arquivo_saida: str = "metricas.csv"):
        self.arquivo_saida = arquivo_saida
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        """Cria o arquivo CSV com cabeçalho caso ainda não exista."""
        if not os.path.exists(self.arquivo_saida):
            with open(self.arquivo_saida, mode="w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(["datetime", "metrica", "valor", "unidade"])

    def salvar_metricas(self, metricas: list):
        with open(self.arquivo_saida, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            for metrica in metricas:
                dados = metrica.obter_dados()
                escritor.writerow(dados)
                print(f"📊 Coletado: {dados[0]} | {dados[1]}: {dados[2]} {dados[3]}")


def main():
    # Configuração de argumentos via terminal (Desafio Extra B)
    parser = argparse.ArgumentParser(description="Coletor de Métricas do Sistema em Python")
    parser.add_argument("--intervalo", type=int, default=5, help="Intervalo entre coletas em segundos (padrão: 5)")
    parser.add_argument("--iteracoes", type=int, default=1, help="Quantidade de coletas a realizar (padrão: 1)")
    parser.add_argument("--arquivo", type=str, default="metricas.csv", help="Nome do arquivo CSV de saída")
    parser.add_argument("--metrica", type=str, choices=["cpu", "memoria", "disco", "todas"], default="todas", 
                        help="Escolha uma métrica específica ou todas")

    args = parser.parse_args()

    # Mapeamento de métricas disponíveis
    todas_metricas = {
        "cpu": CpuMetrica(),
        "memoria": MemoriaMetrica(),
        "disco": DiscoMetrica()
    }

    # Seleção de métricas conforme entrada do usuário
    if args.metrica == "todas":
        metricas_para_coletar = list(todas_metricas.values())
    else:
        metricas_para_coletar = [todas_metricas[args.metrica]]

    coletor = ColetorMetricas(arquivo_saida=args.arquivo)

    print(f"🚀 Iniciando coleta ({args.iteracoes} iteração(ões), intervalo de {args.intervalo}s)...")

    # Coleta periódica em loop (Desafio Extra A)
    for i in range(args.iteracoes):
        if args.iteracoes > 1:
            print(f"\n--- Coleta {i + 1}/{args.iteracoes} ---")
        
        coletor.salvar_metricas(metricas_para_coletar)
        
        if i < args.iteracoes - 1:
            time.sleep(args.intervalo)

    print(f"\n✅ Coleta concluída! Dados salvos em '{args.arquivo}'.")


if __name__ == "__main__":
    main()
