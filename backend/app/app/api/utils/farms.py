from app import crud

def get_farm_list(
        db,
        farm_id=None,
        farm_id_list=None,
        farm_url=None,
        get_all=True,
        skip=0,
        limit=100
    ):
    farm_list = []

    if farm_id is not None:
        farm = crud.farm.get_by_id(db, farm_id=farm_id)
        if farm is not None:
            farm_list.append(farm)

    if farm_id_list is not None:
        farms = crud.farm.get_by_multi_id(db, farm_id_list=farm_id_list)
        if farms is not None:
            farm_list.extend(farms)

    if farm_url is not None:
        farm = crud.farm.get_by_url(db, farm_url=farm_url)
        if farm is not None:
            farm_list.append(farm)

    if get_all and not farm_url and not farm_id_list and not farm_id:
        farms = crud.farm.get_multi(db, skip=skip, limit=limit)
        if farms is not None:
            farm_list.extend(farms)

    return farm_list
