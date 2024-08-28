class HasNotLoginCGTeamwork(Exception):
    """
        has not login cgteamwork
    """

    def __init__(self):
        message = 'Has not logged in!'
        super(HasNotLoginCGTeamwork, self).__init__(message)


class ProjectHasNotAnyEpisode(Exception):
    """
        Exception raised for current project has not any episode
    """

    def __init__(self, project_db: str):
        messge = f"{project_db} has not any episode"
        super().__init__(messge)


class ModuleError(Exception):
    """
     raised for errors in the module
    """

    def __init__(self, module_name: str):
        messge = f"{module_name} module error"
        super().__init__(messge)


class CreateShotAttributeIncomplete(Exception):
    def __init__(self):
        super().__init__('Create Shot Attribute Incomplete')


class ShotNumberIsExists(Exception):
    def __init__(self):
        super().__init__('Shot Number Exists')


class ProjectHasNotFrameRate(Exception):
    def __init__(self):
        super().__init__('Project has not Frame Rate')


class HasNotThisAccount(Exception):
    def __init__(self):
        super().__init__('Has Not This account')
