from judgement_system import JudgementSystem


def main():
    judgement_system = JudgementSystem()

    note_time = 10.0

    test_inputs = [
        10.01,
        10.08,
        10.13,
        10.18,
        10.50,
    ]

    print("=== Judgement System Test ===")

    for input_time in test_inputs:
        result = judgement_system.judge(
            note_time,
            input_time
        )

        print(
            f"노트 시간: {note_time:.2f}초 | "
            f"입력 시간: {input_time:.2f}초 | "
            f"판정: {result.value}"
        )


if __name__ == "__main__":
    main()
