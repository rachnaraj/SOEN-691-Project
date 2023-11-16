import ast
import os
import subprocess
import matplotlib.pyplot as plt



def clone_github_repo(repo_url, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    subprocess.run(["git", "clone", repo_url, local_dir], check=True)


def parse_python_file(file_path):
    with open(file_path, 'r') as file:
        node = ast.parse(file.read(), filename=file_path)
    return node


def extract_imports(node):
    imports = []
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.append(alias.name)
        elif isinstance(n, ast.ImportFrom):
            imports.append(n.module)
    return imports


def analyze_repository(directory):
    dependencies = {}
    all_imported_modules = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                node = parse_python_file(file_path)
                imports = extract_imports(node)
                dependencies[file_path] = imports
                all_imported_modules.update(imports)

    return dependencies, all_imported_modules


def compute_fan_in(module_name, dependencies):
    fan_in = 0
    for file, imports in dependencies.items():
        if module_name in imports:
            fan_in += 1
    return fan_in


def compute_total_fan_in(dependencies, all_modules):
    total_fan_in = sum(compute_fan_in(module, dependencies) for module in all_modules)
    return total_fan_in


def compute_average_fan_in(dependencies, all_modules):
    total_fan_in = compute_total_fan_in(dependencies, all_modules)
    return total_fan_in / len(all_modules) if all_modules else 0


def compute_max_fan_in(dependencies, all_modules):
    return max((compute_fan_in(module, dependencies) for module in all_modules), default=0)


def compute_median_fan_in(dependencies, all_modules):
    fan_in_list = sorted(compute_fan_in(module, dependencies) for module in all_modules)
    n = len(fan_in_list)
    if n == 0:
        return 0
    mid = n // 2
    return (fan_in_list[mid] + fan_in_list[-(mid+1)]) / 2 if n % 2 == 0 else fan_in_list[mid]


def compute_max_fan_in(dependencies, all_modules):
    return max((compute_fan_in(module, dependencies) for module in all_modules), default=0)



def compute_weighted_fan_in(dependencies, all_modules, weights):
    return sum(compute_fan_in(module, dependencies) * weights.get(module, 1) for module in all_modules)


def plot_fan_in_distribution(dependencies, all_modules):
    fan_in_values = [compute_fan_in(module, dependencies) for module in all_modules]
    plt.hist(fan_in_values, bins='auto')
    plt.title('Fan-in Distribution')
    plt.xlabel('Fan-in')
    plt.ylabel('Frequency')
    plt.show()


def main():
    repo_name = 'kengz/SLM-Lab'
    github_repo_url = 'https://github.com/'+repo_name+'.git'
    local_repo_dir = 'repos/'+repo_name.split('/')[-1] 

    # Clone the GitHub repository
    clone_github_repo(github_repo_url, local_repo_dir)

    # Analyze the repository and get all modules
    dependencies, all_modules = analyze_repository(local_repo_dir)

    # Compute Fan-in for each module
    for module in all_modules:
        fan_in = compute_fan_in(module, dependencies)
        print(f"Fan-in for {module}: {fan_in}")

    # Other metrics
    print("Total Fan-in:", compute_total_fan_in(dependencies, all_modules))
    print("Average Fan-in:", compute_average_fan_in(dependencies, all_modules))
    print("Median Fan-in:", compute_median_fan_in(dependencies, all_modules))
    print("Maximum Fan-in:", compute_max_fan_in(dependencies, all_modules))

    plot_fan_in_distribution(dependencies, all_modules)

if __name__ == "__main__":
    main()