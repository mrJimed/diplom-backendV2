"""
Демонстрация использования модуля SpeechRecognitionModule.
"""
import torch

from transcribation.SpeechRecognitionModule import speech2text


def transcribation(file_path: str):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    return speech2text(file_path,
                       device,
                       verbose=0)
