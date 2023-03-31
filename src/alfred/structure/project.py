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
        "dailies": {},
        # Start scene project structure
        "{sequence}": {
            # Start shot project structure
            "{shot}": {
                "assets": {},
                "houdini": [
                    "crowds",
                    "env",
                    "fx",
                    "light",
                    "lookdev",
                ],
                "maya": [
                    "anim",
                    "modeler",
                    "texture"
                ],
                "nuke": [
                    "comp",
                    "env",
                    "fx"
                    "light",
                    "prep",
                ],
                "renders": {},
                "substance": [
                    "texture"
                ]
            }
        }
    }
}
