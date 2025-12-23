from .models import UserProfile
from .utils import parse_csv_list, clamp_1_3, yes_no_to_int


def run_interactive_questionnaire() -> UserProfile:
    print("\n🧭 CUESTIONARIO DE ORIENTACIÓN\n")

    interests = input("1) ¿Qué te interesa? (separado por comas)\n> ")
    skills = input("2) ¿Qué habilidades tenés? (separado por comas)\n> ")

    math = clamp_1_3(int(input("3) Matemática (1=baja, 2=media, 3=alta)\n> ")))
    communication = clamp_1_3(int(input("4) Comunicación (1..3)\n> ")))
    creativity = clamp_1_3(int(input("5) Creatividad (1..3)\n> ")))

    people = input("6) ¿Te gusta trabajar con personas? (s/n)\n> ")
    teamwork = clamp_1_3(int(input("7) Trabajo en equipo (1..3)\n> ")))

    return UserProfile(
        interests=parse_csv_list(interests),
        skills=parse_csv_list(skills),
        math=math,
        communication=communication,
        creativity=creativity,
        people_work=yes_no_to_int(people),
        teamwork=teamwork,
    )
