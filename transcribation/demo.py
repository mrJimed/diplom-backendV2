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

# Setting up parameters
# path2audio = "../transcribation/test.mp4"
# f = open('1.txt', 'r')
# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
# verbose = 2  # 0 = just output, 1 = output + time stats, 2 = output + time stats + all in-between outputs
#
# # Getting text from audio
# output_text = speech2text(path2audio,
#                           device,
#                           verbose=0)
# print(output_text)
