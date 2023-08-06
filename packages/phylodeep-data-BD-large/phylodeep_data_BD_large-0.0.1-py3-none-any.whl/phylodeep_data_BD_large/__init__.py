import os


def get_ci():
    predicted_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ci_computation/predicted_values')
    target_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ci_computation/target_values')

    return predicted_path, target_path
