from elasticsearch_dsl.analysis import analyzer

word_analyzer = analyzer(
    "word_analyzer", tokenizer="standard", filter=["lowercase", "stop", "snowball"]
)
lower_keyword_analyzer = analyzer(
    "lowercase_keyword", tokenizer="keyword", filter=["standard", "lowercase"]
)
