import json


def get_vott_info(json_file_path):

    info_map = dict()

    with open(json_file_path) as f:
        data = json.load(f)

    # Prolazak kroz sve slike
    for asset_id, asset_data in data['assets'].items():
        # print('Asset data = ', asset_data)
        image_name = asset_data['asset']['name']

        info_map[asset_id] = image_name

        regions = asset_data['regions']

        # print(f"Slika: {image_name}")

        # Prolazak kroz sve regije
        for region in regions:
            region_id = region['id']
            region_type = region['type']
            tags = region['tags']
            bounding_box = region['boundingBox']

            # print(f"Regija ID: {region_id}")
            # print(f"Tip regije: {region_type}")
            # print(f"Oznake: {tags}")
            # print(f"Bounding Box: {bounding_box}")
            # print()

    return info_map