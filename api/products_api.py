from api.base_client import BaseClient


class ProductsApi(BaseClient):
    def get_products(self):
        return self.request("GET", "/productsList")

    def search_product(self, product_name):
        return self.request("POST", "/searchProduct", data={"search_product": product_name})

    def update_products(self):
        return self.request("PUT", "/productsList")