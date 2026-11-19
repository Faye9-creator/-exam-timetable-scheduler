import json
import os
import random

os.makedirs("data", exist_ok=True)


def generate_dataset(
    filename, num_courses, num_students, num_rooms, num_slots, seed=42
):
    random.seed(seed)

    # 1. Generate Rooms
    rooms = []
    for r in range(1, num_rooms + 1):
        rooms.append({
            "room_id": f"R{r}",
            "room_name": f"Hall {r}",
            "capacity": random.choice([30, 50, 100, 150, 250]),
        })

    # 2. Generate Timeslots (e.g., 3 slots per day: Morning, Afternoon, Evening)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = [("09:00", "12:00"), ("14:00", "17:00")]
    timeslots = []
    slot_idx = 1
    for d in days:
        for start, end in periods:
            if slot_idx > num_slots:
                break
            timeslots.append({
                "slot_id": f"T{slot_idx}",
                "day": d,
                "start_time": start,
                "end_time": end,
            })
            slot_idx +=1
    # 3. Generate Courses
    courses = []
    for c in range(1, num_courses + 1):
        courses.append({
            "course_id": f"CS{100 + c}",
            "course_name": f"Module {c}",
            "student_count": 0,  # Will be calculated from enrollments
        })

    # 4. Generate Synthetic Student Enrollments (each student takes 3 to 5 courses)
    enrollments = []
    course_counts = {c["course_id"]: 0 for c in courses}

    for s in range(1, num_students + 1):
        student_id = f"STU_{s:03d}"
        k = min(num_courses, random.randint(3, 5))
        chosen_courses = random.sample([c["course_id"] for c in courses], k)
        for cid in chosen_courses:
            enrollments.append({"student_id": student_id, "course_id": cid})
            course_counts[cid] += 1

    # Update student_count per course & ensure at least one room can fit each course (unless impossible test)
    max_room_cap = max(r["capacity"] for r in rooms)
    for c in courses:
        count = course_counts[c["course_id"]]
        c["student_count"] = max(count, 5)
        if filename != "impossible_edge.json" and c["student_count"] > max_room_cap:
            rooms[0]["capacity"] = c["student_count"] + 10

    dataset = {
        "rooms": rooms,
        "timeslots": timeslots,
        "courses": courses,
        "enrollments": enrollments,
    }

    with open(os.path.join("data", filename), "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Generated data/{filename}")


if __name__ == "__main__":
    # 1. Tiny dataset for quick developer testing
    generate_dataset("tiny_smoke.json", num_courses=5, num_students=20, num_rooms=2, num_slots=4)
    # 2. Medium dataset for standard benchmarking
    generate_dataset("medium_standard.json", num_courses=20, num_students=150, num_rooms=5, num_slots=10)
    # 3. Hard dataset with high conflict density
    generate_dataset("hard_tight.json", num_courses=40, num_students=400, num_rooms=6, num_slots=12)
    # 4. Impossible dataset (10 courses, only 2 slots, high overlap -> guaranteed unsolvable)
    generate_dataset("impossible_edge.json", num_courses=10, num_students=50, num_rooms=1, num_slots=2)       