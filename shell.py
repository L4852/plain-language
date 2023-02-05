from plain import Plain


def main():
    while True:
        user_input = input("> ")
        result = Plain(user_input).interpret()

        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
