def authors(poems: dict) -> dict:
    result = {}

    for poem_id in poems:
        poem = poems[poem_id]

        author = poem['author']
        title = poem['title']

        if author in result:
            result[author].append({
                "id": poem_id,
                "title": title,
            })
        else:
            result[author] = [{
                "id": poem_id,
                "title": title
            }]

    return result
