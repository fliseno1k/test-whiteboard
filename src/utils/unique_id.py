def __unique_id_factory(start: int = 0, prefix: str = ""):
    count = start

    def gen():
        nonlocal count, prefix

        count += 1

        return prefix + "-" + str(count)

    return gen


generate_id = __unique_id_factory(0, "symbol")
