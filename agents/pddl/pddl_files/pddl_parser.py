from string import Template
problem_template= Template("""(define (problem sample_problem)
    (:domain angry_birds_scaled)
    (:objects
        $objects
    )
    (:init
        $initial
    )
    (:goal
        ; Define your goal conditions here
        (and
            $goal
        )
    )
)
""")

def generate_pddl(problem_data: dict,init_angle,angel_rate):
    objects = list()
    goals = list()
    initial_state= [
        f"(= (angle) {init_angle})",
        f"(= (angle_rad) {0})",
        f"(= (angle_rate) {angel_rate})",
        f"(= (bounce_count) 0)",
        f"(= (gravity) 87.2)",
        f"(= (active_bird) 0)"
    ]
    for object,object_data in problem_data.items():
        objects.append(f"{object} - {object.split('_')[0]}")
        if "pig" in object:
            goals.append(f"(pig_dead {object})")
        for pred, val in object_data.items():
            initial_state.append(f"(= ({pred} {object}) {val})")
    objects_str = "\n".join(objects)
    goals_str = "\n".join(goals)
    initial_state_str = "\n".join(initial_state)
    return objects_str, initial_state_str, goals_str


def write_problem_file(path:str, problem_data:dict,init_angle,angel_rate):
    objects, initial_state, goals = generate_pddl(problem_data,init_angle,angel_rate)
    problem = problem_template.substitute({"objects":objects, "initial":initial_state, "goal": goals })
    with open(path,'w') as file:
        file.write(problem)


def action_filter(line):
    return 'pa-twang' in line

def parse_action(line,init_angle,angel_rate):
    n = float(line.split(':')[0])
    return 'shoot', n*angel_rate+init_angle

def parse_solution_to_actions(solution_path:str,init_angle,angel_rate):
    with open(solution_path) as solution_file:
        lines = solution_file.readlines()
        actions = list(filter(action_filter,lines))
        actions = list(map(lambda l: parse_action(l,init_angle,angel_rate),actions))
        return actions