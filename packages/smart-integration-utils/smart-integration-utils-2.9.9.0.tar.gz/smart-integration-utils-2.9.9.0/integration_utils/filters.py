__all__ = ('validate_data', 'parse_for_mongo_query', 'parse_for_django_query')


class __Validate(object):
    def __init__(self, filter_str: str, validate_obj: dict):
        self.parsed_filters = self.__parse_filters(filter_str)
        self.validate_obj = validate_obj

    def __parse_filters(self, filter_str: str):
        """
        :param filter_:
        :return: list of dicts/lists
        """
        parsed_filters = []
        if filter_str:
            filter_values = filter_str.split(",")
            for filters in filter_values:
                if filters:
                    if ";" in filters:  # check 'AND' statement
                        and_filters = []
                        for f in filters.split(";"):
                            and_filters.append(
                                self.__create_filter_row(f.strip())
                            )  # strip string for del spaces
                        parsed_filters.append(and_filters)  # return list of AND filters
                        continue
                    parsed_filters.append(
                        self.__create_filter_row(filters.strip())
                    )  # strip string for del spaces
        return parsed_filters

    def generate_mongo_query(self, parsed: dict) -> dict:
        """Generation mongodantic query"""
        query = {}
        operator = parsed['set']
        field = parsed['field']
        exclude = field.startswith('!')
        field = field.replace('!', '')
        if operator == 'in_':
            query[f'{field}__regex' if not exclude else f'{field}__regex_ne'] = parsed[
                'value'
            ]
        elif operator == 'not_in':
            query[f'{field}__regex_ne' if not exclude else f'{field}__regex'] = parsed[
                'value'
            ]
        elif operator == 'start':
            query[
                f'{field}__startswith' if not exclude else f'{field}__not_startswith'
            ] = parsed['value']
        elif operator == 'end':
            query[
                f'{field}__endswith' if not exclude else f'{field}__not_endswith'
            ] = parsed['value']
        elif operator == 'eq':
            query[f'{field}' if not exclude else f'{field}__ne'] = parsed['value']
        elif operator == 'not_eq':
            query[f'{field}__ne' if not exclude else f'{field}'] = parsed['value']
        return query

    def generate_query(self, mongo: bool = True) -> list:
        queries = []
        for parsed in self.parsed_filters:
            if isinstance(parsed, list):
                query_dict = {} if mongo else {'filter': {}, 'exclude': {}}
                for p in parsed:
                    if mongo:
                        query_dict.update(self.generate_mongo_query(p))
                    else:
                        _dict = self.generate_django_orm_query(p)
                        query_dict['filter'].update(_dict['filter'])
                        query_dict['exclude'].update(_dict['exclude'])
                queries.append(query_dict)
            else:
                queries.append(
                    self.generate_mongo_query(parsed)
                    if mongo
                    else self.generate_django_orm_query(parsed)
                )
        return queries

    def generate_django_orm_query(self, parsed: dict) -> dict:
        query = {'filter': {}, 'exclude': {}}
        operator = parsed['set']
        field = parsed['field']
        exclude = field.startswith('!')
        field = field.replace('!', '')
        if operator == 'in_':
            query['filter' if not exclude else 'exclude'][f'{field}__iexact'] = parsed[
                'value'
            ]
        elif operator == 'not_in':
            query['exclude' if not exclude else 'filter'][field] = parsed['value']
        elif operator == 'start':
            query['filter' if not exclude else 'exclude'][
                f'{field}__startswith'
            ] = parsed['value']
        elif operator == 'end':
            query['filter' if not exclude else 'exclude'][
                f'{field}__endswith'
            ] = parsed['value']
        elif operator == 'eq':
            query['filter' if not exclude else 'exclude'][field] = parsed['value']
        elif operator == 'not_eq':
            query['exclude' if not exclude else 'filter'][field] = parsed['value']
        return query

    # create one query for parse_filters
    def __create_filter_row(self, f: str) -> dict:
        """
        :param f: string
        :return: dict
        """
        operators = {
            "=@": "in_",
            "!@": "not_in",
            "=$": "end",
            "=^": "start",
            "==": "eq",
            "!=": "not_eq",
        }
        for operator in operators:
            if operator in f:
                set = operators[operator]
                field, value = f.split(operator)
                return {"field": field, "value": value, "set": set}
        else:
            raise ValueError("invalid operator")

    def _validate_row(self, row: dict):
        exclude = False
        exist = False
        if row['field'].startswith('!'):
            exclude = True
            row['field'] = row['field'][1:]
        method = getattr(self, row['set'])
        check_value = self.validate_obj.get(row['field'], '')
        exist = method(row['value'], check_value)
        return self.create_filter_result(exist, exclude)

    def validate_data(self):
        validated_result = []
        for filter_row in self.parsed_filters:
            if isinstance(filter_row, list):
                result = [self._validate_row(row) for row in filter_row]
                validated_result.append(all(result))
            else:
                validated_result.append(self._validate_row(filter_row))
        return any(validated_result)

    def in_(self, value, check_value):
        return value in check_value

    def not_in(self, value, check_value):
        return value not in check_value

    def start(self, value, check_value):
        return check_value.startswith(value)

    def end(self, value, check_value):
        return check_value.endswith(value)

    def eq(self, value, check_value):
        return check_value == value

    def not_eq(self, value, check_value):
        return check_value != value

    def create_filter_result(self, exist: bool, exclude: bool):
        """
        :param exist bool
        :param exclude bool
        :return: bool
        """
        return exist ^ exclude


def validate_data(filter_str: str, validate_obj: dict) -> bool:
    return __Validate(filter_str, validate_obj).validate_data()


def parse_for_django_query(filter_str: str) -> list:
    """
    :param filter_str: filter string
    :return: dict like {'filter': {'url__iexact': 'test.io'}, 'exclude': {'url__iexact': 'us.test.io'}}
    """
    return __Validate(filter_str, {}).generate_query(mongo=False)


def parse_for_mongo_query(filter_str: str) -> list:
    """
    :param filter_str: filter string
    :return: dict (dict for mongodantic odm)
    """
    return __Validate(filter_str, {}).generate_query(mongo=True)
