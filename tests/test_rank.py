from app.services.rank import calculate_rank

def test_calculate_rank_basic():
    # Test with some arbitrary values
    stats = {
        "commits": 100,
        "prs": 10,
        "issues": 5,
        "reviews": 2,
        "stars": 20,
        "followers": 5
    }
    rank = calculate_rank(**stats)
    assert "level" in rank
    assert "percentile" in rank
    assert isinstance(rank["level"], str)
    assert 0 <= rank["percentile"] <= 100

def test_calculate_rank_high_stats():
    # Test with high stats should give 'S' or 'A+'
    stats = {
        "commits": 5000,
        "prs": 500,
        "issues": 200,
        "reviews": 100,
        "stars": 1000,
        "followers": 500
    }
    rank = calculate_rank(**stats)
    assert rank["level"] in ["S", "A+"]

def test_calculate_rank_low_stats():
    # Test with low stats should give 'C' or 'B-'
    stats = {
        "commits": 1,
        "prs": 0,
        "issues": 0,
        "reviews": 0,
        "stars": 0,
        "followers": 0
    }
    rank = calculate_rank(**stats)
    assert rank["level"] in ["C", "B-", "B"]
