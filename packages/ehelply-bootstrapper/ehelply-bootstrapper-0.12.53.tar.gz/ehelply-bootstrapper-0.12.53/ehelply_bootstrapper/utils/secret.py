class SecretManager:
    def __init__(self) -> None:
        self._secrets = {}

    def get(self, category: str = "default") -> list:
        """
        Get a list of secrets from the category
        :param category:
        :return:
        """
        if category not in self._secrets:
            return []
        return self._secrets[category]

    def add(self, secret, category: str = "default", prepend: bool = False) -> bool:
        """
        Add a new secret to a category
        :param prepend:
        :param secret:
        :param category:
        :return:
        """
        if self.exists(secret, category):
            return False
        if category not in self._secrets:
            self._secrets[category] = []

        if prepend:
            self._secrets[category].insert(0, secret)
        else:
            self._secrets[category].append(secret)

        return True

    def remove(self, secret, category: str = "default"):
        """
        Remove a secret from a category
        :param secret:
        :param category:
        :return:
        """
        self._secrets[category].remove(secret)

    def exists(self, secret, category: str = "default") -> bool:
        """
        Determine whether a secret exists in a category
        :param secret:
        :param category:
        :return:
        """
        if category not in self._secrets:
            return False
        return secret in self._secrets[category]
