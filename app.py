
#!/usr/bin/env python3
"""
Sistema de Treinos do Gabriel - Versão Online Mobile
Aplicação Flask otimizada para smartphones Android e iOS
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

class WorkoutWebManager:
    def __init__(self):
        self.data_file = "gabriel_workouts.json"
        self.history_file = "gabriel_history.json"
        self.media_file = "gabriel_media.json"
        self.media_links = self.load_media_links()
        self.workouts = self.load_workouts()
        self.history = self.load_history()

    def load_media_links(self):
        """Carrega links de mídia (imagens, vídeos) para exercícios"""
        media_file = "gabriel_media_links.json"
        
        if not os.path.exists(media_file):
            exemplo_media = {
                "exercicios": {},
                "grupos_musculares": {}
            }
            
            with open(media_file, 'w', encoding='utf-8') as f:
                json.dump(exemplo_media, f, ensure_ascii=False, indent=2)
            
            return exemplo_media
        
        try:
            with open(media_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"exercicios": {}, "grupos_musculares": {}}

    def get_exercise_media(self, exercise_name):
        """Retorna mídia específica de um exercício"""
        normalized_name = exercise_name.lower().replace(" ", "_")
        
        if "exercicios" in self.media_links and normalized_name in self.media_links["exercicios"]:
            return self.media_links["exercicios"][normalized_name]
        
        return {"video": "", "imagem": "", "gif": ""}    
    
    def load_workouts(self):
        """Carrega os treinos do arquivo JSON"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_workouts()
    
    def save_workouts(self):
        """Salva os treinos no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.workouts, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """Carrega o histórico de treinos"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Salva o histórico de treinos"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_default_workouts(self):
        """Retorna os treinos padrão"""
        return {
            "mes_1": {
                "nome": "Fundação Funcional",
                "objetivo": "Estabelecer base de força, estabilidade articular e mobilidade",
                "semanas": [1, 2, 3, 4],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Inferiores (Força Explosiva)",
                        "grupo_muscular": "Pernas e Glúteos",
                        "exercicios": [
                            {"nome": "Agachamento Livre", "series": 4, "reps": "4-6", "descanso": "90-120s", "observacao": "85-90% 1RM", "dica": "Mantenha o core contraído e desça até 90°"},
                            {"nome": "Levantamento Terra Trap Bar", "series": 4, "reps": "4-6", "descanso": "90s", "observacao": "RPE 8", "dica": "Ombros para trás, barra próxima ao corpo"},
                            {"nome": "Leg Press", "series": 3, "reps": "8-10", "descanso": "60s", "observacao": "RPE 7", "dica": "Desça controlado, não trave totalmente os joelhos"},
                            {"nome": "Cadeira Extensora Unilateral", "series": 3, "reps": "10-12", "descanso": "45s", "dica": "Foque na contração no topo do movimento"},
                            {"nome": "Panturrilha em Pé", "series": 3, "reps": "12-15", "descanso": "45s", "dica": "Amplitude máxima, pausa no topo"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Superiores (Força e Estabilidade)",
                        "grupo_muscular": "Peito, Costas e Ombros",
                        "exercicios": [
                            {"nome": "Supino Reto com Barra", "series": 4, "reps": "4-6", "descanso": "90s", "observacao": "85-90% 1RM", "dica": "Escápulas retraídas, barra na linha do mamilo"},
                            {"nome": "Puxada Frontal", "series": 4, "reps": "6-8", "descanso": "60s", "observacao": "RPE 8", "dica": "Puxe com os cotovelos, foque nos dorsais"},
                            {"nome": "Desenvolvimento com Halteres", "series": 3, "reps": "8-10", "descanso": "60s", "dica": "Amplitude completa, core estabilizado"},
                            {"nome": "Remada Unilateral", "series": 3, "reps": "10-12", "descanso": "60s", "dica": "Puxe o cotovelo para trás, aperte a escápula"},
                            {"nome": "Prancha Abdominal", "series": 3, "reps": "30-45s", "descanso": "30s", "dica": "Corpo alinhado, respiração controlada"}
                        ]
                    },
                    "quarta": {
                        "nome": "Treino Complementar - Resistência e Agilidade",
                        "grupo_muscular": "Cardio e Condicionamento",
                        "exercicios": [
                            {"nome": "Circuito de cones", "series": 3, "reps": "1 volta", "descanso": "60s", "dica": "Troque direção rapidamente"},
                            {"nome": "Tiros de 30m", "series": 6, "reps": "1 tiro", "descanso": "incompleto", "dica": "Máxima velocidade"},
                            {"nome": "Bike ergométrica Z2", "series": 1, "reps": "20 min", "descanso": "0s", "dica": "Zona 2: ritmo moderado"}
                        ]
                    },
                    "quinta": {
                        "nome": "Core, Mobilidade e Prevenção",
                        "grupo_muscular": "Core e Mobilidade",
                        "exercicios": [
                            {"nome": "Prancha Lateral com Elevação", "series": 3, "reps": "30s por lado", "descanso": "30s", "dica": "Quadril alinhado"},
                            {"nome": "Glute Bridge Unilateral", "series": 3, "reps": "12", "descanso": "45s", "dica": "Aperte o glúteo no topo"},
                            {"nome": "Mobilidade de Quadril/Tornozelo", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Movimentos lentos"},
                            {"nome": "Alongamento Dinâmico", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Aquecimento progressivo"}
                        ]
                    },
                    "sexta": {
                        "nome": "Treino A - Inferiores (Potência e Controle)",
                        "grupo_muscular": "Pernas e Potência",
                        "exercicios": [
                            {"nome": "Box Jump", "series": 4, "reps": "5", "descanso": "60s", "dica": "Aterrissagem suave"},
                            {"nome": "Afundo com Halteres", "series": 3, "reps": "8-10", "descanso": "60s", "dica": "Joelho não passa da ponta do pé"},
                            {"nome": "Cadeira Flexora", "series": 3, "reps": "10-12", "descanso": "60s", "dica": "Controle o excêntrico"},
                            {"nome": "Gêmeos Sentado", "series": 3, "reps": "15", "descanso": "45s", "dica": "Muitas repetições"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo / Futebol Competitivo",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Jogo Completo", "series": 1, "reps": "90 min", "descanso": "0s", "dica": "Hidratação constante"}
                        ]
                    }
                }
            },
            "mes_2": {
                "nome": "Força Funcional e Controle",
                "objetivo": "Aumentar força máxima e controle motor, iniciando variações unilaterais e foco em estabilidade",
                "semanas": [5, 6, 7, 8],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Inferiores (Força com Estabilidade)",
                        "grupo_muscular": "Pernas e Estabilidade",
                        "exercicios": [
                            {"nome": "Agachamento Búlgaro", "series": 3, "reps": "8 (cada perna)", "descanso": "60s", "observacao": "RPE 8", "dica": "Mantenha equilíbrio, desça controlado"},
                            {"nome": "Levantamento Terra Romeno com Halteres", "series": 3, "reps": "10", "descanso": "60s", "observacao": "RPE 7", "dica": "Quadril para trás, costas retas"},
                            {"nome": "Avanço na Barra Guiada", "series": 3, "reps": "10", "descanso": "60s", "dica": "Passo firme, não bater o joelho no chão"},
                            {"nome": "Elevação de Gêmeos Unilateral", "series": 3, "reps": "12", "descanso": "45s", "dica": "Uma perna de cada vez, amplitude máxima"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Superiores (Força e Coordenação)",
                        "grupo_muscular": "Peito, Costas e Coordenação",
                        "exercicios": [
                            {"nome": "Supino Inclinado com Halteres", "series": 4, "reps": "8", "descanso": "60s", "observacao": "RPE 8", "dica": "Halteres descendo na linha do peito superior"},
                            {"nome": "Remada Curvada", "series": 3, "reps": "8", "descanso": "60s", "observacao": "RPE 8", "dica": "Tronco inclinado, puxe cotovelos para trás"},
                            {"nome": "Elevação Lateral + Desenvolvimento (Combo)", "series": 3, "reps": "10", "descanso": "60s", "dica": "Laterais primeiro, depois desenvolvimento"},
                            {"nome": "Puxada na Polia Inversa", "series": 3, "reps": "10-12", "descanso": "60s", "dica": "Pegada invertida, foque nos bíceps"},
                            {"nome": "Prancha com Remada (Renegade Row)", "series": 3, "reps": "10", "dica": "Posição de prancha, reme alternando braços"}
                        ]
                    },
                    "quarta": {
                        "nome": "Treino Complementar - HIIT e Coordenação",
                        "grupo_muscular": "Cardio e Agilidade",
                        "exercicios": [
                            {"nome": "Corridas curtas com mudança de direção", "series": 6, "reps": "20m", "descanso": "45s", "dica": "Mudanças bruscas de direção"},
                            {"nome": "Circuito em escada de agilidade", "series": 3, "reps": "1 round", "descanso": "60s", "dica": "Pés rápidos, coordenação"},
                            {"nome": "HIIT na esteira ou bike", "series": 10, "reps": "30s/30s", "descanso": "30s", "dica": "30s forte, 30s leve"}
                        ]
                    },
                    "quinta": {
                        "nome": "Core, Mobilidade e Estabilidade",
                        "grupo_muscular": "Core e Mobilidade",
                        "exercicios": [
                            {"nome": "Prancha Frontal com Toque de Ombros", "series": 3, "reps": "30s", "descanso": "30s", "dica": "Toque ombros alternadamente"},
                            {"nome": "Dead Bug", "series": 3, "reps": "10 cada lado", "descanso": "45s", "dica": "Core estabilizado, braço e perna opostos"},
                            {"nome": "Mobilidade de Ombro e Quadril", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Movimentos amplos e controlados"},
                            {"nome": "Liberação Miofascial", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Foam roller nos músculos tensos"}
                        ]
                    },
                    "sexta": {
                        "nome": "Treino A - Pliometria e Controle Excêntrico",
                        "grupo_muscular": "Potência e Controle",
                        "exercicios": [
                            {"nome": "Salto Unilateral Alternado", "series": 3, "reps": "8 cada perna", "descanso": "60s", "dica": "Saltos explosivos, uma perna"},
                            {"nome": "Afundo com Pausa (3s excêntrico)", "series": 3, "reps": "10", "descanso": "60s", "dica": "Desça em 3 segundos, pause 1s"},
                            {"nome": "Mesa Flexora", "series": 3, "reps": "10", "descanso": "60s", "dica": "Controle a descida do peso"},
                            {"nome": "Elevação de Panturrilhas com Halteres", "series": 3, "reps": "12", "dica": "Halteres nas mãos, amplitude máxima"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo ou Treino Técnico",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Treino Técnico", "series": 1, "reps": "60-90 min", "descanso": "0s", "dica": "Foque na técnica, não só no físico"}
                        ]
                    }
                }
            },
            "mes_3": {
                "nome": "Potência e Transferência Esportiva",
                "objetivo": "Desenvolver potência e explosão muscular com foco na transferência para o futebol",
                "semanas": [9, 10, 11, 12],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Pliometria + Força Inferior",
                        "grupo_muscular": "Pernas e Explosão",
                        "exercicios": [
                            {"nome": "Saltos Verticais com Peso", "series": 3, "reps": "5", "descanso": "90s", "dica": "Peso leve, salto máximo"},
                            {"nome": "Agachamento Frontal", "series": 4, "reps": "6", "descanso": "90s", "observacao": "RPE 8", "dica": "Barra na frente, cotovelos altos"},
                            {"nome": "Passada com Salto", "series": 3, "reps": "8", "descanso": "60s", "dica": "Passo grande + salto explosivo"},
                            {"nome": "Gêmeos Explosivo em Pé", "series": 3, "reps": "12", "descanso": "45s", "dica": "Subida explosiva, descida controlada"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Superiores Explosivo",
                        "grupo_muscular": "Peito, Costas e Explosão",
                        "exercicios": [
                            {"nome": "Supino com Explosão (Speed Bench)", "series": 4, "reps": "5", "descanso": "90s", "dica": "Subida explosiva, carga 60-70%"},
                            {"nome": "Pull-up com Impulso", "series": 3, "reps": "6", "descanso": "90s", "dica": "Use impulso para passar da barra"},
                            {"nome": "Arremesso de Bola Medicinal", "series": 3, "reps": "10", "descanso": "60s", "dica": "Arremesso explosivo do peito"},
                            {"nome": "Core Dinâmico (Cable Rotation)", "series": 3, "reps": "12", "descanso": "45s", "dica": "Rotação rápida do tronco"}
                        ]
                    },
                    "quarta": {
                        "nome": "Recuperação Ativa + Mobilidade",
                        "grupo_muscular": "Recuperação",
                        "exercicios": [
                            {"nome": "Alongamentos Ativos", "series": 1, "reps": "15 min", "descanso": "0s", "dica": "Movimentos amplos, sem dor"},
                            {"nome": "Alongamentos Estáticos", "series": 1, "reps": "15 min", "descanso": "0s", "dica": "Hold 30s cada posição"},
                            {"nome": "Liberação Miofascial", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Foam roller, pontos doloridos"}
                        ]
                    },
                    "quinta": {
                        "nome": "Treino C - Full Body Contrast",
                        "grupo_muscular": "Corpo Todo - Contraste",
                        "exercicios": [
                            {"nome": "Agachamento + Salto (Complexo)", "series": 3, "reps": "5", "descanso": "90s", "dica": "5 agachamentos + 5 saltos"},
                            {"nome": "Terra + Sprint Curto", "series": 3, "reps": "3 rounds", "descanso": "90s", "dica": "3 terras + sprint 20m"},
                            {"nome": "Supino + Flexão Explosiva", "series": 3, "reps": "5 cada", "descanso": "90s", "dica": "5 supinos + 5 flexões explosivas"},
                            {"nome": "Prancha com Instabilidade", "series": 3, "reps": "30s", "descanso": "45s", "dica": "Prancha em superfície instável"}
                        ]
                    },
                    "sexta": {
                        "nome": "Treino Complementar - HIIT + Agilidade",
                        "grupo_muscular": "Cardio e Velocidade",
                        "exercicios": [
                            {"nome": "Sprint 10-20-30m", "series": 3, "reps": "cada distância", "descanso": "60s", "dica": "Máxima velocidade em cada"},
                            {"nome": "Zig-Zag em cones", "series": 4, "reps": "1 volta", "descanso": "45s", "dica": "Mudanças rápidas de direção"},
                            {"nome": "Bike HIIT", "series": 10, "reps": "20s/40s", "descanso": "40s", "dica": "20s forte, 40s leve"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo / Futebol Competitivo",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Jogo Completo", "series": 1, "reps": "90 min", "descanso": "0s", "dica": "Aplique toda explosão treinada"}
                        ]
                    }
                }
            },
            "mes_4": {
                "nome": "Hipertrofia Funcional Controlada",
                "objetivo": "Ganho controlado de massa muscular magra com preservação da mobilidade e leveza corporal",
                "semanas": [13, 14, 15, 16],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Inferiores Funcional",
                        "grupo_muscular": "Pernas - Hipertrofia",
                        "exercicios": [
                            {"nome": "Agachamento com Halteres", "series": 3, "reps": "12", "descanso": "60s", "dica": "Halteres nas mãos, amplitude total"},
                            {"nome": "Cadeira Flexora Unilateral", "series": 3, "reps": "12", "descanso": "60s", "dica": "Uma perna de cada vez"},
                            {"nome": "Leg Press com Pausa", "series": 3, "reps": "10", "descanso": "60s", "dica": "Pause 2s na posição baixa"},
                            {"nome": "Panturrilha no Leg", "series": 3, "reps": "20", "descanso": "45s", "dica": "Alto volume para hipertrofia"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Superiores (Resistência e Volume)",
                        "grupo_muscular": "Peito, Costas - Hipertrofia",
                        "exercicios": [
                            {"nome": "Supino com Halteres", "series": 3, "reps": "12", "descanso": "60s", "dica": "Amplitude máxima, halteres"},
                            {"nome": "Puxada com Pegada Neutra", "series": 3, "reps": "12", "descanso": "60s", "dica": "Pegada paralela, foque dorsais"},
                            {"nome": "Desenvolvimento", "series": 3, "reps": "10", "descanso": "60s", "dica": "Desenvolvimento militar ou halteres"},
                            {"nome": "Remada Máquina", "series": 3, "reps": "12", "descanso": "60s", "dica": "Aperte escápulas no final"},
                            {"nome": "Prancha com Peso", "series": 3, "reps": "30s", "descanso": "45s", "dica": "Anilha nas costas"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo ou Técnica Esportiva",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Treino Técnico", "series": 1, "reps": "60-90 min", "descanso": "0s", "dica": "Foque na qualidade dos movimentos"}
                        ]
                    }
                }
            },
            "mes_5": {
                "nome": "Integração e Potencialização Atlética",
                "objetivo": "Combinar força, potência, velocidade e resistência com foco em performance esportiva",
                "semanas": [17, 18, 19, 20],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Força e Potência Inferior",
                        "grupo_muscular": "Pernas - Potência Integrada",
                        "exercicios": [
                            {"nome": "Trap Bar Jump", "series": 3, "reps": "5", "descanso": "90s", "dica": "Salto explosivo com trap bar"},
                            {"nome": "Agachamento Frontal", "series": 3, "reps": "6", "descanso": "90s", "dica": "Barra na frente, core ativo"},
                            {"nome": "Afundo Explosivo", "series": 3, "reps": "8", "descanso": "60s", "dica": "Subida explosiva do afundo"},
                            {"nome": "Panturrilha em Unilateral", "series": 3, "reps": "15", "descanso": "45s", "dica": "Uma perna, foque no equilíbrio"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Superiores Atléticos",
                        "grupo_muscular": "Peito, Costas - Performance",
                        "exercicios": [
                            {"nome": "Supino Rápido", "series": 4, "reps": "5", "descanso": "90s", "dica": "Velocidade máxima na subida"},
                            {"nome": "Puxada Alternada", "series": 3, "reps": "8", "descanso": "60s", "dica": "Varie pegadas a cada série"},
                            {"nome": "Arremesso com Bola Medicinal", "series": 3, "reps": "10", "descanso": "60s", "dica": "Explosão máxima do peito"},
                            {"nome": "Remada Alta", "series": 3, "reps": "10", "descanso": "60s", "dica": "Cotovelos altos, trapézio"}
                        ]
                    },
                    "quarta": {
                        "nome": "Treino C - Core, Equilíbrio e Mobilidade",
                        "grupo_muscular": "Core e Estabilidade",
                        "exercicios": [
                            {"nome": "Prancha com Bola Bosu", "series": 3, "reps": "30s", "descanso": "45s", "dica": "Mãos na bosu, instabilidade"},
                            {"nome": "Russian Twist", "series": 3, "reps": "20", "descanso": "45s", "dica": "Pés suspensos, rotação do tronco"},
                            {"nome": "Skater Squats", "series": 3, "reps": "10 cada lado", "descanso": "60s", "dica": "Agachamento lateral unilateral"},
                            {"nome": "Mobilidade de Quadril", "series": 1, "reps": "15 min", "descanso": "0s", "dica": "Amplitude máxima, sem dor"}
                        ]
                    },
                    "quinta": {
                        "nome": "Treino A - Força e Potência Inferior",
                        "grupo_muscular": "Pernas - Potência Integrada",
                        "exercicios": [
                            {"nome": "Trap Bar Jump", "series": 3, "reps": "5", "descanso": "90s", "dica": "Repita com mesma intensidade"},
                            {"nome": "Agachamento Frontal", "series": 3, "reps": "6", "descanso": "90s", "dica": "Mantenha postura ereta"},
                            {"nome": "Afundo Explosivo", "series": 3, "reps": "8", "descanso": "60s", "dica": "Explosão máxima na subida"},
                            {"nome": "Panturrilha em Unilateral", "series": 3, "reps": "15", "descanso": "45s", "dica": "Equilíbrio e força"}
                        ]
                    },
                    "sexta": {
                        "nome": "Treino B - Superiores Atléticos",
                        "grupo_muscular": "Peito, Costas - Performance",
                        "exercicios": [
                            {"nome": "Supino Rápido", "series": 4, "reps": "5", "descanso": "90s", "dica": "Velocidade constante"},
                            {"nome": "Puxada Alternada", "series": 3, "reps": "8", "descanso": "60s", "dica": "Pegadas diferentes"},
                            {"nome": "Arremesso com Bola Medicinal", "series": 3, "reps": "10", "descanso": "60s", "dica": "Potência explosiva"},
                            {"nome": "Remada Alta", "series": 3, "reps": "10", "descanso": "60s", "dica": "Trapézio superior"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo / Futebol Competitivo",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Jogo Completo", "series": 1, "reps": "90 min", "descanso": "0s", "dica": "Aplique toda integração treinada"}
                        ]
                    }
                }
            },
            "mes_6": {
                "nome": "Polimento Final e Otimização Funcional",
                "objetivo": "Consolidar ganhos, reduzir volume, manter intensidade e maximizar prontidão para performance",
                "semanas": [21, 22, 23, 24],
                "treinos": {
                    "segunda": {
                        "nome": "Treino A - Full Body Funcional (Carga Média)",
                        "grupo_muscular": "Corpo Todo - Polimento",
                        "exercicios": [
                            {"nome": "Agachamento", "series": 3, "reps": "6", "descanso": "90s", "dica": "Carga média, técnica perfeita"},
                            {"nome": "Supino", "series": 3, "reps": "6", "descanso": "90s", "dica": "Foque na qualidade do movimento"},
                            {"nome": "Terra", "series": 3, "reps": "6", "descanso": "90s", "dica": "Levantamento terra clássico"},
                            {"nome": "Core com Peso", "series": 3, "reps": "10", "descanso": "60s", "dica": "Mantenha core estável"}
                        ]
                    },
                    "terca": {
                        "nome": "Treino B - Pliometria + Técnica",
                        "grupo_muscular": "Potência e Técnica",
                        "exercicios": [
                            {"nome": "Saltos Curtos", "series": 3, "reps": "5", "descanso": "90s", "dica": "Qualidade sobre quantidade"},
                            {"nome": "Arranque com Bola Medicinal", "series": 3, "reps": "10", "descanso": "60s", "dica": "Movimento olímpico adaptado"},
                            {"nome": "Sprint com Foco Técnico", "series": 3, "reps": "20m", "descanso": "90s", "dica": "Técnica de corrida perfeita"},
                            {"nome": "Mobilidade e Alongamento", "series": 1, "reps": "15 min", "descanso": "0s", "dica": "Prepare o corpo para performance"}
                        ]
                    },
                    "quarta": {
                        "nome": "Regeneração e Prevenção",
                        "grupo_muscular": "Recuperação",
                        "exercicios": [
                            {"nome": "Liberação Miofascial", "series": 1, "reps": "20 min", "descanso": "0s", "dica": "Foam roller completo"},
                            {"nome": "Alongamento Passivo", "series": 1, "reps": "20 min", "descanso": "0s", "dica": "Relaxe e respire"},
                            {"nome": "Exercícios Respiratórios", "series": 1, "reps": "10 min", "descanso": "0s", "dica": "Controle da respiração"}
                        ]
                    },
                    "quinta": {
                        "nome": "Treino A - Full Body Funcional (Carga Média)",
                        "grupo_muscular": "Corpo Todo - Polimento",
                        "exercicios": [
                            {"nome": "Agachamento", "series": 3, "reps": "6", "descanso": "90s", "dica": "Mesma intensidade do segunda"},
                            {"nome": "Supino", "series": 3, "reps": "6", "descanso": "90s", "dica": "Técnica impecável"},
                            {"nome": "Terra", "series": 3, "reps": "6", "descanso": "90s", "dica": "Força e controle"},
                            {"nome": "Core com Peso", "series": 3, "reps": "10", "descanso": "60s", "dica": "Estabilidade final"}
                        ]
                    },
                    "sexta": {
                        "nome": "Treino B - Pliometria + Técnica",
                        "grupo_muscular": "Potência e Técnica",
                        "exercicios": [
                            {"nome": "Saltos Curtos", "series": 3, "reps": "5", "descanso": "90s", "dica": "Máxima qualidade"},
                            {"nome": "Arranque com Bola Medicinal", "series": 3, "reps": "10", "descanso": "60s", "dica": "Explosão técnica"},
                            {"nome": "Sprint com Foco Técnico", "series": 3, "reps": "20m", "descanso": "90s", "dica": "Perfeição na corrida"},
                            {"nome": "Mobilidade e Alongamento", "series": 1, "reps": "15 min", "descanso": "0s", "dica": "Finalize com qualidade"}
                        ]
                    },
                    "sabado": {
                        "nome": "Jogo / Futebol Competitivo",
                        "grupo_muscular": "Esporte",
                        "exercicios": [
                            {"nome": "Futebol - Performance Máxima", "series": 1, "reps": "90 min", "descanso": "0s", "dica": "Mostre toda evolução dos 6 meses!"}
                        ]
                    }
                }
            }
        }

# Instância global do gerenciador
workout_manager = WorkoutWebManager()

# Rotas principais
@app.route('/')
def home():
    """Página inicial mobile"""
    return render_template('index.html', workouts=workout_manager.workouts)

@app.route('/treinos')
def treinos():
    """Página de treinos mobile"""
    return render_template('treinos.html', workouts=workout_manager.workouts)

@app.route('/grupos')
def grupos():
    """Página de grupos musculares mobile"""
    grupos = {}
    for mes_key, mes_data in workout_manager.workouts.items():
        for dia, treino in mes_data["treinos"].items():
            grupo = treino["grupo_muscular"]
            if grupo not in grupos:
                grupos[grupo] = []
            grupos[grupo].append({
                "dia": dia.capitalize(),
                "nome": treino["nome"],
                "exercicios": len(treino["exercicios"]),
                "mes": mes_key.replace("mes_", "Mês ")
            })
    
    return render_template('grupos.html', grupos=grupos)

@app.route('/historico')
def historico():
    """Página de histórico mobile"""
    return render_template('historico.html', history=workout_manager.history)

@app.route('/estatisticas')
def estatisticas():
    """Página de estatísticas mobile"""
    if workout_manager.history:
        total_treinos = len(workout_manager.history)
        total_exercicios = sum(s.get("exercises_completed", 0) for s in workout_manager.history)
        tempo_total = sum(s.get("duration_minutes", 0) for s in workout_manager.history)
        taxa_media = sum(s.get("completion_rate", 0) for s in workout_manager.history) / total_treinos if total_treinos > 0 else 0
        
        stats = {
            "total_treinos": total_treinos,
            "total_exercicios": total_exercicios,
            "tempo_total": tempo_total,
            "taxa_media": taxa_media,
            "calorias": tempo_total * 8
        }
    else:
        stats = None
    
    return render_template('estatisticas.html', stats=stats)

@app.route('/treino/<mes>/<dia>')
def treino_detalhes(mes, dia):
    """Página de detalhes do treino mobile"""
    treino = workout_manager.workouts[mes]["treinos"][dia]
    return render_template('treino_detalhes.html', 
                         treino=treino, 
                         mes=mes, 
                         dia=dia,
                         workout_manager=workout_manager)

@app.route('/executar-treino/<mes>/<dia>')
def executar_treino(mes, dia):
    """Página de execução do treino mobile"""
    treino = workout_manager.workouts[mes]["treinos"][dia]
    session['treino_atual'] = {
        'mes': mes,
        'dia': dia,
        'exercicio_atual': 0,
        'start_time': datetime.now().isoformat()
    }
    return render_template('executar_treino.html', treino=treino, mes=mes, dia=dia)

# APIs mobile
@app.route('/api/concluir-exercicio', methods=['POST'])
def concluir_exercicio():
    """API para marcar exercício como concluído"""
    try:
        data = request.json
        peso = data.get('peso', 0)
        
        if 'treino_atual' in session:
            session['treino_atual']['exercicio_atual'] += 1
            session.modified = True
            
            return jsonify({
                'success': True,
                'proximo_exercicio': session['treino_atual']['exercicio_atual'],
                'message': 'Exercício concluído com sucesso!'
            })
        
        return jsonify({
            'success': False,
            'error': 'Sessão de treino não encontrada'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/finalizar-treino', methods=['POST'])
def finalizar_treino():
    """API para finalizar treino"""
    try:
        if 'treino_atual' not in session:
            return jsonify({
                'success': False,
                'error': 'Sessão de treino não encontrada'
            })
        
        treino_data = session['treino_atual']
        mes = treino_data['mes']
        dia = treino_data['dia']
        treino = workout_manager.workouts[mes]["treinos"][dia]
        
        start_time = datetime.fromisoformat(treino_data['start_time'])
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds() / 60)
        
        exercicios_completados = treino_data['exercicio_atual']
        total_exercicios = len(treino['exercicios'])
        
        # Salvar no histórico
        session_data = {
            "date": start_time.strftime("%Y-%m-%d %H:%M"),
            "workout_name": treino["nome"],
            "muscle_group": treino["grupo_muscular"],
            "exercises_completed": exercicios_completados,
            "total_exercises": total_exercicios,
            "duration_minutes": duration,
            "completion_rate": (exercicios_completados / total_exercicios) * 100 if total_exercicios > 0 else 0
        }
        
        workout_manager.history.append(session_data)
        workout_manager.save_history()

        def load_media_links(self):
            if os.path.exists(self.media_file):
                with open(self.media_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}

        def save_media_links(self):
            with open(self.media_file, 'w', encoding='utf-8') as f:
                json.dump(self.media_links, f, ensure_ascii=False, indent=2)        
        
        # Limpar sessão
        session.pop('treino_atual', None)
        
        return jsonify({
            'success': True,
            'resumo': session_data,
            'message': 'Treino finalizado com sucesso!'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@app.route('/api/obter-midia/<exercise_name>')
def obter_midia(exercise_name):
    """API para obter mídia de um exercício"""
    try:
        media = workout_manager.get_exercise_media(exercise_name)
        return jsonify({
            'success': True, 
            'media': media,
            'exercise_name': exercise_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'media': {"video": "", "imagem": "", "gif": ""}
        })

@app.route('/api/salvar-midia', methods=['POST'])
def salvar_midia():
    data = request.json
    exercise_name = data.get('exercise_name')
    if exercise_name:
        workout_manager.media_links[exercise_name] = {
            'video': data.get('video_url', ''),
            'imagem': data.get('image_url', ''),
            'descricao': data.get('description', '')
        }
        workout_manager.save_media_links()
        return jsonify({'success': True})
    return jsonify({'success': False})

# Headers de segurança
@app.after_request
def after_request(response):
    """Adiciona headers de segurança"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)