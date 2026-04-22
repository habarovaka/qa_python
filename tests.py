import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize(
        'book_name_valid',
        [
            'Я',  # 1 символ
            'Гарри Поттер и Дары Смерти: Часть первая',  # 40 символов
        ]

    )
    def test_add_new_book_valid_name_length_is_added(self, collector, book_name_valid):
        collector.add_new_book(book_name_valid)
        assert book_name_valid in collector.get_books_genre(),\
            f"Книга с валидным названием '{book_name_valid}' (длина {len(book_name_valid)}) не была добавлена в словарь"
    @pytest.mark.parametrize(
        'book_name_invalid',
        [
            '',  # 0 символов
            'Приключения Шерлока Холмса и док. Ватсона',  # 41 символов
        ]

    )
    def test_add_new_book_invalid_lengths_not_added(self, collector, book_name_invalid):
        collector.add_new_book(book_name_invalid)
        print (collector.get_books_genre())
        assert book_name_invalid not in collector.get_books_genre(),\
            f"Книга с невалидной длиной ({len(book_name_invalid)}) была ошибочно добавлена в словарь"


    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_add_duble_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Гордость и предубеждение и зомби')
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_existing_genre(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1','Комедии')
        assert collector.books_genre['1+1'] == 'Комедии'

    def test_set_book_genre_non_existent_genre_not_assigned(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1','Комеди')
        assert collector.books_genre['1+1'] == ''

    def test_get_book_genre_existing_name(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедии')
        assert collector.get_book_genre('1+1') == 'Комедии'

    def test_get_books_with_specific_genre_existing_genre(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедии')
        assert '1+1' in collector.get_books_with_specific_genre('Комедии')

    def test_get_books_genre_list_books_genre(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедии')
        assert collector.get_books_genre() == {'1+1': 'Комедии'}

    def test_get_books_for_children_excludes_age_rating(self, collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert 'Оно' not in collector.get_books_for_children()

    def test_get_books_for_children_add_age_rating(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедии')
        assert '1+1' in collector.get_books_for_children()

    @pytest.mark.parametrize(
        'name, genre',
        [
            ['1+1', 'Комедии'],
            ['Оно', 'Ужасы'],
            ['Зыездные воины', 'Фантастика']
        ]
    )
    def test_add_book_in_favorites_various_books(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        collector.add_book_in_favorites(name)
        assert name in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize(
        'name, genre',
        [
            ['1+1', 'Комедии'],
            ['Оно', 'Ужасы'],
            ['Звездные воины', 'Фантастика']
        ]
    )
    def test_add_book_in_favorites_duble_book(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        collector.add_book_in_favorites(name)
        collector.add_book_in_favorites(name)
        assert len(collector.get_list_of_favorites_books()) == 1


    def test_add_book_in_favorites_book_not_in_collector(self, collector):
        collector.add_book_in_favorites('Это Мы') # такой книги нет в словаре
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_delete_book_from_favorites_existing_book(self, collector):
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедии')
        collector.add_book_in_favorites('1+1')
        collector.delete_book_from_favorites('1+1')
        assert '1+1' not in collector.get_list_of_favorites_books()

