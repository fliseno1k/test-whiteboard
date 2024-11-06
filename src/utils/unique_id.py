def __unique_id_factory(start: int = 0, prefix: str = ""):
    count = start

    def create_unique_id():
        nonlocal count, prefix

        count += 1

        return prefix + "-" + str(count)

    return create_unique_id


unique_id = __unique_id_factory(0, "symbol")
