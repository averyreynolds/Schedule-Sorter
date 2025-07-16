# Schedule Sorter
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx

class Course:                                                                                                   # Course Constructor
    def __init__(self, id, credits, difficulty, prereqs=None):
        self.id = id
        self.credits = credits
        self.difficulty = difficulty
        self.prereqs = prereqs or []

    def __repr__(self):
        return f"{self.id}: {self.credits} Hours, {self.difficulty} Difficulty, Prereqs: {self.prereqs}"

class Schedule:
    def __init__(self, max_credits=17, max_difficulty=30):
        self.max_credits = max_credits
        self.max_difficulty = max_difficulty
        self.semesters = []

    def construct(self, unsorted_list):
        sorted_courses = topological_sort(unsorted_list)
        curr_semester = []
        curr_credits = 0
        curr_difficulty = 0

        for course in sorted_courses:
            if curr_credits + course.credits <= self.max_credits and curr_difficulty + course.difficulty <= self.max_difficulty:
                curr_semester.append(course)
                curr_credits += course.credits
                curr_difficulty += course.difficulty
            else:
                self.semesters.append(curr_semester)
                curr_semester = [course]
                curr_credits = course.credits
                curr_difficulty = course.difficulty
        if curr_semester:
            self.semesters.append(curr_semester)

    def display(self):
        for i, semester in enumerate(self.semesters, 1):
            print(f"\nSemester {i}:")
            for course in semester:
                print(f"    {course}")


def topological_sort(courses:list):                                                                             # Will sort classes by topological order of prerequisites (dependencies)
    graph = defaultdict(list)              # list of adjacent courses
    in_degree = defaultdict(int)           # number of prereqs leading into
    course_map = {course.id: course for course in courses}

    for course in courses:
        for prereq in course.prereqs:
            graph[prereq].append(course.id)
            in_degree[course.id] += 1

    queue = deque([course.id for course in courses if in_degree[course.id] == 0])                               # first classes in queue have 0 prereqs
    sorted_order = []

    while queue:
        current = queue.popleft()                                                                               # deals with leftmost (oldest) course in queue of 0 prereq classes
        sorted_order.append(course_map[current])
        for adjacent in graph[current]:
            in_degree[adjacent] -= 1                                                                            # remove in degree after current is migrated to sorted order
            if in_degree[adjacent] == 0:
                queue.append(adjacent)                                                                          # add to queue if this neighbor has no further prereqs

    if len(sorted_order) != len(courses):                                                                       # error fetching, likely means an error in user input
        raise ValueError("Loop detected in course prerequisites")

    return sorted_order

def viz_semester_load(schedule):            # Plots courses and credits per semester
    semesters = [f"Semester {i+1}" for i in range(len(schedule.semesters))]
    course_counts = [len(sem) for sem in schedule.semesters]
    total_credits = [sum(c.credits for c in sem) for sem in schedule.semesters]

    plt.figure(figsize=(8,5))
    plt.bar(semesters, course_counts, color="blue")
    plt.title("Number of Courses per Semester")
    plt.ylabel("Courses")
    plt.show()

    plt.figure(figsize=(8,5))
    plt.bar(semesters, total_credits, color="orange")
    plt.title("Total Credit Hours per Semester")
    plt.ylabel("Credits")
    plt.show()

def viz_prereqs(courses):
    G = nx.DiGraph()

    for course in courses:
        if course.prereqs:
            for prereq in course.prereqs:
                G.add_edge(prereq, course.id)
        else:
            G.add_node(course.id)

    plt.figure(figsize=(10,7))
    nx.draw(G, with_labels=True, node_color="lightgreen", node_size=2000, arrows=True)
    plt.title("Prerequisite Structure")
    plt.show()

def main():
    initial_input = []
    schedule = Schedule()
    class_count = int(input("How many classes would you like to sort: "))
    class_number = 1

    while class_number <= class_count:
        new_id = input(f"\nInsert the course number of class {class_number}: ")
        new_credits = int(input(f"Insert the amount of credit hours for this class {class_number}: "))
        new_diff = int(input("Difficulty Rating (1-10): "))
        new_prereqs_input = input("Please list any uncompleted prerequisites (comma-separated), or enter 0 if none: ").strip()
        if new_prereqs_input == "0" or not new_prereqs_input:
            new_prereqs = []
        else:
            new_prereqs = [prereq.strip() for prereq in new_prereqs_input.split(",")]

        initial_input.append(Course(new_id, new_credits, new_diff, new_prereqs))
        class_number += 1

    schedule.construct(initial_input)
    schedule.display()

    viz_semester_load(schedule)
    viz_prereqs(initial_input)

if __name__ == "__main__":
    main()