from tools.search import search


def main():

    results = search(
        query="Best hotels in Goa under 5000 INR",
        max_results=5,
    )

    print(results)


if __name__ == "__main__":
    main()