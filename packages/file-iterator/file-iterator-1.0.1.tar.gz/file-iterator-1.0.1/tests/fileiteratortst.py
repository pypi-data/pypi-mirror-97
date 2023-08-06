
# TODO: Something to add to the good one.
# def test_next_empty_file():
#     assert 1


# The old one.

# @pytest.fixture(params=[plain_iter])
# def FileIter(request):
#     yield request.param

# def test_file_factory_invalid_type(txt_file):
    # with pytest.raises(FileIteratorException):
    #     LocalFileIterator(str(txt_file), 'any')


# def test_lines_read_init(plain_iter):
#     assert plain_iter.lines_read == 0
# def test_lines_read_next(plain_iter):
#     for _ in range(5):
#         next(plain_iter)
#     assert plain_iter.lines_read == 5
    
# def test_lines_read_skip(plain_iter):
#     plain_iter.skip_lines(5)
#     assert plain_iter.lines_read == 5

    
# def test_lines_read_init(FileIter):
#     assert FileIter.lines_read == 0

# def test_lines_read_5(FileIter):
#     for _ in range(5):
#         FileIter.skip_lines(5)
#     assert FileIter.lines_read == 5


# def test_next_empty_file():
#     assert 1

# def test_next_non_empty_file():
#     assert 1

# def test_natural_iteration(FileIter):
#     # "For loop behaviour."
#     # for line in FileIter:
#     #     pass
#     it = iter(FileIter)
#     with pytest.raises(StopIteration):
#         line = next(it)
#         while line:
#             line = next(it)

# def test_simplified_iteration(FileIter):
#     # Return None when file has been read.
#     line = next(FileIter)
#     while line:
#         line = next(FileIter)
#     assert line is None

# def test_copy_lines_read(FileIter):
#     for _ in range(5):
#         next(FileIter)
#     copy = FileIter.copy()
#     assert copy.lines_read == FileIter.lines_read
    

# def test_copy_has_same_events():
#     pass


# def test_context_manager(FileIter):
#     with FileIter as it:
#         for line in it:
#             pass








# @pytest.fixture
# def order():
#     return []


# @pytest.fixture
# def outer(order, inner):
#     order.append("outer")
    
    
# class TestOne:
#     @pytest.fixture
#     def inner(self, order):
#         order.append("one")

#     def test_order(self, order, outer):
#         assert order == ["one", "outer"]


# class TestTwo:
#     @pytest.fixture
#     def inner(self, order):
#         order.append("two")

#     def test_order(self, order, outer):
#         assert order == ["two", "outer"]