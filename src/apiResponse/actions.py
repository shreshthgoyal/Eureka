def apiAction(query: str, query_type: str, retriever_instace):
    metadata = retriever_instace.get_metadata(query)
    action_map = {
        "Gym": {"url": "curefit://allgyms", "actionType": "NAVIGATION", "title": "Gyms"},
        "Price": {"url": "curefit://listpage?pageId=SKUPurchasePage&selectedTab=black", "actionType": "NAVIGATION", "title": "Pricing"},
        "Default": {"url": "curefit://fl_support", "actionType": "NAVIGATION", "title": "Support"},
        "Queries": {"url": metadata['deep_link'], "actionType": "NAVIGATION", "title": metadata['title']} if ('deep_link' in metadata and len(metadata['deep_link']) > 0) else None,
    }
    
    return [action_map[query_type]] if query_type in action_map else None
