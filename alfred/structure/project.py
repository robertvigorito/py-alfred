"""Project folder schema.
"""
folder_hierarchy = {
    "{job}": {
        "config": {},
        "prod": {
            "reference": {},
            "script": {},
            "sound": {},
            "storyboard": {}
        },
        "sends": {},
        # Start scene project structure
        "{scene}": {
            # Start shot project structure
            "{shot}": {
                "assets": {},
                "houdini": [
                    "fx",
                    "env",
                    "crowds"
                ],
                "katana": [
                    "light",
                    "fx"
                ],
                "maya": [
                    "anim",
                     "light",
                     "modeler",
                     "texture"
                ],
                "nuke": [
                    "comp",
                    "prep",
                    "env",
                    "light",
                    "fx"
                ],
                "renders": {},
                "substance": [
                    "texture"
                ]
            }
        }
    }
}
