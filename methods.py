from tabulate import tabulate
import inspect


# TODO check that a function is continuous on an interval
def verify_interval(f, a, b):
    """
    Checks for the presence of a root at a given interval

    :param f: function
    :param a: left border of interval
    :param b: right border of interval
    :return: interval containing roots or error message
    """

    if a >= b:
        raise Exception("Error: The left border of the interval must be less than the right border!")

    print("Checking the interval for the presence of roots...")

    fa = f(a)
    fb = f(b)

    print(str(fa) + " * " + str(f(b)) + " = " + str(fa * fb))

    if f(a) * f(b) > 0:
        print("=> f(a) * f(b) > 0!")

        delta = 0.01

        warning = \
            f"""
            We reduce the interval until we find the roots or until the difference 
            between a and b becomes less than Δ = {delta}
            """

        print(warning)

        number_of_decreases = 0
        while abs(b - a) > delta:
            a += delta
            b -= delta

            number_of_decreases += 1

            fa = f(a)
            fb = f(b)

            print(str(fa) + " * " + str(f(b)) + " = " + str(fa * fb))

            if f(a) * f(b) <= 0:
                if f(a) * f(b) < 0:
                    message = \
                        f"""
                        We have decreased the interval {number_of_decreases} 
                        times and found several roots [maybe several]    
                        """
                    print(message)
                else:
                    print(f"We have decreased the interval {number_of_decreases} times and found one root")

                print(f"New borders: a = {a}, b = {b}")
                return a, b

        raise Exception("Error: There are no roots on this interval!")

    elif f(a) * f(b) == 0:
        print("There is one root on a given interval!")
    else:
        print("There are several roots on a given interval!")

    return a, b


def bisection_method(f, a, b, epsilon):
    """
    The bisection method for finding the root of an equation.

    :param f: function = f(x)
    :param a: left border of the interval
    :param b: right border of the interval
    :param epsilon: accuracy
    :return: root of equation
    """

    """
    pros: simple and reliable, has absolute convergence
    cons: too slow, if the interval contains several roots, it is unknown which root it will find :>
    convergence: linear convergence
    """

    # TODO move the check outside the function
    if f(a) * f(b) >= 0:
        raise ValueError("The function must have different signs at the ends of the interval!")

    table_data = [["a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"]]

    iterations = 1
    while abs(b - a) > epsilon:
        x0 = (a + b) / 2

        solution = f(x0)
        iterations += 1

        table_data.append([a, b, x0, f(a), f(b), f(x0), abs(a - b)])

        if abs(solution) <= epsilon:
            print("Root was found in " + str(iterations) + " iterations!")
            print("Root = " + str(solution))

            table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
            print(table)

            return solution

        if f(a) * f(x0) < 0:
            b = x0
        else:
            a = x0

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    print("Root was not found in " + str(iterations) + " iterations!")
    print("Returning (a_last + b_last) / 2. It's equals " + str((a + b) / 2))

    return (a + b) / 2


def check_derivative_sign(f, a, b):
    critical_points = []
    for point in [a, b]:
        if f(point) == 0:
            critical_points.append(point)

    if len(critical_points) != 0:
        print("Critical points found!")

        for point in critical_points:
            print(point)

    intervals = zip([a] + critical_points, critical_points + [b])
    for interval in intervals:
        fa = f(interval[0])
        fb = f(interval[1])

        if fa * fb < 0:
            print("The sign of the derivative has changed!")
            return False

    print("The sign of the derivative does not change!")
    return True


def secant_method(f, a, b, epsilon, max_iterations=50):  # TODO estimate the number of iterations
    """
    secant method for finding the approximate value of the root of the equation
    :param f: function
    :param a: left border of interval
    :param b: right border of interval
    :param epsilon: accuracy
    :param max_iterations: if we can't find the root after n iterations, we'll say
    that the equation has no solution
    :return: root :>
    """

    """
    firstly, let's define initial approximation
    
    x_0 = a_0 => if f(a_0) * f''(a_0) > 0
        = b_0 => if f(b_0) * f''(b_0) > 0
    """

    if f[1](a) * f[3](a) > 0:
        x0 = a
    elif f[1](b) * f[3](b) > 0:
        x0 = b
    else:
        raise Exception("Unable to determine initial approximation!")

    """
    secondly, let's check convergence conditions
    
    1) The sign of the derivative f'(x) must not change in [a, b]   
    2) The sign of the derivative f''(x) must not change in [a, b]
    3) f'(x) != 0   
    """

    # for f() documentation see functions.py
    necessity_1 = check_derivative_sign(f[2], a, b)
    necessity_2 = check_derivative_sign(f[3], a, b)

    try:
        necessity_3 = float(inspect.getsource(f[2])) != 0  # getting the text representation of a lambda expression
    except ValueError:
        necessity_3 = True  # TODO refactor using sumpy!

    if necessity_1 & necessity_2 & necessity_3:
        print("The convergence conditions = TRUE!")

        default_h = 0.005
        h = input("Enter the value for h: ") or default_h

        """
        criterion for ending the iteration process:
        |x_n - x_n-1| <= ε OR |f(x_n)| <= ε
        """

        table_data = [["x_(i-1)", "x_(i)", "x_(i+1)", "f(x_(i+1))", "|x_(i+1) - x_(i)|"]]

        if x0 == a:
            x1 = x0 + float(h)
        else:
            x1 = x0 - float(h)

        iteration = 1
        while iteration < max_iterations:

            if abs(x1 - x0) <= epsilon or abs(f[1](x1)) <= epsilon:
                print("abs(x1 - x0) = " + str(abs(x1 - x0)))
                print("f[1](x1) = " + str(abs(f[1](x1))))

                print(f"The root was found in {iteration} iterations")
                print(f"Root ≈ {x1}")

                table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
                print(table)
                return x1

            x_next = x1 - ((x1 - x0) / (f[1](x1) - f[1](x0))) * f[1](x1)  # TODO check for non zero division

            table_data.append([x0, x1, x_next, f[1](x_next), abs(x_next - x1)])

            x0 = x1
            x1 = x_next

            iteration += 1

        table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
        print(table)

        raise Exception(f"Could not find the root after {max_iterations} iterations!")