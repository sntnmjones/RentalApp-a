def get_rating_average(reviews) -> float:
    """
    Calculate the average rating for a property
    """
    rating_sum = 0
    num_reviews = len(reviews)
    for review in reviews:
        rating_sum += review.rating
    if num_reviews > 0:
        return round(rating_sum / num_reviews, 1)
    return 0.0
