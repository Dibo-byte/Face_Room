import cv2
import json
import time
from abc import ABC, abstractmethod
from twilio.rest import Client
from picamera2 import Picamera2


class Aluno:
    def __init__(self, nome):
        self._nome = nome  # encapsulamento: atributo privado

    @property
    def nome(self):
        return self._nome

    def __str__(self):
        return self._nome


class Notificacao(ABC):
    @abstractmethod
    def enviar(self, mensagem: str):
        pass


class NotificacaoTwilio(Notificacao):
    def __init__(self, sid, token, from_, to):
        self._client = Client(sid, token)
        self._from = from_
        self._to = to

    def enviar(self, mensagem: str):
        self._client.messages.create(body=mensagem, from_=self._from, to=self._to)
        print("SMS enviado via Twilio:", mensagem)


class SistemaPresenca:
    def __init__(self, nome_materia, hora_inicio, hora_fim, notificacao: Notificacao):
        self._nome_materia = nome_materia
        self._hora_inicio = hora_inicio
        self._hora_fim = hora_fim
        self._notificacao = notificacao
        self._alunos_presentes = []
        self._alerta_enviado = False

        # Carrega labels dos alunos
        self._label_map = self._carregar_labels("labels.txt")

        # Inicializa a câmera
        self._picam2 = Picamera2()
        self._picam2.configure(self._picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
        self._picam2.start()
        time.sleep(2)

        # Carrega modelos de detecção e reconhecimento facial
        self._face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self._recognizer = cv2.face.LBPHFaceRecognizer_create()
        self._recognizer.read("modelo_lbph.yml")

    def _carregar_labels(self, arquivo):
        labels = {}
        with open(arquivo, "r") as f:
            for line in f:
                label, nome = line.strip().split(":")
                labels[int(label)] = nome
        return labels

    def detectar_e_registrar(self):
        print("Sistema iniciado. Pressione Ctrl+C para sair.")
        cv2.namedWindow("Câmera - Presença", cv2.WINDOW_NORMAL)  # Cria janela uma única vez
        try:
            while True:
                frame = self._picam2.capture_array()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self._face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces:
                    rosto = gray[y:y + h, x:x + w]
                    rosto = cv2.resize(rosto, (200, 200))
                    label, confidence = self._recognizer.predict(rosto)
                    nome = self._label_map.get(label, "Desconhecido")

                    if nome != "Desconhecido" and not self._existe_aluno(nome):
                        aluno = Aluno(nome)
                        self._alunos_presentes.append(aluno)
                        self._salvar_presenca()
                        print(f"Aluno {nome} registrado presente.")

                        if not self._alerta_enviado:
                            self._notificacao.enviar(f"Aula de {self._nome_materia} iniciada. Aluno {nome} presente na sala.")
                            self._alerta_enviado = True

                    # Desenha retângulo e nome no frame
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{nome} ({confidence:.2f})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                cv2.imshow("Câmera - Presença", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Encerrando por comando do usuário...")
                    break

                time.sleep(1)
        except KeyboardInterrupt:
            print("Sistema encerrado pelo usuário (Ctrl+C).")
        finally:
            self._picam2.stop()
            cv2.destroyAllWindows()

    def _existe_aluno(self, nome):
        return any(aluno.nome == nome for aluno in self._alunos_presentes)

    def _salvar_presenca(self):
        dados = {
            "materia": self._nome_materia,
            "inicio": self._hora_inicio,
            "fim": self._hora_fim,
            "total_alunos": len(self._alunos_presentes),
            "alunos": [aluno.nome for aluno in self._alunos_presentes]
        }
        with open("presenca.json", "w") as f:
            json.dump(dados, f, indent=4)


if __name__ == "__main__":
    # Configurações Twilio - preencha com suas credenciais
    SID = "AC65b7ca7683a338665205b14ba876301a"
    TOKEN = "286e012bcf5441c71fcea05b0a5c53d5"
    FROM = "+17753689668"
    TO = "+5592993112002"

    notificacao = NotificacaoTwilio(SID, TOKEN, FROM, TO)
    sistema = SistemaPresenca(
        nome_materia="Programação Orientada a Máquinas Virtuais",
        hora_inicio="19:40",
        hora_fim="21:30",
        notificacao=notificacao
    )
    sistema.detectar_e_registrar()
