import pyparsing as pp
from math import log10, ceil


class MusicConverterError(Exception):
    pass


class MusicConverter:
    def __init__(self,
                 base_freq=440.0,
                 amplitude=.5,
                 max_gain=10.,
                 min_gain=-200.,
                 new_scale='C/a',
                 clef='violin'):

        # an important constant value for the conversion of musical halt tone steps to frequency values
        # is the twelfth root of 2
        self.__root__ = 1.0594630943592952645618252949463  # (2 ** (1 / 12))

        # *** parser definitions ***
        # helper
        no_whites = pp.NotAny(pp.White())
        tok_end = (pp.StringEnd() | pp.LineEnd()).suppress()

        # numbers
        real = pp.Combine(
            pp.Word(pp.nums) + pp.Optional(pp.Char(',.') + pp.Word(pp.nums))
        ).setParseAction(lambda t: float(t[0].replace(',', '.')))

        integer = (
                pp.Optional(pp.Literal('-')) + pp.Word(pp.nums)
        ).setParseAction(lambda t: int(t[0] + t[1]) if len(t) > 1 else int(t[0]))

        # signs
        must_sign = pp.Char('+-').setParseAction(lambda t: float(t[0] + '1'))
        may_sign = pp.Optional(pp.Char('+-')).setParseAction(lambda t: float(t[0] + '1' if len(t) > 0 else '1'))

        # note value cents
        cent = (must_sign + no_whites + real).setParseAction(lambda t: t[0] * t[1] / 100)

        # helpers for the note name parser
        note_name_offset = {
            'C': -9,
            'D': -7,
            'E': -5,
            'F': -4,
            'G': -2,
            'A': 0,
            'B': 2,
        }
        note_name = pp.Char('CDEFGABcdefgab').setParseAction(
            lambda t: note_name_offset[t[0] if t[0] in 'CDEFGAB' else t[0].upper()]
        )

        flat_sharp = pp.Char('#b').setParseAction(lambda t: 1 if t[0] == '#' else -1)
        octave = pp.Char('0123456789').setParseAction(lambda t: (int(t[0]) - 4) * 12)
        full_note = (note_name + no_whites + pp.Optional(pp.FollowedBy(flat_sharp) + flat_sharp)
                     + no_whites + pp.FollowedBy(octave) + octave
                     ).setParseAction(lambda t: sum(t))

        self.note_name_parser = (
                full_note + pp.Optional(pp.White()).suppress() + pp.Optional(cent) + tok_end
        ).setParseAction(lambda t: float(sum(t))).setResultsName('note_value')

        # frequency parsers
        hertz = real + pp.Literal('Hz').suppress()

        self.frequency_parser = (
                hertz + tok_end
        ).setParseAction(lambda t: float(t[0])).setResultsName('frequency')

        self.base_freq_parser = (
                full_note + pp.Literal('=').suppress() + hertz + tok_end
        ).setParseAction(lambda t: t[1] * (1.0594630943592952645618252949463 ** -t[0])).setResultsName('base_freq')

        # parses a string like "sc -7:b" into a musical half tone step (using the MusicConverter.set method)
        sign = (pp.Keyword('##') | pp.Keyword('bb') | pp.Keyword('#') | pp.Keyword('b') | pp.Keyword('n') | pp.Keyword(
            '_'))
        self.score_parser = (
                integer + pp.Literal(':').suppress() + sign + tok_end
        ).setResultsName('notation')

        # amplitude parser
        self.amp_parser = (
                real + pp.Literal('%').suppress() + tok_end
        ).setParseAction(lambda t: float(t[0])).setResultsName('amplitude')

        self.gain_parser = (
                may_sign + real + pp.Literal('dB').suppress() + tok_end
        ).setParseAction(lambda t: float(t[0] * t[1])).setResultsName('gain')

        # clef parser
        self.clef_parser = (
                pp.Keyword('violin') | pp.Keyword('alto') | pp.Keyword('bass')
        ).setResultsName('clef')

        # key parser
        key_token = pp.NoMatch()
        for key in self.keys:
            key_token = key_token | pp.Keyword(key)

        self.key_parser = (
            key_token
        ).setResultsName('key')

        # complete parser
        self.input_parser = self.note_name_parser | \
                            self.frequency_parser | \
                            self.base_freq_parser | \
                            self.amp_parser | \
                            self.gain_parser | \
                            self.clef_parser | \
                            self.key_parser | \
                            self.score_parser

        # *** initializations ***
        self.__note_value__ = 0.
        self.__base_freq__ = 440.
        self.base_freq = base_freq

        self.key = new_scale
        self.__names__ = 'C D EF G A B'
        self.clef = clef
        self.__clef__ = 'violin'

        self.max_gain = max_gain
        self.min_gain = min_gain
        self.amplitude = amplitude

    # *** core property ***
    @property
    def note_value(self):
        """
        The note_value is the core property-value of the converter class. The whole numbers represent the keys on the
        piano keyboard, zero being the A above the middle C (A4). Float values express tones between the keys.
        :return: note value
        """
        return self.__note_value__

    @note_value.setter
    def note_value(self, new_val):
        if isinstance(new_val, (int, float)):
            if -58. <= new_val <= 66.:  # roughly corresponds to 16..20000Hz if A4=440Hz
                self.__note_value__ = new_val
            else:
                raise MusicConverterError(f'<note_value> out of audible range!')
        else:
            raise TypeError('MusicConverter.note_value only accepts <float> or <int>')

    # *** properties for conversion to the physical world ***
    @property
    def frequency(self):
        """
        converts the converters note_value into its corresponding frequency
        using the base frequency (default is A4=440Hz)
        :return: frequency in Hz
        """
        return self.base_freq * (self.__root__ ** self.__note_value__)

    @frequency.setter
    def frequency(self, new_freq):
        if isinstance(new_freq, str):
            try:
                new_freq = self.frequency_parser.parseString(new_freq)[0]
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_freq}" @ col {e.col}!')
        if isinstance(new_freq, (int, float)):
            if 16. <= new_freq <= 20000.:
                self.__note_value__ = log10(new_freq / self.__base_freq__) / log10(self.__root__)
            else:
                raise MusicConverterError(f'<frequency> out of audible range!')
        else:
            raise TypeError('MusicConverter.frequency only accepts <str>, <float>, or <int>')

    @property
    def base_freq(self):
        """
        base frequency. note value 0 has this frequency. all other frequencies / note values are calculated
        on this base
        :return: base frequency in Hz
        """
        return self.__base_freq__

    @base_freq.setter
    def base_freq(self, new_freq):
        if isinstance(new_freq, str):
            try:
                new_freq = self.base_freq_parser.parseString(new_freq)[0]
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_freq}" @ col {e.col}!')
        if isinstance(new_freq, (int, float)):
            if 16. <= new_freq <= 20000.:
                self.__base_freq__ = new_freq
            else:
                raise MusicConverterError(f'<base_freq> out of audible range!')
        else:
            raise TypeError('MusicConverter.base_freq only accepts <str>, <float>, or <int>')

    @property
    def amplitude(self):
        """
        this amplitude can be used by e.g. an audio app to control the loudness
        :return: amplitude as a factor 0..1
        """
        return self.__amplitude__

    @amplitude.setter
    def amplitude(self, new_amp):
        if isinstance(new_amp, str):
            try:
                new_amp = self.amp_parser.parseString(new_amp)[0]
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_amp}" @ col {e.col}!')
        if isinstance(new_amp, (int, float)):
            if 0. <= new_amp <= 1.:
                self.__amplitude__ = new_amp
            else:
                raise MusicConverterError(f'<amplitude> out of range!')
        else:
            raise TypeError('MusicConverter.amplitude only accepts <str>, <float>, or <int>')

    @property
    def gain(self):
        """
        a second way to look at the amplitude is gain.
        :return: gain in dB -inf..0
        """
        return 20. * log10(self.__amplitude__)

    @gain.setter
    def gain(self, new_gain):
        """
        :param new_gain: pass new gain as number (float or int) or as string to be parsed
        :return: None. gain value is converted into an amplitude value an stored this class' instance
        """
        if isinstance(new_gain, str):
            try:
                new_gain = self.gain_parser.parseString(new_gain)[0]
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_gain}" @ col {e.col}!')

        if isinstance(new_gain, (int, float)):
            if new_gain < 0.0 or new_gain == 0.0:
                self.__amplitude__ = 10. ** (new_gain / 20.)
            else:
                raise MusicConverterError(f'maximum <gain> is 0.0dB')
        else:
            raise TypeError(f'MusicConverter.gain only accepts <str>, <float>, or <int>')

    # *** properties for conversion to the musical world ***
    @property
    def octave(self):
        """
        :return: the octave the current note value is in: A4 is in octave 4
        """
        return int(ceil((round(self.note_value) - 2) / 12) + 4)

    @property
    def note_name(self):
        """
        :return: name of the current note value as string
        """
        steps = int(round(self.note_value))
        octave = self.octave
        note_names = {
            -9: f'C{octave}',
            -8: f'C#{octave}/Db{octave}',
            -7: f'D{octave}',
            -6: f'D#{octave}/Eb{octave}',
            -5: f'E{octave}',
            -4: f'F{octave}',
            -3: f'F#{octave}/Gb{octave}',
            -2: f'G{octave}',
            -1: f'G#{octave}/Ab{octave}',
            0: f'A{octave}',
            1: f'A#{octave}/Bb{octave}',
            2: f'B{octave}'
        }
        name = note_names[steps - (octave - 4) * 12]

        cents = str(int(round((self.note_value - steps) * 100)))
        cents_str = '' if cents == '0' else '+' + cents if not cents.startswith('-') else cents

        return ' '.join([name, cents_str]).strip()

    @note_name.setter
    def note_name(self, new_name):
        """
        converts a given note name into a note value, the note value is stored in this class' instance
        :param new_name: name of new note
        """
        if isinstance(new_name, str):
            try:
                self.__note_value__ = self.note_name_parser.parseString(new_name)[0]
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_name}" @ col {e.col}!')
        else:
            raise TypeError('MusicConverter.note_name only accepts <str>')

    @property
    def key(self):
        """
        :return: the current key used to calc key_name and notation
        """
        return self.__key__

    @key.setter
    def key(self, new_key):
        if new_key in self.keys:
            self.__key__ = new_key
        else:
            keys = '", "'.join([exiting_key for exiting_key in self.keys])
            raise MusicConverterError(f'<key> must be one of "{keys}"')

    @property
    def key_name(self):

        notation = self.notation
        vorzeichen = self.keys[self.key][1]

        key_type = vorzeichen.replace(' ', '').replace('_', '')
        key_type = key_type[0] if key_type else 'X'

        if (len(notation) > 1 and key_type == 'b') or (key_type == 'X' and self.note_value % 12 == 1):
            head, acc = notation[1]
        else:
            head, acc = notation[0]

        print(f'key: {self.key}; vorzeichen: {vorzeichen}; type: {key_type}')

        head = head - self.clefs[self.clef]

        name = f'{"CDEFGAB"[head % 7]}{vorzeichen[(int(self.note_value) - 3) % 12]}{acc}'

        return name.replace(' ', '').replace('_', '').replace('n', '')

    @property
    def keys(self):
        """
        available keys
        :return: dict of available keys mapping some internal conversion data
        """
        return {
            'C/a':    (0, '_ _ __ _ _ _'),
            'F/d':    (1, '_ _ __ _ _b '),
            'Bb/g':   (2, '_ _b _ _ _b '),
            'Eb/c':   (3, '_ _b _ _b b '),
            'Ab/f':   (4, '_b b _ _b b '),
            'Db/bb':  (5, '_b b _b b b '),
            'C#/a#':  (5, '## # ## # # '),
            'F#/d#':  (6, ' # # ## # #_'),
            'Gb/eb':  (6, ' b b _b b bb'),
            'B/g#':   (7, ' # #_ # # #_'),
            'Cb/ab':  (7, ' b bb b b bb'),
            'E/c#':   (8, ' # #_ # #_ _'),
            'A/f#':   (9, ' #_ _ # #_ _'),
            'D/b':   (10, ' #_ _ #_ _ _'),
            'G/e':   (11, '_ _ _ #_ _ _')
        }

    @property
    def notation(self):
        """
        based on the current key and clef the note value is converted into a notation (head position and accidental)
        :return: tuple(head_position, accidental)
        """
        # basic (C/a) note values
        # c_values = [-9, -7, -5, -4, -2, 0, 2]

        # calc the head position of the C of the current octave
        head_offset = (self.octave - 4) * 7 + self.clefs[self.clef]

        # actual note values
        key_offset = [1 if c == '#' else -1 if c == 'b' else 0 for c in self.keys[self.key][1].replace(' ', '')]
        key_offset.append(key_offset[0])
        values = [i - 9 for i in range(12) if not self.keys[self.key][1][i] == ' ']
        values.append(values[0] + 12)

        # calc the index of the current note value within the current octave (C=0)
        note_index_in_octave = int((round(self.note_value) + 9) % 12) -9

        # signs
        acc = {
            -2: 'bb',
            -1: 'b',
             0: 'n',
             1: '#',
             2: '##'
        }

        # adjust the head position according to the note_index_in_octave
        try:
            head_position = values.index(note_index_in_octave)
            notation = [(head_offset + head_position, '_')]
        except ValueError:
            for i in range(8):
                if values[i] > note_index_in_octave:
                    break
            head_position = i
            notation = [(head_offset + head_position - 1, acc[key_offset[(head_position - 1) % 7] + 1]),
                        (head_offset + head_position, acc[key_offset[head_position] - 1])]
        return notation

    @notation.setter
    def notation(self, new_score):
        """
        parses a string like "sc 5:#" and converts it into the note value based on the current key and clef.
        now accepts also tuple like (5, '#') or list like [5, '#'] or int like 5 (epuivalent to "sc 5" or "sc 5:_")
        :param new_score: string holding the head position and accidental
        """
        # input verification
        signs = ['##', '#', 'n', '_', 'b', 'bb']
        if isinstance(new_score, str):
            try:
                new_score = tuple(self.score_parser.parseString(new_score))
            except pp.ParseException as e:
                raise MusicConverterError(f'Could not parse "{new_score}" @ col {e.col}!')
        elif isinstance(new_score, list):
            if len(new_score) < 2:
                new_score.append('_')
            new_score = tuple(new_score)
        elif isinstance(new_score, (int, tuple)):
            pass
        else:
            raise TypeError(f'MusicConverter.notation only accepts <str>, <int>, <list>, or <tuple> ( is <{type(new_score).__name__}>: {new_score})')

        if isinstance(new_score, int):
            new_score = (new_score, '_')

        if isinstance(new_score, tuple):
            if len(new_score) == 2 and isinstance(new_score[0], int) and isinstance(new_score[1], str) \
                    and new_score[1] in signs:
                score = new_score
            else:
                raise MusicConverterError(f"MusicConverter.notation must be formed (<head position>, <accidental>) e.g (-7, '_') "
                                          f"with accidental in {signs}")

        # calculation
        head_position, acc = score
        base_pos = head_position - self.clefs[self.clef]
        octave = base_pos // 7 + 4
        head_index_in_octave = base_pos % 7

        # calc note value

        values = [i - 9 for i in range(12) if not self.keys[self.key][1][i] == ' ']

        note_index_in_octave = values[head_index_in_octave]
        octave_c_value = (octave - 4) * 12
        head_note_value = note_index_in_octave + octave_c_value

        # calc accidental offset
        vorzeichen = self.keys[self.key][1].replace(' ', '')[head_index_in_octave]
        acc_offset = 0
        if acc == '_':
            pass
        elif acc == 'n' and vorzeichen in ['b', '#']:
            if vorzeichen == 'b':
                acc_offset = 1
            else:
                acc_offset = -1
        elif acc in ['b', '#'] and vorzeichen == '_':
            if acc == 'b':
                acc_offset = -1
            else:
                acc_offset = 1
        elif acc == 'bb' and vorzeichen == 'b':
            acc_offset = -1
        elif acc == '##' and vorzeichen == '#':
            acc_offset = 1
        else:
            raise MusicConverterError(f"<{acc}> not applicable with <{vorzeichen}> in key {self.key}!")

        self.note_value = head_note_value + acc_offset


    @property
    def clefs(self):
        """
        available clefs
        :return: dict holding the available clefs and corresponding offsets for the notation-conversion
        """
        return {
            'violin': -6,
            'alto': 0,
            'bass': +6
        }

    @property
    def clef(self):
        """
        current clef
        :return: current clef as string
        """
        return self.__clef__

    @clef.setter
    def clef(self, new_clef):
        if isinstance(new_clef, str):
            if new_clef in self.clefs:
                self.__clef__ = new_clef
            else:
                raise MusicConverterError(f'no clef with name "{new_clef}" available!')
        else:
            raise TypeError('MusicConverter.clef only accepts <str>')

    def parse(self, input):
        """
        use the classes parsers to set the classes properties
        :param input:
        :return:
        """
        if isinstance(input, str):
            try:
                result = self.input_parser.parseString(input).asDict()
            except pp.ParseException as e:
                raise MusicConverterError(f'<input_parser> could not parse "{input}" @ col {e.col}; ')
            for attribute in result:
                setattr(self, attribute, result[attribute])
        else:
            raise TypeError('MusicConverter.set() only accepts <str> as input')


