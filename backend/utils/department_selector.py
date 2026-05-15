def select_department():

    departments = [
        "CSE",
        "ECE",
        "ME",
        "CIVIL"
    ]

    print("\n🎛 Select Department:\n")

    for i, dept in enumerate(departments, start=1):
        print(f"{i} → {dept}")

    while True:
        try:
            choice = int(input("\nEnter Department Number: "))

            if 1 <= choice <= len(departments):
                selected_dept = departments[choice - 1]

                print(
                    f"\n✅ Selected Department: {selected_dept}\n"
                )

                return selected_dept

            else:
                print("❌ Invalid choice")

        except:
            print("❌ Enter valid number")