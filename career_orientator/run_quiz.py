from career_orientator.questionnaire import run_interactive_questionnaire
from career_orientator.recommender import recommend
from career_orientator.persistence import save_run

if __name__ == "__main__":
    user = run_interactive_questionnaire()
    recs = recommend(user, top_k=5)

    print("\n🎯 Recomendaciones:\n")
    for r in recs:
        print(f"🔹 {r.career} (score: {r.score:.2f})")
        for reason in r.reasons:
            print("   ✅", reason)
        for caution in r.cautions:
            print("   ⚠️", caution)
        print()

    path = save_run(user, recs)
    print(f"💾 Guardado en: {path}")
