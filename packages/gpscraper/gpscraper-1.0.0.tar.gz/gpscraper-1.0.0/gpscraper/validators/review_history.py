def review_history(app_id, review_id):
    if not isinstance(app_id, str):
        raise TypeError("'app_id' must be of type str.")
    if not app_id:
        raise ValueError("'app_id' cannot be empty.")

    if not isinstance(review_id, str):
        raise TypeError("'review_id' must be of type str.")
    if not review_id:
        raise ValueError("'review_id' cannot be empty.")