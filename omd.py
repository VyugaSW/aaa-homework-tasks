from collections import Counter, defaultdict


def task_1():
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}

    print(
        "Id товаров, которые можно забрать в Москве и Казани: "
        f"{moscow & kazan}"
    )
    print(
        "Id товаров, которые можно забрать только в Москве: "
        f"{moscow - kazan}"
    )
    print(
        "Id товаров, которые можно забрать только в Казани: "
        f"{kazan - moscow}"
    )
    print(
        "Кол-во разных товаров на обоих складах вместе: "
        f"{len(moscow | kazan)}"
    )


def task_2():
    queries = [
        "чехол",
        "iphone",
        "чехол",
        "наушники",
        "iphone",
        "iphone",
        "кабель",
        "чехол",
        "iphone",
    ]

    print(f"Кол-во всех поисковых запросов в ленте: {len(queries)}")

    count_queries = Counter(queries)
    single_queries = []
    most_popular_query = None
    max_count = 0

    print("Сколько раз ввели каждый запрос:")
    for query, count in count_queries.items():
        if count == 1:
            single_queries.append(query)

        if count > max_count:
            most_popular_query = (query, count)
            max_count = count

        print(f" {query} - {count}")

    print(f"Самый частый запрос: {most_popular_query[0]}")
    print(
        "Доля запросов, которую он занимает: "
        f"{most_popular_query[1] / len(queries):.3f}"
    )

    print(f"Запросы, встретившиеся один раз: {', '.join(single_queries)}")


def task_3():
    orders = [
        {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
        {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
        {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
        {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
        {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
        {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
    ]

    return_amount = 0
    return_once_or_more = set()
    amount_delivered = 0
    count_delivered = 0

    for order in orders:
        status = order["status"]
        amount = order["amount"]
        buyer = order["buyer"]

        if status == "returned":
            return_amount += amount
            return_once_or_more.add(buyer)
        elif status == "delivered":
            amount_delivered += amount
            count_delivered += 1

    print(f"Сумма оформления возвратов: {return_amount}")
    print(f"Кто хотя бы раз вернул заказ: {', '.join(return_once_or_more)}")
    print(f"Кол-во заказов, доставленных покупателю: {count_delivered}")
    print(
        "Средний чек доставленных заказов: "
        f"{amount_delivered / count_delivered}"
    )


def task_4():
    days = [
        {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
        {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
        {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
        {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
        {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
    ]

    total_revenue = 0
    max_revenue_day = None
    max_revenue = 0
    high_return_days = []

    for day in days:
        day_name = day["day"]
        orders = day["orders"]
        revenue = day["revenue"]
        returns = day["returns"]

        total_revenue += revenue
        if revenue > max_revenue:
            max_revenue_day = day
            max_revenue = revenue

        if returns / orders > 0.2:
            high_return_days.append(day_name)

    print(f"Выручка за всю неделю: {total_revenue}")
    print(
        f"День с самой большой выручкой: {max_revenue_day['day']} "
        f"({max_revenue_day['revenue']})"
    )

    print("Средняя выручка на один заказ:")
    for day in days:
        avg_revenue = day["revenue"] / day["orders"]
        print(f" {day['day']}: {avg_revenue:.3f}")

    print(
        "Дни, когда возвратов было больше 20%: "
        f"{', '.join(high_return_days)}"
    )


def task_5():
    reviews = [
        {"id": 1, "product": "Чехол", "stars": 5},
        {"id": 1, "product": "Чехол", "stars": 3},
        {"id": 1, "product": "Чехол", "stars": 4},
        {"id": 2, "product": "Наушники", "stars": 2},
        {"id": 2, "product": "наушники", "stars": 2},
        {"id": 2, "product": "НАУШНИКИ", "stars": 5},
        {"id": 3, "product": "Планшет", "stars": 5},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 5, "product": "Кабель", "stars": 1},
    ]

    product_rating = defaultdict(list)
    bad_reviews_count = 0

    for review in reviews:
        product = review["product"].capitalize()
        stars = review["stars"]

        product_rating[product].append(stars)

        if stars <= 2:
            bad_reviews_count += 1

    worst_product = ""
    min_avg_stars = float("+inf")

    print("Средняя оценка каждого товара:")
    for product, stars_list in product_rating.items():
        avg_stars = sum(stars_list) / len(stars_list)

        if len(stars_list) >= 2 and avg_stars < min_avg_stars:
            worst_product = product
            min_avg_stars = avg_stars

        print(f" {product}: {avg_stars:.3f}")

    print(
        f"Худший товар (от 2 отзывов): {worst_product} "
        f"со средней оценкой {min_avg_stars:.3f}"
    )
    print(f"Количество отзывов на 1 или 2 звезды: {bad_reviews_count}")


if __name__ == "__main__":
    task_1()
    print("\n\n")
    task_2()
    print("\n\n")
    task_3()
    print("\n\n")
    task_4()
    print("\n\n")
    task_5()