def test_csv():
    converter = MusicConverter()
    converter.clef = 'violin'

    values = []
    names = []
    frequencies = []
    heads = {key: [] for key in converter.keys}
    recalc = {key: [] for key in converter.keys}
    key_names = {key: [] for key in converter.keys}

    for value in range(-10, 5):
        converter.note_value = value
        values.append(f'{converter.note_value:6}     ')
        name = converter.note_name
        lead = (11 - len(name)) // 2
        names.append(f'{" " * lead}{converter.note_name}{" " * (11 - len(name) - lead)}')
        frequencies.append(f'{converter.frequency:7.1f}Hz  ')
        for key in converter.keys:
            converter.key = key
            heads[key].append(converter.notation)
            key_names[key].append(converter.key_name)

    for key in heads:
        converter.key = key
        for item in heads[key]:
            index = heads[key].index(item)
            note_values = []
            for notation in item:
                try:
                    converter.notation = notation
                    value = converter.note_value
                    if int(values[index]) == value:
                        note_values.append((value, ' '))
                    else:
                        note_values.append((value, '$'))
                except MusicConverterError as err:
                    note_values.append((-111, '$'))
            recalc[key].append(note_values)

    with open('overview.csv', 'w') as file:
        file.write(f'{converter.clef:7};' + ';'.join(values) + ';\n')
        file.write(f'{" ":7};' + ';'.join(names) + ';\n')
        file.write(f'{" ":7};' + ';'.join(frequencies) + ';\n')
        for key in heads:
            vorzeichen = converter.keys[key][1][:].replace(' ', 'X')
            vorzeichen = vorzeichen[-1] + vorzeichen + vorzeichen[:2]
            file.write(f'{key:7};' + ';'.join(f'{c:11}' for c in vorzeichen) + ';\n')
            file.write(f'{" ":7};' + ';'.join(
                f'{"/".join([f"{head:2}:{acc:2}" for head, acc in notation]):11}' for notation in heads[key]) + ';\n')
            file.write(f'{" ":7};' + ';'.join(
                f'{"/".join([f"{value:4}{err}" for value, err in calc]):11}' for calc in recalc[key]) + ';\n')
            file.write(f'{" ":7};' + ';'.join(f'{name:11}' for name in key_names[key]) + ';\n')


def parser_test():
    converter = MusicConverter()
    converter.clef = 'violin'
    converter.key = 'C/a'
    input_string = 'A4'

    while not input_string == 'quit':
        try:
            converter.parse(input_string)
        except Exception as err:
            print(f'{type(err).__name__}: {err}')
        print(f'clef: {converter.clef}')
        print(f'key: {converter.key}')
        print(f'base_freq: {converter.base_freq:4.2f}Hz')
        print(f'value: {converter.note_value}')
        print(f'frequency: {converter.frequency:4.2f}Hz')
        print(f'level: {converter.amplitude*100:3.1f}% / {converter.gain:3.1f}dB')
        print(f'name: {converter.key_name}')
        print(f'notation: {converter.notation}')
        input_string = input('>> ')

    print('terminated.')


if __name__ == '__main__':
    test_csv()