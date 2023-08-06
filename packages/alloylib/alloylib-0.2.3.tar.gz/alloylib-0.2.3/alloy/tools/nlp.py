import enum
import typing

en_num_list = ['zero', 'one', 'two', 'three',
               'four', 'five', 'six', 'seven', 'eight', 'nine']

en_teen_list = ['eleven', 'twelve', 'thirteen', 'fourteen',
                'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

en_ten_list = ['ten', 'twenty', 'thirty', 'forty',
               'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


@enum.unique
class Position(enum.Enum):
    unknown = -1
    ones = 0
    tenths = 1
    hundreds = 2
    thousands = 3
    millions = 4


def convert_word_list_to_num_str(local: typing.List[str]) -> str:
    """Converts literal word list ("four two") into number string ("42").
    It tries to seperate numbers like "four two two one" into "4221". It
    works up to 999,999.

    Parameters
    ----------
    local : Typing.list[str]
        List of number words

    Returns
    -------
    str
        return word list

    Raises
    ------
    ValueError
        If the word list is not formed correctly
    """
    val_group = []
    current_val = 0
    buffer_val = -1
    last_pos = Position.unknown

    for n in local:
        # if its in the ones group
        if n in en_num_list:
            # previous unknown
            if last_pos == Position.unknown:
                buffer_val = en_num_list.index(n)
            elif last_pos == Position.ones:
                # this means the previous stack/buffer is a different number group
                if buffer_val != -1:
                    current_val += buffer_val
                val_group.append(current_val)
                current_val = 0
                buffer_val = en_num_list.index(n)
            elif last_pos == Position.thousands:
                current_val = buffer_val
                buffer_val = en_num_list.index(n)
            else:
                buffer_val += en_num_list.index(n)
            last_pos = Position.ones

        elif n in en_teen_list:
            if last_pos == Position.unknown:
                buffer_val = en_teen_list.index(n) + 11
            elif last_pos == Position.tenths:
                # this mean the previous stack/buffer is a different number group
                if buffer_val != -1:
                    current_val += buffer_val
                val_group.append(current_val)
                current_val = 0
                buffer_val = en_teen_list.index(n) + 11
            else:
                buffer_val += en_teen_list.index(n) + 11

            last_pos = Position.tenths

        elif n in en_ten_list:
            # previous unknown
            if last_pos == Position.unknown:
                buffer_val = (en_ten_list.index(n) + 1) * 10
            elif last_pos.value <= Position.tenths.value:
                # this means the previous stack/buffer is a different number group
                if buffer_val != -1:
                    current_val += buffer_val
                val_group.append(current_val)
                current_val = 0
                buffer_val = (en_ten_list.index(n) + 1) * 10
            else:
                buffer_val += (en_ten_list.index(n) + 1) * 10

            last_pos = Position.tenths

        elif n == 'hundred':
            if last_pos == Position.unknown:
                raise ValueError("hundred without prefix")

            buffer_val = buffer_val * 100
            last_pos = Position.hundreds

        elif n == 'thousand':
            if last_pos == Position.unknown:
                raise ValueError("thousands without prefix")

            buffer_val = buffer_val * 1000
            last_pos = Position.thousands

    if buffer_val != -1:
        current_val += buffer_val
        val_group.append(current_val)
    elif current_val != 0:
        val_group.append(current_val)

    return "".join([str(n) for n in val_group])
