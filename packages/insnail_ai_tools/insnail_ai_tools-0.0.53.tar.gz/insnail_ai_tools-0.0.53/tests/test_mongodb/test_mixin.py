from insnail_ai_tools.mongodb.mixin import IntChoicesMixin, StrChoicesMixin


class GenderIntChoices(IntChoicesMixin):
    MAN = 1
    WOMEN = 2


class GenderStrChoices(StrChoicesMixin):
    MAN = "MAN"
    WOMEN = "WOMEN"


def test_int_choices_mixin():
    assert GenderIntChoices.choices() == [(1, "MAN"), (2, "WOMEN")]
    assert GenderIntChoices.MAN.value == 1


def test_str_choices_mixin():
    assert GenderStrChoices.choices() == [("MAN", "MAN"), ("WOMEN", "WOMEN")]
    assert GenderStrChoices.MAN.value == "MAN"
