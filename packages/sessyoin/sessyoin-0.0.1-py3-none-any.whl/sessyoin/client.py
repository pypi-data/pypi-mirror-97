from .http import HttpClient
from .models import CATEGORIES, Result


class Client:
    """Client to make requests to sessyoinAPI."""

    def __init__(self):
        self.http = HttpClient()

    async def teardown(self):
        """
        |crot|
        
        A function to cleanup our http session.
        """
        await self.http.session.close()

    async def get_image(self, category: str) -> Result:
        """
        |crot|
        
        Returns an image URL of a specific category.

        Parameters
        ----------
        category: str
            The category of image you want to get.
        
        Returns
        -------
        sessyoin.Result
        """
        if not category in CATEGORIES:
            raise TypeError("This isn't a valid category.")

        result = await self.http.get(category)
        return Result(result)
