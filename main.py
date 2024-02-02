import json
import os

from datetime import datetime


def render_json(filename: str) -> dict:
    """Читает файл формата .json возвращая его словарем данных"""

    file_path = f"29-01-2024-w1ntexx/{filename}"

    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="UTF-8") as file:
                data = json.load(file)

                return data
        else:
            print(f"Файл {filename} не существует")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")


def render_txt(filename: str) -> dict:
    """Читает файл формата .txt возвращая его словарем данных"""

    relative_path_txt = f"29-01-2024-w1ntexx/{filename}"
    data = {}

    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = file.read().splitlines()

            for _, time in enumerate(reader, start=1):
                parts = time.split()
                time_str = datetime.strptime(parts[2], "%H:%M:%S,%f")
                number = parts[0]
                res = parts[1]

                if res == "start":
                    data[number] = {"start": time_str}
                elif res == "finish":
                    data[number]["finish"] = time_str

            return data
    except IOError:
        print(f"Файл {filename} не существует")


def result_run(start_time, finish_time) -> str:
    result = finish_time - start_time

    hours, remainder = divmod(result.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{int(hours):02}:{int(minutes):02},{int(seconds):02}"


def sorted_results(file_txt: dict, file_json: dict) -> list:
    results = []
    for key, value in file_json.items():
        if key in file_txt.keys():
            time = result_run(file_txt[key]["start"], file_txt[key]["finish"])
            results.append(
                {
                    "Нагрудный номер": key,
                    "Имя": value["Surname"],
                    "Фамилия": value["Name"],
                    "Результат": time,
                }
            )
    sorted_results = sorted(results, key=lambda x: x["Результат"])
    return sorted_results


data_txt = render_txt("results_RUN.txt")
data_json = render_json("competitors2.json")


def main():
    results = sorted_results(data_txt, data_json)
    final_results = {}
    
    print("Занятое место	Нагрудный номер	Имя	Фамилия	Результат")
    
    for num, key in enumerate(results, start=1):
        print(f"{num:<5}{key['Нагрудный номер']:<15}{key['Имя']:<15}{key['Фамилия']:<16}{key['Результат']}")
        final_results[num] = key
        json_data = json.dumps(final_results, ensure_ascii=False, indent=4)

        file = "29-01-2024-w1ntexx/final_results.json"
        with open("final_results.json", "w", encoding="utf-8") as file:
            file.write(json_data)


if __name__ ==  "__main__":
    main()

