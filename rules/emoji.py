import re
import SimpleBot

letters = {
    ' ': ("000000" "\n"
          "000000" "\n"
          "000000" "\n"
          "000000" "\n"
          "000000" "\n"
          ),
    'A': ("001100" "\n"
          "010010" "\n"
          "011110" "\n"
          "100001" "\n"
          "100001" "\n"
          ),
    'B': ("111110" "\n"
          "100001" "\n"
          "111110" "\n"
          "100001" "\n"
          "111110" "\n"
          ),
    'C': ("011111" "\n"
          "100000" "\n"
          "100000" "\n"
          "100000" "\n"
          "011111" "\n"
          ),
    'D': ("111110" "\n"
          "100001" "\n"
          "100001" "\n"
          "100001" "\n"
          "111110" "\n"
          ),
    'E': ("111111" "\n"
          "100000" "\n"
          "111111" "\n"
          "100000" "\n"
          "111111" "\n"
          ),
    'F': ("111111" "\n"
          "100000" "\n"
          "111111" "\n"
          "100000" "\n"
          "100000" "\n"
          ),
    'G': ("011110" "\n"
          "100000" "\n"
          "100110" "\n"
          "100001" "\n"
          "011110" "\n"
          ),
    'H': ("100001" "\n"
          "100001" "\n"
          "111111" "\n"
          "100001" "\n"
          "100001" "\n"
          ),
    'I': ("111111" "\n"
          "001100" "\n"
          "001100" "\n"
          "001100" "\n"
          "111111" "\n"
          ),
    'J': ("011111" "\n"
          "000010" "\n"
          "000010" "\n"
          "010010" "\n"
          "001100" "\n"
          ),
    'K': ("100011" "\n"
          "101100" "\n"
          "110000" "\n"
          "101100" "\n"
          "100011" "\n"
          ),
    'L': ("100000" "\n"
          "100000" "\n"
          "100000" "\n"
          "100000" "\n"
          "111111" "\n"
          ),
    'M': ("110011" "\n"
          "110011" "\n"
          "101101" "\n"
          "100001" "\n"
          "100001" "\n"
          ),
    'N': ("110001" "\n"
          "101001" "\n"
          "101101" "\n"
          "100101" "\n"
          "100011" "\n"
          ),
    'O': ("011110" "\n"
          "100001" "\n"
          "100001" "\n"
          "100001" "\n"
          "011110" "\n"
          ),
    'P': ("111110" "\n"
          "100001" "\n"
          "111110" "\n"
          "100000" "\n"
          "100000" "\n"
          ),
    'Q': ("011110" "\n"
          "100001" "\n"
          "100101" "\n"
          "100011" "\n"
          "011111" "\n"
          ),
    'R': ("111110" "\n"
          "100001" "\n"
          "111110" "\n"
          "101100" "\n"
          "100011" "\n"
          ),
    'S': ("011111" "\n"
          "100000" "\n"
          "011110" "\n"
          "000001" "\n"
          "111110" "\n"
          ),
    'T': ("111111" "\n"
          "001100" "\n"
          "001100" "\n"
          "001100" "\n"
          "001100" "\n"
          ),
    'U': ("100001" "\n"
          "100001" "\n"
          "100001" "\n"
          "100001" "\n"
          "011110" "\n"
          ),
    'V': ("100001" "\n"
          "100001" "\n"
          "010010" "\n"
          "010010" "\n"
          "001100" "\n"
          ),
    'W': ("100001" "\n"
          "100001" "\n"
          "101101" "\n"
          "101101" "\n"
          "010010" "\n"
          ),
    'X': ("100001" "\n"
          "010010" "\n"
          "001100" "\n"
          "010010" "\n"
          "100001" "\n"
          ),
    'Y': ("100001" "\n"
          "010010" "\n"
          "001100" "\n"
          "001100" "\n"
          "001100" "\n"
          ),
    'Z': ("111111" "\n"
          "000010" "\n"
          "001100" "\n"
          "010000" "\n"
          "111111" "\n"
          )
}


def replace_emoji(t, sender):
    a, b = t.body.split()[1:3]
    text = ' '.join(t.body.split()[3:])
    text = text.upper()
    result = ''
    for i in text:
        l = letters.get(i, letters[' '])
        l = l.replace('0', a)
        l = l.replace('1', b)
        if result:
            result += a*6 + "\n"
        result += l

    sender.send(SimpleBot.Message(result))
    return True


templates = {
    'emojitext\\s.\\s.\\s(\\w\\s*)+': replace_emoji
}