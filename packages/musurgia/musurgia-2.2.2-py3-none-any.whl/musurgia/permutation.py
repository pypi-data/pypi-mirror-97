from itertools import cycle


def permute(input_list, permutation_order):
    if input_list is None:
        raise ValueError('input_list cannot be None')
    if permutation_order is None:
        raise ValueError('permutation_order cannot be None')
    if len(input_list) == len(permutation_order):
        return [input_list[m - 1] for m in permutation_order]
    else:
        raise ValueError('input_list = {} and permutation_order {} must have the same length'.format(str(input_list),
                                                                                                     str(
                                                                                                         permutation_order)))


def self_permute(permutation_order):
    output = [permutation_order]

    for i in range(1, len(permutation_order)):
        output.append(permute(output[i - 1], permutation_order))

    return output


def get_self_multiplied_permutation(permutation_order):
    self_permuted_order = self_permute(permutation_order)
    multiplied = [permute(self_permuted_order, current_order) for current_order in self_permuted_order]
    return multiplied


def get_reordered_self_multiplied_permutation(permutation_order):
    def _reorder(matrix):
        index_of_first_row = None
        for index_of_first_row in range(len(matrix)):
            if matrix[index_of_first_row][0] == permutation_order:
                break
        output = []
        for i in range(index_of_first_row, index_of_first_row + len(matrix)):
            output.append(matrix[i % len(matrix)])
        return output

    multiplied = get_self_multiplied_permutation(permutation_order)
    return _reorder(multiplied)


def get_vertical_self_multiplied_permutation(permutation_order):
    def _transpose(matrix):
        output = []
        for i in range(len(matrix)):
            temp = []
            for j in range(len(matrix)):
                temp2 = []
                for k in range(len(matrix)):
                    temp2.append(matrix[i][k][j])
                temp.append(temp2)
            output.append(temp)
        return output

    multiplied = get_self_multiplied_permutation(permutation_order)
    return _transpose(multiplied)


def permute_matrix_rowwise(matrix, main_permutation_order):
    lp = LimitedPermutation(main_permutation_order=main_permutation_order, input_list=[1, 2, 3, 4, 5, 6, 7])
    output = []
    for row in matrix:
        permutation_order = lp.__next__()
        output.append(permute(input_list=row, permutation_order=permutation_order))
    return output


def invert_matrix(matrix):
    return [x for x in zip(*matrix)]


def permute_matrix_columnwise(matrix, main_permutation_order):
    inverted_matrix = invert_matrix(matrix)
    inverted_matrix = permute_matrix_rowwise(inverted_matrix, main_permutation_order)
    return invert_matrix(inverted_matrix)


def permute_matrix(matrix, main_permutation_order):
    output = permute_matrix_rowwise(matrix, main_permutation_order)
    return permute_matrix_columnwise(output, main_permutation_order)


class LimitedPermutation(object):
    class Element(object):
        def __init__(self, value, order):
            self.value = value
            '''order of element in the original input_list'''
            self.order = order

    def __init__(self, input_list, main_permutation_order, multi=(1, 1), reading_direction='horizontal'):

        self._iterator = None
        self._element_generator = None
        self._multiplied_orders = None
        self._multi = None
        self._reading_direction = None

        self.input_list = input_list
        self.main_permutation_order = list(main_permutation_order)
        self.multi = multi
        self.reading_direction = reading_direction

    @staticmethod
    def get_next_multi(multi, input_length):
        m_1 = multi[0]
        m_2 = multi[1] + 1
        m_1, m_2 = ((m_1 - 1) % input_length) + 1, ((m_2 - 1) % input_length) + 1
        return m_1, m_2

    @property
    def reading_direction(self):
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, val):
        if val not in ('horizontal', 'vertical'):
            raise ValueError()
        self._multiplied_orders = None
        self._reading_direction = val

    @property
    def multi(self):
        return self._multi

    @multi.setter
    def multi(self, val):
        m_1 = val[0]
        m_2 = val[1]
        input_length = len(self.input_list)
        m_1, m_2 = (((m_1 - 1) % input_length) + 1 + ((m_2 - 1) // input_length)) % input_length, (
                (m_2 - 1) % input_length) + 1
        if m_1 == 0:
            m_1 = len(self.input_list)
        self._multi = (m_1, m_2)

    @property
    def multiplied_orders(self):
        if self._multiplied_orders is None:
            if self.reading_direction == 'horizontal':
                multiplied = get_reordered_self_multiplied_permutation(self.main_permutation_order)
            else:
                multiplied = get_vertical_self_multiplied_permutation(self.main_permutation_order)

            self._multiplied_orders = [order for orders in multiplied for order in orders]
        return self._multiplied_orders

    @property
    def permutation_order(self):
        index = (self.multi[0] - 1) * len(self.input_list) + self.multi[1] - 1
        return self.multiplied_orders[index]

    @property
    def iterator(self):
        if self._iterator is None:
            self._iterator = cycle(self.multiplied_orders)
            if self.multi is None:
                raise Exception('multi must be set first')

            first_index = (self.multi[0] - 1) * len(self.main_permutation_order) + (self.multi[1] - 1)
            for i in range(first_index):
                self._iterator.__next__()

        return self._iterator

    def __next__(self):
        return self.iterator.__next__()

    @property
    def element_generator(self):
        if self._element_generator is None:
            def gen():
                next_permutations = self.__next__()
                while True:
                    for order in next_permutations:
                        yield self.Element(value=self.input_list[order - 1], order=order)

                    next_permutations = self.__next__()

            self._element_generator = gen()

        return self._element_generator

    def next_element(self):
        return self.element_generator.__next__()

    @property
    def next_multi(self):
        return self.get_next_multi(self.multi, len(self.input_list))
