"""Handlers to convert various boolean options to boolean flag strings."""


def filter_des_days_to_str(value):
    """Translate a boolean to the filter_des_days flag.

        Args:
            value: Either a boolean or one of two text strings.

            * filter-des-days
            * all-des-days

        Returns:
            str -- filter_des_days flag text.
    """
    acceptable = ('filter-des-days', 'all-des-days')
    if isinstance(value, str):
        assert value in acceptable, 'filter_des_days value "{}" is not acceptable. ' \
            'Must be one of the following: {}'.format(value, acceptable)
        filter_des_days = value
    elif isinstance(value, bool):
        filter_des_days = acceptable[0] if value else acceptable[1]
    else:
        raise ValueError(
            'filter_des_days input should be a string or a boolean. '
            'Not {}.'.format(type(value))
        )
    return filter_des_days


def use_multiplier_to_str(value):
    """Translate a boolean to the use_multiplier flag.

        Args:
            value: Either a boolean or one of two text strings.

            * multiplier
            * full-geometry

        Returns:
            str -- use_multiplier flag text.
    """
    acceptable = ('multiplier', 'full-geometry')
    if isinstance(value, str):
        assert value in acceptable, 'use_multiplier value "{}" is not acceptable. ' \
            'Must be one of the following: {}'.format(value, acceptable)
        use_multiplier = value
    elif isinstance(value, bool):
        use_multiplier = acceptable[0] if value else acceptable[1]
    else:
        raise ValueError(
            'use_multiplier input should be a string or a boolean. '
            'Not {}.'.format(type(value))
        )
    return use_multiplier


def is_residential_to_str(value):
    """Translate a boolean to the is_residential flag.

        Args:
            value: Either a boolean or one of two text strings.

            * residential
            * nonresidential

        Returns:
            str -- is_residential flag text.
    """
    acceptable = ('residential', 'nonresidential')
    if isinstance(value, str):
        assert value in acceptable, 'is_residential value "{}" is not acceptable. ' \
            'Must be one of the following: {}'.format(value, acceptable)
        is_residential = value
    elif isinstance(value, bool):
        is_residential = acceptable[0] if value else acceptable[1]
    else:
        raise ValueError(
            'is_residential input should be a string or a boolean. '
            'Not {}.'.format(type(value))
        )
    return is_residential


def write_set_map_to_str(value):
    """Translate a boolean to the write_set_map flag.

        Args:
            value: Either a boolean or one of two text strings.

            * write-op-map
            * write-set-map

        Returns:
            str -- write_set_map flag text.
    """
    acceptable = ('write-set-map', 'write-op-map')
    if isinstance(value, str):
        assert value in acceptable, 'write_set_map value "{}" is not acceptable. ' \
            'Must be one of the following: {}'.format(value, acceptable)
        write_set_map = value
    elif isinstance(value, bool):
        write_set_map = acceptable[0] if value else acceptable[1]
    else:
        raise ValueError(
            'write_set_map input should be a string or a boolean. '
            'Not {}.'.format(type(value))
        )
    return write_set_map
