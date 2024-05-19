"""Модуль со вспомогательными функциями."""

def is_cur_sentence_instance_of_prev(last_symbol_of_prev_sent) -> bool:
    """
    Функция определяет, является ли текущее предложение продолжением предыдущего.
    """
    symbols = ['.', '?', '!']
    return not (last_symbol_of_prev_sent in symbols)


def uncapitalize(sentence: str) -> str:
    """
    Функция приводит первый символ предложения к нижнему регистру.
    """
    if ord("А") <= ord(sentence[0]) <= ord("Я"):
        new_char = chr(ord(sentence[0]) - ord("А") + ord("а"))
        return new_char + sentence[1:]
    return sentence


def correct_cur_sent(prev_sent: str, cur_sent: str) -> str:
    """
    Функция применяет правки к текущему предложению в зависимости от предыдущего.
    Если на конце предыдущего предложения не знак "строгой" пунктуации (. ! ?), то первое слово
    текущего предложения при слиянии с предыдущим нужно привести к нижнему регистру.
    Args:
        prev_sent: Предыдущее предложение.
        cur_sent: Текущее предложение.
    Returns: Исправленное текущее предложение.
    """
    if is_cur_sentence_instance_of_prev(prev_sent[-1]):
        return uncapitalize(cur_sent)
    return cur_sent


def pretty_time_delta(seconds):
    """
    Returns seconds in pretty format.
    """
    seconds = int(seconds)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = ""
    if days > 0:
        result += f"{days}d "
    if hours > 0:
        result += f"{hours}h "
    if minutes > 0:
        result += f"{minutes}m "
    result += f"{seconds}s"
    return result


def print_stats(audio_duration, time_for_splitting_audio, time_for_transcribing, time_for_spelling_correction):
    """
    Вывод статистики по скорости выполнения.
    Args:
        audio_duration: Длительность аудио (s).
        time_for_splitting_audio: Время для выполнения этапа разделения аудио на чанки (s).
        time_for_transcribing: Время для выполнения этапа транскрибирования чанков (s)
        time_for_spelling_correction: Время для выполнения этапа корректировки транскрибирования (s)
    """
    text = f"""---------------\nOverall stats:
    \tDuration of audio = {pretty_time_delta(audio_duration)}
    \tTime for splitting audio = {pretty_time_delta(time_for_splitting_audio)}
    \tTime for transcribing audio = {pretty_time_delta(time_for_transcribing)}
    \tTime for spelling audio = {pretty_time_delta(time_for_spelling_correction)}
    \t-----------------
    \tOverall time for processing audio = {pretty_time_delta(time_for_splitting_audio + time_for_transcribing + time_for_spelling_correction)}
    \tProcessing is {round(audio_duration / (time_for_splitting_audio + time_for_transcribing + time_for_spelling_correction), 2)} times faster than audio duration
    """
    print(text)

