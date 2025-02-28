{
    'name' : "Real Estate",
    'version' : '1.0',
    'depends' : ['base'],
    'category' : "Uncategorized",
    'author' : "Mohamed Emad",
    'description' : "Module to manage Real Estate (First Module)",
    'installable' : True,
    'application' : True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_action_prototype.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/inherited_views.xml',
        'views/estate_property_type_action.xml',
        'views/estate_property_tag_action.xml',
        'views/estate_property_action.xml',
        'views/estate_property_menus.xml'
    ]
}
