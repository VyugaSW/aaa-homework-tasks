import csv
from collections import defaultdict


IN_FILE = 'Corp_Summary.csv'
OUT_FILE = 'Department_Summary.csv'


def read_csv_data(path: str = IN_FILE, delimiter: str = ';') -> list[dict]:
    data = []
    with open(path, mode='r', encoding='utf-8') as file:
        read_csv = csv.DictReader(file, delimiter=delimiter)
        for row in read_csv:
            data.append({
                'fio': row['ФИО полностью'],
                'department': row['Департамент'],
                'team': row['Отдел'],
                'position': row['Должность'],
                'rating': float(row['Оценка']),
                'salary': int(row['Оклад'])
            })
    return data


def get_hierarchy(data: list[dict]) -> dict[str, set[str]]:
    hierarchy = defaultdict(set)
    for employee in data:
        hierarchy[employee["department"]].add(employee["team"])

    return hierarchy


def calculate_department_summary(data: list[dict]) -> dict[str, dict]:
    summary = defaultdict(list)
    for employee in data:
        summary[employee['department']].append(employee['salary'])

    department_summary = {}
    for department, salaries in summary.items():
        department_summary[department] = {
            'count': len(salaries),
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_salary': round(sum(salaries) / len(salaries), 2)
        }

    return department_summary


def print_hierarchy(hierarchy: dict[str, set[str]]):
    print("\nИерархия:")
    for department, teams in hierarchy.items():
        print(f"\nДепартамент: {department}")
        print("Команды:")
        for team in sorted(teams):
            print(f" -{team}")


def print_summary(summary: dict[str, dict]):
    print("\nСводка по департаментам:\n")
    print(
        f"{'Департамент':<15} {'Кол-во сотрудников':<20} "
        f"{'Мин. зп':<10} {'Макс. зп.':<10} {'Средняя зп.':<10}"
    )
    print('-' * 70)
    for department, stats in summary.items():
        print(
            f"{department:<15} {stats['count']:<20} "
            f"{stats['min_salary']:<10} {stats['max_salary']:<10} "
            f"{stats['avg_salary']:<10}"
        )


def write_csv_summary(
    summary: dict[str, dict], output_path: str = OUT_FILE, delimiter: str = ';'
):
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        write_csv = csv.writer(file, delimiter=delimiter)
        write_csv.writerow([
            'Департамент', 'Кол-во сотрудников',
            'Мин. зп.', 'Макс. зп.', 'Средняя зп.'
        ])

        for department, stats in summary.items():
            write_csv.writerow([
                department,
                stats['count'],
                stats['min_salary'],
                stats['max_salary'],
                stats['avg_salary']
            ])


def get_report(
    report_type: int, input_file: str = IN_FILE, output_file: str = OUT_FILE
):
    data = read_csv_data(input_file)

    if report_type == 1:
        hierarchy = get_hierarchy(data)
        print_hierarchy(hierarchy)

    elif report_type == 2:
        summary = calculate_department_summary(data)
        print_summary(summary)

    elif report_type == 3:
        summary = calculate_department_summary(data)
        write_csv_summary(summary, output_file)


def main():
    get_report(3)


if __name__ == "__main__":
    main()
