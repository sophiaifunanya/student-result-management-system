def calculate_total_and_average(scores_dict):
    """"Calculate total score and average for a student given a dictionary of scores."""
    if not scores_dict:
        return 0, 0.0
    total = sum(scores_dict.values())
    average = total / len(scores_dict)
    return total, round(average, 2)

def assign_grade(average):
    """Ässign letter grades based on the average score."""
    if average >= 70:
        return 'A'
    elif average >= 60:
        return 'B'
    elif average >= 50:
        return 'C'
    elif average >= 40:
        return 'D'
    else:
        return 'F'