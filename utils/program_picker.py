import json

from utils.md_loader import load_all_programs
programs = load_all_programs()

def get_program(gender, age_group, level):
    programs = load_all_programs()  # Загружаем все программы
    print(f"Ищем программу для: {gender}, {age_group}, {level}")
    
    for program_name, program in programs.items():
        if program["gender"] == gender and program["age_group"] == age_group and program["level"] == level:
            return program
    
    # Если программа не найдена, печатаем доступные параметры для отладки
    print("Не найдено. Доступные программы:", list(programs.keys()))
    return None