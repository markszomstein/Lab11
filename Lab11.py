import matplotlib.pyplot as plt
import os

def load_students():
    students = {}
    with open('data/students.txt') as f:
        for line in f:
            i = 0
            while line[i].isdigit():
                i += 1
            student_id = line[:i]
            student_name = line[i:].strip()  # Everything after the digits is the name
            students[student_id] = student_name
    return students



def load_assignments():
    assignments = {}
    with open('data/assignments.txt') as file:
        lines = [line.strip() for line in file.readlines()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            id_ = lines[i + 1]
            points = int(lines[i + 2])
            assignments[id_] = {'name': name, 'points': points}
    return assignments


def load_submissions():
    submissions = []
    submissions_folder = 'data/submissions/'

    # Check all .txt files in the submissions folder
    for filename in os.listdir(submissions_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(submissions_folder, filename)
            with open(file_path) as f:
                for line in f:
                    student_id, assignment_id, percentage = line.strip().split('|')
                    submissions.append((student_id, assignment_id, float(percentage)))
    return submissions


def get_student_id_by_name(students, name):
    name = name.strip().lower()  # Normalize input by stripping spaces and converting to lowercase
    for sid, sname in students.items():
        if sname.strip().lower() == name:  # Strip spaces and compare case-insensitively
            return sid
    return None


def get_assignment_id_by_name(assignments, name):
    for aid, data in assignments.items():
        if data["name"].lower() == name.lower():
            return aid
    return None


def student_grade():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    name = input("What is the student's name: ")
    student_id = get_student_id_by_name(students, name)

    if not student_id:
        print("Student not found")
        return

    total_score = 0
    for sid, aid, percent in submissions:
        if sid == student_id:
            points = assignments[aid]["points"]
            total_score += (percent / 100.0) * points

    final_grade = round((total_score / 1000.0) * 100)
    print(f"{final_grade}%")


def assignment_statistics():
    assignments = load_assignments()
    submissions = load_submissions()

    name = input("What is the assignment name: ")
    assignment_id = get_assignment_id_by_name(assignments, name)

    if not assignment_id:
        print("Assignment not found")
        return

    scores = [percent for sid, aid, percent in submissions if aid == assignment_id]

    if not scores:
        print("No submissions found.")
        return

    print(f"Min: {round(min(scores))}%")
    print(f"Avg: {round(sum(scores) / len(scores))}%")
    print(f"Max: {round(max(scores))}%")


def assignment_graph(assignment_name, assignments, submissions):
    assignment_id = None
    for id_, info in assignments.items():
        if info['name'].lower() == assignment_name.lower():
            assignment_id = id_
            break

    if assignment_id is None:
        print("Assignment not found")
        return

    scores = []

    for student_id, aid, percentage in submissions:
        if aid == assignment_id:
            scores.append(percentage)

    if not scores:
        print("No submissions found for this assignment.")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.show()


def main():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")

    choice = int(input("Enter your selection: "))

    if choice == 1:
        student_grade()
    elif choice == 2:
        assignment_statistics()
    elif choice == 3:
        assignment_name = input("What is the assignment name: ")
        assignments = load_assignments()
        submissions = load_submissions()
        assignment_graph(assignment_name, assignments, submissions)
    else:
        print("Invalid selection.")



if __name__ == "__main__":
    main()
