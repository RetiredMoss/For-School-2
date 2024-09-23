from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)
    deanslist_grade = 90

    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    current_total = prelim_grade * prelim_weight
    required_total = passing_grade - current_total
    min_required_average = required_total / (midterm_weight + final_weight)

    # If the preliminary grade meets the passing score
    if prelim_grade >= passing_grade:
        message = f"You need a {min_required_average:.2f}% average on the Midterms and Finals to pass."
        if prelim_grade >= deanslist_grade:
            message += " You already qualify for Dean's Lister! Keep up the great work!"
        else:
            # Calculate the required grades for Dean's List
            deanslist_total = deanslist_grade - current_total
            min_deanslist_average = deanslist_total / (midterm_weight + final_weight)
            message += (
                f" To qualify for Dean's Lister, you need a Midterm grade of {min_deanslist_average:.2f}% "
                f"and a Final grade of {min_deanslist_average:.2f}%."
            )
        return message

    # If the needed average is higher than 100%
    if min_required_average > 100:
        return "Error: Achieving the passing grade is not possible with this preliminary score."

    # Ensure the minimum required average is not less than 0%
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]

    deanslist_total = deanslist_grade - current_total
    min_deanslist_average = deanslist_total / (midterm_weight + final_weight)

    return (
        f"You need a {min_required_average:.2f}% average on the Midterms and Finals to pass. "
        f"You need a Midterm grade of {min_deanslist_average:.2f}% and a Final grade of {min_deanslist_average:.2f}% to qualify for Dean's Lister."
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    prelim_grade = None  # Initialize prelim_grade
    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            result = calculate_required_grades(prelim_grade)
        except ValueError:
            result = "Error: Please enter a valid numeric value."
    
    return render_template('index.html', result=result, prelim_grade=prelim_grade)


if __name__ == '__main__':
    app.run(debug=True)


