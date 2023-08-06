from dli.models.dictionary_model import DictionaryModel


class TestDictionary:
    def test_dictionary_with_fields(self, test_client):
        model = DictionaryModel(
            {'attributes': {'fields': []}, 'id': '123'}, test_client
        )

        assert not test_client.session.get.called

    def test_dictionary_fields(self, test_client):
        model = DictionaryModel(
            {'attributes': {}, 'id': '123'}, test_client
        )
        model.fields

        assert test_client.session.get.called

    def test_dictionary_field_pagination(self, test_client):

        def _response():
            i = 0
            while True:
                #as the default page_size is 25, to get
                #'6' we effectively *3 as we have two items
                yield {
                    'meta': {'total_count':75},
                    'data': {
                        'attributes': {
                            'fields': [
                                {f'{i}': i},
                                {f"-{i}": i}
                            ]
                        }
                    }
                }
                i += 1

        test_client._session.get().json.side_effect = _response()
        model = DictionaryModel(
            {'attributes': {}, 'id': '123'}, test_client
        )

        assert len(model.fields) == 6
